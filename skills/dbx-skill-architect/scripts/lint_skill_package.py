#!/usr/bin/env python3
"""Lint an Agent Skill package with DBX-specific checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from eval_schema import validate_eval_file  # noqa: E402

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
PLACEHOLDER_PATTERNS = [
    re.compile(r"(?m)^\s*-\s*\.\.\.\s*$"),
    re.compile(r"(?i)\bdescribe the recurring scenario\b"),
    re.compile(r"(?i)\bdescribe what the skill does\b"),
    re.compile(r"(?i)\ba realistic prompt\b"),
    re.compile(r"(?i)\btodo\b|\btbd\b"),
    re.compile(r"procedure\s*\|\s*tool\s*\|\s*knowledge"),
    re.compile(r"dominant_failure_modes:\s*\[\]\s*$", re.MULTILINE),
    re.compile(r"implementation_implications:\s*\[\]\s*$", re.MULTILINE),
]


def placeholder_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            hits.append(" ".join(match.group(0).split())[:80])
    return hits


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, "SKILL.md must start with YAML frontmatter using separate --- lines"
    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return fields, f"Invalid frontmatter line: {raw_line!r}"
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields, None


def lint_skill(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return [f"{path}: missing SKILL.md"], warnings
    text = skill_md.read_text(encoding="utf-8")
    fields, err = parse_frontmatter(text)
    if err:
        errors.append(err)
    name = fields.get("name")
    description = fields.get("description")
    if not name:
        errors.append("frontmatter.name is required")
    elif not NAME_RE.match(name):
        errors.append(f"frontmatter.name is invalid: {name!r}")
    elif name != path.name:
        errors.append(f"frontmatter.name {name!r} must match directory name {path.name!r}")
    if not description:
        errors.append("frontmatter.description is required")
    elif len(description) > 1024:
        errors.append("frontmatter.description exceeds 1024 characters")
    elif "use" not in description.lower() and "when" not in description.lower():
        warnings.append("description should say when to use the skill")
    if text.count("```yaml") == 0:
        warnings.append("SKILL.md should include a YAML contract or structured examples")
    if len(text.splitlines()) > 500:
        warnings.append("SKILL.md is over 500 lines; consider moving detail into references/")
    if path.name != "dbx-skill-architect":
        for hit in placeholder_hits(text):
            errors.append(f"SKILL.md contains placeholder text: {hit!r}")
    refs = path / "references"
    if refs.exists():
        for ref in refs.glob("*.md"):
            if not ref.read_text(encoding="utf-8").strip():
                warnings.append(f"empty reference file: {ref.relative_to(path)}")
    evals = path / "evals" / "evals.json"
    if evals.exists():
        result = validate_eval_file(evals, path.name)
        errors.extend(result.errors)
        warnings.extend(result.warnings)
    else:
        warnings.append("missing evals/evals.json")
    triggers = path / "evals" / "triggers.json"
    if not triggers.exists():
        warnings.append("missing evals/triggers.json")
    else:
        try:
            trigger_data = json.loads(triggers.read_text(encoding="utf-8"))
            if trigger_data.get("skill_name") != path.name:
                warnings.append("evals/triggers.json skill_name does not match directory")
            if not isinstance(trigger_data.get("cases"), list) or not trigger_data["cases"]:
                errors.append("evals/triggers.json cases must be a non-empty array")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"evals/triggers.json invalid JSON: {exc}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a DBX skill package.")
    parser.add_argument("path", help="Skill package directory")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on-warnings", action="store_true")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    errors, warnings = lint_skill(path)
    payload = {"ok": not errors and not (warnings and args.fail_on_warnings), "errors": errors, "warnings": warnings}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "OK" if payload["ok"] else "ERROR"
        print(f"Skill lint: {status} ({path})")
        for err in errors:
            print(f"ERROR: {err}")
        for warning in warnings:
            print(f"WARNING: {warning}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
