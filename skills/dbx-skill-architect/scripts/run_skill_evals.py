#!/usr/bin/env python3
"""Validate and score captured outputs for dbx-skill-architect evals.

This script does not call an LLM. It validates eval schema and, if --outputs-dir
is provided, scores saved outputs named <eval-id>.md or <eval-id>.txt.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from eval_schema import CHECK_BUCKETS, load_json, validate_eval_file  # noqa: E402


def find_output(outputs_dir: Path, case_id: str) -> Path | None:
    for suffix in (".md", ".txt", ".out"):
        candidate = outputs_dir / f"{case_id}{suffix}"
        if candidate.exists():
            return candidate
    return None


def run_check(text: str, check: dict[str, Any]) -> tuple[bool, str]:
    check_type = check.get("type")
    value = str(check.get("value", ""))
    if check_type == "must_contain":
        ok = value in text
        return ok, f"contains {value!r}: {ok}"
    if check_type == "must_not_contain":
        ok = value not in text
        return ok, f"does not contain {value!r}: {ok}"
    if check_type == "must_start_with":
        ok = text.lstrip().startswith(value)
        return ok, f"starts with {value!r}: {ok}"
    if check_type == "regex":
        ok = re.search(value, text, flags=re.MULTILINE) is not None
        return ok, f"regex {value!r}: {ok}"
    return False, f"unsupported check type {check_type!r}"


def score_case(case: dict[str, Any], text: str) -> dict[str, Any]:
    required_results: list[bool] = []
    all_results: list[bool] = []
    details: list[dict[str, Any]] = []
    for bucket in CHECK_BUCKETS:
        for idx, check in enumerate(case.get("checks", {}).get(bucket, [])):
            ok, evidence = run_check(text, check)
            required = bool(check.get("required"))
            if required:
                required_results.append(ok)
            all_results.append(ok)
            details.append({
                "bucket": bucket,
                "index": idx,
                "type": check.get("type"),
                "value": check.get("value"),
                "required": required,
                "passed": ok,
                "evidence": evidence,
            })
    score = sum(1 for item in all_results if item) / len(all_results) if all_results else 1.0
    criteria = case.get("pass_criteria", {})
    all_required = bool(criteria.get("all_required", True))
    min_score = float(criteria.get("min_score", 0.85))
    passed_required = all(required_results) if required_results else True
    passed = (passed_required or not all_required) and score >= min_score
    return {
        "id": case.get("id"),
        "kind": case.get("kind"),
        "score": score,
        "passed_required": passed_required,
        "passed": passed,
        "details": details,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate dbx eval schema and optionally score captured outputs.")
    parser.add_argument("evals_json", help="Path to evals/evals.json")
    parser.add_argument("--validate-only", action="store_true", help="Only validate the schema.")
    parser.add_argument("--outputs-dir", help="Directory containing <eval-id>.md or <eval-id>.txt outputs to score.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    eval_path = Path(args.evals_json)
    data, err = load_json(eval_path)
    if err or not isinstance(data, dict):
        print(json.dumps({"ok": False, "errors": [err or "root is not object"]}, ensure_ascii=False, indent=2))
        return 1
    result = validate_eval_file(eval_path, data.get("skill_name"))
    if args.validate_only or not args.outputs_dir:
        payload = {"ok": result.ok, "errors": result.errors, "warnings": result.warnings}
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            status = "OK" if result.ok else "ERROR"
            print(f"Eval validation: {status}")
            for err in result.errors:
                print(f"ERROR: {err}")
            for warning in result.warnings:
                print(f"WARNING: {warning}")
        return 0 if result.ok else 1

    if not result.ok:
        print(json.dumps({"ok": False, "errors": result.errors, "warnings": result.warnings}, ensure_ascii=False, indent=2))
        return 1

    outputs_dir = Path(args.outputs_dir)
    case_results: list[dict[str, Any]] = []
    missing: list[str] = []
    for case in data.get("evals", []):
        case_id = str(case.get("id"))
        output_path = find_output(outputs_dir, case_id)
        if not output_path:
            missing.append(case_id)
            case_results.append({"id": case_id, "passed": False, "score": 0.0, "missing_output": True})
            continue
        text = output_path.read_text(encoding="utf-8")
        scored = score_case(case, text)
        scored["output_path"] = str(output_path)
        case_results.append(scored)
    pass_rate = sum(1 for item in case_results if item.get("passed")) / len(case_results) if case_results else 0.0
    threshold = float(data.get("pass_threshold", 0.85))
    payload = {
        "ok": pass_rate >= threshold and not missing,
        "pass_rate": pass_rate,
        "threshold": threshold,
        "missing": missing,
        "results": case_results,
        "warnings": result.warnings,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if payload["ok"] else "FAIL"
        print(f"Eval scoring: {status} pass_rate={pass_rate:.2f} threshold={threshold:.2f}")
        for item in case_results:
            marker = "PASS" if item.get("passed") else "FAIL"
            print(f"[{marker}] {item.get('id')} score={item.get('score', 0):.2f}")
        for case_id in missing:
            print(f"MISSING OUTPUT: {case_id}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
