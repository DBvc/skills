#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读 workspace/repo 上下文扫描器：输出 hints，不做最终判断。

Usage: python3 scripts/repo_context.py [--root ROOT]
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
from typing import List, Optional

CONFIG_REL = Path(".plan-first") / "config.toml"
MANIFESTS = [
    "package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "bun.lockb", "bun.lock",
    "pyproject.toml", "requirements.txt", "uv.lock", "Pipfile", "poetry.lock",
    "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle",
    "Gemfile", "composer.json", "deno.json", "nx.json", "turbo.json",
    "Makefile", "Dockerfile", "docker-compose.yml", "compose.yaml",
]
DOCS = ["AGENTS.md", "README.md", "CONTRIBUTING.md", "ARCHITECTURE.md", "docs", ".plan-first/rules.md"]
CONTRACT_HINTS = ["openapi", "swagger", "graphql", "schema", "proto", "protobuf", "migrations", "prisma", "drizzle"]
TEST_HINTS = ["test", "tests", "spec", "e2e", "cypress", "playwright", "vitest", "jest", "pytest"]
SOURCE_DIRS = ["src", "app", "apps", "packages", "services", "server", "client", "frontend", "backend", "lib", "cmd", "internal"]


def run_git_root(path: Path) -> Optional[Path]:
    cp = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(path),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if cp.returncode != 0:
        return None
    value = cp.stdout.strip()
    return Path(value).resolve() if value else None


def find_config_root(start: Path) -> Optional[Path]:
    current = start.resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / CONFIG_REL).exists():
            return candidate
    return None


def resolve_root(cli_root: Optional[str]) -> Path:
    if cli_root:
        return Path(cli_root).expanduser().resolve()
    env_root = os.environ.get("PLAN_FIRST_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    config_root = find_config_root(Path.cwd())
    if config_root:
        return config_root
    git_root = run_git_root(Path.cwd())
    if git_root:
        return git_root
    return Path.cwd().resolve()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace(os.sep, "/")
    except ValueError:
        return str(path.resolve())


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


def discover_repos(root: Path) -> List[Path]:
    root = root.resolve()
    root_git = run_git_root(root)
    if root_git and root_git == root:
        return [root]

    repos: List[Path] = []
    seen: set[Path] = set()
    direct_non_git: List[Path] = []
    for child in child_dirs(root):
        child_git = run_git_root(child)
        if child_git and child_git == child.resolve():
            if child_git not in seen:
                seen.add(child_git)
                repos.append(child_git)
        else:
            direct_non_git.append(child)
    for parent in direct_non_git:
        for child in child_dirs(parent):
            child_git = run_git_root(child)
            if child_git and child_git == child.resolve() and child_git not in seen:
                seen.add(child_git)
                repos.append(child_git)
    return repos


def find_named(root: Path, names: List[str]) -> List[str]:
    out = []
    for name in names:
        p = root / name
        if p.exists():
            out.append(rel(root, p))
    return out


def walk_limited(root: Path, predicate, limit: int = 80) -> List[str]:
    out = []
    skip_dirs = {".git", ".plan-first", "node_modules", ".next", "dist", "build", "coverage", ".venv", "vendor", "target"}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".__")]
        base_path = Path(base)
        for item in files:
            p = base_path / item
            rp = rel(root, p)
            if predicate(rp, item):
                out.append(rp)
                if len(out) >= limit:
                    return out
    return out


def print_list(items: List[str], empty: str) -> None:
    if items:
        for item in items:
            print(f"- {item}")
    else:
        print(f"- {empty}")


def print_repo_hints(workspace_root: Path, repo_root: Path) -> None:
    repo_label = rel(workspace_root, repo_root)
    print(f"## Repo: {repo_label}")
    print()
    print("### 项目规则候选")
    print_list(find_named(repo_root, DOCS), "未发现常见规则文档")
    print()
    print("### manifest / 构建配置候选")
    print_list(find_named(repo_root, MANIFESTS), "未发现常见 manifest")
    print()
    print("### contract / schema / migration 候选")
    print_list(walk_limited(repo_root, lambda rp, name: any(h in rp.lower() for h in CONTRACT_HINTS), limit=40), "未发现明显 contract/schema/migration hint")
    print()
    print("### 测试 / 验证候选")
    print_list(walk_limited(repo_root, lambda rp, name: any(h in rp.lower() for h in TEST_HINTS), limit=40), "未发现明显测试目录或配置 hint")
    print()
    print("### source surface 候选")
    common = [rel(repo_root, repo_root / name) for name in SOURCE_DIRS if (repo_root / name).exists()]
    print_list(common, "未发现常见 source surface 目录")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="只读 workspace/repo 上下文扫描器")
    parser.add_argument("--root", help="workspace root；默认向上查找 .plan-first/config.toml，找不到则使用当前 Git root；非 Git 目录用当前目录")
    args = parser.parse_args()

    root = resolve_root(args.root)
    repos = discover_repos(root)

    print("# 只读 workspace 上下文扫描")
    print()
    print("说明：以下结果只是 hints，不是最终事实。finalize 前必须读取相关文件确认。")
    print()
    print(f"Workspace root: {root}")
    print()
    print("## Workspace 规则候选")
    print_list(find_named(root, DOCS + ["AI_CONTEXT.md"]), "未发现 workspace 级规则文档")
    print()
    if repos:
        print("## Git repos")
        for repo in repos:
            print(f"- {rel(root, repo)}")
        print()
        for repo in repos:
            print_repo_hints(root, repo)
    else:
        print("## Git repos")
        print("- 未发现")
        print()
        print_repo_hints(root, root)


if __name__ == "__main__":
    main()
