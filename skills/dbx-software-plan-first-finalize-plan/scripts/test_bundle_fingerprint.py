#!/usr/bin/env python3
"""Usage: python3 test_bundle_fingerprint.py"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from issue_workflow import plan_bundle_identity

SCRIPT = Path(__file__).with_name("issue_workflow.py")


class PlanBundleFingerprintTest(unittest.TestCase):
    def materialize(self, root: Path, issue_id: str) -> tuple[Path, Path]:
        subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), "init", issue_id],
            check=True,
            capture_output=True,
            text=True,
        )
        issue_dir = root / ".plan-first" / "issues" / issue_id
        plan = issue_dir / "plan.md"
        tasks = issue_dir / "tasks.md"
        plan.write_text("# Plan\n", encoding="utf-8")
        tasks.write_text(
            "- [ ] [t1] Do\n"
            "验收: 任务类型=step; done\n"
            "验证: # 无程序化验证: fixture\n"
            "依赖: none\n",
            encoding="utf-8",
        )
        return plan, tasks

    def test_known_fixture_and_content_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.md"
            tasks = Path(tmp) / "tasks.md"
            plan.write_bytes(b"plan\n")
            tasks.write_bytes(b"tasks\n")

            first = plan_bundle_identity(plan, tasks)
            self.assertEqual(first["scheme"], "plan-first-bundle-sha256-v1")
            self.assertEqual(
                first["fingerprint"],
                "sha256:d0e5d5578224bff412c13523f3a7c18b51e91c7c8c6d36822cdb915f2dbb156e",
            )

            tasks.write_bytes(b"tasks changed\n")
            self.assertNotEqual(plan_bundle_identity(plan, tasks)["fingerprint"], first["fingerprint"])

    def test_linus_eval_fixture_identity(self) -> None:
        fixture = Path(__file__).resolve().parents[3] / "skills" / "dbx-linus-review" / "evals" / "fixtures"
        identity = plan_bundle_identity(fixture / "plan.md", fixture / "tasks.md")
        self.assertEqual(
            identity,
            {
                "scheme": "plan-first-bundle-sha256-v1",
                "files": {
                    "plan.md": "052e5fbfda6765a4d836a00d367fe2d7abb2967f72e72cdc69fdfdea28958c5b",
                    "tasks.md": "33d7f2007f4a016c944892625ba9bd8248ad4442457765113bdfd9085ce9c41c",
                },
                "fingerprint": "sha256:5b6891e696db45d40864d399329f0b2c9ca0150d5a46783dd853da9f8423f63b",
            },
        )

    def test_selected_seal_accepts_match_and_rejects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.materialize(root, "manual")
            subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "seal", "manual"],
                check=True,
                capture_output=True,
                text=True,
            )
            manual_seal = json.loads(
                (root / ".plan-first" / "issues" / "manual" / "state" / "seal.json").read_text()
            )
            self.assertNotIn("bundle_fingerprint", manual_seal)

            plan, tasks = self.materialize(root, "match")
            identity = plan_bundle_identity(plan, tasks)
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--expected-bundle-scheme",
                    identity["scheme"],
                    "--expected-bundle-fingerprint",
                    identity["fingerprint"],
                    "seal",
                    "match",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            seal = json.loads((root / ".plan-first" / "issues" / "match" / "state" / "seal.json").read_text())
            self.assertEqual(seal["bundle_fingerprint_scheme"], identity["scheme"])
            self.assertEqual(seal["bundle_fingerprint"], identity["fingerprint"])
            self.assertEqual(seal["plan_hash"], identity["files"]["plan.md"])
            self.assertEqual(seal["task_hash"], identity["files"]["tasks.md"])

            stale_plan, stale_tasks = self.materialize(root, "stale")
            stale_identity = plan_bundle_identity(stale_plan, stale_tasks)
            stale_plan.write_text("# Changed after review\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--expected-bundle-scheme",
                    stale_identity["scheme"],
                    "--expected-bundle-fingerprint",
                    stale_identity["fingerprint"],
                    "seal",
                    "stale",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / ".plan-first" / "issues" / "stale" / "state" / "seal.json").exists())

    def test_read_only_identity_commands_do_not_touch_git_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            plan, tasks = self.materialize(root, "readonly")
            exclude = root / ".git" / "info" / "exclude"
            before = exclude.read_bytes()

            subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "bundle-fingerprint", "readonly"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(exclude.read_bytes(), before)

            exclude.unlink()
            subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "bundle-fingerprint", "readonly"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(exclude.exists())

            identity = plan_bundle_identity(plan, tasks)
            plan.write_text("# Changed after review\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--expected-bundle-scheme",
                    identity["scheme"],
                    "--expected-bundle-fingerprint",
                    identity["fingerprint"],
                    "seal",
                    "readonly",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(exclude.exists())
            self.assertFalse((root / ".plan-first" / "issues" / "readonly" / "state" / "seal.json").exists())


if __name__ == "__main__":
    unittest.main()
