#!/usr/bin/env python3
"""Fixture tests for task-start gates. Usage: python3 test_implementation_gate.py"""

import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Optional, Tuple


SCRIPT = Path(__file__).with_name("issue_workflow.py")


class ImplementationGateTest(unittest.TestCase):
    def run_workflow(self, root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def make_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "--quiet", str(root)], check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
        (root / "src").mkdir()
        (root / "src" / "app.py").write_text("old\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/app.py"], cwd=root, check=True)
        subprocess.run(["git", "commit", "--quiet", "-m", "base"], cwd=root, check=True)

    def materialize(
        self,
        root: Path,
        issue_id: str,
        task_type: str,
        programmatic: bool = True,
        command: Optional[str] = None,
        allowed_paths: Optional[Tuple[str, ...]] = None,
        required_paths: Optional[Tuple[str, ...]] = None,
    ) -> Path:
        self.run_workflow(root, "init", issue_id)
        issue_dir = root / ".plan-first" / "issues" / issue_id
        command = command or (
            "test -f src/app.py" if programmatic else "# 无程序化验证: fixture review evidence"
        )
        if allowed_paths is None:
            allowed_paths = ("src/app.py",) if task_type in {"step", "loop-batch"} else ()
        if required_paths is None:
            required_paths = ("src/app.py",) if task_type in {"step", "loop-batch"} else ()
        scope_lines = "".join(f"约束: allowed-path={path}\n" for path in allowed_paths)
        scope_lines += "".join(f"约束: required-path={path}\n" for path in required_paths)
        (issue_dir / "plan.md").write_text(
            "# Plan\n\n## 最终验证\n\n```sh\n" + command + "\n```\n",
            encoding="utf-8",
        )
        (issue_dir / "tasks.md").write_text(
            f"- [ ] [t1] Fixture task\n"
            f"验收: 任务类型={task_type}; fixture accepted\n"
            f"验证: {command}\n"
            "依赖: none\n"
            + scope_lines,
            encoding="utf-8",
        )
        self.run_workflow(root, "seal", issue_id)
        return issue_dir

    def test_sealed_code_task_records_delta_and_real_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "code", "step", programmatic=True)

            self.run_workflow(root, "begin-implementation", "code")
            start_file = issue_dir / "state" / "seal.json"
            baseline = start_file.read_bytes()
            (root / "src" / "app.py").write_text("new\n", encoding="utf-8")

            repeated = self.run_workflow(root, "begin-implementation", "code")
            self.assertIn("保持原 baseline", repeated.stdout)
            self.assertEqual(start_file.read_bytes(), baseline)
            reseal = self.run_workflow(root, "seal", "code", check=False)
            self.assertNotEqual(reseal.returncode, 0)
            self.assertIn("不能重新 seal", reseal.stderr)
            self.assertEqual(start_file.read_bytes(), baseline)

            ready = self.run_workflow(root, "review-ready", "code")
            self.assertIn("状态：review-ready", ready.stdout)
            review = json.loads((issue_dir / "state" / "review-ready.json").read_text(encoding="utf-8"))
            self.assertEqual(review["version"], 5)
            self.assertEqual(review["task_type"], "step")
            implementation = json.loads(start_file.read_text(encoding="utf-8"))["implementation"]
            self.assertEqual(
                implementation["task_scope"],
                {
                    "scheme": "workspace-relative-path-v1",
                    "allowed_paths": ["src/app.py"],
                    "required_paths": ["src/app.py"],
                },
            )
            self.assertEqual(set(implementation["repo_heads"]), {"."})
            changed = {
                name
                for payload in review["implementation_delta"].values()
                for name in payload["files"]
            }
            self.assertEqual(changed, {"src/app.py"})
            self.assertGreaterEqual(review["validation_evidence"]["programmatic_successes"], 1)
            self.assertEqual(review["implementation_scope"], implementation["task_scope"])
            self.assertIn("implementation_repo_state", review)
            complete = self.run_workflow(root, "complete", "code")
            self.assertIn("状态：complete", complete.stdout)

    def test_code_task_without_post_baseline_delta_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "no-code", "loop-batch", programmatic=True)
            self.run_workflow(root, "begin-implementation", "no-code")

            result = self.run_workflow(root, "review-ready", "no-code", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("没有验证前可归因实现 delta", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())

    def test_auto_mode_snapshots_the_post_validation_staged_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            (root / ".plan-first").mkdir()
            (root / ".plan-first" / "config.toml").write_text(
                'version = 1\n\n[workspace]\ncommit = "auto"\n\n[plan_docs]\nmode = "local"\n',
                encoding="utf-8",
            )
            self.materialize(root, "auto", "step")
            self.run_workflow(root, "begin-implementation", "auto")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")

            ready = self.run_workflow(root, "review-ready", "auto")
            self.assertIn("已 stage 当前 review snapshot", ready.stdout)
            complete = self.run_workflow(root, "complete", "auto")
            self.assertIn("状态：complete", complete.stdout)
            self.assertEqual(
                subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout,
                "",
            )

    def test_validation_cannot_create_or_rewrite_implementation_delta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            creator = self.materialize(
                root,
                "validation-creates",
                "step",
                command="printf 'from-validation\\n' > src/app.py",
            )
            self.run_workflow(root, "begin-implementation", "validation-creates")

            result = self.run_workflow(root, "review-ready", "validation-creates", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("没有验证前可归因实现 delta", result.stderr)
            self.assertEqual((root / "src" / "app.py").read_text(encoding="utf-8"), "old\n")
            self.assertFalse((creator / "state" / "review-ready.json").exists())

            rewriter = self.materialize(
                root,
                "validation-rewrites",
                "step",
                command="printf 'from-validation\\n' > src/app.py",
            )
            self.run_workflow(root, "begin-implementation", "validation-rewrites")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")
            result = self.run_workflow(root, "review-ready", "validation-rewrites", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("验证期间 repo HEAD、index 或 Git 可见 workspace 发生变化", result.stderr)
            self.assertFalse((rewriter / "state" / "review-ready.json").exists())

    def test_validation_cannot_change_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "validation-stages", "step", command="git add src/app.py")
            self.run_workflow(root, "begin-implementation", "validation-stages")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")

            result = self.run_workflow(root, "review-ready", "validation-stages", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("验证期间 repo HEAD、index 或 Git 可见 workspace 发生变化", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())

    def test_delta_must_stay_allowed_and_hit_every_required_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            outside = self.materialize(root, "outside", "step")
            self.run_workflow(root, "begin-implementation", "outside")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")
            (root / "src" / "other.py").write_text("outside\n", encoding="utf-8")

            result = self.run_workflow(root, "review-ready", "outside", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("超出 sealed allowed-path", result.stderr)
            self.assertFalse((outside / "state" / "review-ready.json").exists())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            missed = self.materialize(
                root,
                "required",
                "step",
                allowed_paths=("src/",),
                required_paths=("src/app.py",),
            )
            self.run_workflow(root, "begin-implementation", "required")
            (root / "src" / "other.py").write_text("allowed-but-not-required\n", encoding="utf-8")

            result = self.run_workflow(root, "review-ready", "required", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("没有命中 sealed required-path", result.stderr)
            self.assertFalse((missed / "state" / "review-ready.json").exists())

    def test_task_start_dirty_or_untracked_path_cannot_disappear(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "dirty-revert", "documentation-only", programmatic=False)
            (root / "src" / "app.py").write_text("preexisting dirty\n", encoding="utf-8")
            self.run_workflow(root, "begin-implementation", "dirty-revert")
            subprocess.run(["git", "restore", "src/app.py"], cwd=root, check=True)

            result = self.run_workflow(root, "review-ready", "dirty-revert", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task-start baseline 中已有的 Git 可见路径在实现期间消失", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "untracked-delete", "step")
            secret = root / "src" / "secret.py"
            secret.write_text("user work\n", encoding="utf-8")
            self.run_workflow(root, "begin-implementation", "untracked-delete")
            secret.unlink()
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")

            result = self.run_workflow(root, "review-ready", "untracked-delete", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task-start baseline 中已有的 Git 可见路径在实现期间消失", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())

    def test_only_owner_execute_bit_is_a_git_relevant_delta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "group-executable", "step")
            app = root / "src" / "app.py"
            app.write_text("preexisting dirty\n", encoding="utf-8")
            self.run_workflow(root, "begin-implementation", "group-executable")
            app.chmod(0o654)

            ignored = self.run_workflow(root, "review-ready", "group-executable", check=False)
            self.assertNotEqual(ignored.returncode, 0)
            self.assertIn("没有验证前可归因实现 delta", ignored.stderr)

            app.chmod(0o754)
            ready = self.run_workflow(root, "review-ready", "group-executable")
            self.assertIn("状态：review-ready", ready.stdout)
            review = json.loads(
                (issue_dir / "state" / "review-ready.json").read_text(encoding="utf-8")
            )
            self.assertIn("src/app.py", review["implementation_delta"]["."]["files"])

    def test_code_task_without_machine_readable_scope_cannot_be_sealed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            self.run_workflow(root, "init", "missing-scope")
            issue_dir = root / ".plan-first" / "issues" / "missing-scope"
            (issue_dir / "plan.md").write_text(
                "# Plan\n\n## 最终验证\n\n```sh\ntest -f src/app.py\n```\n",
                encoding="utf-8",
            )
            (issue_dir / "tasks.md").write_text(
                "- [ ] [t1] Missing scope\n"
                "验收: 任务类型=step; done\n"
                "验证: test -f src/app.py\n"
                "依赖: none\n",
                encoding="utf-8",
            )

            result = self.run_workflow(root, "seal", "missing-scope", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("必须声明机器可读的 allowed-path 和 required-path", result.stderr)
            self.assertFalse((issue_dir / "state" / "seal.json").exists())

    def test_head_change_after_begin_is_rejected_even_when_commit_hides_delta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "early-commit", "step")
            self.run_workflow(root, "begin-implementation", "early-commit")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")
            subprocess.run(["git", "add", "src/app.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "--quiet", "-m", "too early"], cwd=root, check=True)

            result = self.run_workflow(root, "review-ready", "early-commit", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("begin-implementation 后 repo HEAD 已变化", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())

    def test_no_code_task_with_git_visible_delta_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "docs-with-code", "documentation-only", programmatic=False)
            self.run_workflow(root, "begin-implementation", "docs-with-code")
            (root / "src" / "app.py").write_text("unexpected\n", encoding="utf-8")

            result = self.run_workflow(root, "review-ready", "docs-with-code", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("无代码任务 [t1] 检测到 Git 可见实现 delta", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())

    def test_validation_runner_enforces_total_timeout_and_output_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            timeout_issue = self.materialize(
                root,
                "timeout",
                "step",
                command="python3 -c 'import time; time.sleep(30)'",
            )
            self.run_workflow(root, "begin-implementation", "timeout")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")

            started = time.monotonic()
            result = self.run_workflow(
                root,
                "--validation-timeout-seconds",
                "1",
                "review-ready",
                "timeout",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertLess(time.monotonic() - started, 5)
            timeout_log = (timeout_issue / "state" / "validation.log").read_text(encoding="utf-8")
            self.assertIn("超过总超时预算", timeout_log)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            output_issue = self.materialize(
                root,
                "output",
                "step",
                command="python3 -c 'print(\"x\" * 100000)'",
            )
            self.run_workflow(root, "begin-implementation", "output")
            (root / "src" / "app.py").write_text("implemented\n", encoding="utf-8")

            result = self.run_workflow(
                root,
                "--validation-output-bytes",
                "512",
                "review-ready",
                "output",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            output_log_path = output_issue / "state" / "validation.log"
            output_log = output_log_path.read_text(encoding="utf-8")
            self.assertIn("验证输出超过总上限 512 bytes", output_log)
            self.assertLess(output_log_path.stat().st_size, 4096)

    def test_documentation_only_task_may_be_review_ready_without_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "docs", "documentation-only", programmatic=False)
            self.run_workflow(root, "begin-implementation", "docs")

            ready = self.run_workflow(root, "review-ready", "docs")
            self.assertIn("documentation-only 无 Git 可见实现 delta", ready.stdout)
            review = json.loads((issue_dir / "state" / "review-ready.json").read_text(encoding="utf-8"))
            self.assertEqual(review["implementation_delta"], {})
            self.assertEqual(review["validation_evidence"]["programmatic_successes"], 0)
            self.assertTrue(any("review" in item or "跳过" in item for item in review["validation_summary"]))

    def test_code_delta_with_review_only_validation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            issue_dir = self.materialize(root, "review-only-code", "step", programmatic=False)
            self.run_workflow(root, "begin-implementation", "review-only-code")
            (root / "src" / "app.py").write_text("new\n", encoding="utf-8")

            result = self.run_workflow(root, "review-ready", "review-only-code", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("没有真实程序化验证成功记录", result.stderr)
            self.assertFalse((issue_dir / "state" / "review-ready.json").exists())


if __name__ == "__main__":
    unittest.main()
