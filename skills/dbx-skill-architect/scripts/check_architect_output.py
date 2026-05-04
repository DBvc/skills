#!/usr/bin/env python3
"""Validate captured output from dbx-skill-architect.

This checks the architect's own protocol, not just generated skill packages.
It catches mode/route/operation mismatch, full-skill overbuild, missing domain
substance gates, self-check drift, and runner-eval JSON that only claims to be
compatible.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from eval_schema import INVALID_KIND_ALIASES, VALID_KINDS, validate_eval_data

MODES = {"create", "critique", "improve", "eval", "triage"}
ROUTES = {
    "full_skill", "mini_skill", "needs_clarification", "domain_discovery",
    "checklist", "direct_answer", "refuse_or_redesign", "not_a_creation_request",
}
OPERATIONS = {
    "ask_questions", "ask_domain_questions", "build_domain_content_contract", "draft_package",
    "critique_package", "propose_patch_plan", "patch_existing_package",
    "design_runner_evals", "design_human_rubric", "run_lint", "run_evals", "provide_alternative",
}
GATE_VALUES = {"pass", "fail", "unknown", "not_applicable"}
BOOLISH = {"true", "false", "not_applicable"}
HARD_GATES = ("repeatability", "stable_job", "evaluability", "safety_legitimacy")
DOMAIN_GATES = (
    "target_user_defined", "output_depth_defined", "domain_variables_identified",
    "data_source_policy_defined", "failure_knowledge_identified",
    "expert_quality_rubric_defined", "worked_example_available",
)
SELF_CHECKS = (
    "mode_route_compatible", "operation_compatible", "hard_gates_applied",
    "domain_substance_gates_applied", "full_package_overbuilt", "eval_artifact_present",
    "eval_schema_runner_compatible", "patch_not_rebuild",
)

COMPAT = {
    "create": {
        "routes": {"full_skill", "mini_skill", "needs_clarification", "domain_discovery"},
        "operations": {"ask_questions", "ask_domain_questions", "build_domain_content_contract", "draft_package"},
    },
    "critique": {"routes": {"not_a_creation_request"}, "operations": {"critique_package", "propose_patch_plan"}},
    "improve": {"routes": {"not_a_creation_request"}, "operations": {"patch_existing_package", "propose_patch_plan", "ask_questions", "run_lint", "run_evals"}},
    "eval": {"routes": {"not_a_creation_request"}, "operations": {"design_runner_evals", "design_human_rubric", "run_evals"}},
    "triage": {"routes": {"mini_skill", "checklist", "direct_answer", "refuse_or_redesign"}, "operations": {"ask_questions", "provide_alternative"}},
}


def extract_yaml_block(text: str) -> str | None:
    match = re.search(r"^\s*```yaml\s*\n(.*?)\n\s*```", text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    return match.group(1) if match else None


def scalar(block: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*([^\n#]+)", block, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def boolish(block: str, key: str) -> str | None:
    value = scalar(block, key)
    return value.lower() if isinstance(value, str) else None


def gate(block: str, key: str) -> str | None:
    return scalar(block, key)


def extract_json_blocks(text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for match in re.finditer(r"```json\s*\n(.*?)\n\s*```", text, re.IGNORECASE | re.DOTALL):
        raw = match.group(1)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            out.append({"raw": raw, "parsed": None, "errors": [f"Invalid JSON block: {exc}"]})
            continue
        out.append({"raw": raw, "parsed": parsed, "errors": []})
    return out


def looks_like_eval_artifact(obj: Any) -> bool:
    return isinstance(obj, dict) and any(key in obj for key in ("evals", "cases", "skill_name", "pass_threshold"))


def validate_eval_artifacts(text: str) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    found = False
    for block in extract_json_blocks(text):
        parsed = block.get("parsed")
        if block["errors"]:
            raw = str(block.get("raw", ""))
            if "evals" in raw or "cases" in raw or "skill_name" in raw:
                found = True
                errors.extend(block["errors"])
            continue
        if not looks_like_eval_artifact(parsed):
            continue
        found = True
        if not isinstance(parsed, dict):
            errors.append("Eval artifact JSON must be an object")
            continue
        e, w = validate_eval_data(parsed)
        errors.extend(e)
        warnings.extend(w)
    return found, errors, warnings


def scan_invalid_kind_aliases(text: str) -> list[str]:
    errors: list[str] = []
    for alias in sorted(INVALID_KIND_ALIASES):
        if re.search(rf'"kind"\s*:\s*"{re.escape(alias)}"', text, re.IGNORECASE):
            errors.append(f"Invalid eval kind alias found in JSON: {alias!r}; use one of {sorted(VALID_KINDS)}")
    return errors


def validate_output(text: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not text.lstrip().startswith("```yaml"):
        errors.append("Output must start with a fenced YAML block")
    block = extract_yaml_block(text)
    if block is None:
        return {"ok": False, "errors": errors + ["No fenced yaml block found"], "warnings": warnings}
    if "skill_architect_decision:" not in block:
        errors.append("YAML block missing skill_architect_decision")

    mode = scalar(block, "mode")
    route = scalar(block, "route")
    operation = scalar(block, "operation")
    if mode not in MODES:
        errors.append(f"Invalid or missing mode: {mode!r}")
    if route not in ROUTES:
        errors.append(f"Invalid or missing route: {route!r}")
    if operation not in OPERATIONS:
        errors.append(f"Invalid or missing operation: {operation!r}")
    if mode in COMPAT and route in ROUTES and route not in COMPAT[mode]["routes"]:
        errors.append(f"route {route!r} is not allowed for mode {mode!r}")
    if mode in COMPAT and operation in OPERATIONS and operation not in COMPAT[mode]["operations"]:
        errors.append(f"operation {operation!r} is not allowed for mode {mode!r}")

    for key in HARD_GATES:
        value = gate(block, key)
        if value not in GATE_VALUES:
            errors.append(f"hard_gates.{key} invalid or missing: {value!r}")
    for key in DOMAIN_GATES:
        value = gate(block, key)
        if value not in GATE_VALUES:
            errors.append(f"domain_substance_gates.{key} invalid or missing: {value!r}")

    if route == "full_skill":
        for key in HARD_GATES:
            if gate(block, key) != "pass":
                errors.append(f"full_skill requires hard_gates.{key}: pass")
        domain_values = [gate(block, key) for key in DOMAIN_GATES]
        if not (all(v == "pass" for v in domain_values) or all(v == "not_applicable" for v in domain_values)):
            errors.append("full_skill requires domain_substance_gates all pass for domain skills, or all not_applicable for non-domain skills")
    if route == "domain_discovery":
        if operation not in {"ask_domain_questions", "build_domain_content_contract"}:
            errors.append("domain_discovery requires ask_domain_questions or build_domain_content_contract")
        domain_values = [gate(block, key) for key in DOMAIN_GATES]
        if all(v == "pass" for v in domain_values):
            warnings.append("domain_discovery route used even though all domain_substance_gates are pass")

    if mode in {"critique", "improve", "eval"}:
        for key in HARD_GATES:
            if gate(block, key) not in {"not_applicable", "pass"}:
                warnings.append(f"{mode} usually uses hard_gates.{key}: not_applicable")
        for key in DOMAIN_GATES:
            if gate(block, key) not in {"not_applicable", "pass"}:
                warnings.append(f"{mode} usually uses domain_substance_gates.{key}: not_applicable")

    for key in SELF_CHECKS:
        value = boolish(block, key)
        if value not in BOOLISH:
            errors.append(f"contract_self_check.{key} invalid or missing: {value!r}")
    if boolish(block, "mode_route_compatible") == "false":
        errors.append("self-check reports mode_route_compatible: false")
    if boolish(block, "operation_compatible") == "false":
        errors.append("self-check reports operation_compatible: false")
    if boolish(block, "hard_gates_applied") == "false":
        errors.append("self-check reports hard_gates_applied: false")
    if boolish(block, "domain_substance_gates_applied") == "false":
        errors.append("self-check reports domain_substance_gates_applied: false")
    if boolish(block, "full_package_overbuilt") == "true" and route != "full_skill":
        errors.append("self-check reports full_package_overbuilt: true")
    if mode == "improve" and boolish(block, "patch_not_rebuild") == "false":
        warnings.append("improve mode reports patch_not_rebuild: false; rebuild_reason should be present")

    artifact_found, artifact_errors, artifact_warnings = validate_eval_artifacts(text)
    errors.extend(scan_invalid_kind_aliases(text))
    if artifact_found:
        if boolish(block, "eval_artifact_present") != "true":
            errors.append("Eval artifact present but eval_artifact_present is not true")
        if artifact_errors:
            errors.extend([f"Eval artifact invalid: {e}" for e in artifact_errors])
            if boolish(block, "eval_schema_runner_compatible") == "true":
                errors.append("self-check claims eval_schema_runner_compatible: true but eval artifact is invalid")
        elif boolish(block, "eval_schema_runner_compatible") != "true":
            errors.append("Valid-looking eval artifact present but eval_schema_runner_compatible is not true")
        warnings.extend(artifact_warnings)
    else:
        if boolish(block, "eval_artifact_present") == "true":
            errors.append("eval_artifact_present is true but no fenced runner eval JSON artifact was found")
        if mode == "eval" and operation == "design_runner_evals":
            errors.append("design_runner_evals requires a fenced runner-compatible JSON eval artifact")
        if boolish(block, "eval_schema_runner_compatible") == "true" and mode not in {"eval", "improve"}:
            warnings.append("eval_schema_runner_compatible true but no eval artifact found")

    if mode == "eval" and operation == "design_human_rubric" and artifact_found:
        errors.append("design_human_rubric must not output runner eval JSON; use design_runner_evals instead")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "parsed": {"mode": mode, "route": route, "operation": operation, "eval_artifact_found": artifact_found}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    text = args.output_file.read_text(encoding="utf-8")
    result = validate_output(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
