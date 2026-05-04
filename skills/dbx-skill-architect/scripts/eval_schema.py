#!/usr/bin/env python3
"""Shared schema and quality helpers for dbx-skill-architect eval files.

Standard library only. This module is imported by run_skill_evals.py and can also
be executed directly for schema validation.

The schema validator intentionally checks more than structure. A marker-only eval
suite can make shallow outputs look good, so each eval case must include at
least one required, non-marker quality check.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CANONICAL_KINDS = {"positive", "negative", "near_miss", "failure_mode", "safety"}
CHECK_BUCKETS = ("trigger", "process", "output", "safety")
CHECK_TYPES = {"must_contain", "must_not_contain", "must_start_with", "regex"}
CHECK_QUALITIES = {"structural", "behavior", "artifact", "specificity", "domain", "safety", "validation"}
STRONG_QUALITIES = {"behavior", "artifact", "specificity", "domain", "safety", "validation"}
MIN_KIND_COUNTS = {"positive": 2, "negative": 1, "near_miss": 1}
PLACEHOLDER_PATTERNS = [
    re.compile(r"(?i)\ba realistic prompt\b"),
    re.compile(r"(?i)\bdescribe the recurring scenario\b"),
    re.compile(r"(?i)\bdescribe what the skill does\b"),
    re.compile(r"(?i)\btodo\b|\btbd\b"),
    re.compile(r"(?m)^\s*-\s*\.\.\.\s*$"),
]
WEAK_VALUE_EXACT = {
    "## summary",
    "## validation",
    "## result",
    "## evidence or inputs used",
    "## risks or open questions",
    "skill.md",
    "evals/evals.json",
    "evals/triggers.json",
    "scripts/",
    "references/",
    "checks",
    "pass_threshold",
    "skill_shape",
    "dominant_failure_modes",
    "domain_substance_gates",
    "patch_hypothesis",
    "mode:",
    "route:",
    "operation:",
}
WEAK_VALUE_PATTERNS = [
    re.compile(r"^#{1,6}\s+"),
    re.compile(r"^(mode|route|operation):\s*[-_a-z0-9]+$"),
    re.compile(r"^```(?:yaml|json|markdown|text)?$"),
    re.compile(r"^#\s*skill\.md$", re.IGNORECASE),
    re.compile(r"^(scripts|references|assets|evals)/?$"),
]


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def has_placeholder(value: str) -> bool:
    return any(pattern.search(value) for pattern in PLACEHOLDER_PATTERNS)


def is_weak_marker_value(value: str) -> bool:
    normalized = " ".join(value.strip().lower().split())
    if normalized in WEAK_VALUE_EXACT:
        return True
    if normalized.endswith("/") and normalized.rstrip("/") in {"scripts", "references", "assets", "evals"}:
        return True
    return any(pattern.search(value.strip()) for pattern in WEAK_VALUE_PATTERNS)


def validate_check(check: Any, prefix: str) -> tuple[list[str], list[str], bool, bool]:
    """Return (errors, warnings, is_required, is_strong_required)."""
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(check, dict):
        return [f"{prefix}: check must be an object"], warnings, False, False
    check_type = check.get("type")
    if check_type not in CHECK_TYPES:
        errors.append(f"{prefix}: type must be one of {sorted(CHECK_TYPES)}")
    value = check.get("value")
    if not isinstance(value, str) or not value:
        errors.append(f"{prefix}: value must be a non-empty string")
        value = ""
    elif has_placeholder(value):
        errors.append(f"{prefix}: value contains placeholder text, not a real assertion: {value!r}")
    required = check.get("required")
    if not isinstance(required, bool):
        errors.append(f"{prefix}: required must be true or false")
        required = False
    quality = check.get("quality", "structural")
    if quality not in CHECK_QUALITIES:
        errors.append(f"{prefix}: quality must be one of {sorted(CHECK_QUALITIES)}")
        quality = "structural"
    if check_type == "regex" and isinstance(value, str):
        try:
            re.compile(value)
        except re.error as exc:
            errors.append(f"{prefix}: invalid regex: {exc}")
    if "notes" in check and not isinstance(check["notes"], str):
        warnings.append(f"{prefix}: notes should be a string")
    weak = is_weak_marker_value(value)
    if weak and quality in STRONG_QUALITIES:
        errors.append(f"{prefix}: quality={quality!r} cannot be used with marker-only value {value!r}")
    is_strong_required = bool(required) and quality in STRONG_QUALITIES and not weak and not has_placeholder(value)
    return errors, warnings, bool(required), is_strong_required


def validate_eval_file(path: Path, expected_skill_name: str | None = None) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    data, err = load_json(path)
    if err:
        return ValidationResult([f"{path}: invalid JSON: {err}"], warnings)
    if not isinstance(data, dict):
        return ValidationResult([f"{path}: root must be an object"], warnings)
    skill_name = data.get("skill_name")
    if not isinstance(skill_name, str) or not skill_name.strip():
        errors.append(f"{path}: skill_name must be a non-empty string")
    elif expected_skill_name and skill_name != expected_skill_name:
        errors.append(f"{path}: skill_name is {skill_name!r}, expected {expected_skill_name!r}")
    threshold = data.get("pass_threshold", 0.85)
    if not isinstance(threshold, (int, float)) or not 0 < float(threshold) <= 1:
        errors.append(f"{path}: pass_threshold must be a number in (0, 1]")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append(f"{path}: evals must be a non-empty array")
        return ValidationResult(errors, warnings)
    seen_ids: set[str] = set()
    kinds: dict[str, int] = {}
    for index, case in enumerate(evals):
        prefix = f"{path}#evals[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: case must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        elif has_placeholder(case_id):
            errors.append(f"{prefix}: id contains placeholder text: {case_id!r}")
        elif case_id in seen_ids:
            errors.append(f"{prefix}: duplicate id {case_id!r}")
        else:
            seen_ids.add(case_id)
        kind = case.get("kind")
        if kind not in CANONICAL_KINDS:
            errors.append(f"{prefix}: kind must be one of {sorted(CANONICAL_KINDS)}")
        else:
            kinds[kind] = kinds.get(kind, 0) + 1
        for field in ("prompt", "expected_behavior"):
            value = case.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}: {field} must be a non-empty string")
            elif has_placeholder(value):
                errors.append(f"{prefix}: {field} contains placeholder text, not a realistic case")
        checks = case.get("checks")
        total_checks = 0
        required_checks = 0
        strong_required_checks = 0
        weak_checks = 0
        if not isinstance(checks, dict):
            errors.append(f"{prefix}: checks must be an object")
        else:
            for bucket in CHECK_BUCKETS:
                bucket_checks = checks.get(bucket)
                if not isinstance(bucket_checks, list):
                    errors.append(f"{prefix}: checks.{bucket} must be an array")
                    continue
                for check_index, check in enumerate(bucket_checks):
                    total_checks += 1
                    e, w, is_required, is_strong_required = validate_check(
                        check, f"{prefix}.checks.{bucket}[{check_index}]"
                    )
                    errors.extend(e)
                    warnings.extend(w)
                    required_checks += 1 if is_required else 0
                    strong_required_checks += 1 if is_strong_required else 0
                    if isinstance(check, dict) and isinstance(check.get("value"), str) and is_weak_marker_value(check["value"]):
                        weak_checks += 1
        if total_checks == 0:
            errors.append(f"{prefix}: at least one deterministic check is required")
        if required_checks == 0:
            errors.append(f"{prefix}: at least one required check is required")
        if strong_required_checks == 0:
            errors.append(
                f"{prefix}: at least one required non-marker quality check is required "
                "(quality must be behavior, artifact, specificity, domain, safety, or validation)"
            )
        if total_checks and weak_checks / total_checks > 0.60:
            warnings.append(f"{prefix}: more than 60% of checks are structural markers; consider stronger assertions")
        pass_criteria = case.get("pass_criteria")
        if not isinstance(pass_criteria, dict):
            errors.append(f"{prefix}: pass_criteria must be an object")
        else:
            if not isinstance(pass_criteria.get("all_required"), bool):
                errors.append(f"{prefix}: pass_criteria.all_required must be true or false")
            min_score = pass_criteria.get("min_score")
            if not isinstance(min_score, (int, float)) or not 0 < float(min_score) <= 1:
                errors.append(f"{prefix}: pass_criteria.min_score must be a number in (0, 1]")
    for needed, minimum in MIN_KIND_COUNTS.items():
        count = kinds.get(needed, 0)
        if count < minimum:
            errors.append(f"{path}: requires at least {minimum} {needed} eval(s), found {count}")
    risk_count = kinds.get("failure_mode", 0) + kinds.get("safety", 0)
    if risk_count == 0:
        errors.append(f"{path}: requires at least one failure_mode or safety eval")
    return ValidationResult(errors, warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a dbx-skill-architect evals/evals.json file.")
    parser.add_argument("path", help="Path to evals.json")
    parser.add_argument("--skill-name", help="Expected skill name")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    result = validate_eval_file(Path(args.path), args.skill_name)
    payload = {"ok": result.ok, "errors": result.errors, "warnings": result.warnings}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "OK" if result.ok else "ERROR"
        print(f"Eval schema validation: {status}")
        for err in result.errors:
            print(f"ERROR: {err}")
        for warning in result.warnings:
            print(f"WARNING: {warning}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
