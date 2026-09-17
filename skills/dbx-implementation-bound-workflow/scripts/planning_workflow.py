#!/usr/bin/env python3
"""Deterministic, manual-only draft-to-first-code controller."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import time
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

import fcntl

sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from git_evidence import (  # noqa: E402
    EvidenceError,
    calculate_delta,
    capture_snapshot,
    resolve_repo,
    validate_implementation_delta,
    validate_snapshot,
)

STATE_VERSION = 6
PLANNER = "dbx-technical-plan"
REVIEWER = "dbx-linus-review"
REVIEW_CAPABILITY = "strict_pragmatic_plan_review"
REVIEW_DIMENSIONS = [
    "problem_and_proportionality",
    "data_model_and_ownership",
    "compatibility_and_user_breakage",
    "first_executable_slice_readiness",
    "validation_rollout_and_rollback",
]
REVIEW_NON_GOALS = [
    "workflow_transition",
    "implementation_authority",
    "artifact_or_code_modification",
]
VALIDATION_TIMEOUT_SECONDS = 300
VALIDATION_OUTPUT_LIMIT_BYTES = 1024 * 1024
SHA_PREFIX = "sha256:"
PHASES = {
    "draft",
    "initial_review",
    "correction_cycle",
    "final_review",
    "implementation",
    "host_validation",
    "needs_host_validation",
    "blocked",
}
OPERATIONS = PHASES - {"needs_host_validation", "blocked"}
ACTIVE_OPERATIONS = OPERATIONS - {"host_validation"}
ACCEPTED = {"accept", "accept_with_advisories"}
JUDGMENTS = ACCEPTED | {"changes_required", "reject", "insufficient_evidence"}
STATE_KEYS = {
    "state_version",
    "run_id",
    "start_signature",
    "origin",
    "phase",
    "artifact",
    "first_slice",
    "review_request",
    "accepted_review",
    "correction",
    "active_operation",
    "authority",
    "workspace_baseline",
    "pre_validation_snapshot",
    "validation_request",
    "applied_events",
    "block",
}


class WorkflowError(RuntimeError):
    """Invalid workflow input, evidence, or transition."""


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _fingerprint(value: Any) -> str:
    return SHA_PREFIX + hashlib.sha256(_canonical(value)).hexdigest()


def _valid_sha(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith(SHA_PREFIX)
        and all(character in "0123456789abcdef" for character in value[7:])
    )


def _hash_file(path: Path) -> str:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError(f"required file does not exist: {path}") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise WorkflowError(f"required path must be a regular file, not a symlink: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return SHA_PREFIX + digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"cannot read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise WorkflowError(f"JSON root must be an object: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def _normalize_path(value: str) -> str:
    candidate = PurePosixPath(value.replace("\\", "/"))
    if not value or candidate.is_absolute() or ".." in candidate.parts:
        raise WorkflowError(f"scope path must be repository-relative: {value!r}")
    return candidate.as_posix().rstrip("/") or "."


def _within(relative: str, containers: Sequence[str]) -> bool:
    relative = _normalize_path(relative)
    return any(
        allowed == "." or relative == allowed or relative.startswith(allowed + "/")
        for allowed in map(_normalize_path, containers)
    )


def _inside(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def _review_request_id(binding: dict[str, Any]) -> str:
    return "review-" + hashlib.sha256(_canonical(binding)).hexdigest()


def _make_review_request(state: dict[str, Any], purpose: str) -> dict[str, Any]:
    if purpose not in {"initial", "final_acceptance"}:
        raise WorkflowError(f"unsupported review purpose: {purpose}")
    artifact = state["artifact"]
    if not _valid_sha(artifact.get("sha256")):
        raise WorkflowError("cannot bind a review request before the plan is frozen")
    envelope = {
        "parent_controller": "dbx-implementation-bound-workflow",
        "originating_intent": state["origin"]["goal"],
        "completion_profile": "strict_acceptance",
        "reviewer_provider_id": REVIEWER,
        "reviewer_capability": REVIEW_CAPABILITY,
        "reviewer_independence": "independent",
        "artifact": {
            "type": artifact["type"],
            "version": artifact["version"],
            "fingerprint_scheme": "exact-bytes-sha256",
            "fingerprint": artifact["sha256"],
            "content_ref": {
                "kind": "path",
                "value": artifact["path"],
                "plan": None,
                "tasks": None,
            },
        },
        "review_scope": {
            "kind": "full",
            "contract_id": None,
            "accepted_finding_ids": [],
            "check_direct_regressions": purpose == "final_acceptance",
            "check_anchor_drift": purpose == "final_acceptance",
            "check_evidence_boundary": True,
            "check_scope_and_bloat": True,
        },
        "requested_dimensions": list(REVIEW_DIMENSIONS),
        "evidence_boundary": {
            "kind": "run_owned_plan_only",
            "artifact_fingerprint": artifact["sha256"],
            "authority_source_ref": state["authority"]["source_ref"],
            "authority_paths": list(state["authority"]["paths"]),
        },
        "non_goals": list(REVIEW_NON_GOALS),
        "write_prohibition": {
            "modify_artifact": False,
            "modify_code": False,
            "commit": False,
            "push": False,
        },
    }
    binding = {"run_id": state["run_id"], "purpose": purpose, "delegated_review": envelope}
    envelope = {**envelope, "review_id": _review_request_id(binding)}
    return {"purpose": purpose, "delegated_review": envelope}


def _validate_review_request(state: dict[str, Any], request: Any) -> None:
    if not isinstance(request, dict):
        raise WorkflowError("fixed delegated review request is missing")
    purpose = request.get("purpose")
    if purpose not in {"initial", "final_acceptance"} or request != _make_review_request(
        state, purpose
    ):
        raise WorkflowError("fixed delegated review request/context changed")


def _make_validation_request(state: dict[str, Any], operation_id: str) -> dict[str, Any]:
    review = state.get("accepted_review")
    review_request = state.get("review_request")
    pre_validation = state.get("pre_validation_snapshot")
    if (
        not isinstance(review, dict)
        or not isinstance(review_request, dict)
        or not isinstance(pre_validation, dict)
    ):
        raise WorkflowError("cannot bind validation before a fixed accepted review")
    argv = list(state["first_slice"]["validation_argv"])
    request = {
        "schema_version": 1,
        "producer": "dbx-implementation-bound-workflow",
        "run_id": state["run_id"],
        "operation_id": operation_id,
        "repo_root": state["workspace_baseline"]["repo_root"],
        "cwd": state["workspace_baseline"]["repo_root"],
        "workspace_baseline_fingerprint": state["workspace_baseline"]["fingerprint"],
        "pre_validation_snapshot_fingerprint": pre_validation["fingerprint"],
        "artifact_sha256": state["artifact"]["sha256"],
        "artifact_version": state["artifact"]["version"],
        "review_id": review["review_id"],
        "review_request_id": review_request["delegated_review"]["review_id"],
        "first_slice_id": state["first_slice"]["id"],
        "target_paths": list(state["first_slice"]["target_paths"]),
        "authority_paths": list(state["authority"]["paths"]),
        "validation_argv": argv,
        "command_sha256": _fingerprint(argv),
        "timeout_seconds": VALIDATION_TIMEOUT_SECONDS,
        "output_limit_bytes": VALIDATION_OUTPUT_LIMIT_BYTES,
        "external_side_effect_policy": "forbidden_without_separate_host_approval",
    }
    return {**request, "request_fingerprint": _fingerprint(request)}


def _validate_validation_request(state: dict[str, Any], request: Any) -> None:
    if not isinstance(request, dict) or not isinstance(request.get("operation_id"), str):
        raise WorkflowError("host validation request is invalid")
    if request != _make_validation_request(state, request["operation_id"]):
        raise WorkflowError("host validation request binding changed")


def _private_dir(path: Path, *, create: bool = False) -> None:
    if create:
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError(f"runtime directory does not exist: {path}") from exc
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or stat.S_IMODE(metadata.st_mode) & 0o077
    ):
        raise WorkflowError(f"runtime directory must be owner-only, owned, and not a symlink: {path}")


def _private_file(path: Path) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError(f"runtime file does not exist: {path}") from exc
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or stat.S_IMODE(metadata.st_mode) & 0o077
    ):
        raise WorkflowError(f"runtime file must be owner-only, owned, and not a symlink: {path}")


def _origin_token(origin_ref: str) -> str:
    return hashlib.sha256(origin_ref.encode()).hexdigest()[:32]


def _start_paths(args: argparse.Namespace, repo: Path, *, create: bool) -> tuple[Path, Path, Path]:
    if not args.origin_ref:
        raise WorkflowError("start requires non-empty --origin-ref")
    runtime = Path(args.runtime_dir).resolve()
    if _inside(runtime, repo):
        raise WorkflowError("trusted runtime directory must be outside the Git worktree")
    _private_dir(runtime, create=create)
    token = _origin_token(args.origin_ref)
    return runtime, runtime / f"{token}.state.json", runtime / f"{token}.plan.md"


@contextmanager
def _lock(state_path: Path):
    state_path = state_path.resolve()
    _private_dir(state_path.parent)
    with state_path.with_name(state_path.name + ".lock").open("a+") as handle:
        os.chmod(handle.name, 0o600)
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _validate_state(state: dict[str, Any], state_path: Path | None = None) -> None:
    if set(state) != STATE_KEYS or state.get("state_version") != STATE_VERSION:
        raise WorkflowError("workflow state shape/version is invalid")
    if not _valid_sha(state.get("start_signature")) or state.get("phase") not in PHASES:
        raise WorkflowError("workflow state identity/phase is invalid")
    origin = state.get("origin")
    if not isinstance(origin, dict) or set(origin) != {"ref", "goal"} or not all(
        isinstance(value, str) and value for value in origin.values()
    ):
        raise WorkflowError("workflow origin_ref/goal is invalid")
    if state.get("run_id") != f"run-{_origin_token(origin['ref'])}":
        raise WorkflowError("workflow run_id does not match its origin registry key")
    artifact = state.get("artifact")
    if not isinstance(artifact, dict) or set(artifact) != {"path", "type", "version", "sha256"}:
        raise WorkflowError("workflow artifact identity is invalid")
    if artifact["sha256"] is not None and not _valid_sha(artifact["sha256"]):
        raise WorkflowError("workflow artifact fingerprint is invalid")
    if state["phase"] not in {"draft", "blocked"} and not _valid_sha(artifact["sha256"]):
        raise WorkflowError("post-draft state has no plan fingerprint")
    authority = state.get("authority")
    if not isinstance(authority, dict) or set(authority) != {"source_ref", "paths"}:
        raise WorkflowError("workflow authority is invalid")
    if not authority["source_ref"] or not isinstance(authority["paths"], list) or not authority["paths"]:
        raise WorkflowError("workflow requires start-time authorized explicit paths")
    paths = list(map(_normalize_path, authority["paths"]))
    if len(paths) != len(set(paths)):
        raise WorkflowError("authority paths must be unique")
    first = state.get("first_slice")
    if _valid_sha(artifact["sha256"]):
        if not isinstance(first, dict) or set(first) != {
            "id", "summary", "target_paths", "validation_argv"
        }:
            raise WorkflowError("post-draft state has no first_slice contract")
        if not isinstance(first["target_paths"], list) or not first["target_paths"] or not all(
            isinstance(value, str) and _within(value, paths) for value in first["target_paths"]
        ):
            raise WorkflowError("first_slice target paths are invalid")
        if not isinstance(first["validation_argv"], list) or not first["validation_argv"] or not all(
            isinstance(value, str) and value for value in first["validation_argv"]
        ):
            raise WorkflowError("first_slice validation argv is invalid")
        _validate_review_request(state, state.get("review_request"))
    elif first is not None or state.get("review_request") is not None:
        raise WorkflowError("draft state cannot carry a first_slice or review request")
    correction = state.get("correction")
    expected = {
        "limit",
        "used",
        "required_finding_ids",
        "closed_finding_ids",
        "frozen_contract",
    }
    if not isinstance(correction, dict) or set(correction) != expected:
        raise WorkflowError("correction contract is invalid")
    if not all(isinstance(correction[key], int) for key in ("limit", "used")):
        raise WorkflowError("correction counters are invalid")
    if not 0 <= correction["used"] <= correction["limit"] <= 1:
        raise WorkflowError("correction budget is invalid")
    for key in ("required_finding_ids", "closed_finding_ids"):
        values = correction[key]
        if not isinstance(values, list) or len(values) != len(set(values)) or not all(
            isinstance(value, str) and value for value in values
        ):
            raise WorkflowError(f"correction {key} is invalid")
    frozen = correction["frozen_contract"]
    if correction["required_finding_ids"]:
        if (
            not isinstance(frozen, dict)
            or set(frozen) != {"artifact_type", "first_slice"}
            or frozen["artifact_type"] != artifact["type"]
            or frozen["first_slice"] != first
        ):
            raise WorkflowError("frozen correction contract changed")
    elif frozen is not None or correction["closed_finding_ids"]:
        raise WorkflowError("correction closure exists without a frozen finding contract")
    active = state.get("active_operation")
    if active is not None and (
        not isinstance(active, dict)
        or active.get("kind") not in ACTIVE_OPERATIONS
        or active.get("kind") != state["phase"]
        or not active.get("id")
    ):
        raise WorkflowError("active operation is invalid")
    try:
        validate_snapshot(state["workspace_baseline"])
    except EvidenceError as exc:
        raise WorkflowError(str(exc)) from exc
    pre_validation = state.get("pre_validation_snapshot")
    if pre_validation is not None:
        try:
            validate_snapshot(pre_validation)
        except EvidenceError as exc:
            raise WorkflowError(str(exc)) from exc
        if pre_validation["repo_root"] != state["workspace_baseline"]["repo_root"]:
            raise WorkflowError("pre-validation snapshot refers to another repository")
    expected_signature = _fingerprint(
        {
            "repo": state["workspace_baseline"]["repo_root"],
            "origin_ref": origin["ref"],
            "goal": origin["goal"],
            "correction_limit": correction["limit"],
            "authority_source_ref": authority["source_ref"],
            "authority_paths": authority["paths"],
        }
    )
    if state["start_signature"] != expected_signature:
        raise WorkflowError("workflow start contract changed after registration")
    validation_request = state.get("validation_request")
    if validation_request is not None:
        _validate_validation_request(state, validation_request)
    if (pre_validation is None) != (validation_request is None):
        raise WorkflowError("host validation snapshot/request must be persisted together")
    if state["phase"] == "needs_host_validation" and validation_request is None:
        raise WorkflowError("needs_host_validation requires a frozen host request")
    if validation_request is not None and state["phase"] != "needs_host_validation":
        raise WorkflowError("host validation request exists outside its terminal handoff")
    if state["phase"] == "blocked" and not isinstance(state["block"], dict):
        raise WorkflowError("blocked state requires block evidence")
    if not isinstance(state.get("applied_events"), dict):
        raise WorkflowError("applied_events is invalid")
    if state_path is not None:
        repo = Path(state["workspace_baseline"]["repo_root"])
        runtime = state_path.resolve().parent
        artifact_path = Path(artifact["path"]).resolve()
        token = _origin_token(origin["ref"])
        if _inside(runtime, repo) or state_path.resolve() != runtime / f"{token}.state.json":
            raise WorkflowError("state escaped its outside-worktree origin registry")
        if artifact_path != runtime / f"{token}.plan.md":
            raise WorkflowError("plan escaped its origin registry")
        _private_dir(runtime)
        _private_file(state_path)
        mutable = isinstance(active, dict) and active.get("kind") in {"draft", "correction_cycle"}
        if artifact_path.exists() and not mutable:
            _private_file(artifact_path)


def _load_state(path: Path) -> dict[str, Any]:
    path = path.resolve()
    state = _read_json(path)
    _validate_state(state, path)
    return state


def _artifact_current(state: dict[str, Any]) -> str:
    expected = state["artifact"]["sha256"]
    current = _hash_file(Path(state["artifact"]["path"]))
    if current != expected:
        raise WorkflowError(f"plan changed outside its active operation: expected {expected}, got {current}")
    return current


def _review_current(state: dict[str, Any]) -> bool:
    review = state.get("accepted_review")
    request = state.get("review_request")
    return (
        isinstance(review, dict)
        and isinstance(request, dict)
        and isinstance(request.get("delegated_review"), dict)
        and review.get("review_id") == request["delegated_review"].get("review_id")
        and review.get("review_request_id") == request["delegated_review"].get("review_id")
        and review.get("artifact_sha256") == state["artifact"]["sha256"]
        and review.get("artifact_version") == state["artifact"]["version"]
        and review.get("provider_id") == REVIEWER
        and review.get("reviewer_capability") == REVIEW_CAPABILITY
        and review.get("scope") == "full"
        and review.get("judgment") in ACCEPTED
    )


def _remember(state: dict[str, Any], event_id: str, digest: str, result: dict[str, Any]) -> None:
    state["applied_events"][event_id] = {
        "payload_sha256": digest,
        "result": result,
        "recorded_ns": time.time_ns(),
    }


def _replay(state: dict[str, Any], event_id: str, digest: str) -> dict[str, Any] | None:
    previous = state["applied_events"].get(event_id)
    if previous is None:
        return None
    if previous.get("payload_sha256") != digest:
        raise WorkflowError(f"event_id {event_id!r} already has a different payload")
    return {
        "ok": True,
        "idempotent_replay": True,
        "event_id": event_id,
        "recorded_result": previous["result"],
        "state": state,
    }


def _next(state: dict[str, Any]) -> dict[str, Any]:
    if state["phase"] in {"needs_host_validation", "blocked"}:
        terminal = {
            "is_terminal": True,
            "outcome": state["phase"],
            "block": state["block"],
        }
        result = {
            "run_id": state["run_id"],
            "phase": state["phase"],
            "action": "stop",
            "terminal": terminal,
        }
        if state["phase"] == "needs_host_validation":
            terminal.update(
                {
                    "first_slice_present": True,
                    "validation_status": "not_run_by_controller",
                    "implementation_completion_claim": False,
                }
            )
            result["host_validation_request"] = state["validation_request"]
        return result
    if state["active_operation"]:
        result = {
            "run_id": state["run_id"],
            "phase": state["phase"],
            "action": "record",
            "operation": state["active_operation"]["kind"],
            "operation_id": state["active_operation"]["id"],
        }
        if state["active_operation"]["kind"] in {"initial_review", "final_review"}:
            result["delegated_review"] = state["review_request"]["delegated_review"]
        if state["active_operation"]["kind"] == "host_validation":
            result["host_validation_request"] = state["validation_request"]
        return result
    if state["phase"] != "draft":
        _artifact_current(state)
    result = {
        "run_id": state["run_id"],
        "phase": state["phase"],
        "action": "begin",
        "operation": state["phase"],
    }
    if state["phase"] == "correction_cycle":
        result["required_finding_ids"] = state["correction"]["required_finding_ids"]
        result["frozen_contract"] = state["correction"]["frozen_contract"]
    if state["phase"] in {"initial_review", "final_review"}:
        result["delegated_review"] = state["review_request"]["delegated_review"]
    return result


def _response(state: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {"ok": True, **extra, "next": _next(state), "state": state}


def _block(state: dict[str, Any], code: str, note: str, operation: str, **details: Any) -> None:
    state["phase"] = "blocked"
    state["active_operation"] = None
    state["block"] = {
        "code": code,
        "note": note or code,
        "operation": operation,
        "details": details,
        "recorded_ns": time.time_ns(),
    }


def _start_signature(args: argparse.Namespace, repo: Path, paths: list[str]) -> str:
    return _fingerprint(
        {
            "repo": str(repo),
            "origin_ref": args.origin_ref,
            "goal": args.goal,
            "correction_limit": args.correction_limit,
            "authority_source_ref": args.authority_source_ref,
            "authority_paths": paths,
        }
    )


def start_workflow(args: argparse.Namespace) -> dict[str, Any]:
    repo = resolve_repo(Path(args.workspace))
    runtime, state_path, artifact_path = _start_paths(args, repo, create=True)
    if not args.goal or not args.authority_source_ref:
        raise WorkflowError("start requires a goal and trusted authority source ref")
    paths = sorted({_normalize_path(path) for path in args.authority_path})
    if not paths:
        raise WorkflowError("start requires authorized explicit --authority-path values")
    signature = _start_signature(args, repo, paths)
    if state_path.exists():
        existing = _load_state(state_path)
        if existing["start_signature"] != signature:
            raise WorkflowError("origin_ref already has conflicting start input in this runtime registry")
        return _response(
            existing,
            created=False,
            idempotent_start=True,
            state_path=str(state_path),
            artifact_path=str(artifact_path),
        )
    if os.path.lexists(artifact_path):
        raise WorkflowError("origin registry has a plan without state; refusing a budget reset")
    token = _origin_token(args.origin_ref)
    state = {
        "state_version": STATE_VERSION,
        "run_id": f"run-{token}",
        "start_signature": signature,
        "origin": {"ref": args.origin_ref, "goal": args.goal},
        "phase": "draft",
        "artifact": {"path": str(artifact_path), "type": None, "version": None, "sha256": None},
        "first_slice": None,
        "review_request": None,
        "accepted_review": None,
        "correction": {
            "limit": args.correction_limit,
            "used": 0,
            "required_finding_ids": [],
            "closed_finding_ids": [],
            "frozen_contract": None,
        },
        "active_operation": None,
        "authority": {"source_ref": args.authority_source_ref, "paths": paths},
        "workspace_baseline": capture_snapshot(repo),
        "pre_validation_snapshot": None,
        "validation_request": None,
        "applied_events": {},
        "block": None,
    }
    _validate_state(state)
    _write_json(state_path, state)
    return _response(state, created=True, state_path=str(state_path), artifact_path=str(artifact_path))


def begin_operation(args: argparse.Namespace) -> dict[str, Any]:
    state_path = Path(args.state).resolve()
    state = _load_state(state_path)
    digest = _fingerprint({"command": "begin", "operation": args.operation})
    replay = _replay(state, args.event_id, digest)
    if replay:
        return replay
    expected = _next(state)
    if expected.get("action") != "begin" or expected.get("operation") != args.operation:
        raise WorkflowError(f"cannot begin {args.operation}; next action is {expected}")
    if args.operation == "draft":
        if os.path.lexists(Path(state["artifact"]["path"])):
            raise WorkflowError("draft must begin before the plan exists")
        artifact_sha = None
    else:
        artifact_sha = _artifact_current(state)
    if args.operation == "correction_cycle":
        correction = state["correction"]
        if not correction["required_finding_ids"] or correction["used"] >= correction["limit"]:
            raise WorkflowError("correction has no persisted finding set or remaining budget")
        correction["used"] += 1
    if args.operation == "implementation":
        if not _review_current(state):
            raise WorkflowError("implementation requires a current accepted review")
        baseline = state["workspace_baseline"]
        current = capture_snapshot(Path(baseline["repo_root"]))
        drift = calculate_delta(baseline, current)
        if drift["changes"] or drift["head_changed"] or drift["index_changed"]:
            _block(
                state,
                "workspace_changed_during_planning",
                "Git workspace changed before implementation",
                args.operation,
                delta=drift,
            )
            result = {"operation": args.operation, "phase": state["phase"]}
            _remember(state, args.event_id, digest, result)
            _write_json(state_path, state)
            return _response(state, event_id=args.event_id, operation_started=result)
        state["workspace_baseline"] = current
    if args.operation == "host_validation":
        if not _review_current(state):
            raise WorkflowError("host validation requires a current accepted review")
        current = capture_snapshot(Path(state["workspace_baseline"]["repo_root"]))
        try:
            validate_implementation_delta(
                state["workspace_baseline"],
                current,
                state["authority"]["paths"],
                state["first_slice"]["target_paths"],
            )
        except EvidenceError as exc:
            _block(state, "implementation_evidence_invalid", str(exc), args.operation)
            result = {"operation": args.operation, "phase": state["phase"]}
            _remember(state, args.event_id, digest, result)
            _write_json(state_path, state)
            return _response(state, event_id=args.event_id, operation_started=result)
        state["pre_validation_snapshot"] = current
        state["validation_request"] = _make_validation_request(state, args.event_id)
        state["phase"] = "needs_host_validation"
        state["active_operation"] = None
        result = {
            "operation": args.operation,
            "phase": state["phase"],
            "first_slice_present": True,
            "validation_status": "not_run_by_controller",
            "implementation_completion_claim": False,
        }
        _remember(state, args.event_id, digest, result)
        _write_json(state_path, state)
        return _response(
            state,
            event_id=args.event_id,
            host_validation_handoff=result,
        )
    state["active_operation"] = {
        "id": args.event_id,
        "kind": args.operation,
        "artifact_sha256": artifact_sha,
        "started_ns": time.time_ns(),
    }
    result = {"operation_id": args.event_id, "operation": args.operation, "phase": state["phase"]}
    _remember(state, args.event_id, digest, result)
    _write_json(state_path, state)
    return _response(state, event_id=args.event_id, operation_started=result)


def _runtime_result(
    path_value: str | None, key: str, state: dict[str, Any], argument: str
) -> tuple[dict[str, Any], dict[str, str]]:
    if not path_value:
        raise WorkflowError(f"{key} requires {argument}")
    path = Path(path_value).resolve()
    runtime = Path(state["artifact"]["path"]).resolve().parent
    if path.parent != runtime or _inside(path, Path(state["workspace_baseline"]["repo_root"])):
        raise WorkflowError("result JSON must be inside the trusted outside-worktree runtime directory")
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError(f"result JSON does not exist: {path}") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.getuid():
        raise WorkflowError("result JSON owner/type is unsafe")
    os.chmod(path, 0o600)
    identity = {"path": str(path), "sha256": _hash_file(path)}
    root = _read_json(path)
    if set(root) != {key} or not isinstance(root[key], dict):
        raise WorkflowError(f"result JSON must contain only one {key} object")
    return root[key], identity


def _provider_result(
    path_value: str | None, key: str, state: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, str]]:
    return _runtime_result(path_value, key, state, "--provider-result")


def _plan_result(state: dict[str, Any], result: dict[str, Any], purpose: str) -> dict[str, Any]:
    required = {
        "correlation_id",
        "provider_id",
        "purpose",
        "status",
        "artifact",
        "first_slice",
        "closed_finding_ids",
        "consumed_revision_rounds",
        "unresolved_blockers",
    }
    if set(result) != required:
        raise WorkflowError("workflow_plan_result shape is not canonical")
    if (
        result["correlation_id"] != state["run_id"]
        or result["provider_id"] != PLANNER
        or result["purpose"] != purpose
        or result["status"] != "produced"
        or result["consumed_revision_rounds"] != (0 if purpose == "draft" else 1)
        or result["unresolved_blockers"] != []
    ):
        raise WorkflowError("workflow_plan_result correlation/provider/purpose/status is invalid")
    artifact = result["artifact"]
    if not isinstance(artifact, dict) or set(artifact) != {
        "type", "version", "fingerprint_scheme", "fingerprint", "content_ref"
    }:
        raise WorkflowError("workflow_plan_result artifact shape is invalid")
    if artifact["type"] not in {
        "technical_plan", "architecture_proposal", "migration_plan", "implementation_proposal"
    } or not isinstance(artifact["version"], str) or not artifact["version"]:
        raise WorkflowError("workflow_plan_result artifact type/version is invalid")
    ref = artifact["content_ref"]
    path = Path(state["artifact"]["path"]).resolve()
    if (
        artifact["fingerprint_scheme"] != "exact-bytes-sha256"
        or not _valid_sha(artifact["fingerprint"])
        or not isinstance(ref, dict)
        or set(ref) != {"kind", "value"}
        or ref["kind"] != "path"
        or not isinstance(ref["value"], str)
        or Path(ref["value"]).resolve() != path
    ):
        raise WorkflowError("workflow_plan_result is not bound to the run-owned plan path")
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError("workflow_plan_result plan path does not exist") from exc
    if stat.S_ISLNK(metadata.st_mode) or metadata.st_uid != os.getuid():
        raise WorkflowError("plan artifact owner/type is unsafe")
    os.chmod(path, 0o600)
    actual_hash = _hash_file(path)
    if artifact["fingerprint"] != actual_hash:
        raise WorkflowError("workflow_plan_result fingerprint does not match plan bytes")
    if purpose == "bounded_revision" and (
        actual_hash == state["artifact"]["sha256"] or artifact["version"] == state["artifact"]["version"]
    ):
        raise WorkflowError("bounded_revision must change bytes and version")
    first = result["first_slice"]
    if not isinstance(first, dict) or set(first) != {"id", "summary", "target_paths", "validation_argv"}:
        raise WorkflowError("first_slice shape is invalid")
    if not all(isinstance(first.get(key), str) and first[key] for key in ("id", "summary")):
        raise WorkflowError("first_slice id/summary is empty")
    targets = first["target_paths"]
    argv = first["validation_argv"]
    if not isinstance(targets, list) or not targets or not all(isinstance(value, str) for value in targets):
        raise WorkflowError("first_slice target_paths is invalid")
    targets = sorted({_normalize_path(value) for value in targets})
    outside = [value for value in targets if not _within(value, state["authority"]["paths"])]
    if outside:
        raise WorkflowError("first_slice target_paths exceed start-time authority: " + ", ".join(outside))
    if not isinstance(argv, list) or not argv or not all(isinstance(value, str) and value for value in argv):
        raise WorkflowError("first_slice validation_argv is invalid")
    closed = result["closed_finding_ids"]
    expected = [] if purpose == "draft" else state["correction"]["required_finding_ids"]
    if (
        not isinstance(closed, list)
        or not all(isinstance(value, str) and value for value in closed)
        or len(closed) != len(set(closed))
        or sorted(closed) != sorted(expected)
    ):
        raise WorkflowError("bounded revision must close exactly the persisted blocking finding set")
    contract = {
        "artifact": {
            "path": str(path),
            "type": artifact["type"],
            "version": artifact["version"],
            "sha256": actual_hash,
        },
        "first_slice": {
            "id": first["id"],
            "summary": first["summary"],
            "target_paths": targets,
            "validation_argv": list(argv),
        },
        "closed_finding_ids": sorted(closed),
    }
    if purpose == "bounded_revision":
        frozen = state["correction"]["frozen_contract"]
        if not isinstance(frozen, dict) or (
            contract["artifact"]["type"] != frozen["artifact_type"]
            or contract["first_slice"] != frozen["first_slice"]
        ):
            raise WorkflowError(
                "bounded_revision cannot replace the frozen artifact type or first_slice"
            )
    return contract


def _review_result(state: dict[str, Any], result: dict[str, Any], purpose: str) -> dict[str, Any]:
    request_wrapper = state.get("review_request")
    if not isinstance(request_wrapper, dict) or request_wrapper.get("purpose") != purpose:
        raise WorkflowError("active delegated review purpose is not fixed")
    request = request_wrapper.get("delegated_review")
    if not isinstance(request, dict):
        raise WorkflowError("active delegated review request is missing")
    required = {
        "review_id",
        "reviewer_provider_id",
        "reviewer_capability",
        "artifact_type",
        "artifact_version",
        "artifact_fingerprint_scheme",
        "artifact_fingerprint",
        "artifact_content_ref",
        "scope",
        "independence",
        "judgment",
        "findings",
    }
    if set(result) != required:
        raise WorkflowError("delegated_review_result shape is not canonical")
    if (
        result["review_id"] != request["review_id"]
        or result["reviewer_provider_id"] != request["reviewer_provider_id"]
        or result["reviewer_capability"] != request["reviewer_capability"]
        or result["scope"] != request["review_scope"]["kind"]
        or result["independence"] != request["reviewer_independence"]
        or result["judgment"] not in JUDGMENTS
    ):
        raise WorkflowError(
            "delegated_review_result does not match the fixed review id/provider/capability/scope/independence"
        )
    artifact = state["artifact"]
    requested_artifact = request["artifact"]
    if (
        result["artifact_type"] != requested_artifact["type"]
        or result["artifact_version"] != requested_artifact["version"]
        or result["artifact_fingerprint_scheme"] != requested_artifact["fingerprint_scheme"]
        or result["artifact_fingerprint"] != requested_artifact["fingerprint"]
        or result["artifact_fingerprint"] != _artifact_current(state)
    ):
        raise WorkflowError("delegated_review_result does not match current plan identity")
    ref = result["artifact_content_ref"]
    if (
        not isinstance(ref, dict)
        or set(ref) != {"kind", "value", "plan", "tasks"}
        or ref["kind"] != "path"
        or not isinstance(ref["value"], str)
        or ref != requested_artifact["content_ref"]
        or Path(ref["value"]).resolve() != Path(artifact["path"]).resolve()
        or ref["plan"] is not None
        or ref["tasks"] is not None
    ):
        raise WorkflowError("delegated_review_result does not reference the exact plan path")
    findings = result["findings"]
    if not isinstance(findings, list):
        raise WorkflowError("delegated_review_result findings is invalid")
    ids: set[str] = set()
    blockers: list[str] = []
    decision_owners: list[str] = []
    keys = {"id", "severity", "blocking", "residual", "decision_owner_required"}
    for finding in findings:
        if (
            not isinstance(finding, dict)
            or set(finding) != keys
            or not isinstance(finding["id"], str)
            or not finding["id"]
            or finding["id"] in ids
        ):
            raise WorkflowError("delegated_review_result finding shape/id is invalid")
        ids.add(finding["id"])
        if finding["severity"] not in {"S0", "S1", "S2", "S3"} or not all(
            isinstance(finding[key], bool) for key in ("blocking", "residual", "decision_owner_required")
        ):
            raise WorkflowError("delegated_review_result finding severity/flags is invalid")
        if finding["severity"] in {"S0", "S1"} and not finding["blocking"]:
            raise WorkflowError("S0/S1 finding must be blocking")
        if finding["decision_owner_required"] and (
            not finding["blocking"] or finding["residual"]
        ):
            raise WorkflowError("decision_owner_required finding must be unresolved and blocking")
        if finding["blocking"]:
            blockers.append(finding["id"])
        if finding["decision_owner_required"]:
            decision_owners.append(finding["id"])
    judgment = result["judgment"]
    if judgment == "accept" and findings:
        raise WorkflowError("accept requires no findings")
    if judgment == "accept_with_advisories" and (
        not findings or any(finding["blocking"] or not finding["residual"] for finding in findings)
    ):
        raise WorkflowError("accept_with_advisories requires only residual advisories")
    if judgment == "changes_required" and not blockers:
        raise WorkflowError("changes_required requires blocking findings")
    if judgment in ACCEPTED and blockers:
        raise WorkflowError("accepted review cannot contain blockers")
    return {
        "review_id": result["review_id"],
        "review_request_id": request["review_id"],
        "provider_id": REVIEWER,
        "reviewer_capability": request["reviewer_capability"],
        "scope": request["review_scope"]["kind"],
        "purpose": purpose,
        "artifact_sha256": artifact["sha256"],
        "artifact_version": artifact["version"],
        "judgment": judgment,
        "blocking_finding_ids": sorted(blockers),
        "decision_owner_finding_ids": sorted(decision_owners),
        "recorded_ns": time.time_ns(),
    }


def record_result(args: argparse.Namespace) -> dict[str, Any]:
    state_path = Path(args.state).resolve()
    state = _load_state(state_path)
    payload = {
        "command": "record",
        "operation_id": args.operation_id,
        "result": args.result,
        "provider_result": args.provider_result,
        "note": args.note,
        "block_code": args.block_code,
    }
    digest = _fingerprint(payload)
    replay = _replay(state, args.event_id, digest)
    if replay:
        return replay
    active = state.get("active_operation")
    if not isinstance(active, dict) or active.get("id") != args.operation_id:
        raise WorkflowError("--operation-id does not match the active operation")
    operation = active["kind"]
    provider: dict[str, Any] | None = None
    if args.result != "blocked" and operation in {"draft", "correction_cycle"}:
        provider, _ = _provider_result(args.provider_result, "workflow_plan_result", state)
    elif args.result != "blocked" and operation in {"initial_review", "final_review"}:
        provider, _ = _provider_result(args.provider_result, "delegated_review_result", state)
    elif args.provider_result:
        raise WorkflowError(f"{operation} does not accept --provider-result")
    if args.result == "blocked":
        if args.provider_result:
            raise WorkflowError("blocked result does not accept result evidence")
        _block(state, args.block_code, args.note, operation)
    elif operation == "draft":
        if args.result != "drafted" or provider is None:
            raise WorkflowError("draft requires drafted + workflow_plan_result")
        contract = _plan_result(state, provider, "draft")
        state["artifact"] = contract["artifact"]
        state["first_slice"] = contract["first_slice"]
        state["review_request"] = _make_review_request(state, "initial")
        state["active_operation"] = None
        state["phase"] = "initial_review"
    elif operation == "initial_review":
        if args.result != "reviewed" or provider is None:
            raise WorkflowError("initial_review requires reviewed + delegated_review_result")
        review = _review_result(state, provider, "initial")
        state["active_operation"] = None
        if review["decision_owner_finding_ids"]:
            _block(
                state,
                "initial_review_decision_owner_required",
                "review requires a decision owner; bounded correction is not authorized",
                operation,
                finding_ids=review["decision_owner_finding_ids"],
            )
        elif review["judgment"] in ACCEPTED:
            state["accepted_review"] = review
            state["phase"] = "implementation"
        elif review["judgment"] == "changes_required" and state["correction"]["limit"]:
            state["correction"]["required_finding_ids"] = review["blocking_finding_ids"]
            state["correction"]["frozen_contract"] = {
                "artifact_type": state["artifact"]["type"],
                "first_slice": json.loads(json.dumps(state["first_slice"])),
            }
            state["phase"] = "correction_cycle"
        else:
            _block(state, f"initial_review_{review['judgment']}", "initial review did not qualify", operation)
    elif operation == "correction_cycle":
        if args.result != "corrected" or provider is None:
            raise WorkflowError("correction_cycle requires corrected + workflow_plan_result")
        contract = _plan_result(state, provider, "bounded_revision")
        state["artifact"] = contract["artifact"]
        state["first_slice"] = contract["first_slice"]
        state["correction"]["closed_finding_ids"] = contract["closed_finding_ids"]
        state["accepted_review"] = None
        state["review_request"] = _make_review_request(state, "final_acceptance")
        state["active_operation"] = None
        state["phase"] = "final_review"
    elif operation == "final_review":
        if args.result != "reviewed" or provider is None:
            raise WorkflowError("final_review requires reviewed + delegated_review_result")
        review = _review_result(state, provider, "final_acceptance")
        state["active_operation"] = None
        if review["decision_owner_finding_ids"]:
            _block(
                state,
                "final_review_decision_owner_required",
                "final review requires a decision owner; no further correction is available",
                operation,
                finding_ids=review["decision_owner_finding_ids"],
            )
        elif review["judgment"] in ACCEPTED:
            state["accepted_review"] = review
            state["phase"] = "implementation"
        else:
            code = "final_review_new_blocker" if review["blocking_finding_ids"] else f"final_review_{review['judgment']}"
            _block(state, code, "final review did not qualify; no second correction is available", operation)
    elif operation == "implementation":
        if args.result != "implemented":
            raise WorkflowError("implementation requires implemented or blocked")
        _artifact_current(state)
        if not _review_current(state):
            raise WorkflowError("implementation cannot close against a stale review")
        state["active_operation"] = None
        state["phase"] = "host_validation"
    result = {"operation": operation, "result": args.result, "phase": state["phase"]}
    _remember(state, args.event_id, digest, result)
    _write_json(state_path, state)
    return _response(state, event_id=args.event_id, recorded=result)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Own one bounded draft-to-first-code workflow.")
    commands = parser.add_subparsers(dest="command_name", required=True)
    start = commands.add_parser("start")
    start.add_argument("--runtime-dir", required=True)
    start.add_argument("--workspace", required=True)
    start.add_argument("--origin-ref", required=True)
    start.add_argument("--goal", required=True)
    start.add_argument("--correction-limit", type=int, choices=[0, 1], default=1)
    start.add_argument("--authority-source-ref", required=True)
    start.add_argument("--authority-path", action="append", default=[])
    for name in ("next", "status"):
        command = commands.add_parser(name)
        command.add_argument("--state", required=True)
    begin = commands.add_parser("begin")
    begin.add_argument("--state", required=True)
    begin.add_argument("--event-id", required=True)
    begin.add_argument("--operation", choices=sorted(OPERATIONS), required=True)
    record = commands.add_parser("record")
    record.add_argument("--state", required=True)
    record.add_argument("--event-id", required=True)
    record.add_argument("--operation-id", required=True)
    record.add_argument("--result", required=True)
    record.add_argument("--provider-result")
    record.add_argument("--note", default="")
    record.add_argument("--block-code", default="operation_blocked")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command_name == "start":
            repo = resolve_repo(Path(args.workspace))
            _, state_path, _ = _start_paths(args, repo, create=True)
            with _lock(state_path):
                result = start_workflow(args)
        elif args.command_name in {"begin", "record"}:
            with _lock(Path(args.state)):
                result = begin_operation(args) if args.command_name == "begin" else record_result(args)
        else:
            state = _load_state(Path(args.state))
            result = _next(state) if args.command_name == "next" else _response(state)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (WorkflowError, EvidenceError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
