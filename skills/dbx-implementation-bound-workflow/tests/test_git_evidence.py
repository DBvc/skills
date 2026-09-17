from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from git_evidence import (  # noqa: E402
    EvidenceError,
    calculate_delta,
    capture_snapshot,
    validate_implementation_delta,
    verify_workspace_delta,
)


def run(*command: str, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def init_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    run("git", "init", "-q", cwd=repo)
    run("git", "config", "user.email", "fixture@example.com", cwd=repo)
    run("git", "config", "user.name", "Fixture", cwd=repo)
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    run("git", "add", "src/app.py", "README.md", cwd=repo)
    run("git", "commit", "-qm", "fixture", cwd=repo)
    return repo


class GitEvidenceTest(unittest.TestCase):
    def test_tracks_only_post_baseline_tracked_and_untracked_delta(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            (repo / "README.md").write_text("user dirty\n", encoding="utf-8")
            (repo / "notes.txt").write_text("user note\n", encoding="utf-8")
            baseline = capture_snapshot(repo)
            (repo / "src" / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            (repo / "src" / "new.py").write_text("NEW = True\n", encoding="utf-8")
            pre = capture_snapshot(repo)
            evidence = validate_implementation_delta(baseline, pre, ["src"])

            paths = {item["path"] for item in evidence["changes"]}
            self.assertEqual(paths, {"src/app.py", "src/new.py"})
            self.assertEqual(
                {item["path"] for item in evidence["tracked_changes"]},
                {"src/app.py"},
            )
            self.assertEqual(
                {item["path"] for item in evidence["untracked_changes"]},
                {"src/new.py"},
            )

    def test_scope_violation_and_missing_target_are_rejected_before_host_run(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            baseline = capture_snapshot(repo)
            (repo / "README.md").write_text("outside scope\n", encoding="utf-8")
            pre = capture_snapshot(repo)
            with self.assertRaisesRegex(EvidenceError, "exceeds authority scope"):
                validate_implementation_delta(baseline, pre, ["src"])

        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            baseline = capture_snapshot(repo)
            (repo / "README.md").write_text("wrong target\n", encoding="utf-8")
            pre = capture_snapshot(repo)
            with self.assertRaisesRegex(EvidenceError, "first-slice target"):
                validate_implementation_delta(baseline, pre, ["."], ["src/app.py"])

    def test_caller_supplied_host_evidence_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            baseline = capture_snapshot(repo)
            (repo / "src" / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            pre = capture_snapshot(repo)
            with self.assertRaisesRegex(EvidenceError, "caller-supplied.*unsupported"):
                verify_workspace_delta(baseline, pre, pre, {}, ["src"], {})

    def test_index_mutation_is_rejected_before_host_run(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            baseline = capture_snapshot(repo)
            (repo / "src" / "app.py").write_text("VALUE = 5\n", encoding="utf-8")
            run("git", "add", "src/app.py", cwd=repo)
            pre = capture_snapshot(repo)
            with self.assertRaisesRegex(EvidenceError, "Git index changed"):
                validate_implementation_delta(baseline, pre, ["src"])

    def test_ignored_runtime_files_do_not_enter_delta(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            runtime = repo / ".workflow" / "state.json"
            baseline = capture_snapshot(repo, [".workflow"])
            runtime.parent.mkdir()
            runtime.write_text("{}\n", encoding="utf-8")
            (repo / "src" / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
            current = capture_snapshot(repo, [".workflow"])
            self.assertEqual(
                [item["path"] for item in calculate_delta(baseline, current)["changes"]],
                ["src/app.py"],
            )

    def test_only_git_relevant_regular_file_mode_is_compared(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            baseline = capture_snapshot(repo)
            os.chmod(repo / "README.md", 0o600)
            hardened = capture_snapshot(repo)
            self.assertEqual(calculate_delta(baseline, hardened)["changes"], [])

            os.chmod(repo / "README.md", 0o654)
            group_executable = capture_snapshot(repo)
            self.assertEqual(calculate_delta(baseline, group_executable)["changes"], [])

            os.chmod(repo / "README.md", 0o754)
            executable = capture_snapshot(repo)
            change = calculate_delta(baseline, executable)["changes"][0]
            self.assertNotEqual(change["before_mode"], change["after_mode"])

    def test_file_to_symlink_change_records_type(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = init_repo(Path(raw))
            baseline = capture_snapshot(repo)
            (repo / "src" / "app.py").unlink()
            (repo / "src" / "app.py").symlink_to("../README.md")
            current = capture_snapshot(repo)
            change = validate_implementation_delta(
                baseline, current, ["src/app.py"]
            )["changes"][0]
            self.assertEqual(change["before_kind"], "file")
            self.assertEqual(change["after_kind"], "symlink")


if __name__ == "__main__":
    unittest.main()
