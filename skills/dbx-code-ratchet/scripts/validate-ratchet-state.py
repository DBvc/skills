#!/usr/bin/env python3
"""Validate a dbx-code-ratchet state JSON file."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_FINAL_STATES = {
    "in_progress",
    "pass-ready",
    "needs-human-decision",
    "stopped-direction-failure",
    "stopped-diverging",
    "stopped-validation-failed",
    "stopped-scope-unsafe",
}
ALLOWED_TARGET_SOURCES = {
    "pasted_patch",
    "pr",
    "branch",
    "staged",
    "unstaged",
    "local",
    "commit",
    "commit_range",
    "selected_files",
}
ALLOWED_SEVERITIES = {"S0", "S1", "S2", "S3"}
ALLOWED_TRIAGE = {
    "auto_fix",
    "defer_not_worth",
    "reject_false_positive",
    "escalate_human_decision",
    "direction_failure",
    "rollback_recommended",
}


def load(path: Path) -> Any:
    if str(path) == "-":
        return json.loads(sys.stdin.read())
    return json.loads(path.read_text(encoding="utf-8"))


def add(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def require_obj(errors: list[str], data: Any, path: str) -> dict[str, Any]:
    if not isinstance(data, dict):
        add(errors, path, "must be an object")
        return {}
    return data


def validate_state(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    root = require_obj(errors, data, "$" )
    if not root:
        return errors, warnings

    if root.get("ratchet_state_version") != 1:
        add(errors, "$.ratchet_state_version", "must be 1")

    target = require_obj(errors, root.get("target"), "$.target")
    source = target.get("source")
    if source not in ALLOWED_TARGET_SOURCES:
        add(errors, "$.target.source", f"must be one of {sorted(ALLOWED_TARGET_SOURCES)}")

    for key in ["included_files", "selected_files", "out_of_scope_dirty_files", "partial_out_of_scope_files"]:
        if key in target and not isinstance(target[key], list):
            add(errors, f"$.target.{key}", "must be a list")

    iteration = root.get("iteration")
    max_rounds = root.get("max_repair_rounds")
    if not isinstance(iteration, int) or iteration < 0:
        add(errors, "$.iteration", "must be a non-negative integer")
    if not isinstance(max_rounds, int) or max_rounds < 0:
        add(errors, "$.max_repair_rounds", "must be a non-negative integer")
    if isinstance(iteration, int) and isinstance(max_rounds, int) and iteration > max_rounds:
        warnings.append("$.iteration exceeds $.max_repair_rounds")

    final_state = root.get("final_state")
    if final_state not in ALLOWED_FINAL_STATES:
        add(errors, "$.final_state", f"must be one of {sorted(ALLOWED_FINAL_STATES)}")

    findings = root.get("findings", [])
    if not isinstance(findings, list):
        add(errors, "$.findings", "must be a list")
    else:
        seen: set[str] = set()
        for idx, item in enumerate(findings):
            if not isinstance(item, dict):
                add(errors, f"$.findings[{idx}]", "must be an object")
                continue
            finding_id = item.get("id")
            if not finding_id:
                add(errors, f"$.findings[{idx}].id", "is required")
            elif finding_id in seen:
                add(errors, f"$.findings[{idx}].id", f"duplicate id {finding_id!r}")
            else:
                seen.add(str(finding_id))
            severity = item.get("severity")
            if severity not in ALLOWED_SEVERITIES:
                add(errors, f"$.findings[{idx}].severity", f"must be one of {sorted(ALLOWED_SEVERITIES)}")

    triage = root.get("triage", [])
    if not isinstance(triage, list):
        add(errors, "$.triage", "must be a list")
    else:
        for idx, item in enumerate(triage):
            if not isinstance(item, dict):
                add(errors, f"$.triage[{idx}]", "must be an object")
                continue
            status = item.get("status")
            if status not in ALLOWED_TRIAGE:
                add(errors, f"$.triage[{idx}].status", f"must be one of {sorted(ALLOWED_TRIAGE)}")

    if final_state == "pass-ready" and errors:
        warnings.append("state claims pass-ready but structural errors exist")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a dbx-code-ratchet state JSON file.")
    parser.add_argument("state", help="State JSON path. Use '-' for stdin.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    args = parser.parse_args()

    try:
        data = load(Path(args.state))
    except Exception as exc:  # noqa: BLE001
        if args.format == "json":
            print(json.dumps({"errors": [str(exc)], "warnings": []}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: failed to read state: {exc}")
        return 1

    errors, warnings = validate_state(data)
    if args.format == "json":
        print(json.dumps({"errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        print(f"Ratchet state validation: {len(errors)} errors, {len(warnings)} warnings")
        for err in errors:
            print(f" - ERROR: {err}")
        for warning in warnings:
            print(f" - WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
