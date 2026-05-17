#!/usr/bin/env python3
"""Collect safe, read-only context for DBX diff review.

The script selects an explicit review target before collecting changed files:
staged/index, unstaged, local, branch, branch-plus-local, commit range, named
commits, or selected files. It does not run project test/build commands and it
does not modify files.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass
class CommandResult:
    code: int
    stdout: str
    stderr: str


def run(cmd: list[str], cwd: Path) -> CommandResult:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return CommandResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())
    except FileNotFoundError:
        return CommandResult(127, "", f"command not found: {cmd[0]}")


def is_git_repo(root: Path) -> bool:
    return run(["git", "rev-parse", "--is-inside-work-tree"], root).stdout == "true"


def infer_base(root: Path, explicit_base: str | None) -> str | None:
    if explicit_base:
        return explicit_base
    candidates = ["origin/main", "origin/master", "main", "master", "develop", "origin/develop"]
    for candidate in candidates:
        res = run(["git", "rev-parse", "--verify", candidate], root)
        if res.code == 0:
            merge_base = run(["git", "merge-base", "HEAD", candidate], root)
            if merge_base.code == 0 and merge_base.stdout:
                return merge_base.stdout.splitlines()[0]
            return candidate
    return None


def parse_name_status(text: str, source: str) -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        if len(parts) >= 3 and status.startswith("R"):
            files.append({"status": status, "path": parts[2], "old_path": parts[1], "source": source})
        elif len(parts) >= 2:
            files.append({"status": status, "path": parts[1], "source": source})
    return files


def parse_status_porcelain(text: str) -> dict[str, list[str]]:
    buckets = {"staged": [], "unstaged": [], "untracked": []}
    for line in text.splitlines():
        if not line:
            continue
        if line.startswith("?? "):
            buckets["untracked"].append(line[3:])
            continue
        if len(line) < 4:
            continue
        index_status = line[0]
        worktree_status = line[1]
        path = line[3:]
        if index_status != " ":
            buckets["staged"].append(path)
        if worktree_status != " ":
            buckets["unstaged"].append(path)
    return buckets


def dedup_files(files: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    seen: dict[tuple[str, str, str], dict[str, str]] = {}
    for item in files:
        key = (item.get("source", ""), item.get("status", ""), item.get("path", ""))
        seen[key] = item
    return list(seen.values())


def file_args(paths: list[str]) -> list[str]:
    return ["--", *paths] if paths else []


def diff_name_status(root: Path, args: list[str], source: str) -> list[dict[str, str]]:
    return parse_name_status(run(args, root).stdout, source)


def diff_text(root: Path, args: list[str], max_chars: int) -> str:
    return run(args, root).stdout[:max_chars]


def collect_target(
    root: Path,
    target: str,
    base: str | None,
    head: str,
    commit_range: str | None,
    commits: list[str],
    files: list[str],
    file_scope: str,
    max_diff_chars: int,
) -> tuple[dict[str, Any], str]:
    """Return target data and diff scan text."""
    selected = target
    status = parse_status_porcelain(run(["git", "status", "--porcelain"], root).stdout)
    inferred_base = infer_base(root, base)

    def has_output(cmd: list[str]) -> bool:
        return bool(run(cmd, root).stdout.strip())

    if target == "auto":
        if has_output(["git", "diff", "--cached", "--name-only"]):
            selected = "staged"
        elif inferred_base and has_output(["git", "diff", "--name-only", f"{inferred_base}...{head}"]):
            selected = "branch"
        elif has_output(["git", "diff", "--name-only"]):
            selected = "unstaged"
        else:
            selected = "none"

    changed: list[dict[str, str]] = []
    diff_stat = ""
    diff_scan = ""
    spec: dict[str, Any] = {
        "selected_target": selected,
        "requested_target": target,
        "base": inferred_base,
        "head": head,
        "files_filter": files,
        "file_scope": file_scope if selected == "files" else None,
        "commit_range": commit_range,
        "commits": commits,
    }

    if selected == "staged":
        changed = diff_name_status(root, ["git", "diff", "--cached", "--name-status"], "staged")
        diff_stat = run(["git", "diff", "--cached", "--stat"], root).stdout
        diff_scan = diff_text(root, ["git", "diff", "--cached", "--unified=0"], max_diff_chars)
    elif selected == "unstaged":
        changed = diff_name_status(root, ["git", "diff", "--name-status"], "unstaged")
        diff_stat = run(["git", "diff", "--stat"], root).stdout
        diff_scan = diff_text(root, ["git", "diff", "--unified=0"], max_diff_chars)
    elif selected == "local":
        changed = []
        changed.extend(diff_name_status(root, ["git", "diff", "--cached", "--name-status"], "staged"))
        changed.extend(diff_name_status(root, ["git", "diff", "--name-status"], "unstaged"))
        diff_stat = "\n".join(filter(None, [
            run(["git", "diff", "--cached", "--stat"], root).stdout,
            run(["git", "diff", "--stat"], root).stdout,
        ]))
        diff_scan = "\n".join(filter(None, [
            diff_text(root, ["git", "diff", "--cached", "--unified=0"], max_diff_chars // 2),
            diff_text(root, ["git", "diff", "--unified=0"], max_diff_chars // 2),
        ]))[:max_diff_chars]
    elif selected == "branch":
        if not inferred_base:
            spec["error"] = "base could not be inferred; pass --base"
        else:
            rng = f"{inferred_base}...{head}"
            changed = diff_name_status(root, ["git", "diff", "--name-status", rng], "branch")
            diff_stat = run(["git", "diff", "--stat", rng], root).stdout
            diff_scan = diff_text(root, ["git", "diff", "--unified=0", rng], max_diff_chars)
            spec["range"] = rng
    elif selected == "branch-plus-local":
        if not inferred_base:
            spec["error"] = "base could not be inferred; pass --base"
        else:
            rng = f"{inferred_base}...{head}"
            changed.extend(diff_name_status(root, ["git", "diff", "--name-status", rng], "branch"))
            changed.extend(diff_name_status(root, ["git", "diff", "--cached", "--name-status"], "staged"))
            changed.extend(diff_name_status(root, ["git", "diff", "--name-status"], "unstaged"))
            diff_stat = "\n".join(filter(None, [
                run(["git", "diff", "--stat", rng], root).stdout,
                run(["git", "diff", "--cached", "--stat"], root).stdout,
                run(["git", "diff", "--stat"], root).stdout,
            ]))
            diff_scan = "\n".join(filter(None, [
                diff_text(root, ["git", "diff", "--unified=0", rng], max_diff_chars // 3),
                diff_text(root, ["git", "diff", "--cached", "--unified=0"], max_diff_chars // 3),
                diff_text(root, ["git", "diff", "--unified=0"], max_diff_chars // 3),
            ]))[:max_diff_chars]
            spec["range"] = rng
    elif selected == "commit-range":
        if not commit_range:
            spec["error"] = "--commit-range is required for target commit-range"
        else:
            changed = diff_name_status(root, ["git", "diff", "--name-status", commit_range], "commit-range")
            diff_stat = run(["git", "diff", "--stat", commit_range], root).stdout
            diff_scan = diff_text(root, ["git", "diff", "--unified=0", commit_range], max_diff_chars)
    elif selected == "commits":
        if not commits:
            spec["error"] = "--commits is required for target commits"
        else:
            scans = []
            stats = []
            for commit in commits:
                changed.extend(diff_name_status(root, ["git", "show", "--format=", "--name-status", commit], f"commit:{commit}"))
                stats.append(run(["git", "show", "--format=short", "--stat", commit], root).stdout)
                scans.append(diff_text(root, ["git", "show", "--format=medium", "--unified=0", commit], max_diff_chars // max(1, len(commits))))
            diff_stat = "\n\n".join(filter(None, stats))
            diff_scan = "\n\n".join(filter(None, scans))[:max_diff_chars]
    elif selected == "files":
        if not files:
            spec["error"] = "--files is required for target files"
        elif file_scope == "staged":
            changed = diff_name_status(root, ["git", "diff", "--cached", "--name-status", *file_args(files)], "files:staged")
            diff_stat = run(["git", "diff", "--cached", "--stat", *file_args(files)], root).stdout
            diff_scan = diff_text(root, ["git", "diff", "--cached", "--unified=0", *file_args(files)], max_diff_chars)
        elif file_scope == "unstaged":
            changed = diff_name_status(root, ["git", "diff", "--name-status", *file_args(files)], "files:unstaged")
            diff_stat = run(["git", "diff", "--stat", *file_args(files)], root).stdout
            diff_scan = diff_text(root, ["git", "diff", "--unified=0", *file_args(files)], max_diff_chars)
        elif file_scope == "local":
            changed.extend(diff_name_status(root, ["git", "diff", "--cached", "--name-status", *file_args(files)], "files:staged"))
            changed.extend(diff_name_status(root, ["git", "diff", "--name-status", *file_args(files)], "files:unstaged"))
            diff_stat = "\n".join(filter(None, [
                run(["git", "diff", "--cached", "--stat", *file_args(files)], root).stdout,
                run(["git", "diff", "--stat", *file_args(files)], root).stdout,
            ]))
            diff_scan = "\n".join(filter(None, [
                diff_text(root, ["git", "diff", "--cached", "--unified=0", *file_args(files)], max_diff_chars // 2),
                diff_text(root, ["git", "diff", "--unified=0", *file_args(files)], max_diff_chars // 2),
            ]))[:max_diff_chars]
        elif file_scope == "branch":
            if not inferred_base:
                spec["error"] = "base could not be inferred; pass --base"
            else:
                rng = f"{inferred_base}...{head}"
                changed = diff_name_status(root, ["git", "diff", "--name-status", rng, *file_args(files)], "files:branch")
                diff_stat = run(["git", "diff", "--stat", rng, *file_args(files)], root).stdout
                diff_scan = diff_text(root, ["git", "diff", "--unified=0", rng, *file_args(files)], max_diff_chars)
                spec["range"] = rng
    elif selected == "none":
        changed = []
    else:
        spec["error"] = f"unsupported target: {selected}"

    target_paths = sorted({item.get("path", "") for item in changed if item.get("path")})
    dirty_all = sorted(set(status["staged"] + status["unstaged"] + status["untracked"]))
    out_of_scope = [p for p in dirty_all if p not in target_paths]
    partial_out_of_scope: list[str] = []
    if selected == "staged" or (selected == "files" and file_scope == "staged"):
        partial_out_of_scope = sorted(p for p in status["unstaged"] if p in target_paths)

    data = {
        "target_spec": spec,
        "changed_files": dedup_files(changed),
        "diff_stat": diff_stat,
        "status_summary": status,
        "out_of_scope_dirty_files": out_of_scope,
        "partial_out_of_scope_files": partial_out_of_scope,
    }
    return data, diff_scan


def file_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def detect_package_manager(root: Path) -> str:
    if file_exists(root, "pnpm-lock.yaml"):
        return "pnpm"
    if file_exists(root, "yarn.lock"):
        return "yarn"
    if file_exists(root, "bun.lockb") or file_exists(root, "bun.lock"):
        return "bun"
    return "npm"


def detect_validation_commands(root: Path) -> list[str]:
    commands: list[str] = []
    package = load_json(root / "package.json") if file_exists(root, "package.json") else None
    if package:
        pm = detect_package_manager(root)
        scripts = package.get("scripts") or {}
        for script in ["lint", "typecheck", "test", "build", "test:unit", "test:e2e"]:
            if script in scripts:
                commands.append(f"{pm} run {script}" if pm in {"npm", "yarn", "bun"} else f"{pm} {script}")
        if file_exists(root, "tsconfig.json") and "typecheck" not in scripts:
            commands.append("npx tsc --noEmit")
    if file_exists(root, "Cargo.toml"):
        commands.extend(["cargo check", "cargo test"])
    if file_exists(root, "go.mod"):
        commands.append("go test ./...")
    if file_exists(root, "pyproject.toml") or file_exists(root, "pytest.ini"):
        commands.append("pytest")
    if file_exists(root, "Makefile"):
        makefile = (root / "Makefile").read_text(encoding="utf-8", errors="ignore")
        for target in ["test", "check", "lint"]:
            if re.search(rf"^{re.escape(target)}\s*:", makefile, re.M):
                commands.append(f"make {target}")
    return list(dict.fromkeys(commands))


def detect_project_files(root: Path) -> list[str]:
    candidates = [
        "AGENTS.md",
        "CLAUDE.md",
        "REVIEW.md",
        "README.md",
        "package.json",
        "tsconfig.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "package-lock.json",
        "Cargo.toml",
        "go.mod",
        "pyproject.toml",
        "pytest.ini",
        "Makefile",
        ".github/workflows",
    ]
    return [c for c in candidates if file_exists(root, c)]


def detect_risk_flags(files: list[dict[str, str]], diff_scan: str) -> list[dict[str, str]]:
    paths = "\n".join(item.get("path", "") for item in files)
    haystack = f"{paths}\n{diff_scan}"
    rules: list[tuple[str, str, str]] = [
        ("user-impact", r"(route|router|page|screen|component|form|checkout|billing|payment|quota|entitlement|notification|upload|download)", "User-visible flow or UI/API entry changed."),
        ("auth-permission", r"(auth|permission|role|session|token|jwt|oauth|login|logout|tenant|workspace)", "Authentication, authorization, or boundary-sensitive state changed."),
        ("data-model", r"(schema|migration|model|entity|dto|store|reducer|cache|state|selector|normaliz|mapper|adapter|database|prisma|sql)", "Data model, state ownership, cache, or persistence surface changed."),
        ("frontend-async", r"(useEffect|useMemo|useCallback|AbortController|setTimeout|setInterval|localStorage|sessionStorage|hydration|optimistic)", "Frontend async/state lifecycle surface changed."),
        ("security-sink", r"(dangerouslySetInnerHTML|exec\(|spawn\(|eval\(|innerHTML|SQL|query\(|fs\.|path\.|redirect|webhook|secret|password|api[_-]?key)", "Potential trust-boundary or sink-related change."),
        ("contract", r"(export\s+type|export\s+interface|OpenAPI|graphql|proto|public API|breaking|config|env|CLI|argv)", "Public type, API, config, or protocol contract may have changed."),
        ("dependency", r"(package\.json|pnpm-lock\.yaml|yarn\.lock|package-lock\.json|Cargo\.toml|go\.mod|requirements\.txt|pyproject\.toml)", "Dependency or manifest changed."),
        ("generated", r"(__generated__|generated|dist/|build/|\.gen\.|codegen|openapi-generated)", "Generated or built artifact may need sync validation."),
    ]
    flags: list[dict[str, str]] = []
    for name, pattern, reason in rules:
        if re.search(pattern, haystack, re.I):
            flags.append({"name": name, "reason": reason})
    return flags


def render_markdown(data: dict[str, Any]) -> str:
    lines = ["# DBX Diff Review Context", ""]
    lines.append(f"Root: `{data['root']}`")
    lines.append(f"Git repo: `{data['git_repo']}`")
    target_spec = data.get("target_spec") or {}
    lines.append(f"Selected target: `{target_spec.get('selected_target', 'unknown')}`")
    if target_spec.get("base"):
        lines.append(f"Base: `{target_spec['base']}`")
    if target_spec.get("head"):
        lines.append(f"Head: `{target_spec['head']}`")
    if target_spec.get("range"):
        lines.append(f"Range: `{target_spec['range']}`")
    if target_spec.get("files_filter"):
        lines.append("Files filter: " + ", ".join(f"`{p}`" for p in target_spec["files_filter"]))
    if target_spec.get("error"):
        lines.append(f"Target error: `{target_spec['error']}`")
    lines.append("")

    lines.append("## Changed files in selected target")
    files = data.get("changed_files") or []
    if files:
        for item in files:
            old = f" from `{item['old_path']}`" if item.get("old_path") else ""
            source = f" ({item.get('source')})" if item.get("source") else ""
            lines.append(f"- `{item.get('status', '?')}` `{item.get('path', '')}`{old}{source}")
    else:
        lines.append("- No changed files detected for selected target.")
    lines.append("")

    if data.get("out_of_scope_dirty_files"):
        lines.append("## Out-of-scope dirty files")
        for rel in data["out_of_scope_dirty_files"]:
            lines.append(f"- `{rel}`")
        lines.append("These files are not included in the selected target unless you explicitly include them.")
        lines.append("")

    if data.get("partial_out_of_scope_files"):
        lines.append("## Partial out-of-scope files")
        for rel in data["partial_out_of_scope_files"]:
            lines.append(f"- `{rel}`")
        lines.append("The selected staged target includes staged hunks from these files, but they also have unstaged hunks outside this review target.")
        lines.append("")

    if data.get("diff_stat"):
        lines.append("## Diff stat")
        lines.append("```text")
        lines.append(data["diff_stat"])
        lines.append("```")
        lines.append("")

    lines.append("## Risk flags")
    flags = data.get("risk_flags") or []
    if flags:
        for flag in flags:
            lines.append(f"- `{flag['name']}`: {flag['reason']}")
    else:
        lines.append("- No obvious high-risk flags detected from paths/diff text. This is not proof of safety.")
    lines.append("")

    lines.append("## Project files detected")
    project_files = data.get("project_files") or []
    if project_files:
        for rel in project_files:
            lines.append(f"- `{rel}`")
    else:
        lines.append("- None from the known list.")
    lines.append("")

    lines.append("## Suggested validation commands")
    commands = data.get("suggested_validation_commands") or []
    if commands:
        for command in commands:
            lines.append(f"- `{command}`")
    else:
        lines.append("- No validation command detected. Ask the user or inspect project docs/CI.")
    lines.append("")
    lines.append("Note: this script did not run any project validation commands and did not modify files.")
    return "\n".join(lines)


def parse_commits_arg(raw: str | None) -> list[str]:
    if not raw:
        return []
    items: list[str] = []
    for part in raw.replace(",", " ").split():
        if part.strip():
            items.append(part.strip())
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect safe read-only context for DBX diff review.")
    parser.add_argument("--root", default=".", help="Repository root to inspect. Default: current directory.")
    parser.add_argument(
        "--target",
        choices=["auto", "staged", "unstaged", "local", "branch", "branch-plus-local", "commit-range", "commits", "files"],
        default="auto",
        help="Review target to collect. Prefer explicit targets over auto.",
    )
    parser.add_argument("--base", default=None, help="Base branch, commit, or ref for branch/file-scope branch review.")
    parser.add_argument("--head", default="HEAD", help="Head ref for branch review. Default: HEAD.")
    parser.add_argument("--commit-range", default=None, help="Commit range such as main..HEAD or abc123^..abc123.")
    parser.add_argument("--commits", default=None, help="Comma or space separated commits for target=commits.")
    parser.add_argument("--files", nargs="*", default=[], help="File paths for target=files.")
    parser.add_argument(
        "--file-scope",
        choices=["staged", "unstaged", "local", "branch"],
        default="local",
        help="Source for target=files. Default: local.",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format.")
    parser.add_argument("--max-diff-chars", type=int, default=400_000, help="Max diff text scanned for risk flags.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: root does not exist: {root}", file=sys.stderr)
        return 2

    git_repo = is_git_repo(root)
    target_data: dict[str, Any] = {
        "target_spec": {"selected_target": "none", "requested_target": args.target},
        "changed_files": [],
        "diff_stat": "",
        "status_summary": {},
        "out_of_scope_dirty_files": [],
    }
    diff_scan = ""
    if git_repo:
        target_data, diff_scan = collect_target(
            root=root,
            target=args.target,
            base=args.base,
            head=args.head,
            commit_range=args.commit_range,
            commits=parse_commits_arg(args.commits),
            files=args.files,
            file_scope=args.file_scope,
            max_diff_chars=args.max_diff_chars,
        )

    data = {
        "root": str(root),
        "git_repo": git_repo,
        **target_data,
        "risk_flags": detect_risk_flags(target_data.get("changed_files") or [], diff_scan),
        "project_files": detect_project_files(root),
        "suggested_validation_commands": detect_validation_commands(root),
        "script_policy": "read-only; no project commands executed; no files modified",
    }

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
