#!/usr/bin/env python3
"""Lint a DBX skill package with hermetic, standard-library-only checks.

The linter intentionally avoids py_compile because py_compile may try to write
__pycache__ into user or system cache locations in sandboxed environments. It
uses ast.parse instead, which checks syntax without writing files.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
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
            hits.append(" ".join(match.group(0).split())[:100])
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


def load_json_file(path: Path) -> tuple[object | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def lint_python_syntax(script: Path) -> str | None:
    try:
        ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    except SyntaxError as exc:
        return f"{script}: Python syntax error at line {exc.lineno}: {exc.msg}"
    except Exception as exc:  # noqa: BLE001
        return f"{script}: could not parse Python file: {exc}"
    return None


def validate_triggers(path: Path, skill_name: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data, err = load_json_file(path)
    if err or not isinstance(data, dict):
        return [f"{path}: invalid JSON: {err or 'root is not object'}"], warnings

    if skill_name and data.get("skill_name") != skill_name:
        warnings.append(f"{path}: skill_name does not match directory")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{path}: cases must be a non-empty array")
        return errors, warnings

    kinds: dict[str, int] = {}
    for index, case in enumerate(cases):
        prefix = f"{path}#cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: case must be an object")
            continue
        case_id = case.get("id")
        prompt = case.get("prompt")
        expected = case.get("expected")
        expected_trigger = case.get("expected_trigger")
        kind = case.get("kind")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{prefix}: prompt must be a non-empty string")

        if expected in {"trigger", "do_not_trigger", "maybe", "needs_context"}:
            normalized_expected = str(expected)
        elif isinstance(expected_trigger, bool):
            normalized_expected = "trigger" if expected_trigger else "do_not_trigger"
        elif kind in {"positive", "negative", "near_miss", "failure_mode", "safety"}:
            normalized_expected = "trigger" if kind in {"positive", "failure_mode", "safety"} else "do_not_trigger"
            warnings.append(f"{prefix}: expected_trigger missing; inferred from kind={kind!r}")
        else:
            errors.append(
                f"{prefix}: expected must be trigger/do_not_trigger/maybe/needs_context "
                "or expected_trigger must be boolean"
            )
            normalized_expected = "unknown"

        if normalized_expected != "unknown":
            kinds[normalized_expected] = kinds.get(normalized_expected, 0) + 1

        for field in ("rationale", "expected_route"):
            if field in case and not isinstance(case[field], str):
                warnings.append(f"{prefix}: {field} should be a string")

    if kinds.get("trigger", 0) == 0:
        warnings.append(f"{path}: no trigger cases")
    if kinds.get("do_not_trigger", 0) == 0:
        warnings.append(f"{path}: no do_not_trigger cases")
    return errors, warnings


def lint_skill(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    path = path.resolve()

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
    elif len(description) < 40:
        errors.append("frontmatter.description must be specific and at least 40 characters")
    elif len(description) > 1024:
        errors.append("frontmatter.description exceeds 1024 characters")
    elif "use" not in description.lower() and "when" not in description.lower():
        warnings.append("description should say when to use the skill")

    if text.splitlines()[0].strip() != "---":
        errors.append("frontmatter must use a standalone opening --- line")
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
    if triggers.exists():
        trigger_errors, trigger_warnings = validate_triggers(triggers, path.name)
        errors.extend(trigger_errors)
        warnings.extend(trigger_warnings)
    else:
        warnings.append("missing evals/triggers.json")

    scripts_dir = path / "scripts"
    if scripts_dir.exists():
        for script in sorted(scripts_dir.glob("*.py")):
            syntax_error = lint_python_syntax(script)
            if syntax_error:
                errors.append(syntax_error)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a DBX skill package.")
    parser.add_argument("path", help="Skill package directory")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on-warnings", action="store_true")
    args = parser.parse_args()

    errors, warnings = lint_skill(Path(args.path))
    payload = {"ok": not errors and not (warnings and args.fail_on_warnings), "errors": errors, "warnings": warnings}

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "OK" if payload["ok"] else "ERROR"
        print(f"Skill lint: {status} ({Path(args.path).resolve()})")
        for err in errors:
            print(f"ERROR: {err}")
        for warning in warnings:
            print(f"WARNING: {warning}")

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
