#!/usr/bin/env python3
"""Validate and score saved dbx-skill-architect outputs.

This runner does not call an LLM. It validates eval schema and can apply simple
checks to captured output text.

Scoring modes:
- --outputs-dir <dir>: score outputs named <eval-id>.md, <eval-id>.txt, or
  <eval-id>.out. By default every eval case must have a matching output.
- --outputs-dir <dir> --case-id <id>: score only that case's output from the
  directory.
- --captured-output <file> --case-id <id>: score one captured output against one
  explicit case. The runner refuses to apply one captured output to every case,
  because contradictory eval cases make that evidence meaningless.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from eval_schema import CHECK_BUCKETS, load_json, validate_eval_file  # noqa: E402

OUTPUT_SUFFIXES = (".md", ".txt", ".out")


def find_output(outputs_dir: Path, case_id: str) -> Path | None:
    for suffix in OUTPUT_SUFFIXES:
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
        ok = re.search(value, text, flags=re.DOTALL | re.MULTILINE) is not None
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
            details.append(
                {
                    "bucket": bucket,
                    "index": idx,
                    "type": check.get("type"),
                    "value": check.get("value"),
                    "quality": check.get("quality", "structural"),
                    "required": required,
                    "passed": ok,
                    "evidence": evidence,
                }
            )

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


def case_by_id(data: dict[str, Any], case_id: str) -> dict[str, Any] | None:
    for case in data.get("evals", []):
        if str(case.get("id")) == case_id:
            return case
    return None


def score_single_case(data: dict[str, Any], case_id: str, output_path: Path) -> dict[str, Any]:
    case = case_by_id(data, case_id)
    if case is None:
        return {
            "ok": False,
            "errors": [f"unknown case id: {case_id}"],
            "results": [],
        }
    text = output_path.read_text(encoding="utf-8")
    scored = score_case(case, text)
    scored["output_path"] = str(output_path)
    return {
        "ok": bool(scored.get("passed")),
        "pass_rate": 1.0 if scored.get("passed") else 0.0,
        "threshold": float(data.get("pass_threshold", 0.85)),
        "missing": [],
        "results": [scored],
    }


def score_outputs_dir(data: dict[str, Any], outputs_dir: Path, only_case_id: str | None) -> dict[str, Any]:
    cases = data.get("evals", [])
    if only_case_id:
        output_path = find_output(outputs_dir, only_case_id)
        if output_path is None:
            return {
                "ok": False,
                "pass_rate": 0.0,
                "threshold": float(data.get("pass_threshold", 0.85)),
                "missing": [only_case_id],
                "results": [{"id": only_case_id, "passed": False, "score": 0.0, "missing_output": True}],
            }
        return score_single_case(data, only_case_id, output_path)

    case_results: list[dict[str, Any]] = []
    missing: list[str] = []
    for case in cases:
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
    return {
        "ok": pass_rate >= threshold and not missing,
        "pass_rate": pass_rate,
        "threshold": threshold,
        "missing": missing,
        "results": case_results,
    }


def print_text(payload: dict[str, Any], schema_payload: dict[str, Any]) -> None:
    if "schema_ok" in schema_payload:
        status = "OK" if schema_payload["schema_ok"] else "ERROR"
        print(f"Eval validation: {status}")
        for err in schema_payload.get("errors", []):
            print(f"ERROR: {err}")
        for warning in schema_payload.get("warnings", []):
            print(f"WARNING: {warning}")

    if "results" in payload:
        status = "PASS" if payload.get("ok") else "FAIL"
        print(
            f"Eval scoring: {status} pass_rate={payload.get('pass_rate', 0):.2f} "
            f"threshold={payload.get('threshold', 0):.2f}"
        )
        for item in payload.get("results", []):
            marker = "PASS" if item.get("passed") else "FAIL"
            print(f"[{marker}] {item.get('id')} score={item.get('score', 0):.2f}")
            for detail in item.get("details", []):
                if detail.get("required") and not detail.get("passed"):
                    print(f"  - {detail.get('bucket')}[{detail.get('index')}]: {detail.get('evidence')}")
        for case_id in payload.get("missing", []):
            print(f"MISSING OUTPUT: {case_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate dbx eval schema and optionally score captured outputs.")
    parser.add_argument("evals_json", help="Path to evals/evals.json")
    parser.add_argument("--validate-only", action="store_true", help="Only validate the schema.")
    parser.add_argument("--outputs-dir", help="Directory containing outputs named <eval-id>.md/.txt/.out.")
    parser.add_argument("--captured-output", help="Single output file to score. Requires --case-id.")
    parser.add_argument("--case-id", help="Score only this eval case.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    eval_path = Path(args.evals_json)
    data, err = load_json(eval_path)
    if err or not isinstance(data, dict):
        payload = {"ok": False, "errors": [err or "root is not object"]}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    result = validate_eval_file(eval_path, data.get("skill_name"))
    schema_payload = {"schema_ok": result.ok, "errors": result.errors, "warnings": result.warnings}

    if args.validate_only:
        payload = {"ok": result.ok, "errors": result.errors, "warnings": result.warnings}
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print_text({}, schema_payload)
        return 0 if result.ok else 1

    if not result.ok:
        payload = {"ok": False, "errors": result.errors, "warnings": result.warnings}
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print_text({}, schema_payload)
        return 1

    if args.captured_output and not args.case_id:
        payload = {
            "ok": False,
            "errors": ["--captured-output requires --case-id; one output must not be scored against all eval cases"],
            "warnings": result.warnings,
        }
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print_text({}, schema_payload)
            print("ERROR: --captured-output requires --case-id")
        return 1

    if args.captured_output and args.outputs_dir:
        payload = {"ok": False, "errors": ["Use either --captured-output or --outputs-dir, not both."], "warnings": result.warnings}
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print_text({}, schema_payload)
            print("ERROR: Use either --captured-output or --outputs-dir, not both.")
        return 1

    if args.captured_output:
        score_payload = score_single_case(data, args.case_id, Path(args.captured_output))
    elif args.outputs_dir:
        score_payload = score_outputs_dir(data, Path(args.outputs_dir), args.case_id)
    else:
        score_payload = {"ok": result.ok, "errors": result.errors, "warnings": result.warnings}

    score_payload["warnings"] = result.warnings
    if args.format == "json":
        payload = {**schema_payload, **score_payload}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_text(score_payload if "results" in score_payload else {}, schema_payload)

    return 0 if score_payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
