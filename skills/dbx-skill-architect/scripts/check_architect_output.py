#!/usr/bin/env python3
"""Check a captured dbx-skill-architect output for contract, gates, and artifacts.

This checker is a guardrail, not a proof of skill quality. It intentionally goes
beyond marker checks:

- validates the opening YAML contract with fail-closed gate rules;
- allows honest `unknown` shape for needs_clarification only when blocking
  questions are present;
- validates patch hypotheses for concrete target files and exact edit units;
- extracts copy-ready fenced file blocks for full_skill outputs;
- parses SKILL.md frontmatter and eval JSON artifacts;
- rejects common placeholders and marker-only packages;
- applies shape-specific done criteria for tool, coordination, review/procedure,
  and domain/content skills.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from eval_schema import validate_eval_file  # noqa: E402

ALLOWED_MODES = {"create", "critique", "improve", "eval", "triage"}
ALLOWED_ROUTES = {
    "full_skill", "mini_skill", "needs_clarification", "domain_discovery", "checklist",
    "direct_answer", "refuse_or_redesign", "not_a_creation_request",
}
ALLOWED_OPERATIONS = {
    "ask_questions", "ask_domain_questions", "build_domain_content_contract", "draft_package",
    "critique_package", "propose_patch_plan", "patch_existing_package", "design_runner_evals",
    "design_human_rubric", "run_lint", "run_evals", "provide_alternative",
}
ALLOWED_ARCHETYPES = {
    "procedure", "tool", "knowledge", "taste", "decision", "research", "coordination", "meta",
    "hybrid", "unknown", "not_applicable",
}
ALLOWED_FAILURE_MODES = {
    "wrong_trigger", "context_bloat", "domain_shallow", "fragile_operation", "unverified_output",
    "taste_collapse", "safety_overreach", "handoff_failure", "maintenance_drift",
}
GATE_VALUES = {"pass", "fail", "unknown", "not_applicable"}
BOOL_OR_NA = {"true", "false", "not_applicable"}
PATCH_REQUIRED_VALUES = {"true", "false", "not_applicable"}
HARD_GATE_KEYS = ("repeatability", "stable_job", "evaluability", "safety_legitimacy")
DOMAIN_GATE_KEYS = (
    "target_user_defined",
    "output_depth_defined",
    "domain_variables_identified",
    "data_source_policy_defined",
    "failure_knowledge_identified",
    "expert_quality_rubric_defined",
    "worked_example_available",
)
SELF_CHECK_KEYS = (
    "mode_route_compatible",
    "operation_compatible",
    "hard_gates_applied",
    "skill_shape_used_for_architecture",
    "domain_substance_gates_applied",
    "patch_hypothesis_present_when_needed",
    "full_package_overbuilt",
    "eval_artifact_present",
    "eval_schema_runner_compatible",
    "patch_not_rebuild",
)
COMPATIBLE = {
    "create": {
        "routes": {"full_skill", "mini_skill", "needs_clarification", "domain_discovery"},
        "operations": {"ask_questions", "ask_domain_questions", "build_domain_content_contract", "draft_package"},
    },
    "critique": {
        "routes": {"not_a_creation_request"},
        "operations": {"critique_package", "propose_patch_plan"},
    },
    "improve": {
        "routes": {"not_a_creation_request"},
        "operations": {"patch_existing_package", "propose_patch_plan", "ask_questions", "run_lint", "run_evals"},
    },
    "eval": {
        "routes": {"not_a_creation_request"},
        "operations": {"design_runner_evals", "design_human_rubric", "run_evals"},
    },
    "triage": {
        "routes": {"mini_skill", "checklist", "direct_answer", "refuse_or_redesign"},
        "operations": {"ask_questions", "provide_alternative"},
    },
}
DOMAIN_ARCHETYPES = {"knowledge", "taste", "decision", "research"}
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
    re.compile(r"target_failures:\s*\[\]\s*$", re.MULTILINE),
    re.compile(r"acceptance_tests:\s*\[\]\s*$", re.MULTILINE),
    re.compile(r"proposed_change:\s*['\"]{0,2}\s*$", re.MULTILINE),
]
GENERIC_DOMAIN_WORDS = {
    "audience", "user", "users", "goals", "goal", "constraints", "constraint", "context",
    "requirements", "requirement", "preferences", "preference", "inputs", "outputs", "scope",
    "quality", "criteria", "examples", "data", "source",
}


def first_yaml_block(text: str) -> str | None:
    match = re.search(r"\A\s*```yaml\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def contains_key(block: str, key: str) -> bool:
    return re.search(rf"(?m)^\s*{re.escape(key)}:", block) is not None


def scalar_value(block: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([^\n#]*)", block)
    if not match:
        return None
    value = match.group(1).strip().strip('"').strip("'")
    return value or None


def is_placeholder_scalar(value: str | None) -> bool:
    if value is None:
        return True
    return " | " in value or value.strip() in {"", "[]", "{}"}


def key_child_text(block: str, key: str) -> tuple[str | None, str]:
    lines = block.splitlines()
    for index, raw in enumerate(lines):
        match = re.match(rf"^(\s*){re.escape(key)}:\s*(.*)$", raw)
        if not match:
            continue
        indent = len(match.group(1))
        inline = match.group(2).strip()
        child_lines: list[str] = []
        for child in lines[index + 1:]:
            if not child.strip():
                continue
            child_indent = len(child) - len(child.lstrip(" "))
            if child_indent <= indent:
                break
            child_lines.append(child)
        return inline or None, "\n".join(child_lines)
    return None, ""


def nonempty_list(block: str, key: str) -> bool:
    inline, child = key_child_text(block, key)
    if inline:
        if inline == "[]":
            return False
        if inline.startswith("[") and inline.endswith("]"):
            inner = inline[1:-1].strip()
            return bool(inner)
        return True
    return bool(re.search(r"(?m)^\s*-\s+\S", child))


def list_values(block: str, key: str) -> list[str]:
    inline, child = key_child_text(block, key)
    if inline and inline.startswith("[") and inline.endswith("]"):
        inner = inline[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]
    values: list[str] = []
    for match in re.finditer(r"(?m)^\s*-\s+([^#\n]+)", child):
        values.append(match.group(1).strip().strip('"').strip("'"))
    return values


def add_missing(errors: list[str], block: str, keys: tuple[str, ...] | list[str], label: str) -> None:
    for key in keys:
        if not contains_key(block, key):
            errors.append(f"missing {label}: {key}")


def require_scalar(
    errors: list[str],
    block: str,
    key: str,
    allowed: set[str] | None = None,
    *,
    label: str = "field",
) -> str | None:
    value = scalar_value(block, key)
    if is_placeholder_scalar(value):
        errors.append(f"{label} {key} must be set, not a placeholder")
        return value
    if allowed is not None and value not in allowed:
        errors.append(f"{label} {key} has invalid value {value!r}; allowed: {sorted(allowed)}")
    return value


def normalize_path(path: str) -> str:
    cleaned = path.strip().strip('"').strip("'").strip()
    cleaned = cleaned.removeprefix("./")
    return cleaned.replace("\\", "/")


def parse_path_from_fence_info(info: str) -> str | None:
    for match in re.finditer(r"(?:path|file|filename)\s*=\s*([^\s]+)", info):
        return normalize_path(match.group(1))
    parts = info.split()
    for part in parts:
        cleaned = normalize_path(part)
        if "/" in cleaned or cleaned.endswith((".md", ".json", ".py", ".sh", ".js", ".ts")):
            if cleaned not in {"markdown", "json", "python", "yaml", "text"}:
                return cleaned
    return None


def path_from_hint_line(line: str) -> str | None:
    patterns = [
        r"^\s{0,3}#{2,6}\s+`([^`]+)`\s*$",
        r"^\s{0,3}(?:File|Path|filename|path):\s*`?([^`\s]+)`?\s*$",
        r"^\s{0,3}---\s*(?:file|path):\s*([^\s]+)\s*---\s*$",
    ]
    for pattern in patterns:
        match = re.match(pattern, line, flags=re.IGNORECASE)
        if match:
            return normalize_path(match.group(1))
    return None


def extract_file_blocks(text: str) -> dict[str, str]:
    """Extract fenced file blocks keyed by path.

    Supported shapes:
      ### `skills/foo/SKILL.md`
      ```markdown
      ...
      ```

      ```markdown path=skills/foo/SKILL.md
      ...
      ```
    """
    lines = text.splitlines()
    blocks: dict[str, str] = {}
    last_hint: str | None = None
    i = 0
    while i < len(lines):
        hint = path_from_hint_line(lines[i])
        if hint:
            last_hint = hint
            i += 1
            continue
        fence = re.match(r"^```(.*)$", lines[i])
        if not fence:
            i += 1
            continue
        info = fence.group(1).strip()
        path = parse_path_from_fence_info(info) or last_hint
        content_lines: list[str] = []
        i += 1
        while i < len(lines) and not lines[i].startswith("```"):
            content_lines.append(lines[i])
            i += 1
        if path:
            blocks[normalize_path(path)] = "\n".join(content_lines).rstrip() + "\n"
        last_hint = None
        i += 1
    return blocks


def find_block(blocks: dict[str, str], required_suffix: str) -> tuple[str | None, str | None]:
    suffix = normalize_path(required_suffix)
    for path, content in blocks.items():
        if path == suffix or path.endswith("/" + suffix) or path.endswith(suffix):
            return path, content
    return None, None


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


def placeholder_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            snippet = " ".join(match.group(0).split())[:80]
            hits.append(snippet)
    return hits


def validate_skill_md_artifact(content: str, expected_name: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    fields, err = parse_frontmatter(content)
    if err:
        errors.append(err)
    name = fields.get("name")
    description = fields.get("description")
    if not name:
        errors.append("artifact SKILL.md frontmatter.name is required")
    elif expected_name and name != expected_name:
        errors.append(f"artifact SKILL.md name {name!r} must match eval skill_name {expected_name!r}")
    if not description or len(description) < 40:
        errors.append("artifact SKILL.md frontmatter.description must be specific and at least 40 characters")
    elif "use" not in description.lower() and "when" not in description.lower():
        warnings.append("artifact SKILL.md description should say when to use the skill")
    body = FRONTMATTER_RE.sub("", content, count=1)
    if len(body.split()) < 120:
        errors.append("artifact SKILL.md body is too short for a full_skill package")
    for hit in placeholder_hits(content):
        errors.append(f"artifact SKILL.md contains placeholder text: {hit!r}")
    if len(content.splitlines()) > 500:
        warnings.append("artifact SKILL.md exceeds 500 lines; move detail into references/")
    return errors, warnings


def validate_triggers_json(content: str, expected_name: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(content)
    except Exception as exc:  # noqa: BLE001
        return [f"evals/triggers.json invalid JSON: {exc}"], warnings
    if not isinstance(data, dict):
        return ["evals/triggers.json root must be object"], warnings
    if expected_name and data.get("skill_name") != expected_name:
        errors.append("evals/triggers.json skill_name must match SKILL.md name")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("evals/triggers.json cases must be a non-empty array")
        return errors, warnings
    kinds: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"evals/triggers.json cases[{index}] must be object")
            continue
        kinds.add(str(case.get("kind")))
        if not isinstance(case.get("prompt"), str) or placeholder_hits(case.get("prompt", "")):
            errors.append(f"evals/triggers.json cases[{index}].prompt must be realistic, not placeholder")
        if not isinstance(case.get("expected_trigger"), bool):
            errors.append(f"evals/triggers.json cases[{index}].expected_trigger must be boolean")
    for needed in ("positive", "negative", "near_miss"):
        if needed not in kinds:
            errors.append(f"evals/triggers.json requires at least one {needed} case")
    return errors, warnings


def validate_evals_json_artifact(content: str, expected_name: str | None) -> tuple[list[str], list[str]]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    try:
        result = validate_eval_file(tmp_path, expected_name)
        return result.errors, result.warnings
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def has_any_script_block(blocks: dict[str, str]) -> bool:
    return any("/scripts/" in f"/{path}" and path.endswith((".py", ".sh", ".js", ".ts")) for path in blocks)


def contains_all_groups(text: str, groups: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
    lower = text.lower()
    missing: list[tuple[str, ...]] = []
    for group in groups:
        if not any(term in lower for term in group):
            missing.append(group)
    return missing


def domain_specificity_errors(text: str) -> list[str]:
    errors: list[str] = []
    lower = text.lower()
    if re.search(r"audience\s*,\s*goals\s*,\s*constraints", lower):
        errors.append("domain variables are generic ('audience, goals, constraints')")
    # Collect list items near required/domain variable headings.
    variable_items: list[str] = []
    lines = text.splitlines()
    capture = False
    for line in lines:
        if re.search(r"(?i)(required_)?domain[_ -]?variables|required[_ -]?variables|key[_ -]?variables", line):
            capture = True
            continue
        if capture:
            if re.match(r"^\s*(#{1,6}|```)", line) or (line.strip() and not line.lstrip().startswith("-")):
                capture = False
                continue
            match = re.match(r"^\s*-\s+(.+)$", line)
            if match:
                variable_items.append(match.group(1).strip())
    if variable_items:
        specific = []
        for item in variable_items:
            tokens = re.findall(r"[a-zA-Z][a-zA-Z-]{2,}", item.lower())
            if any(token not in GENERIC_DOMAIN_WORDS for token in tokens):
                specific.append(item)
        if len(specific) < 3:
            errors.append("domain variables need at least three domain-specific items, not generic planning words")
    return errors


def validate_full_skill_artifacts(
    text: str,
    blocks: dict[str, str],
    archetype: str | None,
    dominant_failures: set[str],
    domain_required: bool,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not blocks:
        return ["full_skill output must provide copy-ready fenced file blocks, not just mention file names"], warnings

    skill_path, skill_md = find_block(blocks, "SKILL.md")
    eval_path, evals_json = find_block(blocks, "evals/evals.json")
    trigger_path, triggers_json = find_block(blocks, "evals/triggers.json")
    if not skill_md:
        errors.append("full_skill output must include a fenced file block for SKILL.md")
    if not evals_json:
        errors.append("full_skill output must include a fenced file block for evals/evals.json")
    if not triggers_json:
        errors.append("full_skill output must include a fenced file block for evals/triggers.json")
    if errors:
        return errors, warnings

    expected_name: str | None = None
    assert skill_md is not None and evals_json is not None and triggers_json is not None
    fields, fm_err = parse_frontmatter(skill_md)
    if not fm_err:
        expected_name = fields.get("name")
    e, w = validate_skill_md_artifact(skill_md, expected_name)
    errors.extend([f"{skill_path}: {item}" for item in e])
    warnings.extend([f"{skill_path}: {item}" for item in w])
    e, w = validate_evals_json_artifact(evals_json, expected_name)
    errors.extend([f"{eval_path}: {item}" for item in e])
    warnings.extend([f"{eval_path}: {item}" for item in w])
    e, w = validate_triggers_json(triggers_json, expected_name)
    errors.extend([f"{trigger_path}: {item}" for item in e])
    warnings.extend([f"{trigger_path}: {item}" for item in w])

    for path, content in blocks.items():
        for hit in placeholder_hits(content):
            errors.append(f"{path}: contains placeholder text: {hit!r}")

    artifact_text = "\n".join(blocks.values())
    lower = artifact_text.lower()
    if archetype == "tool" or "fragile_operation" in dominant_failures:
        if not has_any_script_block(blocks):
            errors.append("tool/fragile_operation full_skill must include at least one script file block under scripts/")
        missing = contains_all_groups(artifact_text, [
            ("--help", "argparse", "click", "typer"),
            ("exit code", "return code", "non-zero"),
            ("fixture", "sample invalid", "sample valid", "test fixture"),
            ("validation command", "run validation", "python3 scripts/", "node scripts/"),
        ])
        for group in missing:
            errors.append(f"tool/fragile_operation full_skill missing done criterion: one of {group}")
    if archetype == "coordination":
        missing = contains_all_groups(artifact_text, [
            ("authority", "owner", "permission"),
            ("approval", "confirm", "consent"),
            ("handoff", "handover", "handoff contract"),
            ("conflict", "collision", "overlap"),
            ("timezone", "time zone", "deadline", "calendar"),
        ])
        for group in missing:
            errors.append(f"coordination full_skill missing boundary criterion: one of {group}")
    reviewish = any(term in lower for term in ("review", "critique", "audit", "finding", "pull request", "pr description"))
    if archetype == "procedure" and reviewish:
        missing = contains_all_groups(artifact_text, [
            ("evidence", "diff", "source"),
            ("finding", "issue", "observation"),
            ("severity", "priority", "impact"),
            ("confidence", "certainty"),
            ("reviewer", "handoff", "next reader"),
        ])
        for group in missing:
            errors.append(f"review/procedure full_skill missing finding criterion: one of {group}")
    if domain_required:
        errors.extend(domain_specificity_errors(artifact_text))
    return errors, warnings


def check_output(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().startswith("```yaml"):
        errors.append("output must start with a fenced yaml block")
    block = first_yaml_block(text)
    if not block:
        return ["missing opening fenced yaml block"], warnings

    add_missing(errors, block, ["skill_architect_decision"], "root key")
    add_missing(
        errors,
        block,
        [
            "mode", "route", "operation", "skill_shape", "hard_gates", "domain_substance_gates",
            "patch_hypothesis", "blocking_questions", "assumptions", "confidence", "contract_self_check",
        ],
        "opening contract key",
    )

    mode = require_scalar(errors, block, "mode", ALLOWED_MODES, label="contract")
    route = require_scalar(errors, block, "route", ALLOWED_ROUTES, label="contract")
    operation = require_scalar(errors, block, "operation", ALLOWED_OPERATIONS, label="contract")
    require_scalar(errors, block, "confidence", {"high", "medium", "low"}, label="contract")

    if mode in COMPATIBLE:
        if route and route not in COMPATIBLE[mode]["routes"]:
            errors.append(f"incompatible mode/route: {mode}/{route}")
        if operation and operation not in COMPATIBLE[mode]["operations"]:
            errors.append(f"incompatible mode/operation: {mode}/{operation}")

    # Hard gates before shape strictness because clarification depends on blocking unknowns.
    add_missing(errors, block, HARD_GATE_KEYS, "hard gate")
    hard_gate_values = {key: scalar_value(block, key) for key in HARD_GATE_KEYS}
    for key, value in hard_gate_values.items():
        if value not in GATE_VALUES:
            errors.append(f"hard_gates.{key} must be one of {sorted(GATE_VALUES)}, got {value!r}")
    needs_clarification = route == "needs_clarification"
    if route == "full_skill":
        for key, value in hard_gate_values.items():
            if value != "pass":
                errors.append(f"full_skill requires hard_gates.{key}=pass, got {value!r}")
    if needs_clarification:
        if "unknown" not in hard_gate_values.values():
            errors.append("needs_clarification route should mark at least one hard gate as unknown")
        if not nonempty_list(block, "blocking_questions"):
            errors.append("needs_clarification route requires non-empty blocking_questions")

    # Skill shape.
    archetype = require_scalar(errors, block, "archetype", ALLOWED_ARCHETYPES, label="skill_shape")
    if mode in {"create", "critique", "improve", "eval"} and archetype in {"unknown", "not_applicable", None}:
        if not (needs_clarification and nonempty_list(block, "blocking_questions")):
            errors.append(f"skill_shape.archetype must be concrete for mode {mode!r} unless route is needs_clarification with blocking questions")
    if mode in {"create", "critique", "improve", "eval"} and not needs_clarification and not nonempty_list(block, "dominant_failure_modes"):
        errors.append("skill_shape.dominant_failure_modes must be non-empty for architect tasks")
    if mode in {"create", "critique", "improve", "eval"} and not needs_clarification and not nonempty_list(block, "implementation_implications"):
        errors.append("skill_shape.implementation_implications must be non-empty for architect tasks")
    unknown_failures = [item for item in list_values(block, "dominant_failure_modes") if item and item not in ALLOWED_FAILURE_MODES]
    if unknown_failures:
        errors.append(f"unknown dominant_failure_modes: {unknown_failures}")

    # Domain gates.
    add_missing(errors, block, DOMAIN_GATE_KEYS, "domain substance gate")
    domain_gate_values = {key: scalar_value(block, key) for key in DOMAIN_GATE_KEYS}
    for key, value in domain_gate_values.items():
        if value not in GATE_VALUES:
            errors.append(f"domain_substance_gates.{key} must be one of {sorted(GATE_VALUES)}, got {value!r}")
    dominant_failures = set(list_values(block, "dominant_failure_modes"))
    domain_required = bool(
        route == "full_skill"
        and (
            archetype in DOMAIN_ARCHETYPES
            or "domain_shallow" in dominant_failures
            or "taste_collapse" in dominant_failures
        )
    )
    if domain_required:
        for key, value in domain_gate_values.items():
            if value != "pass":
                errors.append(f"domain/content full_skill requires domain_substance_gates.{key}=pass, got {value!r}")
    if route == "domain_discovery":
        if all(value == "pass" for value in domain_gate_values.values()):
            errors.append("domain_discovery route should not have all domain gates already passing")
        if not nonempty_list(block, "blocking_questions"):
            errors.append("domain_discovery route requires non-empty blocking_questions")

    # Patch hypothesis.
    patch_required = mode == "improve" or operation in {"patch_existing_package", "propose_patch_plan"}
    patch_required_value = require_scalar(errors, block, "required", PATCH_REQUIRED_VALUES, label="patch_hypothesis")
    if patch_required and patch_required_value != "true":
        errors.append("improve/propose-patch operations require patch_hypothesis.required=true")
    if patch_required or patch_required_value == "true":
        for key in ("target_failures", "target_files", "exact_edit_units", "acceptance_tests", "rollback_conditions"):
            if not nonempty_list(block, key):
                errors.append(f"patch_hypothesis.{key} must be non-empty when patch is required")
        for key in ("proposed_change", "expected_benefit", "expected_cost"):
            value = scalar_value(block, key)
            if is_placeholder_scalar(value):
                errors.append(f"patch_hypothesis.{key} must be non-empty when patch is required")

    # Self-check.
    add_missing(errors, block, SELF_CHECK_KEYS, "contract_self_check key")
    self_check_values = {key: scalar_value(block, key) for key in SELF_CHECK_KEYS}
    for key, value in self_check_values.items():
        if value not in BOOL_OR_NA:
            errors.append(f"contract_self_check.{key} must be true, false, or not_applicable, got {value!r}")
    if self_check_values.get("mode_route_compatible") != "true":
        errors.append("contract_self_check.mode_route_compatible must be true")
    if self_check_values.get("operation_compatible") != "true":
        errors.append("contract_self_check.operation_compatible must be true")
    if self_check_values.get("hard_gates_applied") != "true":
        errors.append("contract_self_check.hard_gates_applied must be true")
    if mode in {"create", "critique", "improve", "eval"} and not needs_clarification and self_check_values.get("skill_shape_used_for_architecture") != "true":
        errors.append("contract_self_check.skill_shape_used_for_architecture must be true for non-clarification architect tasks")
    if (domain_required or route == "domain_discovery") and self_check_values.get("domain_substance_gates_applied") != "true":
        errors.append("contract_self_check.domain_substance_gates_applied must be true when domain gates matter")
    if patch_required and self_check_values.get("patch_hypothesis_present_when_needed") != "true":
        errors.append("contract_self_check.patch_hypothesis_present_when_needed must be true when patch is required")
    if self_check_values.get("full_package_overbuilt") != "false":
        errors.append("contract_self_check.full_package_overbuilt must be false")
    if route == "full_skill" and self_check_values.get("eval_artifact_present") != "true":
        errors.append("full_skill requires contract_self_check.eval_artifact_present=true")
    if route == "full_skill" and self_check_values.get("eval_schema_runner_compatible") != "true":
        errors.append("full_skill requires contract_self_check.eval_schema_runner_compatible=true")
    if patch_required and "rebuild_reason:" not in text and self_check_values.get("patch_not_rebuild") != "true":
        errors.append("improve mode requires contract_self_check.patch_not_rebuild=true unless rebuild_reason is present")

    if route == "full_skill":
        blocks = extract_file_blocks(text)
        e, w = validate_full_skill_artifacts(text, blocks, archetype, dominant_failures, domain_required)
        errors.extend(e)
        warnings.extend(w)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a captured dbx-skill-architect output contract and artifacts.")
    parser.add_argument("path", help="Captured output file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    errors, warnings = check_output(Path(args.path))
    payload = {"ok": not errors, "errors": errors, "warnings": warnings}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "OK" if not errors else "ERROR"
        print(f"Architect output check: {status}")
        for err in errors:
            print(f"ERROR: {err}")
        for warning in warnings:
            print(f"WARNING: {warning}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
