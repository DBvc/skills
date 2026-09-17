from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from planning_workflow import (  # noqa: E402
    WorkflowError,
    begin_operation,
    record_result,
    start_workflow,
)
def ns(**values: object) -> argparse.Namespace:
    return argparse.Namespace(**values)


def run(*command: str, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, object]) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def init_fixture(root: Path) -> tuple[Path, Path]:
    repo = root / "repo"
    repo.mkdir()
    run("git", "init", "-q", cwd=repo)
    run("git", "config", "user.email", "fixture@example.com", cwd=repo)
    run("git", "config", "user.name", "Fixture", cwd=repo)
    (repo / "src").mkdir()
    (repo / "tests").mkdir()
    (repo / "src" / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text("# fixture\n", encoding="utf-8")
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    run("git", "add", ".", cwd=repo)
    run("git", "commit", "-qm", "fixture", cwd=repo)
    runtime = root / "runtime"
    runtime.mkdir(mode=0o700)
    return repo, runtime


def start_args(repo: Path, runtime: Path, **overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "runtime_dir": str(runtime),
        "workspace": str(repo),
        "origin_ref": "trusted-origin-1",
        "goal": "Implement the first safe slice",
        "correction_limit": 1,
        "authority_source_ref": "user-event-1",
        "authority_path": ["src", "tests"],
    }
    values.update(overrides)
    return ns(**values)


def begin_args(state: Path, event: str, operation: str) -> argparse.Namespace:
    return ns(state=str(state), event_id=event, operation=operation)


def record_args(
    state: Path, event: str, operation: str, result: str, **overrides: object
) -> argparse.Namespace:
    values: dict[str, object] = {
        "state": str(state),
        "event_id": event,
        "operation_id": operation,
        "result": result,
        "provider_result": None,
        "note": "",
        "block_code": "operation_blocked",
    }
    values.update(overrides)
    return ns(**values)


def plan_result(
    runtime: Path,
    state_value: dict[str, object],
    *,
    purpose: str = "draft",
    version: str = "v1",
    artifact_type: str = "technical_plan",
    targets: list[str] | None = None,
    validation: list[str] | None = None,
    closed: list[str] | None = None,
    provider: str = "dbx-technical-plan",
    correlation: str | None = None,
    result_name: str = "plan-result.json",
) -> Path:
    artifact = Path(state_value["artifact"]["path"])  # type: ignore[index]
    payload = {
        "workflow_plan_result": {
            "correlation_id": correlation or state_value["run_id"],
            "provider_id": provider,
            "purpose": purpose,
            "status": "produced",
            "artifact": {
                "type": artifact_type,
                "version": version,
                "fingerprint_scheme": "exact-bytes-sha256",
                "fingerprint": sha(artifact),
                "content_ref": {"kind": "path", "value": str(artifact)},
            },
            "first_slice": {
                "id": "slice-1",
                "summary": "Change the app value",
                "target_paths": targets or ["src/app.py"],
                "validation_argv": validation
                or [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; assert 'VALUE = 2' in Path('src/app.py').read_text()",
                ],
            },
            "closed_finding_ids": closed or [],
            "consumed_revision_rounds": 0 if purpose == "draft" else 1,
            "unresolved_blockers": [],
        }
    }
    return write_json(runtime / result_name, payload)


def review_result(
    runtime: Path,
    state_value: dict[str, object],
    *,
    purpose: str = "initial",
    judgment: str = "accept",
    findings: list[dict[str, object]] | None = None,
    provider: str = "dbx-linus-review",
    capability: str = "strict_pragmatic_plan_review",
    scope: str = "full",
    independence: str = "independent",
    fingerprint: str | None = None,
    review_id: str | None = None,
    result_name: str = "review-result.json",
) -> Path:
    artifact = state_value["artifact"]  # type: ignore[index]
    request = state_value["review_request"]["delegated_review"]  # type: ignore[index]
    payload = {
        "delegated_review_result": {
            "review_id": review_id or request["review_id"],
            "reviewer_provider_id": provider,
            "reviewer_capability": capability,
            "artifact_type": artifact["type"],
            "artifact_version": artifact["version"],
            "artifact_fingerprint_scheme": "exact-bytes-sha256",
            "artifact_fingerprint": fingerprint or artifact["sha256"],
            "artifact_content_ref": {
                "kind": "path",
                "value": artifact["path"],
                "plan": None,
                "tasks": None,
            },
            "scope": scope,
            "independence": independence,
            "judgment": judgment,
            "findings": findings or [],
        }
    }
    return write_json(runtime / result_name, payload)


def fingerprint(value: object) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def start_and_draft(
    root: Path,
    *,
    validation: list[str] | None = None,
    targets: list[str] | None = None,
) -> tuple[Path, Path, Path, dict[str, object]]:
    repo, runtime = init_fixture(root)
    started = start_workflow(start_args(repo, runtime))
    state = Path(started["state_path"])
    artifact = Path(started["artifact_path"])
    begin_operation(begin_args(state, "op-draft", "draft"))
    artifact.write_text("# Plan\n\nImplement the first slice.\n", encoding="utf-8")
    result_file = plan_result(
        runtime,
        started["state"],
        validation=validation,
        targets=targets,
    )
    drafted = record_result(
        record_args(
            state,
            "event-drafted",
            "op-draft",
            "drafted",
            provider_result=str(result_file),
        )
    )
    return repo, runtime, state, drafted["state"]


def accept_initial(runtime: Path, state: Path, state_value: dict[str, object]) -> dict[str, object]:
    begin_operation(begin_args(state, "op-review", "initial_review"))
    result_file = review_result(runtime, state_value)
    accepted = record_result(
        record_args(
            state,
            "event-review",
            "op-review",
            "reviewed",
            provider_result=str(result_file),
        )
    )
    return accepted["state"]


def enter_implementation(runtime: Path, state: Path, state_value: dict[str, object]) -> dict[str, object]:
    accepted = accept_initial(runtime, state, state_value)
    begin_operation(begin_args(state, "op-implementation", "implementation"))
    return accepted


class PlanningWorkflowTest(unittest.TestCase):
    def test_start_is_real_draft_and_origin_registry_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo, runtime = init_fixture(Path(raw))
            args = start_args(repo, runtime)
            first = start_workflow(args)
            self.assertEqual(first["next"]["operation"], "draft")
            self.assertFalse(Path(first["artifact_path"]).exists())
            second = start_workflow(args)
            self.assertTrue(second["idempotent_start"])
            self.assertEqual(second["state"]["run_id"], first["state"]["run_id"])
            with self.assertRaisesRegex(WorkflowError, "conflicting start input"):
                start_workflow(start_args(repo, runtime, goal="Different goal"))

    def test_start_rejects_repo_runtime_and_missing_explicit_authority(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo, runtime = init_fixture(Path(raw))
            with self.assertRaisesRegex(WorkflowError, "outside the Git worktree"):
                start_workflow(start_args(repo, repo / ".runtime"))
            with self.assertRaisesRegex(WorkflowError, "authorized explicit"):
                start_workflow(start_args(repo, runtime, authority_path=[]))
            with self.assertRaisesRegex(WorkflowError, "trusted authority"):
                start_workflow(start_args(repo, runtime, authority_source_ref=""))

    def test_successful_record_replays_before_active_operation_checks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo, runtime = init_fixture(Path(raw))
            started = start_workflow(start_args(repo, runtime))
            state = Path(started["state_path"])
            artifact = Path(started["artifact_path"])
            begin_operation(begin_args(state, "op-draft", "draft"))
            artifact.write_text("# Plan\n", encoding="utf-8")
            result_file = plan_result(runtime, started["state"])
            command = record_args(
                state,
                "draft-record",
                "op-draft",
                "drafted",
                provider_result=str(result_file),
            )
            first = record_result(command)
            self.assertEqual(first["state"]["phase"], "initial_review")
            replay = record_result(command)
            self.assertTrue(replay["idempotent_replay"])
            self.assertEqual(replay["recorded_result"]["phase"], "initial_review")
            with self.assertRaisesRegex(WorkflowError, "different payload"):
                record_result(
                    record_args(
                        state,
                        "draft-record",
                        "wrong-operation",
                        "drafted",
                        provider_result=str(result_file),
                    )
                )

    def test_draft_requires_canonical_provider_result_and_authorized_first_slice(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo, runtime = init_fixture(root)
            started = start_workflow(start_args(repo, runtime, authority_path=["src"]))
            state = Path(started["state_path"])
            artifact = Path(started["artifact_path"])
            begin_operation(begin_args(state, "op-draft", "draft"))
            artifact.write_text("# Plan\n", encoding="utf-8")
            fake = plan_result(runtime, started["state"], correlation="different-run")
            with self.assertRaisesRegex(WorkflowError, "correlation/provider"):
                record_result(
                    record_args(
                        state,
                        "bad-correlation",
                        "op-draft",
                        "drafted",
                        provider_result=str(fake),
                    )
                )
            escaped = plan_result(root, started["state"], result_name="escaped-result.json")
            with self.assertRaisesRegex(WorkflowError, "trusted outside-worktree runtime"):
                record_result(
                    record_args(
                        state,
                        "escaped-provider-result",
                        "op-draft",
                        "drafted",
                        provider_result=str(escaped),
                    )
                )
            outside = plan_result(runtime, started["state"], targets=["tests"], result_name="outside.json")
            with self.assertRaisesRegex(WorkflowError, "exceed start-time authority"):
                record_result(
                    record_args(
                        state,
                        "bad-target",
                        "op-draft",
                        "drafted",
                        provider_result=str(outside),
                    )
                )

    def test_fake_review_is_rejected_then_clean_path_freezes_host_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo, runtime, state, drafted = start_and_draft(root)
            persisted_request = drafted["review_request"]["delegated_review"]
            self.assertEqual(persisted_request["reviewer_capability"], "strict_pragmatic_plan_review")
            self.assertEqual(persisted_request["review_scope"]["kind"], "full")
            self.assertEqual(
                persisted_request["evidence_boundary"]["artifact_fingerprint"],
                drafted["artifact"]["sha256"],
            )
            begin_operation(begin_args(state, "op-review", "initial_review"))
            fake = review_result(runtime, drafted, independence="unknown")
            with self.assertRaisesRegex(WorkflowError, "scope/independence"):
                record_result(
                    record_args(
                        state,
                        "fake-review",
                        "op-review",
                        "reviewed",
                        provider_result=str(fake),
                    )
                )
            wrong_provider = review_result(
                runtime,
                drafted,
                provider="claimed-reviewer",
                result_name="wrong-provider.json",
            )
            with self.assertRaisesRegex(WorkflowError, "provider"):
                record_result(
                    record_args(
                        state,
                        "wrong-provider",
                        "op-review",
                        "reviewed",
                        provider_result=str(wrong_provider),
                    )
                )
            wrong_capability = review_result(
                runtime,
                drafted,
                capability="claimed-capability",
                result_name="wrong-capability.json",
            )
            with self.assertRaisesRegex(WorkflowError, "capability"):
                record_result(
                    record_args(
                        state,
                        "wrong-capability",
                        "op-review",
                        "reviewed",
                        provider_result=str(wrong_capability),
                    )
                )
            wrong_context = review_result(
                runtime,
                drafted,
                review_id="review-" + "0" * 64,
                result_name="wrong-context.json",
            )
            with self.assertRaisesRegex(WorkflowError, "fixed review id"):
                record_result(
                    record_args(
                        state,
                        "wrong-context",
                        "op-review",
                        "reviewed",
                        provider_result=str(wrong_context),
                    )
                )
            stale = review_result(
                runtime,
                drafted,
                fingerprint="sha256:" + "0" * 64,
                result_name="stale-review.json",
            )
            with self.assertRaisesRegex(WorkflowError, "current plan identity"):
                record_result(
                    record_args(
                        state,
                        "stale-review",
                        "op-review",
                        "reviewed",
                        provider_result=str(stale),
                    )
                )
            clean = review_result(runtime, drafted, result_name="clean-review.json")
            accepted = record_result(
                record_args(
                    state,
                    "clean-review",
                    "op-review",
                    "reviewed",
                    provider_result=str(clean),
                )
            )
            self.assertEqual(accepted["state"]["phase"], "implementation")
            begin_operation(begin_args(state, "op-implementation", "implementation"))
            (repo / "src" / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            implemented = record_result(
                record_args(state, "implemented", "op-implementation", "implemented")
            )
            self.assertEqual(implemented["state"]["phase"], "host_validation")
            host_started = begin_operation(begin_args(state, "op-host", "host_validation"))
            validation_request = host_started["state"]["validation_request"]
            self.assertEqual(validation_request["cwd"], str(repo.resolve()))
            self.assertEqual(validation_request["timeout_seconds"], 300)
            self.assertEqual(validation_request["output_limit_bytes"], 1024 * 1024)
            self.assertEqual(
                validation_request["external_side_effect_policy"],
                "forbidden_without_separate_host_approval",
            )
            self.assertEqual(host_started["state"]["phase"], "needs_host_validation")
            self.assertEqual(
                host_started["next"]["terminal"],
                {
                    "is_terminal": True,
                    "outcome": "needs_host_validation",
                    "block": None,
                    "first_slice_present": True,
                    "validation_status": "not_run_by_controller",
                    "implementation_completion_claim": False,
                },
            )
            self.assertEqual(
                host_started["next"]["host_validation_request"],
                validation_request,
            )
            with self.assertRaisesRegex(WorkflowError, "active operation"):
                record_result(
                    record_args(state, "validated", "op-host", "validated")
                )
            self.assertEqual(Path(host_started["state"]["artifact"]["path"]).stat().st_mode & 0o777, 0o600)

    def test_persisted_review_evidence_context_tampering_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            _, _, state, _ = start_and_draft(Path(raw))
            persisted = json.loads(state.read_text(encoding="utf-8"))
            persisted["review_request"]["delegated_review"]["evidence_boundary"][
                "authority_paths"
            ] = ["."]
            state.write_text(json.dumps(persisted), encoding="utf-8")
            with self.assertRaisesRegex(WorkflowError, "review request/context changed"):
                begin_operation(begin_args(state, "op-review", "initial_review"))

    def test_implementation_begin_blocks_workspace_drift_from_planning(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo, runtime, state, drafted = start_and_draft(root)
            accept_initial(runtime, state, drafted)
            (repo / "src" / "app.py").write_text("changed before implementation\n", encoding="utf-8")
            blocked = begin_operation(begin_args(state, "op-implementation", "implementation"))
            self.assertEqual(blocked["state"]["phase"], "blocked")
            self.assertEqual(blocked["state"]["block"]["code"], "workspace_changed_during_planning")

    def test_decision_owner_finding_blocks_instead_of_entering_correction(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            _, runtime, state, drafted = start_and_draft(Path(raw))
            begin_operation(begin_args(state, "op-review", "initial_review"))
            finding = {
                "id": "F-DECIDE",
                "severity": "S2",
                "blocking": True,
                "residual": False,
                "decision_owner_required": True,
            }
            result_file = review_result(
                runtime,
                drafted,
                judgment="changes_required",
                findings=[finding],
            )
            blocked = record_result(
                record_args(
                    state,
                    "decision-owner",
                    "op-review",
                    "reviewed",
                    provider_result=str(result_file),
                )
            )
            self.assertEqual(blocked["state"]["phase"], "blocked")
            self.assertEqual(
                blocked["state"]["block"]["code"],
                "initial_review_decision_owner_required",
            )
            self.assertEqual(blocked["state"]["correction"]["required_finding_ids"], [])
            self.assertEqual(blocked["state"]["correction"]["used"], 0)

    def test_one_correction_closes_exact_persisted_finding_set(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, runtime, state, drafted = start_and_draft(root)
            begin_operation(begin_args(state, "op-review", "initial_review"))
            findings = [
                {
                    "id": "F-001",
                    "severity": "S1",
                    "blocking": True,
                    "residual": False,
                    "decision_owner_required": False,
                },
                {
                    "id": "F-002",
                    "severity": "S2",
                    "blocking": True,
                    "residual": False,
                    "decision_owner_required": False,
                },
            ]
            needs_fix = review_result(
                runtime,
                drafted,
                judgment="changes_required",
                findings=findings,
            )
            reviewed = record_result(
                record_args(
                    state,
                    "needs-fix",
                    "op-review",
                    "reviewed",
                    provider_result=str(needs_fix),
                )
            )
            self.assertEqual(
                reviewed["state"]["correction"]["required_finding_ids"], ["F-001", "F-002"]
            )
            begin_operation(begin_args(state, "op-correction", "correction_cycle"))
            artifact = Path(reviewed["state"]["artifact"]["path"])
            artifact.write_text("# Revised plan\n\nBoth findings closed.\n", encoding="utf-8")
            incomplete = plan_result(
                runtime,
                reviewed["state"],
                purpose="bounded_revision",
                version="v2",
                closed=["F-001"],
                result_name="incomplete.json",
            )
            with self.assertRaisesRegex(WorkflowError, "exactly the persisted"):
                record_result(
                    record_args(
                        state,
                        "incomplete",
                        "op-correction",
                        "corrected",
                        provider_result=str(incomplete),
                    )
                )
            replaced_type = plan_result(
                runtime,
                reviewed["state"],
                purpose="bounded_revision",
                version="v2",
                artifact_type="migration_plan",
                closed=["F-001", "F-002"],
                result_name="replaced-type.json",
            )
            with self.assertRaisesRegex(WorkflowError, "frozen artifact type or first_slice"):
                record_result(
                    record_args(
                        state,
                        "replaced-type",
                        "op-correction",
                        "corrected",
                        provider_result=str(replaced_type),
                    )
                )
            replaced_slice = plan_result(
                runtime,
                reviewed["state"],
                purpose="bounded_revision",
                version="v2",
                targets=["tests/test_app.py"],
                closed=["F-001", "F-002"],
                result_name="replaced-slice.json",
            )
            with self.assertRaisesRegex(WorkflowError, "frozen artifact type or first_slice"):
                record_result(
                    record_args(
                        state,
                        "replaced-slice",
                        "op-correction",
                        "corrected",
                        provider_result=str(replaced_slice),
                    )
                )
            complete = plan_result(
                runtime,
                reviewed["state"],
                purpose="bounded_revision",
                version="v2",
                closed=["F-002", "F-001"],
                result_name="complete.json",
            )
            corrected = record_result(
                record_args(
                    state,
                    "complete",
                    "op-correction",
                    "corrected",
                    provider_result=str(complete),
                )
            )
            self.assertEqual(corrected["state"]["phase"], "final_review")
            self.assertEqual(corrected["state"]["correction"]["used"], 1)
            self.assertEqual(corrected["state"]["correction"]["closed_finding_ids"], ["F-001", "F-002"])

    def test_final_review_new_blocker_stops_without_second_correction(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, runtime, state, drafted = start_and_draft(root)
            begin_operation(begin_args(state, "op-review", "initial_review"))
            finding = {
                "id": "F-001",
                "severity": "S1",
                "blocking": True,
                "residual": False,
                "decision_owner_required": False,
            }
            initial = review_result(runtime, drafted, judgment="changes_required", findings=[finding])
            needs_fix = record_result(
                record_args(state, "needs", "op-review", "reviewed", provider_result=str(initial))
            )
            begin_operation(begin_args(state, "op-correction", "correction_cycle"))
            Path(needs_fix["state"]["artifact"]["path"]).write_text("# Revised\n", encoding="utf-8")
            revision = plan_result(
                runtime,
                needs_fix["state"],
                purpose="bounded_revision",
                version="v2",
                closed=["F-001"],
            )
            corrected = record_result(
                record_args(state, "fixed", "op-correction", "corrected", provider_result=str(revision))
            )
            begin_operation(begin_args(state, "op-final", "final_review"))
            new_finding = dict(finding, id="F-NEW")
            final = review_result(
                runtime,
                corrected["state"],
                purpose="final_acceptance",
                judgment="changes_required",
                findings=[new_finding],
            )
            blocked = record_result(
                record_args(state, "final", "op-final", "reviewed", provider_result=str(final))
            )
            self.assertEqual(blocked["state"]["phase"], "blocked")
            self.assertEqual(blocked["state"]["block"]["code"], "final_review_new_blocker")
            self.assertEqual(blocked["state"]["correction"]["used"], 1)

    def test_helper_never_executes_planner_argv_or_accepts_host_result_json(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            marker = root / "planner-side-effect.txt"
            command = [
                sys.executable,
                "-c",
                f"from pathlib import Path; Path({str(marker)!r}).write_text('executed')",
            ]
            repo, runtime, state, drafted = start_and_draft(root, validation=command)
            enter_implementation(runtime, state, drafted)
            (repo / "src" / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            implemented = record_result(
                record_args(state, "implemented-malicious", "op-implementation", "implemented")
            )
            self.assertEqual(implemented["state"]["phase"], "host_validation")
            host_started = begin_operation(
                begin_args(state, "host-malicious", "host_validation")
            )
            self.assertEqual(
                host_started["state"]["validation_request"]["command_sha256"],
                fingerprint(command),
            )
            self.assertEqual(host_started["state"]["phase"], "needs_host_validation")
            self.assertFalse(host_started["next"]["terminal"]["implementation_completion_claim"])
            self.assertFalse(marker.exists())
            with self.assertRaisesRegex(WorkflowError, "active operation"):
                record_result(
                    record_args(state, "fake-host-result", "host-malicious", "validated")
                )
            self.assertFalse(marker.exists())

    def test_missing_target_delta_blocks_before_host_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo, runtime, state, drafted = start_and_draft(
                root,
                validation=[sys.executable, "-c", "pass"],
                targets=["src/app.py"],
            )
            enter_implementation(runtime, state, drafted)
            (repo / "tests" / "test_app.py").write_text("# changed\n", encoding="utf-8")
            implemented = record_result(
                record_args(state, "wrong-target", "op-implementation", "implemented")
            )
            self.assertEqual(implemented["state"]["phase"], "host_validation")
            blocked = begin_operation(begin_args(state, "host-wrong-target", "host_validation"))
            self.assertEqual(blocked["state"]["block"]["code"], "implementation_evidence_invalid")
            self.assertIn("first-slice target", blocked["state"]["block"]["note"])

    def test_cli_start_creates_private_state(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo, runtime = init_fixture(Path(raw))
            script = SCRIPTS / "planning_workflow.py"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "start",
                    "--runtime-dir",
                    str(runtime),
                    "--workspace",
                    str(repo),
                    "--origin-ref",
                    "cli-origin",
                    "--goal",
                    "Implement slice",
                    "--authority-source-ref",
                    "user-cli",
                    "--authority-path",
                    "src",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["next"]["operation"], "draft")
            self.assertEqual(Path(result["state_path"]).stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
