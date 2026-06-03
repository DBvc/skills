#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Software Plan-First 中文工作流脚本。"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover
    tomllib = None

SCRIPT_DIR = Path(__file__).resolve().parent
REF_DIR = SCRIPT_DIR.parent / "references"

DEFAULT_CONFIG: Dict[str, Any] = {
    "version": 1,
    "paths": {"plan_root": "plans", "state_dir": ".plan-first"},
    "git": {"mode": "auto-commit", "plan_files": "tracked"},
    "commit": {
        "plan_subject": "plan: issue-{issue_id} 新增执行计划",
        "task_subject": "work: issue-{issue_id} 完成 {task_id}",
        "include_default_body": True,
    },
    "project": {"rules": [".plan-first/rules.md", "AGENTS.md", "README.md"]},
}

CN_NO_VALIDATION = "# 无程序化验证:"
EN_NO_VALIDATION = "# no-programmatic-validation:"


def die(message: str, code: int = 1) -> None:
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(code)


def info(message: str) -> None:
    print(message)


def run(cmd: List[str], cwd: Optional[Path] = None, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, check=check,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)


def repo_root() -> Path:
    try:
        cp = run(["git", "rev-parse", "--show-toplevel"])
    except subprocess.CalledProcessError:
        die("必须在 Git 仓库中执行。")
    return Path(cp.stdout.strip())



def ensure_local_exclude(root: Path, cfg: Dict[str, Any]) -> None:
    """把 workflow 本地状态目录加入 .git/info/exclude，避免 seal/review cache 污染工作区。"""
    state_dir = str(cfg.get("paths", {}).get("state_dir", ".plan-first")).strip().strip("/")
    if not state_dir:
        return
    pattern = f"/{state_dir}/issues/"
    exclude_path = root / ".git" / "info" / "exclude"
    try:
        exclude_path.parent.mkdir(parents=True, exist_ok=True)
        existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
        if pattern not in existing.splitlines():
            suffix = "" if existing.endswith("\n") or not existing else "\n"
            exclude_path.write_text(existing + suffix + pattern + "\n", encoding="utf-8")
    except Exception:
        # 这是本地工作区清洁度优化，失败时不应阻断主流程。
        return


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = json.loads(json.dumps(base, ensure_ascii=False))
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(root: Path) -> Dict[str, Any]:
    cfg_path = root / ".plan-first" / "config.toml"
    cfg = DEFAULT_CONFIG
    if cfg_path.exists():
        if tomllib is None:
            die("检测到 .plan-first/config.toml，但当前 Python 不支持 tomllib。请使用 Python 3.11+。")
        try:
            data = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception as exc:
            die(f"无法解析 {cfg_path}: {exc}")
        cfg = deep_merge(DEFAULT_CONFIG, data)
    git_mode = cfg.get("git", {}).get("mode")
    if git_mode not in {"auto-commit", "manual-commit"}:
        die('配置 git.mode 只能是 "auto-commit" 或 "manual-commit"。')
    plan_files = cfg.get("git", {}).get("plan_files")
    if plan_files not in {"tracked", "local"}:
        die('配置 git.plan_files 只能是 "tracked" 或 "local"。')
    return cfg


def rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace(os.sep, "/")


@dataclasses.dataclass
class Paths:
    issue_id: str
    root: Path
    cfg: Dict[str, Any]
    plan_dir: Path
    plan_file: Path
    task_file: Path
    runs_dir: Path
    state_dir: Path
    issue_state_dir: Path
    seal_file: Path
    review_state_file: Path
    validation_log: Path


def issue_paths(issue_id: str, root: Path, cfg: Dict[str, Any]) -> Paths:
    state_dir = root / cfg["paths"]["state_dir"]
    plan_files = cfg["git"]["plan_files"]
    if plan_files == "local":
        plan_dir = state_dir / "issues" / f"issue-{issue_id}"
    else:
        plan_dir = root / cfg["paths"]["plan_root"] / f"issue-{issue_id}"
    issue_state_dir = state_dir / "issues" / f"issue-{issue_id}" / "state"
    return Paths(
        issue_id=issue_id,
        root=root,
        cfg=cfg,
        plan_dir=plan_dir,
        plan_file=plan_dir / "plan.md",
        task_file=plan_dir / "tasks.md",
        runs_dir=plan_dir / "runs",
        state_dir=state_dir,
        issue_state_dir=issue_state_dir,
        seal_file=issue_state_dir / "seal.json",
        review_state_file=issue_state_dir / "review-state.json",
        validation_log=issue_state_dir / "validation.log",
    )


def ensure_templates() -> Tuple[Path, Path]:
    plan_template = REF_DIR / "plan-template.md"
    tasks_template = REF_DIR / "tasks-template.md"
    if not plan_template.exists():
        die(f"缺少计划模板：{plan_template}")
    if not tasks_template.exists():
        die(f"缺少任务模板：{tasks_template}")
    return plan_template, tasks_template


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclasses.dataclass
class Task:
    number: int
    line_index: int
    status: str
    task_id: str
    summary: str
    accept: Optional[str]
    validates: List[str]
    use_checks: List[str]
    depends: List[str]
    constraints: List[str]


def strip_label(line: str, labels: Tuple[str, ...]) -> Optional[str]:
    for label in labels:
        if line.startswith(label):
            return line[len(label):].strip()
    return None


def parse_tasks(task_file: Path, require_valid: bool = True) -> List[Task]:
    if not task_file.exists():
        die(f"找不到 tasks.md：{task_file}")
    lines = task_file.read_text(encoding="utf-8").splitlines()
    tasks: List[Task] = []
    current: Optional[Task] = None
    header_re = re.compile(r"^(?:任务:\s*|Task:\s*)?- \[([ xX])\] \[([^\]]+)\]\s*(.*)$")
    for idx, raw in enumerate(lines):
        line = raw.strip()
        m = header_re.match(line)
        if m:
            current = Task(
                number=len(tasks) + 1,
                line_index=idx,
                status="done" if m.group(1).lower() == "x" else "todo",
                task_id=m.group(2).strip(),
                summary=m.group(3).strip(),
                accept=None,
                validates=[],
                use_checks=[],
                depends=[],
                constraints=[],
            )
            tasks.append(current)
            continue
        if current is None:
            continue
        value = strip_label(line, ("验收:", "Accept:"))
        if value is not None:
            if current.accept is not None and require_valid:
                die(f"任务 [{current.task_id}] 只能有一行 验收:。")
            current.accept = value
            continue
        value = strip_label(line, ("验证:", "Validate:"))
        if value is not None:
            current.validates.append(value)
            continue
        value = strip_label(line, ("使用检查:", "Use-Check:"))
        if value is not None:
            current.use_checks.append(value)
            continue
        value = strip_label(line, ("依赖:", "Depends:"))
        if value is not None:
            current.depends.append(value)
            continue
        value = strip_label(line, ("约束:", "Constraint:"))
        if value is not None:
            current.constraints.append(value)
            continue
    if require_valid:
        if not tasks:
            die("tasks.md 中没有结构化任务。请用 `- [ ] [task-id] 摘要` 格式填写任务。")
        seen = set()
        for task in tasks:
            if task.task_id in seen:
                die(f"任务 id 重复：{task.task_id}")
            seen.add(task.task_id)
            if not task.accept:
                die(f"任务 [{task.task_id}] 缺少 `验收:`。")
            if not task.validates:
                die(f"任务 [{task.task_id}] 至少需要一行 `验证:`。")
    return tasks


def first_unchecked(tasks: List[Task]) -> Optional[Task]:
    for task in tasks:
        if task.status == "todo":
            return task
    return None


def completed_count(tasks: List[Task]) -> int:
    return sum(1 for t in tasks if t.status == "done")


def write_seal(paths: Paths, reason: str) -> None:
    paths.issue_state_dir.mkdir(parents=True, exist_ok=True)
    seal = {
        "version": 1,
        "issue_id": paths.issue_id,
        "created_or_updated_at": utc_now(),
        "reason": reason,
        "plan_file": rel(paths.root, paths.plan_file),
        "task_file": rel(paths.root, paths.task_file),
        "plan_hash": sha256_file(paths.plan_file),
        "task_hash": sha256_file(paths.task_file),
        "git_mode": paths.cfg["git"]["mode"],
        "plan_files": paths.cfg["git"]["plan_files"],
    }
    paths.seal_file.write_text(json.dumps(seal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_seal(paths: Paths) -> Dict[str, Any]:
    if not paths.seal_file.exists():
        die(f"当前 issue 尚未 seal：{paths.seal_file}\n请先运行 `scripts/issue-workflow.sh seal {paths.issue_id}`。")
    return json.loads(paths.seal_file.read_text(encoding="utf-8"))


def verify_seal(paths: Paths) -> Dict[str, Any]:
    seal = load_seal(paths)
    if not paths.plan_file.exists() or not paths.task_file.exists():
        die("plan.md 或 tasks.md 不存在，无法校验 seal。")
    plan_hash = sha256_file(paths.plan_file)
    task_hash = sha256_file(paths.task_file)
    if plan_hash != seal.get("plan_hash"):
        die("plan.md 与 seal 不一致。请不要在实现阶段静默改计划；需要重新 finalize/seal。")
    if task_hash != seal.get("task_hash"):
        die("tasks.md 与 seal 不一致。`tasks.md` 只能由 workflow complete 更新；需要重新 seal 或恢复文件。")
    return seal


def render_template(template: str, issue_id: str, task: Optional[Task] = None) -> str:
    values = {
        "issue_id": issue_id,
        "task_id": task.task_id if task else "",
        "task_summary": task.summary if task else "",
    }
    out = template
    for k, v in values.items():
        out = out.replace("{" + k + "}", v)
    return out


def git_status_names(root: Path, staged_only: bool = False) -> List[str]:
    if staged_only:
        cp = run(["git", "diff", "--cached", "--name-only"], cwd=root)
        return [x for x in cp.stdout.splitlines() if x.strip()]
    names: List[str] = []
    for cmd in (["git", "diff", "--name-only"], ["git", "diff", "--cached", "--name-only"], ["git", "ls-files", "--others", "--exclude-standard"]):
        cp = run(cmd, cwd=root)
        names.extend([x for x in cp.stdout.splitlines() if x.strip()])
    return sorted(set(names))


def should_exclude(paths: Paths, name: str) -> bool:
    norm = name.replace(os.sep, "/")
    state_rel = rel(paths.root, paths.state_dir) if paths.state_dir.exists() else paths.cfg["paths"]["state_dir"]
    state_rel = state_rel.rstrip("/")
    if norm == state_rel or norm.startswith(state_rel + "/"):
        return True
    # 当前 issue 的计划产物不属于 task 代码快照。
    plan_dir_rel = rel(paths.root, paths.plan_dir) if paths.plan_dir.exists() else str(paths.plan_dir.relative_to(paths.root)).replace(os.sep, "/")
    if norm == plan_dir_rel or norm.startswith(plan_dir_rel.rstrip("/") + "/"):
        return True
    return False


def changed_files(paths: Paths) -> List[str]:
    return [n for n in git_status_names(paths.root) if not should_exclude(paths, n)]


def hash_changed_files(root: Path, names: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for name in names:
        path = root / name
        if not path.exists():
            out[name] = "__deleted__"
        elif path.is_file():
            out[name] = sha256_file(path)
        else:
            out[name] = "__not_regular_file__"
    return out


def git_add(root: Path, files: List[str]) -> None:
    if not files:
        return
    run(["git", "add", "--"] + files, cwd=root, capture=True)


def git_commit(root: Path, subject: str, body: Optional[str]) -> bool:
    cp = run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False)
    if cp.returncode == 0:
        return False
    cmd = ["git", "commit", "-m", subject]
    if body:
        cmd += ["-m", body]
    run(cmd, cwd=root, capture=False)
    return True


def staged_non_allowed(root: Path, allowed: List[str]) -> List[str]:
    allowed_set = set(allowed)
    return [n for n in git_status_names(root, staged_only=True) if n not in allowed_set]


def parse_shared_checks(plan_file: Path) -> Dict[str, str]:
    checks: Dict[str, str] = {}
    current_id: Optional[str] = None
    for raw in plan_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        value = strip_label(line, ("检查:", "Check:"))
        if value is not None:
            current_id = value
            continue
        value = strip_label(line, ("命令:", "Command:"))
        if value is not None and current_id:
            checks[current_id] = value
            current_id = None
    return checks


def parse_final_validation(plan_file: Path) -> List[str]:
    lines = plan_file.read_text(encoding="utf-8").splitlines()
    in_section = False
    in_fence = False
    commands: List[str] = []
    for raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("## "):
            title = line.strip().lstrip("#").strip()
            if title in {"最终验证", "Final Validation"}:
                in_section = True
                in_fence = False
                continue
            elif in_section:
                break
        if not in_section:
            continue
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
            else:
                break
            continue
        if in_fence:
            if stripped:
                commands.append(stripped)
    return commands


def is_no_validation_marker(command: str) -> bool:
    stripped = command.strip()
    return stripped.startswith(CN_NO_VALIDATION) or stripped.startswith(EN_NO_VALIDATION)


def run_shell_command(root: Path, command: str, log_lines: List[str]) -> bool:
    log_lines.append(f"$ {command}")
    cp = subprocess.run(["bash", "-lc", command], cwd=str(root), text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if cp.stdout:
        log_lines.append(cp.stdout.rstrip())
    log_lines.append(f"退出码：{cp.returncode}")
    return cp.returncode == 0


def run_validations(paths: Paths, task: Task, is_last_task: bool) -> Tuple[bool, List[str], List[str]]:
    log_lines: List[str] = []
    summary: List[str] = []
    ok = True

    log_lines.append(f"# 验证日志：issue-{paths.issue_id} / task {task.task_id}")
    log_lines.append(f"时间：{utc_now()}")
    log_lines.append("")

    for command in task.validates:
        if is_no_validation_marker(command):
            summary.append(f"跳过程序化验证：{command}")
            log_lines.append(f"[review-only] {command}")
            continue
        passed = run_shell_command(paths.root, command, log_lines)
        summary.append(f"task 验证：{'通过' if passed else '失败'}：{command}")
        ok = ok and passed
        log_lines.append("")

    shared = parse_shared_checks(paths.plan_file)
    for check_id in task.use_checks:
        if check_id not in shared:
            log_lines.append(f"缺少 shared check：{check_id}")
            summary.append(f"shared check 失败：找不到 {check_id}")
            ok = False
            continue
        command = shared[check_id]
        if is_no_validation_marker(command):
            summary.append(f"shared check review-only：{check_id}")
            log_lines.append(f"[review-only shared {check_id}] {command}")
            continue
        passed = run_shell_command(paths.root, command, log_lines)
        summary.append(f"shared check {check_id}：{'通过' if passed else '失败'}")
        ok = ok and passed
        log_lines.append("")

    if is_last_task:
        final_commands = parse_final_validation(paths.plan_file)
        if not final_commands:
            log_lines.append("最后一个任务缺少最终验证命令。")
            summary.append("最终验证失败：缺少命令或 review-only marker")
            ok = False
        else:
            for command in final_commands:
                if is_no_validation_marker(command):
                    summary.append(f"最终验证 review-only：{command}")
                    log_lines.append(f"[review-only final] {command}")
                    continue
                passed = run_shell_command(paths.root, command, log_lines)
                summary.append(f"最终验证：{'通过' if passed else '失败'}：{command}")
                ok = ok and passed
                log_lines.append("")

    paths.issue_state_dir.mkdir(parents=True, exist_ok=True)
    paths.validation_log.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return ok, summary, log_lines


def mark_task_complete(paths: Paths, task: Task) -> None:
    lines = paths.task_file.read_text(encoding="utf-8").splitlines()
    line = lines[task.line_index]
    if "- [ ]" not in line:
        die(f"当前任务行不是未完成状态：{line}")
    lines[task.line_index] = line.replace("- [ ]", "- [x]", 1)
    paths.task_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def command_init(paths: Paths) -> None:
    plan_template, tasks_template = ensure_templates()
    paths.plan_dir.mkdir(parents=True, exist_ok=True)
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    paths.issue_state_dir.mkdir(parents=True, exist_ok=True)
    created = []
    if not paths.plan_file.exists():
        paths.plan_file.write_text(plan_template.read_text(encoding="utf-8"), encoding="utf-8")
        created.append(rel(paths.root, paths.plan_file))
    if not paths.task_file.exists():
        paths.task_file.write_text(tasks_template.read_text(encoding="utf-8"), encoding="utf-8")
        created.append(rel(paths.root, paths.task_file))
    if created:
        info("已创建中文计划过程产物：")
        for item in created:
            info(f"- {item}")
    else:
        info("计划过程产物已存在，未覆盖：")
        info(f"- {rel(paths.root, paths.plan_file)}")
        info(f"- {rel(paths.root, paths.task_file)}")
    info(f"配置：git.mode={paths.cfg['git']['mode']}，git.plan_files={paths.cfg['git']['plan_files']}")
    info("下一步：填写 plan.md/tasks.md 后运行 `scripts/issue-workflow.sh seal <issue-id>`。")


def command_seal(paths: Paths) -> None:
    if not paths.plan_file.exists() or not paths.task_file.exists():
        die("缺少 plan.md 或 tasks.md。请先运行 init 并填写计划。")
    tasks = parse_tasks(paths.task_file, require_valid=True)
    write_seal(paths, "finalize-plan seal")
    info("已写入 workflow seal：")
    info(f"- {rel(paths.root, paths.seal_file)}")
    info(f"任务数量：{len(tasks)}")
    mode = paths.cfg["git"]["mode"]
    plan_files = paths.cfg["git"]["plan_files"]
    if mode == "auto-commit" and plan_files == "tracked":
        plan_rel = rel(paths.root, paths.plan_file)
        task_rel = rel(paths.root, paths.task_file)
        allowed = [plan_rel, task_rel]
        unexpected = staged_non_allowed(paths.root, allowed)
        if unexpected:
            die("检测到非计划文件已 staged，不能自动提交计划：\n" + "\n".join(f"- {x}" for x in unexpected))
        git_add(paths.root, allowed)
        subject = render_template(paths.cfg["commit"]["plan_subject"], paths.issue_id)
        body = None
        if paths.cfg["commit"].get("include_default_body", True):
            body = f"中文 plan-first 过程产物已 seal。\n\nIssue: {paths.issue_id}\n任务数量: {len(tasks)}\n计划文件: {plan_rel}\n任务文件: {task_rel}"
        committed = git_commit(paths.root, subject, body)
        if committed:
            info(f"已自动提交计划：{subject}")
        else:
            info("没有新的计划文件变更需要提交。")
    else:
        subject = render_template(paths.cfg["commit"]["plan_subject"], paths.issue_id)
        info("当前配置不会自动提交计划。建议提交信息：")
        info(subject)


def command_status(paths: Paths) -> None:
    if not paths.plan_file.exists() or not paths.task_file.exists():
        info("当前 issue 尚未初始化。")
        info(f"建议运行：scripts/issue-workflow.sh init {paths.issue_id}")
        return
    sealed = paths.seal_file.exists()
    tasks = parse_tasks(paths.task_file, require_valid=False)
    next_task = first_unchecked(tasks)
    info(f"Issue: {paths.issue_id}")
    info(f"计划文件：{rel(paths.root, paths.plan_file)}")
    info(f"任务文件：{rel(paths.root, paths.task_file)}")
    info(f"配置：git.mode={paths.cfg['git']['mode']}，git.plan_files={paths.cfg['git']['plan_files']}")
    info(f"Seal：{'已建立' if sealed else '未建立'}")
    info(f"任务进度：{completed_count(tasks)}/{len(tasks)}")
    if next_task:
        info(f"下一个任务：[{next_task.task_id}] {next_task.summary}")
    elif tasks:
        info("所有任务已完成。")
    else:
        info("尚未填写结构化任务。")


def command_next(paths: Paths) -> None:
    verify_seal(paths)
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成。")
        return
    info(f"当前任务 #{task.number}: [{task.task_id}] {task.summary}")
    info(f"验收：{task.accept}")
    for command in task.validates:
        info(f"验证：{command}")
    for check_id in task.use_checks:
        info(f"使用检查：{check_id}")
    for dep in task.depends:
        info(f"依赖：{dep}")
    for c in task.constraints:
        info(f"约束：{c}")


def command_notes_template(paths: Paths) -> None:
    verify_seal(paths)
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成，无需 notes template。")
        return
    print(textwrap.dedent(f"""
    # 当前任务笔记

    Issue: {paths.issue_id}
    Task: [{task.task_id}] {task.summary}

    ## 开始前确认

    - 工作区状态：<git status 摘要>
    - 影响边界：<本 task 触达范围>
    - source of truth：<本 task 使用的项目事实>

    ## 实现摘要

    - <改动 1>
    - <改动 2>

    ## 验证

    - <命令或 review-only 证据>

    ## 风险 / 待 review

    - <需要用户 review 的内容>
    """).strip())


def command_review_ready(paths: Paths) -> None:
    verify_seal(paths)
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成，无需 review-ready。")
        return
    is_last = completed_count(tasks) == len(tasks) - 1
    ok, summary, _ = run_validations(paths, task, is_last)
    if not ok:
        info("验证失败，未生成 review-ready。验证日志：")
        info(f"- {rel(paths.root, paths.validation_log)}")
        raise SystemExit(1)

    names = changed_files(paths)
    snapshot = hash_changed_files(paths.root, names)
    review = {
        "version": 1,
        "issue_id": paths.issue_id,
        "task_number": task.number,
        "task_id": task.task_id,
        "task_summary": task.summary,
        "created_at": utc_now(),
        "plan_hash": sha256_file(paths.plan_file),
        "task_hash": sha256_file(paths.task_file),
        "changed_files": snapshot,
        "validation_summary": summary,
        "validation_log": rel(paths.root, paths.validation_log),
        "git_mode": paths.cfg["git"]["mode"],
        "plan_files": paths.cfg["git"]["plan_files"],
    }
    paths.issue_state_dir.mkdir(parents=True, exist_ok=True)
    paths.review_state_file.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if paths.cfg["git"]["mode"] == "auto-commit":
        unexpected = staged_non_allowed(paths.root, names)
        if unexpected:
            die("检测到不属于当前 review snapshot 的 staged 文件，不能继续：\n" + "\n".join(f"- {x}" for x in unexpected))
        git_add(paths.root, names)
        info("已 stage 当前 review snapshot 的变更文件。")
    else:
        info("manual-commit 模式：未 stage 文件，只记录 review snapshot hash。")

    info("状态：review-ready")
    info(f"当前任务：[{task.task_id}] {task.summary}")
    info("验证结果：")
    for item in summary:
        info(f"- {item}")
    if names:
        info("变更文件快照：")
        for name in names:
            info(f"- {name}")
    else:
        info("变更文件快照：无代码文件变更。")
    info(f"验证日志：{rel(paths.root, paths.validation_log)}")
    info("用户 review 通过后运行：")
    info(f"scripts/issue-workflow.sh complete {paths.issue_id}")


def command_complete(paths: Paths) -> None:
    verify_seal(paths)
    if not paths.review_state_file.exists():
        die("缺少 review-ready 快照。请先运行 review-ready。")
    review = json.loads(paths.review_state_file.read_text(encoding="utf-8"))
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成。")
        return
    if review.get("task_id") != task.task_id or review.get("task_number") != task.number:
        die("review-ready 的任务与当前第一个未完成任务不一致。请重新 review-ready。")
    if review.get("plan_hash") != sha256_file(paths.plan_file) or review.get("task_hash") != sha256_file(paths.task_file):
        die("review-ready 后 plan.md 或 tasks.md 发生变化。请重新 review-ready。")
    names = list(review.get("changed_files", {}).keys())
    current_snapshot = hash_changed_files(paths.root, names)
    if current_snapshot != review.get("changed_files"):
        die("review-ready 后变更文件内容发生变化。请重新 review-ready。")

    mark_task_complete(paths, task)
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    evidence_file = paths.runs_dir / f"task-{task.number:03d}-{task.task_id}.md"
    evidence = [
        f"# 任务完成证据：{task.task_id}",
        "",
        f"- Issue: {paths.issue_id}",
        f"- 任务序号: {task.number}",
        f"- 任务摘要: {task.summary}",
        f"- 完成时间: {utc_now()}",
        f"- 验证日志: {review.get('validation_log')}",
        "",
        "## 验收",
        "",
        f"- {task.accept}",
        "",
        "## 验证摘要",
        "",
    ]
    for item in review.get("validation_summary", []):
        evidence.append(f"- {item}")
    evidence += ["", "## 变更文件", ""]
    if names:
        for name in names:
            evidence.append(f"- {name}")
    else:
        evidence.append("- 无代码文件变更")
    evidence += ["", "## 备注", "", "- complete 复用了 review-ready 时的快照和验证缓存。"]
    evidence_file.write_text("\n".join(evidence) + "\n", encoding="utf-8")

    write_seal(paths, f"complete task {task.task_id}")

    mode = paths.cfg["git"]["mode"]
    plan_files = paths.cfg["git"]["plan_files"]
    if mode == "auto-commit":
        files_to_stage = names[:]
        if plan_files == "tracked":
            files_to_stage += [rel(paths.root, paths.task_file), rel(paths.root, evidence_file)]
        # 只允许 review snapshot 文件和当前 workflow 产物进入提交。
        unexpected = staged_non_allowed(paths.root, files_to_stage)
        if unexpected:
            die("检测到不属于当前任务的 staged 文件，不能自动提交：\n" + "\n".join(f"- {x}" for x in unexpected))
        git_add(paths.root, files_to_stage)
        subject = render_template(paths.cfg["commit"]["task_subject"], paths.issue_id, task)
        body = None
        if paths.cfg["commit"].get("include_default_body", True):
            body = "\n".join([
                "中文 plan-first 任务完成。",
                "",
                f"Issue: {paths.issue_id}",
                f"Task: {task.task_id}",
                f"Evidence: {rel(paths.root, evidence_file)}",
            ])
        committed = git_commit(paths.root, subject, body)
        if committed:
            info(f"已自动提交任务：{subject}")
        else:
            info("没有新的代码变更需要提交。")
    else:
        subject = render_template(paths.cfg["commit"]["task_subject"], paths.issue_id, task)
        info("manual-commit 模式：未自动提交。建议提交信息：")
        info(subject)

    # complete 后清理 review state，避免重复完成。
    try:
        paths.review_state_file.unlink()
    except FileNotFoundError:
        pass

    tasks_after = parse_tasks(paths.task_file, require_valid=True)
    next_task = first_unchecked(tasks_after)
    info("状态：complete")
    info(f"已完成任务：[{task.task_id}] {task.summary}")
    info(f"证据文件：{rel(paths.root, evidence_file)}")
    if next_task:
        info(f"下一个任务：[{next_task.task_id}] {next_task.summary}")
    else:
        info("所有任务已完成。")


def main() -> None:
    parser = argparse.ArgumentParser(description="Software Plan-First 中文工作流")
    parser.add_argument("command", nargs="?", help="init|seal|status|next|notes-template|review-ready|complete，或直接传 issue-id 查看 status")
    parser.add_argument("issue_id", nargs="?")
    args = parser.parse_args()

    if not args.command:
        print("用法：scripts/issue-workflow.sh <command> <issue-id>")
        raise SystemExit(2)

    commands = {"init", "seal", "status", "next", "notes-template", "review-ready", "complete"}
    if args.command in commands:
        command = args.command
        issue_id = args.issue_id
    else:
        command = "status"
        issue_id = args.command
    if not issue_id:
        die("缺少 issue-id。")

    root = repo_root()
    cfg = load_config(root)
    ensure_local_exclude(root, cfg)
    paths = issue_paths(issue_id, root, cfg)

    if command == "init":
        command_init(paths)
    elif command == "seal":
        command_seal(paths)
    elif command == "status":
        command_status(paths)
    elif command == "next":
        command_next(paths)
    elif command == "notes-template":
        command_notes_template(paths)
    elif command == "review-ready":
        command_review_ready(paths)
    elif command == "complete":
        command_complete(paths)
    else:
        die(f"未知命令：{command}")


if __name__ == "__main__":
    main()
