#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读仓库上下文扫描器：输出 hints，不做最终判断。

Usage: python3 scripts/repo_context.py
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace(os.sep, "/")


def find_named(names):
    out = []
    for name in names:
        p = ROOT / name
        if p.exists():
            out.append(rel(p))
    return out


def walk_limited(predicate, limit=80):
    out = []
    skip_dirs = {".git", "node_modules", ".next", "dist", "build", "coverage", ".venv", "vendor", "target"}
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".__")]
        base_path = Path(base)
        for item in files:
            p = base_path / item
            rp = rel(p)
            if predicate(rp, item):
                out.append(rp)
                if len(out) >= limit:
                    return out
    return out


def main():
    print("# 只读仓库上下文扫描")
    print()
    print("说明：以下结果只是 hints，不是最终事实。finalize 前必须读取相关文件确认。")
    print()

    print("## 项目规则候选")
    docs = find_named(DOCS)
    if docs:
        for x in docs:
            print(f"- {x}")
    else:
        print("- 未发现常见规则文档")
    print()

    print("## manifest / 构建配置候选")
    manifests = find_named(MANIFESTS)
    if manifests:
        for x in manifests:
            print(f"- {x}")
    else:
        print("- 未发现常见 manifest")
    print()

    print("## contract / schema / migration 候选")
    contracts = walk_limited(lambda rp, name: any(h in rp.lower() for h in CONTRACT_HINTS))
    if contracts:
        for x in contracts[:40]:
            print(f"- {x}")
    else:
        print("- 未发现明显 contract/schema/migration hint")
    print()

    print("## 测试 / 验证候选")
    tests = walk_limited(lambda rp, name: any(h in rp.lower() for h in TEST_HINTS))
    if tests:
        for x in tests[:40]:
            print(f"- {x}")
    else:
        print("- 未发现明显测试目录或配置 hint")
    print()

    print("## source surface 候选")
    common = []
    for name in ["src", "app", "apps", "packages", "services", "server", "client", "frontend", "backend", "lib", "cmd", "internal"]:
        p = ROOT / name
        if p.exists():
            common.append(rel(p))
    if common:
        for x in common:
            print(f"- {x}")
    else:
        print("- 未发现常见 source surface 目录")

if __name__ == "__main__":
    main()
