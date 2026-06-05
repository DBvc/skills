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
    "workspace": {"commit": "manual"},
    "commit": {
        "task_subject": "work: issue-{issue_id} 完成 {task_id}",
        "default_type": "chore",
        "include_body": True,
        "body_template": "\n".join([
            "中文 plan-first 任务完成。",
            "",
            "Issue: {issue_id}",
            "Task: {task_id}",
            "Evidence: {evidence_file}",
        ]),
    },
}

CN_NO_VALIDATION = "# 无程序化验证:"
EN_NO_VALIDATION = "# no-programmatic-validation:"
CONFIG_REL = Path(".plan-first") / "config.toml"
ISSUES_REL = Path(".plan-first") / "issues"
ISSUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def die(message: str, code: int = 1) -> None:
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(code)


def info(message: str) -> None:
    print(message)


def run(cmd: List[str], cwd: Optional[Path] = None, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        check=check,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def git_root_for(path: Path) -> Optional[Path]:
    if not path.exists():
        return None
    cp = run(["git", "rev-parse", "--show-toplevel"], cwd=path, check=False)
    if cp.returncode != 0:
        return None
    value = cp.stdout.strip()
    if not value:
        return None
    return Path(value).resolve()


def find_config_root(start: Path) -> Optional[Path]:
    current = start.resolve()
    candidates = [current] + list(current.parents)
    for candidate in candidates:
        if (candidate / CONFIG_REL).exists():
            return candidate
    return None


def multi_repo_parent(git_root: Path) -> Optional[Path]:
    current = git_root.resolve()
    candidates = [current.parent, current.parent.parent]
    for candidate in candidates:
        repos = discover_repos(candidate)
        repo_roots = {repo.root for repo in repos}
        if current in repo_roots and len(repo_roots) > 1:
            return candidate
    return None


def default_config_text() -> str:
    return textwrap.dedent("""\
    version = 1

    [workspace]
    commit = "manual"
    """)


def ensure_root_marker_config(root: Path) -> Optional[Path]:
    cfg_path = root / CONFIG_REL
    if cfg_path.exists():
        return None
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(default_config_text(), encoding="utf-8")
    return cfg_path


def resolve_workspace_root(cli_root: Optional[str], allow_cwd_bootstrap: bool = False) -> Path:
    if cli_root:
        return Path(cli_root).expanduser().resolve()
    env_root = os.environ.get("PLAN_FIRST_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    config_root = find_config_root(Path.cwd())
    if config_root:
        return config_root
    git_root = git_root_for(Path.cwd())
    if git_root:
        parent = multi_repo_parent(git_root) if allow_cwd_bootstrap else None
        if parent is not None:
            die(f"当前目录位于未初始化的多 repo workspace 子仓库。首次 init 请在 workspace root 执行，或传 --root {parent}。")
        return git_root
    if allow_cwd_bootstrap:
        return Path.cwd().resolve()
    die("找不到 workspace root。请在 workspace 根创建 .plan-first/config.toml，或传 --root。")


def reject_unknown(data: Dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(data.keys()) - allowed)
    if unknown:
        die(f"{label} 包含不支持的配置字段：{', '.join(unknown)}。")


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = json.loads(json.dumps(base, ensure_ascii=False))
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def parse_scalar(raw: str, cfg_path: Path, line_no: int) -> Any:
    value = raw.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value.isdigit():
        return int(value)
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    die(f"无法解析 {cfg_path}:{line_no} 的值：{raw}")


def strip_inline_comment(value: str) -> str:
    in_quote = False
    escaped = False
    for idx, ch in enumerate(value):
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"':
            in_quote = not in_quote
            continue
        if ch == "#" and not in_quote:
            return value[:idx].rstrip()
    return value


def parse_minimal_toml(text: str, cfg_path: Path) -> Dict[str, Any]:
    """Python 3.11 以下的极简 TOML fallback，只支持本 workflow 的配置形状。"""
    data: Dict[str, Any] = {}
    current: Dict[str, Any] = data
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line_no = i + 1
        stripped = raw.strip()
        i += 1
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            if not section or "." in section:
                die(f"不支持的 TOML section：{stripped}")
            current = data.setdefault(section, {})
            if not isinstance(current, dict):
                die(f"TOML section 与字段冲突：{section}")
            continue
        if "=" not in stripped:
            die(f"无法解析 {cfg_path}:{line_no}：{raw}")
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = strip_inline_comment(value.strip())
        if not key:
            die(f"无法解析 {cfg_path}:{line_no}：缺少 key")
        if value.startswith('"""'):
            content = value[3:]
            collected: List[str] = []
            if content.endswith('"""') and len(content) >= 3:
                current[key] = content[:-3]
                continue
            if content:
                collected.append(content)
            while i < len(lines):
                next_line = lines[i]
                i += 1
                end = next_line.find('"""')
                if end >= 0:
                    collected.append(next_line[:end])
                    current[key] = "\n".join(collected)
                    break
                collected.append(next_line)
            else:
                die(f"未闭合的 triple-quoted string：{cfg_path}:{line_no}")
            continue
        current[key] = parse_scalar(value, cfg_path, line_no)
    return data


def parse_config_text(text: str, cfg_path: Path) -> Dict[str, Any]:
    if tomllib is not None:
        return tomllib.loads(text)
    return parse_minimal_toml(text, cfg_path)


def load_config(root: Path) -> Dict[str, Any]:
    cfg_path = root / CONFIG_REL
    cfg = DEFAULT_CONFIG
    if cfg_path.exists():
        try:
            data = parse_config_text(cfg_path.read_text(encoding="utf-8"), cfg_path)
        except Exception as exc:
            die(f"无法解析 {cfg_path}: {exc}")
        if not isinstance(data, dict):
            die(f"{cfg_path} 必须是 TOML table。")
        reject_unknown(data, {"version", "workspace", "commit"}, "config.toml")
        if "workspace" in data:
            reject_unknown(data["workspace"], {"commit"}, "workspace")
        if "commit" in data:
            reject_unknown(data["commit"], {"task_subject", "default_type", "include_body", "body_template"}, "commit")
        cfg = deep_merge(DEFAULT_CONFIG, data)
    if cfg.get("version") != 1:
        die("配置 version 只能是 1。")
    commit_mode = cfg.get("workspace", {}).get("commit")
    if commit_mode not in {"none", "manual", "auto"}:
        die('配置 workspace.commit 只能是 "none"、"manual" 或 "auto"。')
    commit_cfg = cfg.get("commit", {})
    if not isinstance(commit_cfg.get("task_subject"), str) or not commit_cfg.get("task_subject", "").strip():
        die("配置 commit.task_subject 必须是非空字符串。")
    if "default_type" in commit_cfg and commit_cfg["default_type"] is not None and not isinstance(commit_cfg["default_type"], str):
        die("配置 commit.default_type 必须是字符串。")
    if not isinstance(commit_cfg.get("include_body"), bool):
        die("配置 commit.include_body 必须是 boolean。")
    if not isinstance(commit_cfg.get("body_template"), str):
        die("配置 commit.body_template 必须是字符串。")
    return cfg


def rel(root: Path, path: Path) -> str:
    root_resolved = root.resolve()
    path_resolved = path.resolve()
    try:
        return str(path_resolved.relative_to(root_resolved)).replace(os.sep, "/")
    except ValueError:
        return str(path_resolved)


@dataclasses.dataclass(frozen=True)
class Repo:
    name: str
    root: Path
    rel_path: str


@dataclasses.dataclass
class Context:
    root: Path
    cfg: Dict[str, Any]
    repos: List[Repo]


def repo_name_for(root: Path, repo_root: Path) -> str:
    rp = rel(root, repo_root)
    return "." if rp == "." else rp


def add_repo(root: Path, repo_root: Path, repos: List[Repo], seen: set[Path]) -> None:
    repo_root = repo_root.resolve()
    if repo_root in seen:
        return
    seen.add(repo_root)
    rp = rel(root, repo_root)
    repos.append(Repo(name=repo_name_for(root, repo_root), root=repo_root, rel_path=rp))


def child_dirs(path: Path) -> List[Path]:
    skip = {".git", ".plan-first", "node_modules", "dist", "build", "coverage", ".venv", "vendor", "target"}
    if not path.exists() or not path.is_dir():
        return []
    out: List[Path] = []
    for child in sorted(path.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        if child.name in skip:
            continue
        if child.name.startswith(".") or child.name.startswith(".__"):
            continue
        out.append(child)
    return out


def discover_repos(root: Path) -> List[Repo]:
    root = root.resolve()
    repos: List[Repo] = []
    seen: set[Path] = set()
    root_git = git_root_for(root)
    if root_git and root_git == root:
        add_repo(root, root, repos, seen)
        return repos

    direct_non_git: List[Path] = []
    for child in child_dirs(root):
        child_git = git_root_for(child)
        if child_git and child_git == child.resolve():
            add_repo(root, child_git, repos, seen)
        else:
            direct_non_git.append(child)

    for parent in direct_non_git:
        for child in child_dirs(parent):
            child_git = git_root_for(child)
            if child_git and child_git == child.resolve():
                add_repo(root, child_git, repos, seen)

    return repos


def git_exclude_path(repo_root: Path) -> Optional[Path]:
    cp = run(["git", "rev-parse", "--git-path", "info/exclude"], cwd=repo_root, check=False)
    if cp.returncode != 0:
        return None
    raw = cp.stdout.strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = repo_root / path
    return path


def ensure_local_exclude(ctx: Context) -> None:
    """如果 workspace root 本身是 Git repo，把本地 issue 状态加入本地 exclude。"""
    root_repo = next((repo for repo in ctx.repos if repo.root == ctx.root.resolve()), None)
    if root_repo is None:
        return
    exclude_path = git_exclude_path(root_repo.root)
    if exclude_path is None:
        return
    pattern = "/.plan-first/"
    try:
        exclude_path.parent.mkdir(parents=True, exist_ok=True)
        existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
        if pattern not in existing.splitlines():
            suffix = "" if existing.endswith("\n") or not existing else "\n"
            exclude_path.write_text(existing + suffix + pattern + "\n", encoding="utf-8")
    except Exception:
        # 这是本地工作区清洁度优化，失败时不应阻断主流程。
        return


def build_context(cli_root: Optional[str], allow_cwd_bootstrap: bool = False) -> Context:
    root = resolve_workspace_root(cli_root, allow_cwd_bootstrap=allow_cwd_bootstrap)
    if not root.exists():
        die(f"workspace root 不存在：{root}")
    if not root.is_dir():
        die(f"workspace root 必须是目录：{root}")
    cfg = load_config(root)
    ctx = Context(root=root.resolve(), cfg=cfg, repos=discover_repos(root))
    ensure_local_exclude(ctx)
    return ctx


@dataclasses.dataclass
class Paths:
    issue_id: str
    plan_dir: Path
    plan_file: Path
    task_file: Path
    runs_dir: Path
    state_dir: Path
    seal_file: Path
    review_state_file: Path
    pending_complete_file: Path
    validation_log: Path


def issue_paths(issue_id: str, ctx: Context) -> Paths:
    if issue_id in {".", ".."} or not ISSUE_ID_RE.match(issue_id):
        die("issue-id 只能是单个安全路径段：字母/数字开头，可包含字母、数字、点、下划线或连字符。")
    issues_root = (ctx.root / ISSUES_REL).resolve()
    issue_dir = (issues_root / issue_id).resolve()
    try:
        issue_dir.relative_to(issues_root)
    except ValueError:
        die("issue-id 不能逃逸 .plan-first/issues 目录。")
    state_dir = issue_dir / "state"
    return Paths(
        issue_id=issue_id,
        plan_dir=issue_dir,
        plan_file=issue_dir / "plan.md",
        task_file=issue_dir / "tasks.md",
        runs_dir=issue_dir / "runs",
        state_dir=state_dir,
        seal_file=state_dir / "seal.json",
        review_state_file=state_dir / "review-ready.json",
        pending_complete_file=state_dir / "complete-pending.json",
        validation_log=state_dir / "validation.log",
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
    commit_type: Optional[str]


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
                commit_type=None,
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
        value = strip_label(line, ("提交类型:", "Commit-Type:", "Commit type:", "Commit-Type:"))
        if value is not None:
            if current.commit_type is not None and require_valid:
                die(f"任务 [{current.task_id}] 只能有一行 提交类型:。")
            current.commit_type = value
            continue
    if require_valid:
        if not tasks:
            die("tasks.md 中没有结构化任务。请用 `- [ ] [task-id] 摘要` 格式填写任务。")
        seen = set()
        type_re = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
        for task in tasks:
            if task.task_id in seen:
                die(f"任务 id 重复：{task.task_id}")
            seen.add(task.task_id)
            if not task.accept:
                die(f"任务 [{task.task_id}] 缺少 `验收:`。")
            if not task.validates:
                die(f"任务 [{task.task_id}] 至少需要一行 `验证:`。")
            if task.commit_type and not type_re.match(task.commit_type):
                die(f"任务 [{task.task_id}] 的 `提交类型:` 只能包含字母、数字、下划线或连字符，并以字母开头。")
    return tasks


def first_unchecked(tasks: List[Task]) -> Optional[Task]:
    for task in tasks:
        if task.status == "todo":
            return task
    return None


def completed_count(tasks: List[Task]) -> int:
    return sum(1 for t in tasks if t.status == "done")


def repo_payload(ctx: Context) -> List[Dict[str, str]]:
    return [{"name": repo.name, "path": repo.rel_path} for repo in ctx.repos]


def repo_manifest_map(payload: Any) -> Optional[Dict[str, str]]:
    if not isinstance(payload, list):
        return None
    out: Dict[str, str] = {}
    for item in payload:
        if not isinstance(item, dict):
            return None
        name = item.get("name")
        path = item.get("path")
        if not isinstance(name, str) or not isinstance(path, str):
            return None
        out[name] = path
    return out


def write_seal(ctx: Context, paths: Paths, reason: str) -> None:
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    seal = {
        "version": 1,
        "issue_id": paths.issue_id,
        "created_or_updated_at": utc_now(),
        "reason": reason,
        "workspace_root": str(ctx.root),
        "plan_file": rel(ctx.root, paths.plan_file),
        "task_file": rel(ctx.root, paths.task_file),
        "plan_hash": sha256_file(paths.plan_file),
        "task_hash": sha256_file(paths.task_file),
        "commit_mode": ctx.cfg["workspace"]["commit"],
        "repos": repo_payload(ctx),
    }
    paths.seal_file.write_text(json.dumps(seal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_seal(paths: Paths) -> Dict[str, Any]:
    if not paths.seal_file.exists():
        die(f"当前 issue 尚未 seal：{paths.seal_file}\n请先运行 `scripts/issue-workflow.sh seal {paths.issue_id}`。")
    return json.loads(paths.seal_file.read_text(encoding="utf-8"))


def verify_seal(ctx: Context, paths: Paths) -> Dict[str, Any]:
    seal = load_seal(paths)
    if seal.get("version") != 1:
        die("seal version 不支持；请重新 init/seal 当前 issue。")
    if not paths.plan_file.exists() or not paths.task_file.exists():
        die("plan.md 或 tasks.md 不存在，无法校验 seal。")
    plan_hash = sha256_file(paths.plan_file)
    task_hash = sha256_file(paths.task_file)
    if plan_hash != seal.get("plan_hash"):
        die("plan.md 与 seal 不一致。请不要在实现阶段静默改计划；需要重新 finalize/seal。")
    if task_hash != seal.get("task_hash"):
        die("tasks.md 与 seal 不一致。`tasks.md` 只能由 workflow complete 更新；需要重新 seal 或恢复文件。")
    if seal.get("workspace_root") != str(ctx.root):
        die("当前 workspace root 与 seal 不一致。请在正确 root 下执行，或重新 seal。")
    return seal


TEMPLATE_RE = re.compile(r"{([A-Za-z_][A-Za-z0-9_]*)}")


def task_commit_type(ctx: Context, task: Optional[Task]) -> str:
    if task is None:
        return ""
    value = task.commit_type or ctx.cfg["commit"].get("default_type") or ""
    return value.strip()


def render_template(
    ctx: Context,
    template: str,
    issue_id: str,
    task: Optional[Task] = None,
    evidence_file: str = "",
    validation_log: str = "",
    changed_files: str = "",
) -> str:
    values = {
        "issue_id": issue_id,
        "task_id": task.task_id if task else "",
        "task_summary": task.summary if task else "",
        "commit_type": task_commit_type(ctx, task),
        "evidence_file": evidence_file,
        "validation_log": validation_log,
        "changed_files": changed_files,
    }

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            die(f"提交模板包含未知变量：{key}")
        if key == "commit_type" and not values[key]:
            die("提交模板使用了 {commit_type}，但当前 task 未写 `提交类型:`，且 commit.default_type 为空。")
        return values[key]

    return TEMPLATE_RE.sub(replace, template)


def render_task_subject(ctx: Context, issue_id: str, task: Task) -> str:
    return render_template(ctx, ctx.cfg["commit"]["task_subject"], issue_id, task).strip()


def render_task_body(
    ctx: Context,
    issue_id: str,
    task: Task,
    evidence_file: str,
    validation_log: str,
    changed_files: str,
) -> Optional[str]:
    if not ctx.cfg["commit"].get("include_body", True):
        return None
    body = render_template(
        ctx,
        ctx.cfg["commit"].get("body_template", ""),
        issue_id,
        task,
        evidence_file=evidence_file,
        validation_log=validation_log,
        changed_files=changed_files,
    ).strip()
    return body or None


def git_status_names(repo: Repo, staged_only: bool = False) -> List[str]:
    if staged_only:
        cp = run(["git", "diff", "--cached", "--name-only"], cwd=repo.root)
        return [x for x in cp.stdout.splitlines() if x.strip()]
    names: List[str] = []
    for cmd in (
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        cp = run(cmd, cwd=repo.root)
        names.extend([x for x in cp.stdout.splitlines() if x.strip()])
    return sorted(set(names))


def should_exclude(ctx: Context, repo: Repo, name: str) -> bool:
    if repo.root != ctx.root:
        return False
    norm = name.replace(os.sep, "/")
    return norm == ".plan-first" or norm.startswith(".plan-first/")


def selected_repos(ctx: Context, selected_repo: Optional[str]) -> List[Repo]:
    if selected_repo is None:
        return ctx.repos
    matches = [
        repo for repo in ctx.repos
        if selected_repo in {repo.name, repo.rel_path} or (repo.name == "." and selected_repo == ctx.root.name)
    ]
    if not matches:
        available = ", ".join(repo.name for repo in ctx.repos) or "无"
        die(f"找不到 repo：{selected_repo}。可用 repo：{available}")
    return matches


def changed_files(ctx: Context, repos: List[Repo]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for repo in repos:
        names = [n for n in git_status_names(repo) if not should_exclude(ctx, repo, n)]
        if names:
            out[repo.name] = names
    return out


def status_files(ctx: Context, repo: Repo) -> List[str]:
    return [n for n in git_status_names(repo) if not should_exclude(ctx, repo, n)]


def hash_changed_files(repo: Repo, names: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for name in names:
        path = repo.root / name
        if not path.exists():
            out[name] = "__deleted__"
        elif path.is_file():
            out[name] = sha256_file(path)
        else:
            out[name] = "__not_regular_file__"
    return out


def snapshot_repos(ctx: Context, repos: List[Repo]) -> Dict[str, Dict[str, Any]]:
    snapshot: Dict[str, Dict[str, Any]] = {}
    for repo in repos:
        names = status_files(ctx, repo)
        snapshot[repo.name] = {
            "path": repo.rel_path,
            "files": hash_changed_files(repo, names),
        }
    return snapshot


def non_empty_snapshot(snapshot: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {repo_name: payload for repo_name, payload in snapshot.items() if payload.get("files")}


def changed_files_text(changed_repos: Dict[str, Dict[str, Any]]) -> str:
    lines: List[str] = []
    for repo_name in sorted(changed_repos):
        files = changed_repos[repo_name].get("files", {})
        for name in sorted(files):
            lines.append(f"{repo_name}:{name}")
    return "\n".join(lines)


def git_add(repo: Repo, files: List[str]) -> None:
    if not files:
        return
    run(["git", "add", "--"] + files, cwd=repo.root, capture=True)


def git_commit(repo: Repo, subject: str, body: Optional[str]) -> bool:
    cp = run(["git", "diff", "--cached", "--quiet"], cwd=repo.root, check=False)
    if cp.returncode == 0:
        return False
    cmd = ["git", "commit", "-m", subject]
    if body:
        cmd += ["-m", body]
    run(cmd, cwd=repo.root, capture=False)
    return True


def staged_non_allowed(repo: Repo, allowed: List[str]) -> List[str]:
    allowed_set = set(allowed)
    return [n for n in git_status_names(repo, staged_only=True) if n not in allowed_set]


def commit_auto_changes(ctx: Context, changed_repos: Dict[str, Dict[str, Any]], subject: str, body: Optional[str]) -> List[str]:
    repos_by_name = {repo.name: repo for repo in ctx.repos}
    messages: List[str] = []
    for repo_name, payload in changed_repos.items():
        repo = repos_by_name[repo_name]
        files = sorted(payload.get("files", {}).keys())
        unexpected = staged_non_allowed(repo, files)
        if unexpected:
            die("检测到不属于当前任务的 staged 文件，不能自动提交：\n" + "\n".join(f"- {repo.name}:{x}" for x in unexpected))
        current_names = set(git_status_names(repo))
        git_add(repo, [name for name in files if name in current_names])
        committed = git_commit(repo, subject, body)
        if committed:
            messages.append(f"已自动提交任务到 {repo.name}：{subject}")
        else:
            messages.append(f"{repo.name} 没有新的代码变更需要提交。")
    if not changed_repos:
        messages.append("没有代码变更需要自动提交。")
    return messages


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


def run_shell_command(ctx: Context, command: str, log_lines: List[str]) -> bool:
    log_lines.append(f"$ {command}")
    cp = subprocess.run(
        ["bash", "-lc", command],
        cwd=str(ctx.root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if cp.stdout:
        log_lines.append(cp.stdout.rstrip())
    log_lines.append(f"退出码：{cp.returncode}")
    return cp.returncode == 0


def run_validations(ctx: Context, paths: Paths, task: Task, is_last_task: bool) -> Tuple[bool, List[str], List[str]]:
    log_lines: List[str] = []
    summary: List[str] = []
    ok = True

    log_lines.append(f"# 验证日志：issue {paths.issue_id} / task {task.task_id}")
    log_lines.append(f"时间：{utc_now()}")
    log_lines.append(f"Workspace root：{ctx.root}")
    log_lines.append("")

    for command in task.validates:
        if is_no_validation_marker(command):
            summary.append(f"跳过程序化验证：{command}")
            log_lines.append(f"[review-only] {command}")
            continue
        passed = run_shell_command(ctx, command, log_lines)
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
        passed = run_shell_command(ctx, command, log_lines)
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
                passed = run_shell_command(ctx, command, log_lines)
                summary.append(f"最终验证：{'通过' if passed else '失败'}：{command}")
                ok = ok and passed
                log_lines.append("")

    paths.state_dir.mkdir(parents=True, exist_ok=True)
    paths.validation_log.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return ok, summary, log_lines


def mark_task_complete(paths: Paths, task: Task) -> None:
    lines = paths.task_file.read_text(encoding="utf-8").splitlines()
    line = lines[task.line_index]
    if "- [ ]" not in line:
        die(f"当前任务行不是未完成状态：{line}")
    lines[task.line_index] = line.replace("- [ ]", "- [x]", 1)
    paths.task_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def command_init(ctx: Context, paths: Paths) -> None:
    plan_template, tasks_template = ensure_templates()
    marker = ensure_root_marker_config(ctx.root)
    paths.plan_dir.mkdir(parents=True, exist_ok=True)
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    created = []
    if marker is not None:
        created.append(rel(ctx.root, marker))
    if not paths.plan_file.exists():
        paths.plan_file.write_text(plan_template.read_text(encoding="utf-8"), encoding="utf-8")
        created.append(rel(ctx.root, paths.plan_file))
    if not paths.task_file.exists():
        paths.task_file.write_text(tasks_template.read_text(encoding="utf-8"), encoding="utf-8")
        created.append(rel(ctx.root, paths.task_file))
    if created:
        info("已创建中文计划过程产物：")
        for item in created:
            info(f"- {item}")
    else:
        info("计划过程产物已存在，未覆盖：")
        info(f"- {rel(ctx.root, paths.plan_file)}")
        info(f"- {rel(ctx.root, paths.task_file)}")
    info(f"Workspace root：{ctx.root}")
    info(f"提交模式：workspace.commit={ctx.cfg['workspace']['commit']}")
    info("下一步：填写 plan.md/tasks.md 后运行 `scripts/issue-workflow.sh seal <issue-id>`。")


def command_seal(ctx: Context, paths: Paths) -> None:
    if not paths.plan_file.exists() or not paths.task_file.exists():
        die("缺少 plan.md 或 tasks.md。请先运行 init 并填写计划。")
    tasks = parse_tasks(paths.task_file, require_valid=True)
    write_seal(ctx, paths, "finalize-plan seal")
    info("已写入 workflow seal：")
    info(f"- {rel(ctx.root, paths.seal_file)}")
    info(f"任务数量：{len(tasks)}")
    info("计划过程产物是本地 workflow 状态，不自动提交。")


def command_status(ctx: Context, paths: Paths) -> None:
    if not paths.plan_file.exists() or not paths.task_file.exists():
        info("当前 issue 尚未初始化。")
        info(f"Workspace root：{ctx.root}")
        info(f"建议运行：scripts/issue-workflow.sh init {paths.issue_id}")
        return
    sealed = paths.seal_file.exists()
    tasks = parse_tasks(paths.task_file, require_valid=False)
    next_task = first_unchecked(tasks)
    info(f"Issue: {paths.issue_id}")
    info(f"Workspace root：{ctx.root}")
    info(f"计划文件：{rel(ctx.root, paths.plan_file)}")
    info(f"任务文件：{rel(ctx.root, paths.task_file)}")
    info(f"提交模式：workspace.commit={ctx.cfg['workspace']['commit']}")
    if ctx.repos:
        info("Git repos：")
        for repo in ctx.repos:
            info(f"- {repo.name}: {repo.rel_path}")
    else:
        info("Git repos：未发现")
    info(f"Seal：{'已建立' if sealed else '未建立'}")
    info(f"任务进度：{completed_count(tasks)}/{len(tasks)}")
    if next_task:
        info(f"下一个任务：[{next_task.task_id}] {next_task.summary}")
    elif tasks:
        info("所有任务已完成。")
    else:
        info("尚未填写结构化任务。")


def command_next(ctx: Context, paths: Paths) -> None:
    verify_seal(ctx, paths)
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成。")
        return
    info(f"当前任务 #{task.number}: [{task.task_id}] {task.summary}")
    info(f"验收：{task.accept}")
    if task.commit_type:
        info(f"提交类型：{task.commit_type}")
    for command in task.validates:
        info(f"验证：{command}")
    for check_id in task.use_checks:
        info(f"使用检查：{check_id}")
    for dep in task.depends:
        info(f"依赖：{dep}")
    for c in task.constraints:
        info(f"约束：{c}")


def command_notes_template(ctx: Context, paths: Paths) -> None:
    verify_seal(ctx, paths)
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

    - 工作区状态：<每个相关 repo 的 git status 摘要>
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


def prepare_review_repos(ctx: Context, selected_repo: Optional[str]) -> List[Repo]:
    mode = ctx.cfg["workspace"]["commit"]
    if mode in {"manual", "none"} and selected_repo is not None:
        die(f"workspace.commit={mode} 必须 review 整个 workspace；--repo 只允许 auto 模式使用。")
    repos = selected_repos(ctx, selected_repo)
    if mode == "auto":
        if not repos:
            die("workspace.commit=auto 需要至少一个 Git repo。")
        if len(repos) != 1:
            die("多 repo workspace 下 workspace.commit=auto 必须为 review-ready 显式传 --repo <name>。")
    return repos


def command_review_ready(ctx: Context, paths: Paths, selected_repo: Optional[str]) -> None:
    verify_seal(ctx, paths)
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成，无需 review-ready。")
        return
    repos = prepare_review_repos(ctx, selected_repo)
    is_last = completed_count(tasks) == len(tasks) - 1
    ok, summary, _ = run_validations(ctx, paths, task, is_last)
    if not ok:
        info("验证失败，未生成 review-ready。验证日志：")
        info(f"- {rel(ctx.root, paths.validation_log)}")
        raise SystemExit(1)

    snapshot = snapshot_repos(ctx, repos)
    changed_snapshot = non_empty_snapshot(snapshot)
    if ctx.cfg["workspace"]["commit"] == "auto":
        repo = repos[0]
        names = sorted(snapshot.get(repo.name, {}).get("files", {}).keys())
        unexpected = staged_non_allowed(repo, names)
        if unexpected:
            die("检测到不属于当前 review snapshot 的 staged 文件，不能继续：\n" + "\n".join(f"- {repo.name}:{x}" for x in unexpected))
    review = {
        "version": 3,
        "issue_id": paths.issue_id,
        "task_number": task.number,
        "task_id": task.task_id,
        "task_summary": task.summary,
        "commit_type": task_commit_type(ctx, task),
        "created_at": utc_now(),
        "plan_hash": sha256_file(paths.plan_file),
        "task_hash": sha256_file(paths.task_file),
        "workspace_repos": repo_payload(ctx),
        "reviewed_repos": [repo.name for repo in repos],
        "repo_snapshots": snapshot,
        "changed_repos": changed_snapshot,
        "validation_summary": summary,
        "validation_log": rel(ctx.root, paths.validation_log),
        "commit_mode": ctx.cfg["workspace"]["commit"],
    }
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    paths.review_state_file.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if ctx.cfg["workspace"]["commit"] == "auto":
        repo = repos[0]
        names = sorted(snapshot.get(repo.name, {}).get("files", {}).keys())
        git_add(repo, names)
        info(f"已 stage 当前 review snapshot 的变更文件：{repo.name}")
    else:
        info(f"{ctx.cfg['workspace']['commit']} 模式：未 stage 文件，只记录 review snapshot hash。")

    info("状态：review-ready")
    info(f"当前任务：[{task.task_id}] {task.summary}")
    if task.commit_type:
        info(f"提交类型：{task.commit_type}")
    info("验证结果：")
    for item in summary:
        info(f"- {item}")
    changed_text = changed_files_text(changed_snapshot)
    if changed_text:
        info("变更文件快照：")
        for line in changed_text.splitlines():
            info(f"- {line}")
    else:
        info("变更文件快照：无代码文件变更。")
    info(f"验证日志：{rel(ctx.root, paths.validation_log)}")
    info("用户 review 通过后运行：")
    info(f"scripts/issue-workflow.sh complete {paths.issue_id}")


def verify_review_snapshot(ctx: Context, review: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    if review.get("version") != 3:
        die("review-ready 快照版本已过期。请重新运行 review-ready。")
    repos_by_name = {repo.name: repo for repo in ctx.repos}
    if review.get("commit_mode") in {"manual", "none"}:
        expected_manifest = repo_manifest_map(review.get("workspace_repos"))
        current_manifest = repo_manifest_map(repo_payload(ctx))
        if expected_manifest is None:
            die("review-ready 快照格式错误：缺少 workspace_repos。")
        if current_manifest != expected_manifest:
            die("review-ready 后 workspace repo 边界发生变化。请重新 review-ready。")
    reviewed_repos = review.get("reviewed_repos")
    repo_snapshots = review.get("repo_snapshots")
    if not isinstance(reviewed_repos, list) or not all(isinstance(x, str) for x in reviewed_repos):
        die("review-ready 快照格式错误：缺少 reviewed_repos。")
    if not isinstance(repo_snapshots, dict):
        die("review-ready 快照格式错误：缺少 repo_snapshots。")

    repos: List[Repo] = []
    for repo_name in reviewed_repos:
        if repo_name not in repos_by_name:
            die(f"review-ready 中的 repo 不存在于当前 workspace：{repo_name}")
        if repo_name not in repo_snapshots:
            die(f"review-ready 中缺少 repo {repo_name} 的快照。")
        repos.append(repos_by_name[repo_name])

    expected = {name: repo_snapshots[name] for name in reviewed_repos}
    for repo_name, payload in expected.items():
        files = payload.get("files", {})
        if not isinstance(files, dict):
            die(f"review-ready 中 repo {repo_name} 的 files 格式错误。")
        if payload.get("path") != repos_by_name[repo_name].rel_path:
            die(f"review-ready 中 repo {repo_name} 的路径与当前 workspace 不一致。请重新 review-ready。")

    current = snapshot_repos(ctx, repos)
    if current != expected:
        die("review-ready 后被 review 的 repo diff 边界发生变化。请重新 review-ready。")
    return repo_snapshots


def build_evidence_lines(ctx: Context, paths: Paths, task: Task, review: Dict[str, Any], changed_text: str) -> List[str]:
    evidence = [
        f"# 任务完成证据：{task.task_id}",
        "",
        f"- Issue: {paths.issue_id}",
        f"- 任务序号: {task.number}",
        f"- 任务摘要: {task.summary}",
        f"- 提交类型: {task_commit_type(ctx, task) or '未设置'}",
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
    if changed_text:
        for line in changed_text.splitlines():
            evidence.append(f"- {line}")
    else:
        evidence.append("- 无代码文件变更")
    evidence += ["", "## 备注", "", "- complete 复用了 review-ready 时的快照和验证缓存。"]
    return evidence


def write_complete_pending(
    paths: Paths,
    task: Task,
    changed_repos: Dict[str, Dict[str, Any]],
    subject: str,
    body: Optional[str],
    evidence_rel: str,
    evidence: List[str],
) -> None:
    pending = {
        "version": 1,
        "issue_id": paths.issue_id,
        "task_number": task.number,
        "task_id": task.task_id,
        "subject": subject,
        "body": body,
        "changed_repos": changed_repos,
        "evidence_file": evidence_rel,
        "evidence": evidence,
        "created_at": utc_now(),
    }
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    paths.pending_complete_file.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resume_auto_pending_if_ready(ctx: Context, paths: Paths) -> bool:
    if not paths.pending_complete_file.exists():
        return False
    pending = json.loads(paths.pending_complete_file.read_text(encoding="utf-8"))
    if pending.get("version") != 1 or pending.get("issue_id") != paths.issue_id:
        die("complete-pending 状态格式错误。")
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = next((item for item in tasks if item.task_id == pending.get("task_id")), None)
    if task is None:
        die("complete-pending 指向的 task 不存在。")
    if task.status != "done":
        paths.pending_complete_file.unlink()
        return False
    if ctx.cfg["workspace"]["commit"] != "auto":
        die("存在 auto complete-pending，但当前 workspace.commit 不是 auto。")

    evidence_rel = str(pending.get("evidence_file", ""))
    evidence_file = ctx.root / evidence_rel if evidence_rel else paths.runs_dir / f"task-{task.number:03d}-{task.task_id}.md"
    evidence = pending.get("evidence", [])
    if isinstance(evidence, list) and all(isinstance(line, str) for line in evidence):
        evidence_file.parent.mkdir(parents=True, exist_ok=True)
        evidence_file.write_text("\n".join(evidence) + "\n", encoding="utf-8")
    write_seal(ctx, paths, f"complete task {task.task_id}")

    changed_repos = pending.get("changed_repos", {})
    if not isinstance(changed_repos, dict):
        die("complete-pending 中 changed_repos 格式错误。")
    body = pending.get("body")
    if body is not None and not isinstance(body, str):
        die("complete-pending 中 body 格式错误。")
    messages = commit_auto_changes(ctx, changed_repos, str(pending.get("subject", "")), body)
    for message in messages:
        info(message)
    try:
        paths.review_state_file.unlink()
    except FileNotFoundError:
        pass
    paths.pending_complete_file.unlink()
    info("状态：complete")
    info(f"已恢复完成任务：[{task.task_id}] {task.summary}")
    info(f"证据文件：{rel(ctx.root, evidence_file)}")
    return True


def command_complete(ctx: Context, paths: Paths) -> None:
    if resume_auto_pending_if_ready(ctx, paths):
        return
    verify_seal(ctx, paths)
    tasks = parse_tasks(paths.task_file, require_valid=True)
    task = first_unchecked(tasks)
    if not task:
        info("所有任务已完成。")
        return
    if not paths.review_state_file.exists():
        die("缺少 review-ready 快照。请先运行 review-ready。")
    review = json.loads(paths.review_state_file.read_text(encoding="utf-8"))
    if review.get("task_id") != task.task_id or review.get("task_number") != task.number:
        die("review-ready 的任务与当前第一个未完成任务不一致。请重新 review-ready。")
    if review.get("plan_hash") != sha256_file(paths.plan_file) or review.get("task_hash") != sha256_file(paths.task_file):
        die("review-ready 后 plan.md 或 tasks.md 发生变化。请重新 review-ready。")
    mode = ctx.cfg["workspace"]["commit"]
    if review.get("commit_mode") != mode:
        die("当前 workspace.commit 与 review-ready 时不一致。请重新 review-ready。")
    repo_snapshots = verify_review_snapshot(ctx, review)
    changed_repos = non_empty_snapshot(repo_snapshots)
    changed_text = changed_files_text(changed_repos)
    evidence_file = paths.runs_dir / f"task-{task.number:03d}-{task.task_id}.md"
    evidence_rel = rel(ctx.root, evidence_file)

    subject: Optional[str] = None
    body: Optional[str] = None
    if mode in {"manual", "auto"}:
        subject = render_task_subject(ctx, paths.issue_id, task)
        body = render_task_body(
            ctx,
            paths.issue_id,
            task,
            evidence_file=evidence_rel,
            validation_log=str(review.get("validation_log", "")),
            changed_files=changed_text,
        )

    repos_by_name = {repo.name: repo for repo in ctx.repos}
    if mode == "auto":
        if len(changed_repos) > 1:
            die("workspace.commit=auto 不允许一次 complete 多个 repo；请重新 review-ready --repo <name>。")
        for repo_name, payload in changed_repos.items():
            repo = repos_by_name[repo_name]
            files = sorted(payload.get("files", {}).keys())
            unexpected = staged_non_allowed(repo, files)
            if unexpected:
                die("检测到不属于当前任务的 staged 文件，不能自动提交：\n" + "\n".join(f"- {repo.name}:{x}" for x in unexpected))

    evidence = build_evidence_lines(ctx, paths, task, review, changed_text)
    if mode == "auto":
        write_complete_pending(paths, task, changed_repos, subject or "", body, evidence_rel, evidence)

    mark_task_complete(paths, task)
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    evidence_file.write_text("\n".join(evidence) + "\n", encoding="utf-8")

    write_seal(ctx, paths, f"complete task {task.task_id}")

    if mode == "auto":
        auto_messages = commit_auto_changes(ctx, changed_repos, subject or "", body)
        for message in auto_messages:
            info(message)
        try:
            paths.pending_complete_file.unlink()
        except FileNotFoundError:
            pass
    elif mode == "manual":
        info("manual 模式：未自动提交。建议提交信息：")
        info(subject or "")
        if changed_repos:
            info("涉及 repo：")
            for repo_name in sorted(changed_repos):
                info(f"- {repo_name}")
    else:
        info("none 模式：未 stage、未提交，也不生成提交建议。")

    try:
        paths.review_state_file.unlink()
    except FileNotFoundError:
        pass

    tasks_after = parse_tasks(paths.task_file, require_valid=True)
    next_task = first_unchecked(tasks_after)
    info("状态：complete")
    info(f"已完成任务：[{task.task_id}] {task.summary}")
    info(f"证据文件：{evidence_rel}")
    if next_task:
        info(f"下一个任务：[{next_task.task_id}] {next_task.summary}")
    else:
        info("所有任务已完成。")


def main() -> None:
    parser = argparse.ArgumentParser(description="Software Plan-First 中文工作流")
    parser.add_argument("--root", help="workspace root；默认向上查找 .plan-first/config.toml，找不到则使用当前 Git root；init 可在非 Git cwd bootstrap")
    parser.add_argument("--repo", help="仅 auto 模式可用；限制 review-ready 的 Git repo，多 repo auto commit 时必填")
    parser.add_argument("command", nargs="?", help="init|seal|status|next|notes-template|review-ready|complete，或直接传 issue-id 查看 status")
    parser.add_argument("issue_id", nargs="?")
    args = parser.parse_args()

    if not args.command:
        print("用法：scripts/issue-workflow.sh [--root ROOT] [--repo NAME] <command> <issue-id>")
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

    ctx = build_context(args.root, allow_cwd_bootstrap=command == "init")
    paths = issue_paths(issue_id, ctx)

    if command == "init":
        command_init(ctx, paths)
    elif command == "seal":
        command_seal(ctx, paths)
    elif command == "status":
        command_status(ctx, paths)
    elif command == "next":
        command_next(ctx, paths)
    elif command == "notes-template":
        command_notes_template(ctx, paths)
    elif command == "review-ready":
        command_review_ready(ctx, paths, args.repo)
    elif command == "complete":
        command_complete(ctx, paths)
    else:
        die(f"未知命令：{command}")


if __name__ == "__main__":
    main()
