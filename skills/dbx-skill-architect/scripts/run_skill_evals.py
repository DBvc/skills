#!/usr/bin/env python3
"""Lightweight eval schema validator and captured-output scorer for skill evals.

Does not invoke an agent. It validates eval definitions and scores saved outputs
using deterministic checks.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from eval_schema import CATEGORIES, validate_eval_data


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"Could not read {path}: {exc}"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, [f"Invalid JSON in {path}: {exc}"]
    if not isinstance(data, dict):
        return None, ["Top-level evals JSON must be an object"]
    return data, []


def find_output(outputs_dir: Path, case_id: str) -> Path | None:
    for candidate in [
        outputs_dir / f"{case_id}.md",
        outputs_dir / f"{case_id}.txt",
        outputs_dir / case_id / "output.md",
        outputs_dir / case_id / "output.txt",
    ]:
        if candidate.exists():
            return candidate
    return None


def run_check(text: str, check: dict[str, Any]) -> tuple[bool, str]:
    ctype = str(check.get("type", ""))
    value = str(check.get("value", ""))
    flags = re.IGNORECASE | re.MULTILINE
    if ctype == "must_contain":
        return value.lower() in text.lower(), f"must_contain {value!r}"
    if ctype == "must_not_contain":
        return value.lower() not in text.lower(), f"must_not_contain {value!r}"
    if ctype == "regex":
        return re.search(value, text, flags) is not None, f"regex {value!r}"
    if ctype == "must_start_with":
        return text.lstrip().lower().startswith(value.lower()), f"must_start_with {value!r}"
    return False, f"unsupported {ctype!r}"


def score_case(case: dict[str, Any], output_text: str | None) -> dict[str, Any]:
    if output_text is None:
        return {"id": case.get("id"), "passed": False, "score": 0.0, "checks": [{"passed": False, "detail": "missing output"}]}
    checks_out: list[dict[str, Any]] = []
    total = passed = 0
    required_failed = False
    for category in CATEGORIES:
        for check in case.get("checks", {}).get(category, []):
            total += 1
            if not isinstance(check, dict):
                required_failed = True
                checks_out.append({"category": category, "passed": False, "detail": "malformed check", "required": True})
                continue
            ok, detail = run_check(output_text, check)
            if ok:
                passed += 1
            if check.get("required", False) and not ok:
                required_failed = True
            checks_out.append({"category": category, "passed": ok, "detail": detail, "required": bool(check.get("required", False))})
    score = passed / total if total else 1.0
    criteria = case.get("pass_criteria", {}) if isinstance(case.get("pass_criteria"), dict) else {}
    min_score = float(criteria.get("min_score", 0.85))
    all_required = bool(criteria.get("all_required", True))
    case_passed = score >= min_score and not (all_required and required_failed)
    return {"id": case.get("id"), "passed": case_passed, "score": round(score, 4), "checks": checks_out}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evals_json", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--outputs-dir", type=Path)
    args = parser.parse_args()

    data, load_errors = load_json(args.evals_json)
    if load_errors:
        print(json.dumps({"ok": False, "errors": load_errors, "warnings": [], "mode": "load"}, ensure_ascii=False, indent=2))
        return 1
    assert data is not None
    errors, warnings = validate_eval_data(data)
    if args.validate_only or not args.outputs_dir:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings, "mode": "validate-only"}, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    case_results = []
    for case in data.get("evals", []):
        if not isinstance(case, dict):
            continue
        output_path = find_output(args.outputs_dir, str(case.get("id", "")))
        output_text = output_path.read_text(encoding="utf-8") if output_path else None
        case_results.append(score_case(case, output_text))
    overall = sum(1 for c in case_results if c["passed"]) / len(case_results) if case_results else 0.0
    ok = not errors and overall >= float(data.get("pass_threshold", 0.85))
    print(json.dumps({"ok": ok, "schema_errors": errors, "warnings": warnings, "overall_pass_rate": round(overall, 4), "cases": case_results}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
