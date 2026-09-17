#!/usr/bin/env python3
"""Validate broad skill changes against current Git paths.

The manifest separates independently releasable change units. The validator
maps every current changed path to exactly one unit, derives affected skill
roots, verifies declared cross-skill/routing surfaces, and enforces the
publication gate without relying on prose in a review response.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

sys.dont_write_bytecode = True

SCHEMA_VERSION = 2
UNIT_KINDS = {"prototype", "known_bad_default_removal", "standard_change"}
NET_VALUES = {"positive", "uncertain", "negative"}
RELEASE_MODES = {"isolated_manual_prototype", "candidate", "stable"}
SURFACE_KEYS = {"cross_skill_protocol", "cross_skill_state", "execution_authority", "routing"}
RELEASE_FLAGS = {
    "changes_default_routing",
    "removes_existing_path",
    "registers_stable",
    "claims_improvement",
}
EVIDENCE_KINDS = {"before_after", "regression", "production_incident", "user_session", "benchmark", "other"}
OUTCOME_KINDS = {"before_after", "operational"}
VALIDATION_KEYS = {"baseline", "outcomes", "costs"}
CHECK_KEYS = {"argv", "expected_exit"}


def load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return None, [f"{path}: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path}: root must be an object"]
    return data, []


def git_output(repo_root: Path, *args: str) -> list[str]:
    process = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=False,
    )
    if process.returncode != 0:
        message = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return [item.decode("utf-8", errors="surrogateescape") for item in process.stdout.split(b"\0") if item]


def find_repo_root(start: Path) -> Path:
    process = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or f"{start} is not inside a Git repository")
    return Path(process.stdout.strip()).resolve()


def collect_changed_paths(repo_root: Path, scope: str) -> list[str]:
    if scope == "staged":
        paths = git_output(repo_root, "diff", "--cached", "--name-only", "--relative", "-z")
    else:
        paths = []
        paths.extend(git_output(repo_root, "diff", "--name-only", "--relative", "-z"))
        paths.extend(git_output(repo_root, "diff", "--cached", "--name-only", "--relative", "-z"))
        paths.extend(git_output(repo_root, "ls-files", "--others", "--exclude-standard", "-z"))
    return sorted({PurePosixPath(path).as_posix() for path in paths})


def pattern_matches(path: str, pattern: str) -> bool:
    normalized = PurePosixPath(pattern).as_posix()
    if normalized.endswith("/**"):
        prefix = normalized[:-3].rstrip("/")
        if not any(token in prefix for token in ("*", "?", "[")):
            return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch.fnmatchcase(path, normalized)


def changed_skill_roots(paths: list[str]) -> list[str]:
    roots: set[str] = set()
    for path in paths:
        parts = PurePosixPath(path).parts
        if len(parts) >= 2 and parts[0] == "skills":
            roots.add("/".join(parts[:2]))
    return sorted(roots)


def looks_like_routing_surface(path: str) -> bool:
    lowered = path.lower()
    name = PurePosixPath(path).name.lower()
    return (
        name == "openai.yaml"
        and "/agents/" in f"/{lowered}"
        or any(token in name for token in ("routing", "registry", "skill_index", "skill-index"))
        or any(part in {"routing", "registry"} for part in PurePosixPath(lowered).parts)
    )


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_repo_ref(value: Any, prefix: str, errors: list[str], repo_root: Path | None) -> str | None:
    if not non_empty_string(value):
        errors.append(f"{prefix} must be a non-empty repository-relative ref")
        return None
    ref = value.strip()
    base = ref.split("#", 1)[0]
    path = PurePosixPath(base)
    if (
        not base
        or path.is_absolute()
        or "\\" in base
        or ":" in path.parts[0]
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        errors.append(f"{prefix} must be a safe repository-relative path with an optional #anchor")
        return None
    if repo_root is not None:
        resolved_root = repo_root.resolve()
        resolved = (resolved_root / base).resolve()
        try:
            resolved.relative_to(resolved_root)
        except ValueError:
            errors.append(f"{prefix} resolves outside the repository: {ref!r}")
            return None
        if not resolved.is_file():
            errors.append(f"{prefix} does not resolve to an existing repository file: {ref!r}")
            return None
    return ref


def validate_check_command(
    value: Any,
    prefix: str,
    errors: list[str],
    *,
    repo_root: Path | None = None,
    require_zero: bool = False,
) -> bool:
    start = len(errors)
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object with argv and expected_exit")
        return False
    extra = set(value) - CHECK_KEYS
    missing = CHECK_KEYS - set(value)
    if extra:
        errors.append(f"{prefix} has unknown keys: {sorted(extra)}")
    if missing:
        errors.append(f"{prefix} is missing keys: {sorted(missing)}")
    argv = value.get("argv")
    if not isinstance(argv, list) or not argv or any(not non_empty_string(item) for item in argv):
        errors.append(f"{prefix}.argv must be a non-empty executable argv array")
    elif "/" in argv[0]:
        if repo_root is None:
            errors.append(f"{prefix}.argv[0] cannot be resolved without a repository root")
        else:
            executable = (repo_root.resolve() / argv[0]).resolve()
            if not executable.is_file() or not executable.stat().st_mode & 0o111:
                errors.append(f"{prefix}.argv[0] is not an executable repository file: {argv[0]!r}")
    elif shutil.which(argv[0]) is None:
        errors.append(f"{prefix}.argv[0] is not available on PATH: {argv[0]!r}")
    expected_exit = value.get("expected_exit")
    if isinstance(expected_exit, bool) or not isinstance(expected_exit, int) or not 0 <= expected_exit <= 255:
        errors.append(f"{prefix}.expected_exit must be an integer from 0 to 255")
    elif require_zero and expected_exit != 0:
        errors.append(f"{prefix}.expected_exit must be 0 for an executable rollback command")
    return len(errors) == start


def validate_release_validation(
    unit: dict[str, Any],
    prefix: str,
    errors: list[str],
    repo_root: Path | None,
) -> bool:
    start = len(errors)
    validation = unit.get("validation")
    if not isinstance(validation, dict):
        errors.append(f"{prefix}.validation must be an object with baseline, outcomes, and costs")
        return False
    extra = set(validation) - VALIDATION_KEYS
    missing = VALIDATION_KEYS - set(validation)
    if extra:
        errors.append(f"{prefix}.validation has unknown keys: {sorted(extra)}")
    if missing:
        errors.append(f"{prefix}.validation is missing keys: {sorted(missing)}")

    baseline = validation.get("baseline")
    baseline_ref: str | None = None
    if not isinstance(baseline, dict):
        errors.append(f"{prefix}.validation.baseline must be an object")
    else:
        baseline_keys = {"ref", "summary", "check"}
        extra_baseline = set(baseline) - baseline_keys
        missing_baseline = baseline_keys - set(baseline)
        if extra_baseline:
            errors.append(f"{prefix}.validation.baseline has unknown keys: {sorted(extra_baseline)}")
        if missing_baseline:
            errors.append(f"{prefix}.validation.baseline is missing keys: {sorted(missing_baseline)}")
        baseline_ref = validate_repo_ref(
            baseline.get("ref"), f"{prefix}.validation.baseline.ref", errors, repo_root
        )
        if not non_empty_string(baseline.get("summary")):
            errors.append(f"{prefix}.validation.baseline.summary must be a non-empty string")
        validate_check_command(
            baseline.get("check"),
            f"{prefix}.validation.baseline.check",
            errors,
            repo_root=repo_root,
        )

    outcomes = validation.get("outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        errors.append(f"{prefix}.validation.outcomes must contain before_after or operational proof")
    else:
        for index, outcome in enumerate(outcomes):
            outcome_prefix = f"{prefix}.validation.outcomes[{index}]"
            if not isinstance(outcome, dict):
                errors.append(f"{outcome_prefix} must be an object")
                continue
            outcome_keys = {"kind", "ref", "summary", "baseline_ref", "candidate_ref", "check"}
            extra_outcome = set(outcome) - outcome_keys
            missing_outcome = outcome_keys - set(outcome)
            if extra_outcome:
                errors.append(f"{outcome_prefix} has unknown keys: {sorted(extra_outcome)}")
            if missing_outcome:
                errors.append(f"{outcome_prefix} is missing keys: {sorted(missing_outcome)}")
            kind = outcome.get("kind")
            if kind not in OUTCOME_KINDS:
                errors.append(f"{outcome_prefix}.kind must be one of {sorted(OUTCOME_KINDS)}")
            outcome_ref = validate_repo_ref(outcome.get("ref"), f"{outcome_prefix}.ref", errors, repo_root)
            if not non_empty_string(outcome.get("summary")):
                errors.append(f"{outcome_prefix}.summary must be a non-empty string")
            validate_check_command(
                outcome.get("check"),
                f"{outcome_prefix}.check",
                errors,
                repo_root=repo_root,
            )
            if kind == "before_after":
                declared_baseline = validate_repo_ref(
                    outcome.get("baseline_ref"), f"{outcome_prefix}.baseline_ref", errors, repo_root
                )
                candidate_ref = validate_repo_ref(
                    outcome.get("candidate_ref"), f"{outcome_prefix}.candidate_ref", errors, repo_root
                )
                if baseline_ref and declared_baseline and declared_baseline != baseline_ref:
                    errors.append(f"{outcome_prefix}.baseline_ref must equal validation.baseline.ref")
                if candidate_ref and declared_baseline and candidate_ref == declared_baseline:
                    errors.append(f"{outcome_prefix}.candidate_ref must differ from baseline_ref")
                if outcome_ref and candidate_ref and outcome_ref != candidate_ref:
                    errors.append(f"{outcome_prefix}.ref must equal candidate_ref for before_after proof")
            elif kind == "operational":
                if outcome.get("baseline_ref") is not None or outcome.get("candidate_ref") is not None:
                    errors.append(f"{outcome_prefix}: operational proof must use null baseline_ref/candidate_ref")

    costs = validation.get("costs")
    if not isinstance(costs, list) or not costs:
        errors.append(f"{prefix}.validation.costs must contain at least one measured cost")
    else:
        for index, cost in enumerate(costs):
            cost_prefix = f"{prefix}.validation.costs[{index}]"
            if not isinstance(cost, dict):
                errors.append(f"{cost_prefix} must be an object")
                continue
            cost_keys = {"metric", "value", "unit", "ref", "check"}
            extra_cost = set(cost) - cost_keys
            missing_cost = cost_keys - set(cost)
            if extra_cost:
                errors.append(f"{cost_prefix} has unknown keys: {sorted(extra_cost)}")
            if missing_cost:
                errors.append(f"{cost_prefix} is missing keys: {sorted(missing_cost)}")
            for field in ("metric", "unit"):
                if not non_empty_string(cost.get(field)):
                    errors.append(f"{cost_prefix}.{field} must be a non-empty string")
            value = cost.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                errors.append(f"{cost_prefix}.value must be a non-negative number")
            validate_repo_ref(cost.get("ref"), f"{cost_prefix}.ref", errors, repo_root)
            validate_check_command(
                cost.get("check"),
                f"{cost_prefix}.check",
                errors,
                repo_root=repo_root,
            )
    return len(errors) == start


def validate_surface_map(
    unit: dict[str, Any],
    unit_prefix: str,
    unit_paths: list[str],
    errors: list[str],
) -> dict[str, list[str]]:
    surfaces = unit.get("surfaces")
    if not isinstance(surfaces, dict):
        errors.append(f"{unit_prefix}.surfaces must be an object")
        return {key: [] for key in SURFACE_KEYS}
    extra = set(surfaces) - SURFACE_KEYS
    missing = SURFACE_KEYS - set(surfaces)
    if extra:
        errors.append(f"{unit_prefix}.surfaces has unknown keys: {sorted(extra)}")
    if missing:
        errors.append(f"{unit_prefix}.surfaces is missing keys: {sorted(missing)}")

    normalized: dict[str, list[str]] = {}
    for key in sorted(SURFACE_KEYS):
        values = surfaces.get(key, [])
        if not isinstance(values, list) or any(not non_empty_string(item) for item in values):
            errors.append(f"{unit_prefix}.surfaces.{key} must be an array of non-empty changed paths")
            normalized[key] = []
            continue
        normalized[key] = sorted(set(values))
        for path in normalized[key]:
            if path not in unit_paths:
                errors.append(f"{unit_prefix}.surfaces.{key}: {path!r} is not owned by this unit")

    auto_routing = {path for path in unit_paths if looks_like_routing_surface(path)}
    undeclared = auto_routing - set(normalized.get("routing", []))
    if undeclared:
        errors.append(f"{unit_prefix}.surfaces.routing omits detected routing paths: {sorted(undeclared)}")
    return normalized


def validate_evidence(
    unit: dict[str, Any],
    prefix: str,
    errors: list[str],
    repo_root: Path | None,
) -> list[dict[str, Any]]:
    evidence = unit.get("evidence")
    if not isinstance(evidence, list):
        errors.append(f"{prefix}.evidence must be an array")
        return []
    valid: list[dict[str, Any]] = []
    for index, item in enumerate(evidence):
        item_prefix = f"{prefix}.evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_prefix} must be an object")
            continue
        if item.get("kind") not in EVIDENCE_KINDS:
            errors.append(f"{item_prefix}.kind must be one of {sorted(EVIDENCE_KINDS)}")
        validate_repo_ref(item.get("ref"), f"{item_prefix}.ref", errors, repo_root)
        if not non_empty_string(item.get("summary")):
            errors.append(f"{item_prefix}.summary must be a non-empty string")
        valid.append(item)
    return valid


def validate_rollback(
    unit: dict[str, Any],
    prefix: str,
    errors: list[str],
    repo_root: Path | None,
) -> tuple[bool, bool]:
    rollback = unit.get("rollback")
    if not isinstance(rollback, dict):
        errors.append(f"{prefix}.rollback must be an object")
        return False, False
    extra = set(rollback) - {"trigger", "steps", "commands"}
    if extra:
        errors.append(f"{prefix}.rollback has unknown keys: {sorted(extra)}")
    trigger = rollback.get("trigger")
    steps = rollback.get("steps")
    if not non_empty_string(trigger):
        errors.append(f"{prefix}.rollback.trigger must be a non-empty string")
    if not isinstance(steps, list) or not steps or any(not non_empty_string(step) for step in steps):
        errors.append(f"{prefix}.rollback.steps must contain at least one non-empty step")
    commands = rollback.get("commands")
    executable = isinstance(commands, list) and bool(commands)
    if commands is not None:
        if not isinstance(commands, list) or not commands:
            errors.append(f"{prefix}.rollback.commands must contain at least one executable argv command")
            executable = False
        else:
            for index, command in enumerate(commands):
                if not validate_check_command(
                    command,
                    f"{prefix}.rollback.commands[{index}]",
                    errors,
                    repo_root=repo_root,
                    require_zero=True,
                ):
                    executable = False
    narrative = (
        non_empty_string(trigger)
        and isinstance(steps, list)
        and bool(steps)
        and all(non_empty_string(step) for step in steps)
    )
    return narrative, executable


def validate_manifest(
    data: dict[str, Any],
    changed_paths: list[str],
    repo_root: Path,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    units = data.get("change_units")
    if not isinstance(units, list) or not units:
        return {"ok": False, "errors": errors + ["change_units must be a non-empty array"], "warnings": warnings}
    if not changed_paths:
        errors.append("current Git scope has no changed paths")

    publication_skill_roots = changed_skill_roots(changed_paths)
    publication_semantic_cross_skill = any(
        isinstance(unit, dict)
        and isinstance(unit.get("surfaces"), dict)
        and any(
            unit["surfaces"].get(key)
            for key in ("cross_skill_protocol", "cross_skill_state", "execution_authority")
        )
        for unit in units
    )
    publication_broad = len(publication_skill_roots) >= 3 or publication_semantic_cross_skill

    ids: set[str] = set()
    unit_by_id: dict[str, dict[str, Any]] = {}
    path_owners: dict[str, list[str]] = {path: [] for path in changed_paths}
    unit_paths_by_id: dict[str, list[str]] = {}

    for index, unit in enumerate(units):
        prefix = f"change_units[{index}]"
        if not isinstance(unit, dict):
            errors.append(f"{prefix} must be an object")
            continue
        unit_id = unit.get("id")
        if not non_empty_string(unit_id):
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        if unit_id in ids:
            errors.append(f"{prefix}.id duplicates {unit_id!r}")
            continue
        ids.add(unit_id)
        unit_by_id[unit_id] = unit

        patterns = unit.get("path_patterns")
        if not isinstance(patterns, list) or not patterns or any(not non_empty_string(item) for item in patterns):
            errors.append(f"{prefix}.path_patterns must contain at least one non-empty pattern")
            patterns = []
        matched = sorted(path for path in changed_paths if any(pattern_matches(path, pattern) for pattern in patterns))
        unit_paths_by_id[unit_id] = matched
        if not matched:
            errors.append(f"{prefix}.path_patterns match no current changed paths")
        for path in matched:
            path_owners[path].append(unit_id)

    for path, owners in path_owners.items():
        if not owners:
            errors.append(f"changed path is not assigned to a change unit: {path}")
        elif len(owners) > 1:
            errors.append(f"changed path is assigned to multiple change units {owners}: {path}")

    reports: list[dict[str, Any]] = []
    for index, unit in enumerate(units):
        if not isinstance(unit, dict) or not non_empty_string(unit.get("id")):
            continue
        unit_id = unit["id"]
        prefix = f"change_units[{index}]({unit_id})"
        unit_paths = unit_paths_by_id.get(unit_id, [])
        skill_roots = changed_skill_roots(unit_paths)
        surfaces = validate_surface_map(unit, prefix, unit_paths, errors)
        kind = unit.get("kind")
        net_value = unit.get("net_value")
        if kind not in UNIT_KINDS:
            errors.append(f"{prefix}.kind must be one of {sorted(UNIT_KINDS)}")
        if net_value not in NET_VALUES:
            errors.append(f"{prefix}.net_value must be one of {sorted(NET_VALUES)}")

        release = unit.get("release")
        if not isinstance(release, dict):
            errors.append(f"{prefix}.release must be an object")
            release = {}
        mode = release.get("mode")
        if mode not in RELEASE_MODES:
            errors.append(f"{prefix}.release.mode must be one of {sorted(RELEASE_MODES)}")
        for flag in sorted(RELEASE_FLAGS):
            if not isinstance(release.get(flag), bool):
                errors.append(f"{prefix}.release.{flag} must be true or false")

        evidence = validate_evidence(unit, prefix, errors, repo_root)
        rollback_ready, executable_rollback = validate_rollback(unit, prefix, errors, repo_root)
        semantic_cross_skill = any(surfaces.get(key) for key in (
            "cross_skill_protocol",
            "cross_skill_state",
            "execution_authority",
        ))
        unit_broad = len(skill_roots) >= 3 or semantic_cross_skill
        broad = publication_broad or unit_broad

        if kind == "prototype" and mode != "isolated_manual_prototype":
            errors.append(f"{prefix}: prototype kind must use release.mode=isolated_manual_prototype")
        if mode == "isolated_manual_prototype":
            for field in ("manual_entry_point", "removal_without_migration"):
                if not non_empty_string(release.get(field)):
                    errors.append(f"{prefix}.release.{field} is required for an isolated prototype")
            enabled_flags = sorted(flag for flag in RELEASE_FLAGS if release.get(flag) is True)
            if enabled_flags:
                errors.append(f"{prefix}: isolated_manual_prototype cannot enable release flags: {enabled_flags}")

        if release.get("changes_default_routing") and not surfaces.get("routing"):
            errors.append(f"{prefix}: changes_default_routing=true requires at least one declared routing surface")

        if broad and net_value in {"uncertain", "negative"}:
            if mode != "isolated_manual_prototype":
                errors.append(f"{prefix}: broad {net_value} unit must remain isolated_manual_prototype")

        if mode == "stable" and net_value != "positive":
            errors.append(f"{prefix}: stable registration requires net_value=positive")
        if release.get("registers_stable") and mode != "stable":
            errors.append(f"{prefix}: registers_stable=true requires release.mode=stable")
        if release.get("claims_improvement") and net_value != "positive":
            errors.append(f"{prefix}: an improvement claim requires net_value=positive")
        positive_release_requires_proof = (
            (broad and net_value == "positive")
            or mode == "stable"
            or release.get("claims_improvement") is True
        )
        if positive_release_requires_proof:
            if not evidence:
                errors.append(f"{prefix}: positive publication requires non-empty before/after or operational evidence")
            if not validate_release_validation(unit, prefix, errors, repo_root):
                errors.append(
                    f"{prefix}: positive publication requires a machine-checkable baseline, "
                    "before/after or operational proof, and measured costs"
                )
            if not rollback_ready or not executable_rollback:
                errors.append(f"{prefix}: positive publication requires executable rollback.commands argv")

        if release.get("removes_existing_path") and kind != "known_bad_default_removal":
            errors.append(f"{prefix}: removing an existing path requires kind=known_bad_default_removal")
        if kind == "known_bad_default_removal":
            if net_value != "positive":
                errors.append(f"{prefix}: known_bad_default_removal must be an independent positive unit")
            if not release.get("removes_existing_path"):
                errors.append(f"{prefix}: known_bad_default_removal must set removes_existing_path=true")
            if not release.get("changes_default_routing"):
                errors.append(f"{prefix}: known_bad_default_removal must set changes_default_routing=true")
            if not evidence:
                errors.append(f"{prefix}: known_bad_default_removal requires evidence")
            if not rollback_ready:
                errors.append(f"{prefix}: known_bad_default_removal requires rollback steps")

        reports.append(
            {
                "id": unit_id,
                "kind": kind,
                "net_value": net_value,
                "changed_paths": unit_paths,
                "affected_skill_roots": skill_roots,
                "surface_counts": {key: len(surfaces.get(key, [])) for key in sorted(SURFACE_KEYS)},
                "broad": broad,
                "unit_broad": unit_broad,
                "release_mode": mode,
            }
        )

    for index, unit in enumerate(units):
        if not isinstance(unit, dict) or not isinstance(unit.get("release"), dict):
            continue
        replacement_id = unit["release"].get("replacement_unit_id")
        if replacement_id is None:
            continue
        prefix = f"change_units[{index}]({unit.get('id', '?')}).release.replacement_unit_id"
        replacement = unit_by_id.get(replacement_id)
        if replacement is None:
            errors.append(f"{prefix} references unknown unit {replacement_id!r}")
            continue
        replacement_release = replacement.get("release", {})
        if replacement.get("net_value") != "positive" or replacement_release.get("mode") == "isolated_manual_prototype":
            errors.append(f"{prefix} cannot use an uncertain, negative, or isolated prototype as the replacement")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "changed_paths": changed_paths,
        "affected_skill_roots": publication_skill_roots,
        "publication_broad": publication_broad,
        "unit_reports": reports,
    }


def print_text(result: dict[str, Any], scope: str) -> None:
    print(f"Change manifest: {'OK' if result.get('ok') else 'ERROR'} scope={scope}")
    print(
        f"Changed paths: {len(result.get('changed_paths', []))}; "
        f"affected skill roots: {len(result.get('affected_skill_roots', []))}"
    )
    for report in result.get("unit_reports", []):
        print(
            f"[{report['id']}] broad={str(report['broad']).lower()} "
            f"skills={len(report['affected_skill_roots'])} surfaces={report['surface_counts']} "
            f"net_value={report['net_value']} release={report['release_mode']}"
        )
    for error in result.get("errors", []):
        print(f"ERROR: {error}")
    for warning in result.get("warnings", []):
        print(f"WARNING: {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a skill change manifest against current Git paths.")
    parser.add_argument("manifest", help="Path to the declarative change manifest JSON")
    parser.add_argument("--repo-root", help="Git repository root; discovered from the current directory by default")
    parser.add_argument("--scope", choices=["working-tree", "staged"], default="working-tree")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    data, load_errors = load_manifest(manifest_path)
    if load_errors or data is None:
        result = {"ok": False, "errors": load_errors, "warnings": []}
    else:
        try:
            repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else find_repo_root(Path.cwd())
            changed_paths = collect_changed_paths(repo_root, args.scope)
            result = validate_manifest(data, changed_paths, repo_root)
            result["repo_root"] = str(repo_root)
            result["scope"] = args.scope
        except RuntimeError as exc:
            result = {"ok": False, "errors": [str(exc)], "warnings": []}

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result, args.scope)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
