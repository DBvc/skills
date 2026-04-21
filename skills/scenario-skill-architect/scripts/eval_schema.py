#!/usr/bin/env python3
"""Single source of truth for scenario-skill-architect eval schema."""
from __future__ import annotations

from typing import Any

SUPPORTED_CHECKS = {"must_contain", "must_not_contain", "regex", "must_start_with"}
CATEGORIES = ("trigger", "process", "output", "safety")
VALID_KINDS = {"positive", "negative", "near_miss", "failure_mode", "safety"}
INVALID_KIND_ALIASES = {"failure", "failure_safety", "failure/safety", "safety_failure", "failure-or-safety"}


def validate_check(case_id: str, category: str, index: int, check: Any) -> list[str]:
    loc = f"{case_id}: checks.{category}[{index}]"
    if not isinstance(check, dict):
        return [f"{loc} must be an object, got {type(check).__name__}"]
    errors: list[str] = []
    ctype = check.get("type")
    if ctype not in SUPPORTED_CHECKS:
        errors.append(f"{loc}.type must be one of {sorted(SUPPORTED_CHECKS)}, got {ctype!r}")
    if not isinstance(check.get("value"), str):
        errors.append(f"{loc}.value must be a string")
    if "required" in check and not isinstance(check.get("required"), bool):
        errors.append(f"{loc}.required must be boolean when present")
    return errors


def validate_eval_data(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if "cases" in data and "evals" not in data:
        errors.append("Top-level key must be 'evals', not 'cases'")
    if not isinstance(data.get("skill_name"), str) or not data.get("skill_name", "").strip():
        errors.append("skill_name is required and must be a non-empty string")
    threshold = data.get("pass_threshold", 0.85)
    if not isinstance(threshold, (int, float)) or not (0 <= threshold <= 1):
        errors.append("pass_threshold must be a number between 0 and 1")

    evals = data.get("evals")
    if not isinstance(evals, list):
        return errors + ["Missing evals list"], warnings
    if len(evals) < 5:
        errors.append("At least 5 evals are required")

    kinds: list[Any] = []
    ids: set[str] = set()
    for index, case in enumerate(evals):
        if not isinstance(case, dict):
            errors.append(f"evals[{index}] must be an object, got {type(case).__name__}")
            continue
        cid = case.get("id", f"<missing-id-{index}>")
        if not isinstance(cid, str) or not cid.strip():
            errors.append(f"evals[{index}].id must be a non-empty string")
            cid = f"<invalid-id-{index}>"
        if cid in ids:
            errors.append(f"Duplicate eval id: {cid}")
        ids.add(cid)
        kind = case.get("kind")
        kinds.append(kind)
        if kind in INVALID_KIND_ALIASES:
            errors.append(f"{cid}: kind {kind!r} is an invalid alias; use 'failure_mode' or 'safety'")
        elif kind not in VALID_KINDS:
            errors.append(f"{cid}: kind must be one of {sorted(VALID_KINDS)}, got {kind!r}")
        for field in ("id", "kind", "prompt", "expected_behavior", "checks", "pass_criteria"):
            if field not in case:
                errors.append(f"{cid}: missing {field}")
        for field in ("prompt", "expected_behavior"):
            if field in case and not isinstance(case.get(field), str):
                errors.append(f"{cid}: {field} must be a string")
        checks = case.get("checks", {})
        if not isinstance(checks, dict):
            errors.append(f"{cid}: checks must be an object")
        else:
            for category in CATEGORIES:
                arr = checks.get(category)
                if not isinstance(arr, list):
                    errors.append(f"{cid}: checks.{category} must be a list")
                    continue
                for check_index, check in enumerate(arr):
                    errors.extend(validate_check(str(cid), category, check_index, check))
        criteria = case.get("pass_criteria", {})
        if not isinstance(criteria, dict):
            errors.append(f"{cid}: pass_criteria must be an object")
        else:
            if not isinstance(criteria.get("all_required"), bool):
                errors.append(f"{cid}: pass_criteria.all_required must be boolean")
            min_score = criteria.get("min_score")
            if not isinstance(min_score, (int, float)) or not (0 <= min_score <= 1):
                errors.append(f"{cid}: pass_criteria.min_score must be number between 0 and 1")

    if kinds.count("positive") < 2:
        errors.append("At least 2 positive evals are required")
    if "negative" not in kinds:
        errors.append("At least one negative eval is required")
    if "near_miss" not in kinds:
        errors.append("At least one near_miss eval is required")
    if not ({"failure_mode", "safety"} & set(kinds)):
        errors.append("At least one failure_mode or safety eval is required")
    return errors, warnings
