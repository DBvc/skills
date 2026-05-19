#!/usr/bin/env python3
"""Validate dbx-attention-control JSON output.

Safe by default:
- no network access;
- no file writes;
- validates shape and important semantic constraints;
- exits non-zero on errors.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALID_MODES = {
    "profile_bootstrap",
    "item_routing",
    "adapter_dry_run",
    "review_and_calibrate",
}

VALID_ROUTES = {
    "act_now",
    "build",
    "test",
    "track",
    "store",
    "incubate",
    "drop",
    "guard",
    "clarify",
}

VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_WRITE_STATUS = {"none", "dry_run_only", "approved_write_requested", "completed_with_tool_evidence"}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"error: file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"error: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate_item(item: dict[str, Any], index: int, errors: list[str]) -> None:
    prefix = f"items[{index}]"
    for field in [
        "id_or_locator",
        "title",
        "route",
        "confidence",
        "evidence_used",
        "reason",
        "next_step_or_no_action",
        "risk_notes",
    ]:
        require(field in item, errors, f"{prefix}: missing required field '{field}'")

    if "route" in item:
        require(item["route"] in VALID_ROUTES, errors, f"{prefix}: invalid route '{item['route']}'")
    if "confidence" in item:
        require(item["confidence"] in VALID_CONFIDENCE, errors, f"{prefix}: invalid confidence '{item['confidence']}'")
    if "evidence_used" in item:
        require(isinstance(item["evidence_used"], list), errors, f"{prefix}: evidence_used must be a list")
        require(len(item["evidence_used"]) > 0, errors, f"{prefix}: evidence_used must not be empty")
    if "risk_notes" in item:
        require(isinstance(item["risk_notes"], list), errors, f"{prefix}: risk_notes must be a list")

    route = item.get("route")
    next_step = str(item.get("next_step_or_no_action", "")).strip()
    require(bool(next_step), errors, f"{prefix}: next_step_or_no_action must not be empty")

    if route == "incubate":
        triggerish = any(word in next_step.lower() for word in ["trigger", "until", "date", "milestone", "review", "再", "直到", "触发", "复查", "日期"])
        require(triggerish, errors, f"{prefix}: incubate route should include a trigger/date/review condition")

    if route == "test":
        testish = any(word in next_step.lower() for word in ["experiment", "test", "signal", "stop", "review", "实验", "验证", "停止", "复盘"])
        require(testish, errors, f"{prefix}: test route should include experiment/signal/stop/review language")

    if route == "guard":
        require(len(item.get("risk_notes", [])) > 0, errors, f"{prefix}: guard route must include risk_notes")


def validate_mutation(row: dict[str, Any], index: int, errors: list[str]) -> None:
    prefix = f"adapter_mutation_plan[{index}]"
    for field in [
        "target_system",
        "item_id_or_locator",
        "operation",
        "field",
        "new_value",
        "reason",
        "rollback_note",
        "confidence",
    ]:
        require(field in row, errors, f"{prefix}: missing required field '{field}'")
    if "confidence" in row:
        require(row["confidence"] in VALID_CONFIDENCE, errors, f"{prefix}: invalid confidence '{row['confidence']}'")
    require(str(row.get("item_id_or_locator", "")).strip() != "", errors, f"{prefix}: stable locator is required")
    require(str(row.get("rollback_note", "")).strip() != "", errors, f"{prefix}: rollback_note must not be empty")


def validate(doc: dict[str, Any], *, require_dry_run: bool) -> list[str]:
    errors: list[str] = []

    for field in ["kernel_version", "mode", "scope", "items", "completion_proof"]:
        require(field in doc, errors, f"missing required top-level field '{field}'")

    if "mode" in doc:
        if doc["mode"] in {"direct_answer", "safety_stop"}:
            errors.append("direct_answer and safety_stop are natural-language escape modes; do not validate them with this JSON contract")
        else:
            require(doc["mode"] in VALID_MODES, errors, f"invalid mode '{doc['mode']}'")

    scope = doc.get("scope", {})
    require(isinstance(scope, dict), errors, "scope must be an object")
    if isinstance(scope, dict):
        for field in ["item_count", "evidence_available", "profile_used", "external_write_status"]:
            require(field in scope, errors, f"scope: missing required field '{field}'")
        if "external_write_status" in scope:
            require(scope["external_write_status"] in VALID_WRITE_STATUS, errors, f"scope: invalid external_write_status '{scope['external_write_status']}'")

    items = doc.get("items", [])
    require(isinstance(items, list), errors, "items must be a list")
    if isinstance(items, list):
        if isinstance(scope, dict) and isinstance(scope.get("item_count"), int):
            require(scope["item_count"] == len(items), errors, "scope.item_count must equal len(items)")
        for index, item in enumerate(items):
            require(isinstance(item, dict), errors, f"items[{index}] must be an object")
            if isinstance(item, dict):
                validate_item(item, index, errors)

    mutation_plan = doc.get("adapter_mutation_plan", [])
    if mutation_plan is not None:
        require(isinstance(mutation_plan, list), errors, "adapter_mutation_plan must be a list when present")
        if isinstance(mutation_plan, list):
            for index, row in enumerate(mutation_plan):
                require(isinstance(row, dict), errors, f"adapter_mutation_plan[{index}] must be an object")
                if isinstance(row, dict):
                    validate_mutation(row, index, errors)

    if doc.get("mode") == "adapter_dry_run" or (require_dry_run and mutation_plan):
        status = scope.get("external_write_status") if isinstance(scope, dict) else None
        require(status == "dry_run_only", errors, "external write status must be dry_run_only for adapter_dry_run output or dry-run mutation validation")
        proof = doc.get("completion_proof", {})
        if isinstance(proof, dict):
            require(proof.get("external_write_happened") is False, errors, "completion_proof.external_write_happened must be false for dry-run output")

    proof = doc.get("completion_proof", {})
    require(isinstance(proof, dict), errors, "completion_proof must be an object")
    if isinstance(proof, dict):
        for field in ["processed_items", "profile_used", "external_write_happened", "uncertainties", "validation"]:
            require(field in proof, errors, f"completion_proof: missing required field '{field}'")
        if "processed_items" in proof and isinstance(items, list):
            require(proof["processed_items"] == len(items), errors, "completion_proof.processed_items must equal len(items)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate dbx-attention-control JSON output.")
    parser.add_argument("path", type=Path, help="Path to JSON output file")
    parser.add_argument("--require-dry-run", action="store_true", help="Require mutation plans to be dry-run only")
    args = parser.parse_args()

    doc = load_json(args.path)
    if not isinstance(doc, dict):
        print("error: top-level JSON must be an object", file=sys.stderr)
        return 2

    errors = validate(doc, require_dry_run=args.require_dry_run)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("ok: attention output is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
