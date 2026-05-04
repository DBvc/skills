#!/usr/bin/env python3
"""Validate DBX skill repository structure.

This script intentionally uses only the Python standard library.
It performs lightweight structural validation, not semantic judging.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
CANONICAL_EVAL_KINDS = {"positive", "negative", "near_miss", "failure_mode", "safety"}
OPTIONAL_SKILL_DIRS = {"references", "scripts", "assets", "evals", "agents", "examples", "checklists"}


@dataclass
class Issue:
    level: str
    path: str
    message: str


@dataclass
class SkillReport:
    name: str
    path: str
    parsed_name: str | None = None
    description: str | None = None
    frontmatter_style: str = "missing"
    line_count: int = 0
    optional_dirs: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "warning"]


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_simple_yaml_map(block: str) -> dict[str, str]:
    """Parse a small subset of YAML frontmatter.

    This is not a full YAML parser. It is enough for name/description/metadata-light checks
    without adding dependencies.
    """
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


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, str, str | None]:
    """Return metadata, body, style, warning.

    style is one of: strict, nonstandard-minified, missing.
    """
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                block = "\n".join(lines[1:idx])
                body = "\n".join(lines[idx + 1 :])
                return parse_simple_yaml_map(block), body, "strict", None
        return {}, text, "missing", "Opening frontmatter delimiter found, but closing delimiter is missing."

    # Compatibility path for accidentally minified frontmatter such as:
    # --- name: dbx-x description: ... --- # Body
    match = re.search(r"^---\s+name:\s*(?P<name>\S+)\s+description:\s*(?P<desc>.*?)\s+---\s*(?P<body>.*)$", text, re.S)
    if match:
        return (
            {"name": strip_quotes(match.group("name")), "description": match.group("desc").strip()},
            match.group("body"),
            "nonstandard-minified",
            "Frontmatter appears minified onto one line. Use strict delimiter lines for maximum compatibility.",
        )

    return {}, text, "missing", "SKILL.md must start with YAML frontmatter delimiter on its own line: ---."


def issue(report: SkillReport, level: str, path: Path, message: str) -> None:
    report.issues.append(Issue(level=level, path=str(path), message=message))


def validate_name(name: str | None, skill_dir_name: str) -> list[str]:
    messages: list[str] = []
    if not name:
        messages.append("Missing required frontmatter field: name.")
        return messages
    if name != skill_dir_name:
        messages.append(f"Frontmatter name '{name}' does not match directory name '{skill_dir_name}'.")
    if len(name) > 64:
        messages.append("Skill name exceeds 64 characters.")
    if not NAME_RE.match(name) or "--" in name or name.startswith("-") or name.endswith("-"):
        messages.append("Skill name must use lowercase letters, numbers, and single hyphens only.")
    return messages


def validate_description(description: str | None) -> list[str]:
    messages: list[str] = []
    if description is None or not description.strip():
        messages.append("Missing required frontmatter field: description.")
        return messages
    if len(description) > 1024:
        messages.append("Description exceeds 1024 characters.")
    if len(description.strip()) < 25:
        messages.append("Description is very short; include what the skill does and when to use it.")
    return messages


def read_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def validate_triggers_json(report: SkillReport, path: Path) -> None:
    data, error = read_json(path)
    if error:
        issue(report, "error", path, f"Invalid JSON: {error}")
        return
    if not isinstance(data, dict):
        issue(report, "error", path, "triggers.json must be a JSON object.")
        return
    if data.get("skill_name") and data.get("skill_name") != report.name:
        issue(report, "warning", path, f"skill_name is '{data.get('skill_name')}', expected '{report.name}'.")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        issue(report, "warning", path, "triggers.json should contain a non-empty cases array.")
        return
    seen_ids: set[str] = set()
    kinds: set[str] = set()
    for idx, case in enumerate(cases):
        case_path = f"{path}#{idx}"
        if not isinstance(case, dict):
            issue(report, "error", path, f"Case {idx} must be an object.")
            continue
        case_id = case.get("id")
        kind = case.get("kind")
        kinds.add(str(kind))
        if not case_id:
            issue(report, "error", path, f"{case_path}: missing id.")
        elif case_id in seen_ids:
            issue(report, "error", path, f"{case_path}: duplicate id '{case_id}'.")
        else:
            seen_ids.add(str(case_id))
        if kind not in CANONICAL_EVAL_KINDS:
            issue(report, "error", path, f"{case_path}: kind must be one of {sorted(CANONICAL_EVAL_KINDS)}.")
        if not isinstance(case.get("prompt"), str) or not case.get("prompt", "").strip():
            issue(report, "error", path, f"{case_path}: prompt must be a non-empty string.")
        if not isinstance(case.get("expected_trigger"), bool):
            issue(report, "error", path, f"{case_path}: expected_trigger must be true or false.")
    if "positive" not in kinds:
        issue(report, "warning", path, "Trigger evals should include positive cases.")
    if "negative" not in kinds:
        issue(report, "warning", path, "Trigger evals should include negative cases.")
    if "near_miss" not in kinds:
        issue(report, "warning", path, "Trigger evals should include near_miss cases.")


def validate_evals_json(report: SkillReport, path: Path) -> None:
    data, error = read_json(path)
    if error:
        issue(report, "error", path, f"Invalid JSON: {error}")
        return
    if not isinstance(data, dict):
        issue(report, "error", path, "evals.json must be a JSON object.")
        return
    if data.get("skill_name") and data.get("skill_name") != report.name:
        issue(report, "warning", path, f"skill_name is '{data.get('skill_name')}', expected '{report.name}'.")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        issue(report, "warning", path, "evals.json should contain a non-empty evals array.")
        return
    seen_ids: set[str] = set()
    kinds: set[str] = set()
    for idx, item in enumerate(evals):
        item_path = f"{path}#{idx}"
        if not isinstance(item, dict):
            issue(report, "error", path, f"Eval {idx} must be an object.")
            continue
        eval_id = item.get("id")
        kind = item.get("kind")
        kinds.add(str(kind))
        if not eval_id:
            issue(report, "error", path, f"{item_path}: missing id.")
        elif eval_id in seen_ids:
            issue(report, "error", path, f"{item_path}: duplicate id '{eval_id}'.")
        else:
            seen_ids.add(str(eval_id))
        if kind not in CANONICAL_EVAL_KINDS:
            issue(report, "error", path, f"{item_path}: kind must be one of {sorted(CANONICAL_EVAL_KINDS)}.")
        if not isinstance(item.get("prompt"), str) or not item.get("prompt", "").strip():
            issue(report, "error", path, f"{item_path}: prompt must be a non-empty string.")
        if not (item.get("expected_behavior") or item.get("expected_output")):
            issue(report, "warning", path, f"{item_path}: add expected_behavior or expected_output.")
        checks = item.get("checks")
        if checks is not None and not isinstance(checks, dict):
            issue(report, "error", path, f"{item_path}: checks must be an object if present.")
    if "positive" not in kinds:
        issue(report, "warning", path, "Output evals should include positive cases.")
    if "near_miss" not in kinds and "failure_mode" not in kinds and "safety" not in kinds:
        issue(report, "warning", path, "Output evals should include near_miss, failure_mode, or safety cases.")


def validate_skill(skill_dir: Path, root: Path) -> SkillReport:
    report = SkillReport(name=skill_dir.name, path=str(skill_dir.relative_to(root)))
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        issue(report, "error", skill_md, "Missing SKILL.md.")
        return report

    text = skill_md.read_text(encoding="utf-8")
    report.line_count = len(text.splitlines())
    meta, _body, style, warning = parse_frontmatter(text)
    report.frontmatter_style = style
    report.parsed_name = meta.get("name")
    report.description = meta.get("description")
    if warning:
        issue(report, "warning" if style != "missing" else "error", skill_md, warning)
    for msg in validate_name(report.parsed_name, skill_dir.name):
        issue(report, "error", skill_md, msg)
    for msg in validate_description(report.description):
        issue(report, "error" if "Missing" in msg else "warning", skill_md, msg)
    if report.line_count > 500:
        issue(report, "warning", skill_md, f"SKILL.md has {report.line_count} lines; consider splitting references.")

    for child in sorted(skill_dir.iterdir()):
        if child.is_dir() and child.name in OPTIONAL_SKILL_DIRS:
            report.optional_dirs.append(child.name)

    evals_dir = skill_dir / "evals"
    if evals_dir.exists():
        triggers = evals_dir / "triggers.json"
        evals = evals_dir / "evals.json"
        if triggers.exists():
            validate_triggers_json(report, triggers)
        else:
            issue(report, "warning", triggers, "Missing trigger evals. Add evals/triggers.json for serious skills.")
        if evals.exists():
            validate_evals_json(report, evals)
        else:
            issue(report, "warning", evals, "Missing output evals. Add evals/evals.json for serious skills.")
    else:
        issue(report, "warning", evals_dir, "Missing evals directory. Simple skills may accept this, but serious skills need evals.")

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in sorted(p for p in scripts_dir.rglob("*") if p.is_file()):
            if script.suffix in {".py", ".sh", ".js", ".ts", ".rb"}:
                try:
                    content = script.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                if "--help" not in content and "argparse" not in content and "Usage" not in content:
                    issue(report, "warning", script, "Script should document --help or usage for agentic use.")

    return report


def scan(root: Path) -> tuple[list[SkillReport], list[Issue]]:
    issues: list[Issue] = []
    skills_dir = root / "skills"
    if not skills_dir.exists():
        return [], [Issue("error", str(skills_dir), "Missing skills directory.")]
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    reports = [validate_skill(skill_dir, root) for skill_dir in skill_dirs]

    readme = root / "README.md"
    index = root / "DBX_SKILL_INDEX.md"
    if readme.exists():
        readme_text = readme.read_text(encoding="utf-8", errors="ignore")
        for report in reports:
            if report.name not in readme_text:
                issues.append(Issue("warning", str(readme), f"README.md does not mention {report.name}."))
    if index.exists():
        index_text = index.read_text(encoding="utf-8", errors="ignore")
        for report in reports:
            if report.name not in index_text:
                issues.append(Issue("warning", str(index), f"DBX_SKILL_INDEX.md does not mention {report.name}."))
    else:
        issues.append(Issue("warning", str(index), "Missing DBX_SKILL_INDEX.md."))

    return reports, issues


def to_json(reports: list[SkillReport], root_issues: list[Issue]) -> dict[str, Any]:
    all_issues = root_issues + [issue for report in reports for issue in report.issues]
    return {
        "summary": {
            "skills": len(reports),
            "errors": sum(1 for i in all_issues if i.level == "error"),
            "warnings": sum(1 for i in all_issues if i.level == "warning"),
        },
        "root_issues": [issue.__dict__ for issue in root_issues],
        "skills": [
            {
                "name": report.name,
                "path": report.path,
                "parsed_name": report.parsed_name,
                "description_length": len(report.description or ""),
                "frontmatter_style": report.frontmatter_style,
                "line_count": report.line_count,
                "optional_dirs": report.optional_dirs,
                "issues": [issue.__dict__ for issue in report.issues],
            }
            for report in reports
        ],
    }


def print_text(reports: list[SkillReport], root_issues: list[Issue]) -> None:
    all_issues = root_issues + [issue for report in reports for issue in report.issues]
    errors = [i for i in all_issues if i.level == "error"]
    warnings = [i for i in all_issues if i.level == "warning"]
    print(f"DBX skill validation: {len(reports)} skills, {len(errors)} errors, {len(warnings)} warnings")
    for report in reports:
        status = "ERROR" if report.errors else "WARN" if report.warnings else "OK"
        dirs = ",".join(report.optional_dirs) if report.optional_dirs else "none"
        print(f"[{status}] {report.name} | frontmatter={report.frontmatter_style} | lines={report.line_count} | dirs={dirs}")
        for item in report.issues:
            print(f"  - {item.level.upper()}: {item.path}: {item.message}")
    for item in root_issues:
        print(f"[ROOT] {item.level.upper()}: {item.path}: {item.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DBX skill repository structure.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Exit non-zero when warnings are present.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    reports, root_issues = scan(root)
    data = to_json(reports, root_issues)
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_text(reports, root_issues)

    errors = data["summary"]["errors"]
    warnings = data["summary"]["warnings"]
    if errors or (args.fail_on_warnings and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
