#!/usr/bin/env python3
"""Validate feedback digest/case structural gates.

This is intentionally lightweight and dependency-free. It enforces the most
important v0.1 safety gates: evidence, conservative resolution, confirmed-bug
proof, and no raw chat dumps.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CATEGORIES = {
    "usage_question", "misuse_or_config", "suspected_bug", "confirmed_bug",
    "feature_request", "product_gap", "known_issue", "incident",
    "data_or_permission_issue", "documentation_gap", "duplicate",
    "noise_or_non_feedback", "unknown",
}
STATUSES = {
    "resolved", "probably_resolved", "pending_user", "pending_dev", "pending_pm",
    "escalated", "not_actionable", "unresolved", "unknown",
}
SEVERITIES = {"p0", "p1", "p2", "p3", "unknown"}
CONFIDENCE = {"high", "medium", "low"}


def read_json(path: str | None) -> Any:
    raw = sys.stdin.read() if not path or path == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def get_cases(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict) and isinstance(obj.get("cases"), list):
        return [x for x in obj["cases"] if isinstance(x, dict)]
    if isinstance(obj, dict):
        return [obj]
    return []


def has_evidence(case: dict[str, Any]) -> bool:
    source = case.get("source")
    if not isinstance(source, dict):
        return False
    mids = source.get("message_ids") or []
    refs = source.get("evidence_refs") or []
    return bool(mids or refs)


def validate_case(case: dict[str, Any], idx: int) -> list[str]:
    prefix = str(case.get("case_id") or f"case[{idx}]")
    errors: list[str] = []
    required = ["case_id", "title", "category", "status", "severity", "confidence", "source", "extracted_facts", "classification_reason", "state_reason"]
    for key in required:
        if key not in case or case.get(key) in (None, "", []):
            errors.append(f"{prefix}: missing {key}")

    if case.get("category") not in CATEGORIES:
        errors.append(f"{prefix}: invalid category {case.get('category')!r}")
    if case.get("status") not in STATUSES:
        errors.append(f"{prefix}: invalid status {case.get('status')!r}")
    if case.get("severity") not in SEVERITIES:
        errors.append(f"{prefix}: invalid severity {case.get('severity')!r}")
    if case.get("confidence") not in CONFIDENCE:
        errors.append(f"{prefix}: invalid confidence {case.get('confidence')!r}")

    if case.get("category") not in {"noise_or_non_feedback", "unknown"} and not has_evidence(case):
        errors.append(f"{prefix}: important case has no message evidence")

    if case.get("status") == "resolved" and not case.get("resolution_evidence"):
        errors.append(f"{prefix}: resolved requires resolution_evidence")

    if case.get("category") == "confirmed_bug" and not case.get("confirmation_evidence"):
        errors.append(f"{prefix}: confirmed_bug requires confirmation_evidence")

    if case.get("category") in {"suspected_bug", "confirmed_bug"}:
        facts = case.get("extracted_facts") or {}
        symptom = facts.get("symptom") if isinstance(facts, dict) else ""
        if not symptom:
            errors.append(f"{prefix}: bug-like case requires extracted_facts.symptom")

    if case.get("category") in {"feature_request", "product_gap"}:
        facts = case.get("extracted_facts") or {}
        if isinstance(facts, dict) and not (facts.get("requested_change") or facts.get("expected")):
            errors.append(f"{prefix}: request/gap case should include requested_change or expected")

    if "raw_messages" in case:
        errors.append(f"{prefix}: raw_messages field is not allowed in final digest")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate feedback case/digest JSON.")
    parser.add_argument("input", nargs="?", default="-", help="Feedback digest/cases JSON path, or stdin")
    parser.add_argument("--strict", action="store_true", help="Require at least one case")
    args = parser.parse_args()

    obj = read_json(args.input)
    cases = get_cases(obj)
    errors: list[str] = []
    warnings: list[str] = []

    if args.strict and not cases:
        errors.append("no cases found")

    if isinstance(obj, dict):
        if obj.get("write_status") not in (None, "not_written", "preview_only", "approved_written", "partial", "failed"):
            errors.append(f"invalid write_status {obj.get('write_status')!r}")
        if obj.get("write_status") in {"approved_written", "partial"} and not obj.get("write_evidence"):
            warnings.append("written digest should include write_evidence")

    for i, case in enumerate(cases):
        errors.extend(validate_case(case, i))

    result = {"ok": not errors, "case_count": len(cases), "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
