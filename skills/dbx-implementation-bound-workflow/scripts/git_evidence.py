#!/usr/bin/env python3
"""Capture and compare Git evidence for the workflow helper.

Usage: internal module imported by ``planning_workflow.py``; no standalone CLI.

This module never executes planner-supplied validation commands. It also fails
closed on caller-supplied host result JSON because this package has no
authenticated host channel.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import time
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

SCHEMA_VERSION = 3


class EvidenceError(RuntimeError):
    """Raised when Git evidence cannot be captured or validated."""


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise EvidenceError(f"git {' '.join(args)} failed: {detail}")
    return completed


def resolve_repo(path: Path) -> Path:
    completed = _run_git(path.resolve(), "rev-parse", "--show-toplevel")
    root = completed.stdout.decode("utf-8", errors="strict").strip()
    if not root:
        raise EvidenceError(f"not a Git repository: {path}")
    return Path(root).resolve()


def _nul_paths(payload: bytes) -> set[str]:
    result: set[str] = set()
    for raw in payload.split(b"\0"):
        if raw:
            result.add(raw.decode("utf-8", errors="surrogateescape"))
    return result


def _path_identity(path: Path) -> tuple[str, int] | tuple[None, None]:
    if not os.path.lexists(path):
        return None, None
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode):
        return "symlink", 0o120000
    if stat.S_ISREG(metadata.st_mode):
        # Git tracks only the executable bit for regular files. Permission
        # hardening such as 0644 -> 0600 must not become an attributable delta.
        return "file", 0o100755 if metadata.st_mode & stat.S_IXUSR else 0o100644
    raise EvidenceError(f"Git entry is not a regular file or symlink: {path}")


def _hash_path(path: Path) -> str | None:
    kind, _ = _path_identity(path)
    if kind is None:
        return None
    digest = hashlib.sha256()
    if kind == "symlink":
        digest.update(b"symlink\0")
        digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        return "sha256:" + digest.hexdigest()
    digest.update(b"file\0")
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _mtime_ns(path: Path) -> int | None:
    try:
        return path.lstat().st_mtime_ns
    except FileNotFoundError:
        return None


def _ctime_ns(path: Path) -> int | None:
    try:
        return path.lstat().st_ctime_ns
    except FileNotFoundError:
        return None


def _ignored(relative: str, ignored_paths: Sequence[str]) -> bool:
    return any(_path_allowed(relative, [path]) for path in ignored_paths)


def capture_snapshot(repo_path: Path, ignored_paths: Sequence[str] = ()) -> dict[str, Any]:
    repo = resolve_repo(repo_path)
    normalized_ignored = sorted({_normalize_scope_path(path) for path in ignored_paths})
    tracked = _nul_paths(_run_git(repo, "ls-files", "-z", "--cached").stdout)
    untracked = _nul_paths(
        _run_git(repo, "ls-files", "-z", "--others", "--exclude-standard").stdout
    )
    entries: dict[str, dict[str, Any]] = {}
    for relative in sorted(tracked | untracked):
        if _ignored(relative, normalized_ignored):
            continue
        kind, mode = _path_identity(repo / relative)
        entries[relative] = {
            "tracked": relative in tracked,
            "kind": kind,
            "mode": mode,
            "sha256": _hash_path(repo / relative),
            "mtime_ns": _mtime_ns(repo / relative),
            "ctime_ns": _ctime_ns(repo / relative),
        }
    head_result = _run_git(repo, "rev-parse", "HEAD", check=False)
    head = head_result.stdout.decode("ascii", errors="replace").strip() if head_result.returncode == 0 else None
    index_fingerprint = "sha256:" + hashlib.sha256(
        _run_git(repo, "ls-files", "-z", "--stage").stdout
    ).hexdigest()
    core = {
        "schema_version": SCHEMA_VERSION,
        "repo_root": str(repo),
        "head": head,
        "index_fingerprint": index_fingerprint,
        "ignored_paths": normalized_ignored,
        "entries": entries,
        "captured_ns": time.time_ns(),
    }
    return {**core, "fingerprint": _fingerprint(core)}


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    core = {
        "schema_version": snapshot.get("schema_version"),
        "repo_root": snapshot.get("repo_root"),
        "head": snapshot.get("head"),
        "index_fingerprint": snapshot.get("index_fingerprint"),
        "ignored_paths": snapshot.get("ignored_paths"),
        "entries": snapshot.get("entries"),
        "captured_ns": snapshot.get("captured_ns"),
    }
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        raise EvidenceError("unsupported workspace snapshot schema")
    if not isinstance(snapshot.get("repo_root"), str) or not snapshot["repo_root"]:
        raise EvidenceError("workspace snapshot has no repo_root")
    if not isinstance(snapshot.get("entries"), dict):
        raise EvidenceError("workspace snapshot entries must be an object")
    for relative, entry in snapshot["entries"].items():
        if not isinstance(relative, str) or not isinstance(entry, dict):
            raise EvidenceError("workspace snapshot entry is invalid")
        if entry.get("kind") not in {"file", "symlink", None}:
            raise EvidenceError(f"workspace snapshot entry kind is invalid: {relative}")
        if entry.get("mode") is not None and not isinstance(entry.get("mode"), int):
            raise EvidenceError(f"workspace snapshot entry mode is invalid: {relative}")
        if entry.get("ctime_ns") is not None and not isinstance(entry.get("ctime_ns"), int):
            raise EvidenceError(f"workspace snapshot entry ctime is invalid: {relative}")
    if not isinstance(snapshot.get("index_fingerprint"), str) or not snapshot["index_fingerprint"].startswith("sha256:"):
        raise EvidenceError("workspace snapshot index_fingerprint is invalid")
    if not isinstance(snapshot.get("ignored_paths"), list):
        raise EvidenceError("workspace snapshot ignored_paths must be an array")
    if not isinstance(snapshot.get("captured_ns"), int) or snapshot["captured_ns"] < 1:
        raise EvidenceError("workspace snapshot captured_ns is invalid")
    if snapshot.get("fingerprint") != _fingerprint(core):
        raise EvidenceError("workspace snapshot fingerprint mismatch")


def _normalize_scope_path(value: str) -> str:
    if not value:
        raise EvidenceError("authority scope path must not be empty")
    candidate = PurePosixPath(value.replace("\\", "/"))
    if candidate.is_absolute() or ".." in candidate.parts:
        raise EvidenceError(f"authority scope path must be repository-relative: {value}")
    normalized = candidate.as_posix().rstrip("/") or "."
    return normalized


def _path_allowed(relative: str, allowed_paths: Sequence[str]) -> bool:
    for raw in allowed_paths:
        allowed = _normalize_scope_path(raw)
        if allowed == "." or relative == allowed or relative.startswith(allowed + "/"):
            return True
    return False


def calculate_delta(baseline: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    validate_snapshot(baseline)
    validate_snapshot(current)
    if Path(baseline["repo_root"]).resolve() != Path(current["repo_root"]).resolve():
        raise EvidenceError("baseline and current snapshot refer to different repositories")
    before = baseline["entries"]
    after = current["entries"]
    changes: list[dict[str, Any]] = []
    for relative in sorted(set(before) | set(after)):
        old = before.get(relative)
        new = after.get(relative)
        old_hash = old.get("sha256") if isinstance(old, dict) else None
        new_hash = new.get("sha256") if isinstance(new, dict) else None
        old_identity = (
            (old or {}).get("tracked"),
            (old or {}).get("kind"),
            (old or {}).get("mode"),
            old_hash,
        )
        new_identity = (
            (new or {}).get("tracked"),
            (new or {}).get("kind"),
            (new or {}).get("mode"),
            new_hash,
        )
        if old_identity == new_identity:
            continue
        tracked = bool((new or old or {}).get("tracked"))
        if old is None or (old_hash is None and new_hash is not None):
            status = "added"
        elif new is None or (old_hash is not None and new_hash is None):
            status = "deleted"
        else:
            status = "modified"
        changes.append(
            {
                "path": relative,
                "status": status,
                "tracked": tracked,
                "before_kind": (old or {}).get("kind"),
                "after_kind": (new or {}).get("kind"),
                "before_mode": (old or {}).get("mode"),
                "after_mode": (new or {}).get("mode"),
                "before_sha256": old_hash,
                "after_sha256": new_hash,
            }
        )
    return {
        "changes": changes,
        "tracked_changes": [item for item in changes if item["tracked"]],
        "untracked_changes": [item for item in changes if not item["tracked"]],
        "head_changed": baseline["head"] != current["head"],
        "index_changed": baseline["index_fingerprint"] != current["index_fingerprint"],
    }


def validate_implementation_delta(
    baseline: dict[str, Any],
    current: dict[str, Any],
    allowed_paths: Sequence[str],
    required_target_paths: Sequence[str] = (),
) -> dict[str, Any]:
    validate_snapshot(baseline)
    validate_snapshot(current)
    if not allowed_paths:
        raise EvidenceError("implementation authority has no allowed paths")
    delta = calculate_delta(baseline, current)
    if delta["head_changed"]:
        raise EvidenceError("Git HEAD changed after the implementation baseline")
    if delta["index_changed"]:
        raise EvidenceError(
            "Git index changed after the implementation baseline; staging is outside this workflow"
        )
    if not delta["changes"]:
        raise EvidenceError("workspace has no attributable changes after the baseline")
    violations = [
        item["path"] for item in delta["changes"] if not _path_allowed(item["path"], allowed_paths)
    ]
    if violations:
        raise EvidenceError("workspace delta exceeds authority scope: " + ", ".join(violations))
    normalized_targets = [_normalize_scope_path(path) for path in required_target_paths]
    if normalized_targets and not any(
        _path_allowed(item["path"], normalized_targets) for item in delta["changes"]
    ):
        raise EvidenceError("workspace delta does not touch the declared first-slice target surface")
    return delta


def verify_workspace_delta(
    baseline: dict[str, Any],
    pre_validation: dict[str, Any],
    post_validation: dict[str, Any],
    validation_result: dict[str, Any],
    allowed_paths: Sequence[str],
    validation_request: dict[str, Any],
    required_target_paths: Sequence[str] = (),
) -> dict[str, Any]:
    """Fail closed: same-runtime caller JSON cannot authenticate a trusted host.

    The experimental controller now stops after freezing ``validation_request``.
    A platform-owned host may execute that request, but this package neither
    accepts its result nor claims implementation completion.
    """
    raise EvidenceError(
        "caller-supplied host validation evidence is unsupported; "
        "the controller terminates at needs_host_validation"
    )
