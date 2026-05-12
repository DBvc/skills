#!/usr/bin/env python3
"""Inventory installed Agent Skills without network access or destructive changes.

The script reads skill directories, parses lightweight frontmatter, detects duplicate
names and basic script risk flags, and emits JSON or Markdown. It intentionally uses
only the Python standard library.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
URL_RE = re.compile(r"https?://[^\s\]\)\}\>'\"]+")

NETWORK_PATTERNS = [
    r"\brequests\.",
    r"\burllib\.",
    r"\bhttpx\.",
    r"\baiohttp\b",
    r"\bcurl\b",
    r"\bwget\b",
    r"\bfetch\s*\(",
    r"\bsocket\.",
    r"https?://",
]
DEPENDENCY_PATTERNS = [
    r"\bpip(?:3)?\s+install\b",
    r"\bnpm\s+(?:install|i)\b",
    r"\byarn\s+add\b",
    r"\bpnpm\s+add\b",
    r"\buv\s+add\b",
    r"\bbrew\s+install\b",
    r"\bapt(?:-get)?\s+install\b",
]
DESTRUCTIVE_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bshutil\.rmtree\b",
    r"\bos\.remove\b",
    r"\bos\.unlink\b",
    r"\bPath\([^\)]*\)\.unlink\b",
    r"\bgit\s+clean\s+-",
    r"\bgit\s+reset\s+--hard\b",
    r"\btruncate\s+-s\s+0\b",
]
SECRET_PATTERNS = [
    r"os\.environ(?:\.get)?\s*\(\s*[\"'][A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)",
    r"os\.environ\s*\[[\"'][A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)",
    r"process\.env\.[A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)",
    r"\$[A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)\b",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\.ssh/(?:id_|config|known_hosts)",
]
GENERIC_DESCRIPTION_RE = re.compile(
    r"\b(help|helps|assistant|general|anything|everything|all tasks|useful|improve)\b",
    re.I,
)


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_simple_yaml_map(block: str) -> dict[str, str]:
    """Parse a small YAML subset for SKILL.md frontmatter."""
    result: dict[str, str] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            i += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value in {"|", ">", "|-", ">-", "|+", ">+"}:
            collected: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line and not next_line.startswith((" ", "\t")) and ":" in next_line:
                    break
                collected.append(next_line.strip())
                i += 1
            result[key] = "\n".join(collected).strip()
            continue
        result[key] = strip_quotes(raw_value)
        i += 1
    return result


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                return parse_simple_yaml_map("\n".join(lines[1:idx])), "strict"
        return {}, "missing_closing_delimiter"
    match = re.search(
        r"^---\s+name:\s*(?P<name>\S+)\s+description:\s*(?P<desc>.*?)\s+---",
        text,
        re.S,
    )
    if match:
        return {
            "name": strip_quotes(match.group("name")),
            "description": match.group("desc").strip(),
        }, "nonstandard_minified"
    return {}, "missing"


def sha256_prefix(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8", errors="ignore")).hexdigest()[:16]


def safe_read_text(path: Path, max_bytes: int = 250_000) -> str:
    try:
        raw = path.read_bytes()[:max_bytes]
    except Exception:
        return ""
    return raw.decode("utf-8", errors="ignore")


def classify_root(root: Path, home: Path) -> str:
    try:
        resolved = root.expanduser().resolve()
    except Exception:
        resolved = root.expanduser()
    mapping = {
        home / ".agents" / "skills": "codex_user_current",
        home / ".codex" / "skills": "codex_user_legacy_or_custom",
        home / ".cursor" / "skills": "cursor_user",
        home / ".claude" / "skills": "claude_user",
        Path("/etc/codex/skills"): "codex_admin",
    }
    for known, label in mapping.items():
        try:
            if resolved == known.resolve():
                return label
        except Exception:
            if str(resolved) == str(known):
                return label
    if ".agents/skills" in str(resolved):
        return "repo_or_nested_agents"
    if str(resolved).endswith("/skills"):
        return "source_or_custom_skills_root"
    return "custom"


def default_roots(home: Path) -> list[Path]:
    return [
        home / ".agents" / "skills",
        home / ".codex" / "skills",
        home / ".cursor" / "skills",
        home / ".claude" / "skills",
        Path("/etc/codex/skills"),
    ]


def repo_roots(cwd: Path) -> list[Path]:
    roots: list[Path] = []
    current = cwd.resolve()
    for parent in [current, *current.parents]:
        roots.append(parent / ".agents" / "skills")
        roots.append(parent / "skills")
        if (parent / ".git").exists():
            break
    return roots


def discover_skill_dirs(root: Path) -> list[Path]:
    root = root.expanduser()
    if not root.exists():
        return []
    if (root / "SKILL.md").exists():
        return [root]
    result: list[Path] = []
    try:
        children = sorted(root.iterdir(), key=lambda p: p.name.lower())
    except Exception:
        return []
    for child in children:
        if child.is_dir() or child.is_symlink():
            if (child / "SKILL.md").exists():
                result.append(child)
            elif child.is_dir():
                # Include malformed active package candidates for review.
                if child.name not in {"references", "scripts", "assets", "evals", "agents"}:
                    result.append(child)
    return result


def parse_openai_yaml(skill_dir: Path) -> dict[str, Any]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return {"exists": False, "allow_implicit_invocation": "unknown"}
    text = safe_read_text(path, max_bytes=20_000)
    match = re.search(r"allow_implicit_invocation\s*:\s*(true|false)", text, re.I)
    value: bool | str = "unknown"
    if match:
        value = match.group(1).lower() == "true"
    return {
        "exists": True,
        "path": str(path),
        "allow_implicit_invocation": value,
    }


def parse_trigger_evals(skill_dir: Path) -> dict[str, Any]:
    path = skill_dir / "evals" / "triggers.json"
    if not path.exists():
        return {"exists": False, "case_count": 0, "counts": {}, "cases": []}

    text = safe_read_text(path, max_bytes=200_000)
    try:
        data = json.loads(text)
    except Exception as exc:  # noqa: BLE001
        return {"exists": True, "path": str(path), "error": str(exc), "case_count": 0, "counts": {}, "cases": []}

    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        return {
            "exists": True,
            "path": str(path),
            "error": "cases is not an array",
            "case_count": 0,
            "counts": {},
            "cases": [],
        }

    counts: dict[str, int] = {}
    summarized_cases: list[dict[str, Any]] = []
    for case in cases:
        if not isinstance(case, dict):
            continue
        kind = str(case.get("kind", "unknown"))
        counts[kind] = counts.get(kind, 0) + 1
        prompt = str(case.get("prompt", ""))
        summarized_cases.append(
            {
                "id": str(case.get("id", "")),
                "kind": kind,
                "expected": case.get("expected"),
                "expected_trigger": case.get("expected_trigger"),
                "prompt": prompt[:500],
            }
        )

    return {
        "exists": True,
        "path": str(path),
        "case_count": len(summarized_cases),
        "counts": counts,
        "cases": summarized_cases,
    }


def scan_text_flags(text: str) -> list[str]:
    flags: list[str] = []
    checks = [
        ("network_reference", NETWORK_PATTERNS),
        ("dependency_install", DEPENDENCY_PATTERNS),
        ("destructive_operation", DESTRUCTIVE_PATTERNS),
        ("secret_or_credential_reference", SECRET_PATTERNS),
    ]
    for label, patterns in checks:
        for pattern in patterns:
            if re.search(pattern, text, re.I):
                flags.append(label)
                break
    return flags


def inspect_scripts(skill_dir: Path, redact_paths: bool, home: Path) -> dict[str, Any]:
    scripts_dir = skill_dir / "scripts"
    files: list[dict[str, Any]] = []
    aggregate_flags: set[str] = set()
    if not scripts_dir.exists():
        return {"count": 0, "files": [], "risk_flags": []}
    for path in sorted(p for p in scripts_dir.rglob("*") if p.is_file()):
        suffix = path.suffix.lower()
        if suffix not in {".py", ".sh", ".js", ".ts", ".rb", ".pl", ".php"}:
            continue
        text = safe_read_text(path)
        flags = scan_text_flags(text)
        if "--help" not in text and "argparse" not in text and "Usage" not in text:
            flags.append("missing_help_or_usage")
        aggregate_flags.update(flags)
        files.append(
            {
                "path": display_path(path, home, redact_paths),
                "suffix": suffix,
                "chars_sampled": len(text),
                "risk_flags": sorted(set(flags)),
                "sha256_prefix": sha256_prefix(text) if text else "",
            }
        )
    return {"count": len(files), "files": files, "risk_flags": sorted(aggregate_flags)}


def display_path(path: Path, home: Path, redact: bool) -> str:
    try:
        resolved = path.expanduser().resolve()
    except Exception:
        resolved = path.expanduser()
    if redact:
        try:
            rel = resolved.relative_to(home.resolve())
            return "$HOME/" + str(rel)
        except Exception:
            return str(resolved)
    return str(resolved)


def inspect_skill(skill_dir: Path, root: Path, home: Path, redact_paths: bool) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    text = safe_read_text(skill_md) if skill_md.exists() else ""
    meta, frontmatter_style = parse_frontmatter(text) if text else ({}, "missing")
    parsed_name = meta.get("name")
    description = meta.get("description", "")
    dir_name = skill_dir.name

    issues: list[str] = []
    if not skill_md.exists():
        issues.append("missing_skill_md")
    if frontmatter_style != "strict":
        issues.append(f"frontmatter_{frontmatter_style}")
    if not parsed_name:
        issues.append("missing_name")
    elif parsed_name != dir_name:
        issues.append("name_does_not_match_directory")
    if parsed_name and (not NAME_RE.match(parsed_name) or "--" in parsed_name):
        issues.append("invalid_name")
    if not description:
        issues.append("missing_description")
    elif len(description) < 40:
        issues.append("short_description")
    elif len(description) > 700:
        issues.append("long_description")
    if description and GENERIC_DESCRIPTION_RE.search(description) and "Use when" not in description and "when" not in description.lower():
        issues.append("generic_description")

    optional_dirs = [
        name
        for name in ["references", "scripts", "assets", "evals", "agents", "examples", "checklists"]
        if (skill_dir / name).exists()
    ]
    eval_files = sorted(p.name for p in (skill_dir / "evals").glob("*.json")) if (skill_dir / "evals").exists() else []
    if "evals" not in optional_dirs:
        issues.append("missing_evals")

    script_info = inspect_scripts(skill_dir, redact_paths, home)
    risk_flags: set[str] = set(script_info["risk_flags"])
    skill_text_flags = scan_text_flags(text)
    for flag in skill_text_flags:
        if flag == "secret_or_credential_reference":
            risk_flags.add("skill_md_mentions_credentials")
    if script_info["count"] > 0:
        risk_flags.add("has_scripts")

    urls = sorted(set(URL_RE.findall(text)))[:20]
    symlink_target = None
    if skill_dir.is_symlink():
        try:
            symlink_target = display_path(skill_dir.resolve(), home, redact_paths)
        except Exception:
            symlink_target = "unresolved"

    try:
        stat = skill_dir.stat()
        mtime = _dt.datetime.fromtimestamp(stat.st_mtime, tz=_dt.timezone.utc).isoformat()
    except Exception:
        mtime = None

    name = parsed_name or dir_name
    return {
        "name": name,
        "directory_name": dir_name,
        "path": display_path(skill_dir, home, redact_paths),
        "root": display_path(root, home, redact_paths),
        "scope_guess": classify_root(root, home),
        "symlink_target": symlink_target,
        "frontmatter": {
            "style": frontmatter_style,
            "name": parsed_name,
            "description": description,
            "description_chars": len(description),
        },
        "skill_md": {
            "exists": skill_md.exists(),
            "line_count": len(text.splitlines()) if text else 0,
            "char_count": len(text),
            "sha256_prefix": sha256_prefix(text) if text else "",
        },
        "context_cost": {
            "startup_chars_estimate": len(name or "") + len(description) + len(str(skill_dir)),
            "description_chars": len(description),
        },
        "optional_dirs": optional_dirs,
        "eval_files": eval_files,
        "scripts": script_info,
        "agents_openai": parse_openai_yaml(skill_dir),
        "trigger_evals": parse_trigger_evals(skill_dir),
        "urls_in_skill_md": urls,
        "issues": sorted(set(issues)),
        "risk_flags": sorted(risk_flags),
        "timestamps": {"directory_mtime_utc": mtime},
    }


def dedupe_roots(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        try:
            key = str(path.expanduser().resolve())
        except Exception:
            key = str(path.expanduser())
        if key not in seen:
            seen.add(key)
            result.append(path)
    return result


def find_duplicates(skills: list[dict[str, Any]]) -> dict[str, Any]:
    by_name: dict[str, list[str]] = {}
    by_hash: dict[str, list[str]] = {}
    for item in skills:
        by_name.setdefault(str(item.get("name")), []).append(str(item.get("path")))
        body_hash = item.get("skill_md", {}).get("sha256_prefix")
        if body_hash:
            by_hash.setdefault(str(body_hash), []).append(str(item.get("path")))
    return {
        "by_name": {k: v for k, v in by_name.items() if len(v) > 1 and k},
        "by_skill_md_hash": {k: v for k, v in by_hash.items() if len(v) > 1 and k},
    }


def build_inventory(args: argparse.Namespace) -> dict[str, Any]:
    home = Path(os.path.expanduser("~"))
    roots: list[Path] = []
    if args.roots:
        roots.extend(Path(p).expanduser() for p in args.roots)
        if args.include_defaults:
            roots.extend(default_roots(home))
    else:
        roots.extend(default_roots(home))
    if args.include_repo:
        roots.extend(repo_roots(Path(args.cwd)))
    roots = dedupe_roots(roots)

    skills: list[dict[str, Any]] = []
    missing_roots: list[str] = []
    for root in roots:
        root_expanded = root.expanduser()
        if not root_expanded.exists():
            missing_roots.append(display_path(root_expanded, home, args.redact_paths))
            continue
        for skill_dir in discover_skill_dirs(root_expanded):
            skills.append(inspect_skill(skill_dir, root_expanded, home, args.redact_paths))

    duplicates = find_duplicates(skills)
    duplicate_names = set(duplicates["by_name"].keys())
    duplicate_paths = {path for paths in duplicates["by_name"].values() for path in paths}
    for item in skills:
        if item["name"] in duplicate_names or item["path"] in duplicate_paths:
            item.setdefault("issues", []).append("duplicate_name")
            item["issues"] = sorted(set(item["issues"]))

    return {
        "schema_version": "1.0",
        "generated_at_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "command": " ".join(sys.argv),
        "roots_requested": [display_path(p, home, args.redact_paths) for p in roots],
        "roots_missing": missing_roots,
        "skill_count": len(skills),
        "skills": skills,
        "duplicates": duplicates,
        "notes": [
            "This inventory does not prove usage frequency.",
            "Script risk flags are keyword heuristics; review flagged files before acting.",
            "No network access or destructive actions are performed by this script.",
        ],
    }


def markdown_escape(value: Any) -> str:
    text = str(value if value is not None else "")
    return text.replace("|", "\\|").replace("\n", " ")


def to_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Skill Inventory",
        "",
        f"Generated: `{data['generated_at_utc']}`",
        f"Skills found: `{data['skill_count']}`",
        "",
        "## Roots",
        "",
    ]
    for root in data["roots_requested"]:
        missing = " (missing)" if root in data.get("roots_missing", []) else ""
        lines.append(f"- `{root}`{missing}")
    lines.extend(
        [
            "",
            "## Skills",
            "",
            "| Skill | Scope | Description chars | Lines | Dirs | Scripts | OpenAI implicit | Issues | Risk flags | Path |",
            "|---|---|---:|---:|---|---:|---|---|---|---|",
        ]
    )
    for item in sorted(data["skills"], key=lambda s: (s.get("scope_guess", ""), s.get("name", ""))):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(item.get('name'))}`",
                    markdown_escape(item.get("scope_guess")),
                    str(item.get("frontmatter", {}).get("description_chars", 0)),
                    str(item.get("skill_md", {}).get("line_count", 0)),
                    markdown_escape(", ".join(item.get("optional_dirs", [])) or "none"),
                    str(item.get("scripts", {}).get("count", 0)),
                    markdown_escape(item.get("agents_openai", {}).get("allow_implicit_invocation", "unknown")),
                    markdown_escape(", ".join(item.get("issues", [])) or "none"),
                    markdown_escape(", ".join(item.get("risk_flags", [])) or "none"),
                    f"`{markdown_escape(item.get('path'))}`",
                ]
            )
            + " |"
        )
    if data.get("duplicates", {}).get("by_name"):
        lines.extend(["", "## Duplicate names", ""])
        for name, paths in data["duplicates"]["by_name"].items():
            lines.append(f"- `{markdown_escape(name)}`")
            for path in paths:
                lines.append(f"  - `{markdown_escape(path)}`")
    lines.extend(["", "## Notes", ""])
    for note in data.get("notes", []):
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory installed or repository Agent Skills without network or destructive changes."
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        help="Skill root directories to scan. If omitted, scans common user/admin locations.",
    )
    parser.add_argument(
        "--include-defaults",
        action="store_true",
        help="When --roots is provided, also scan common user/admin locations.",
    )
    parser.add_argument(
        "--include-repo",
        action="store_true",
        help="Also scan .agents/skills from the current directory upward to the git root.",
    )
    parser.add_argument("--cwd", default=os.getcwd(), help="Directory used for --include-repo. Default: cwd.")
    parser.add_argument("--redact-paths", action="store_true", help="Replace the home directory with $HOME in output paths.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--output", help="Write output to a file instead of stdout.")
    args = parser.parse_args()

    data = build_inventory(args)
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(data)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
