#!/usr/bin/env python3
"""Read-only architecture context collector for dbx-architecture-health.

This script intentionally stays lightweight and dependency-free. It provides evidence
leads, not final review conclusions. It does not run tests, install dependencies,
access the network, or modify files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

IGNORE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".next", ".nuxt", ".turbo", ".cache",
    ".parcel-cache", "dist", "build", "coverage", ".coverage", "target", "out", "vendor",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv", "env",
    ".tox", ".idea", ".vscode",
}

GENERATED_HINTS = (
    "generated", "__generated__", "gen", "autogen", "codegen", "swagger", "openapi",
    "graphql", "proto", "snapshot", "snapshots",
)

TEXT_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".go", ".rs", ".java",
    ".kt", ".kts", ".cs", ".rb", ".php", ".scala", ".swift", ".md", ".mdx",
    ".txt", ".json", ".yaml", ".yml", ".toml", ".xml", ".proto", ".graphql", ".gql",
    ".sql", ".sh", ".bash", ".zsh", ".fish", ".css", ".scss", ".html",
}

MANIFEST_NAMES = {
    "package.json", "pnpm-workspace.yaml", "pnpm-workspace.yml", "turbo.json", "nx.json",
    "tsconfig.json", "tsconfig.base.json", "vite.config.ts", "vite.config.js", "next.config.js",
    "next.config.mjs", "webpack.config.js", "rollup.config.js", "pyproject.toml", "setup.py",
    "setup.cfg", "requirements.txt", "requirements-dev.txt", "poetry.lock", "uv.lock", "go.mod",
    "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle",
    "settings.gradle.kts", "deno.json", "deno.jsonc", "Makefile", "justfile", "Jenkinsfile",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
}

VALIDATION_NAMES = {
    "jest.config.js", "jest.config.ts", "vitest.config.ts", "vitest.config.js",
    "playwright.config.ts", "playwright.config.js", "cypress.config.ts", "cypress.config.js",
    "pytest.ini", "tox.ini", "noxfile.py", "ruff.toml", ".pre-commit-config.yaml",
    "eslint.config.js", "eslint.config.mjs", "eslint.config.cjs", ".eslintrc", ".eslintrc.js",
    ".eslintrc.json", "biome.json", ".github/workflows", ".gitlab-ci.yml",
}

INSTRUCTION_NAMES = {
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "README.mdx", "CONTRIBUTING.md",
    "REVIEW.md", "CODEOWNERS", "llms.txt", ".cursorrules", ".windsurfrules",
}

COMMITMENT_HINTS = (
    "migration", "migrations", "schema", "schemas", "sdk", "public", "api", "openapi", "graphql",
    "proto", "package", "release", "changelog", "auth", "permission", "payment", "billing", "tenant",
    "privacy", "security",
)

JS_IMPORT_RE = re.compile(
    r"(?:import\s+(?:[^'\"]+?\s+from\s+)?|export\s+[^'\"]+?\s+from\s+|require\(|import\()\s*['\"]([^'\"]+)['\"]"
)
PY_IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w\.]+)\s+import\s+|import\s+([\w\.]+))", re.MULTILINE)
EXPORT_RE = re.compile(r"^\s*export\s+(?:type\s+|interface\s+|class\s+|function\s+|const\s+|let\s+|var\s+|enum\s+|\{)", re.MULTILINE)


def run_git(root: Path, args: List[str], timeout: int = 5) -> Optional[str]:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=timeout, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTS:
        return True
    if path.name in MANIFEST_NAMES or path.name in INSTRUCTION_NAMES:
        return True
    return False


def safe_read_text(path: Path, max_bytes: int = 256_000) -> str:
    try:
        if path.stat().st_size > max_bytes:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def generated_path_tokens(rel: str) -> Iterable[str]:
    for part in rel.lower().split("/"):
        if not part:
            continue
        yield part
        for token in re.split(r"[^a-z0-9]+", part):
            if token:
                yield token


def is_generated_or_snapshot_candidate(rel: str) -> bool:
    return any(token in GENERATED_HINTS for token in generated_path_tokens(rel))


def is_commitment_candidate(rel: str) -> bool:
    low = rel.lower()
    return any(token in low for token in COMMITMENT_HINTS)


def relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def should_skip_dir(path: Path) -> bool:
    return path.name in IGNORE_DIRS or (path.name.startswith(".") and path.name not in {".github"})


def walk_files(root: Path, max_files: int) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not should_skip_dir(current / d)]
        for name in filenames:
            p = current / name
            if not is_probably_text(p):
                continue
            files.append(p)
            if len(files) >= max_files:
                return files
    return files


def bucket_for(path: str) -> str:
    parts = [p for p in path.split("/") if p]
    if not parts:
        return "."
    if parts[0] in {"packages", "apps", "services", "libs", "crates"} and len(parts) >= 2:
        return "/".join(parts[:2])
    if parts[0] in {"src", "app", "server", "client", "lib", "domain", "features", "components"} and len(parts) >= 2:
        return "/".join(parts[:2])
    return parts[0]


def resolve_relative_import(source_rel: str, spec: str) -> Optional[str]:
    if not spec.startswith("."):
        return None
    source_dir = Path(source_rel).parent
    normalized = (source_dir / spec).as_posix()
    parts: List[str] = []
    for part in normalized.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return "/".join(parts)


def collect_import_edges(root: Path, files: Iterable[Path], max_edges: int) -> Tuple[Counter, Counter, List[Dict[str, str]]]:
    external_imports: Counter = Counter()
    bucket_edges: Counter = Counter()
    examples: List[Dict[str, str]] = []
    for path in files:
        ext = path.suffix.lower()
        if ext not in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py"}:
            continue
        text = safe_read_text(path, max_bytes=160_000)
        if not text:
            continue
        source_rel = relpath(path, root)
        source_bucket = bucket_for(source_rel)
        specs: List[str] = []
        if ext in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
            specs.extend(m.group(1) for m in JS_IMPORT_RE.finditer(text))
        elif ext == ".py":
            for m in PY_IMPORT_RE.finditer(text):
                specs.append(m.group(1) or m.group(2) or "")
        for spec in specs:
            if not spec:
                continue
            if spec.startswith("."):
                target_rel = resolve_relative_import(source_rel, spec)
                if not target_rel:
                    continue
                target_bucket = bucket_for(target_rel)
                if source_bucket != target_bucket:
                    bucket_edges[(source_bucket, target_bucket)] += 1
                    if len(examples) < max_edges:
                        examples.append({"from": source_rel, "import": spec, "to_bucket": target_bucket})
            else:
                package = spec.split("/")[0] if not spec.startswith("@") else "/".join(spec.split("/")[:2])
                external_imports[package] += 1
    return external_imports, bucket_edges, examples


def collect_churn(root: Path, since: str, max_items: int) -> List[Dict[str, Any]]:
    out = run_git(root, ["log", f"--since={since}", "--name-only", "--pretty=format:"])
    if not out:
        return []
    counts: Counter = Counter()
    for line in out.splitlines():
        line = line.strip()
        if not line or line.endswith("/"):
            continue
        if any(part in IGNORE_DIRS for part in line.split("/")):
            continue
        counts[line] += 1
    return [{"path": path, "commits_touching": count} for path, count in counts.most_common(max_items)]


def print_markdown(result: Dict[str, Any]) -> None:
    print("# Architecture context leads")
    print()
    print(f"Root: `{result['root']}`")
    print(f"Focused paths: {', '.join('`' + p + '`' for p in result['focused_paths'])}")
    print(f"Files scanned: {result['limits']['files_scanned']}" + (" (truncated)" if result['limits']['truncated'] else ""))
    print()

    git = result["git"]
    print("## Git state")
    print(f"Branch: `{git.get('branch') or 'unknown'}`")
    if git.get("status_short_branch"):
        print("```text")
        for line in git["status_short_branch"][:30]:
            print(line)
        if len(git["status_short_branch"]) > 30:
            print("... truncated ...")
        print("```")
    else:
        print("Git status unavailable or not a git repository.")
    print()

    shape = result["repo_shape"]
    print("## Repo shape")
    print("### Top file extensions")
    for ext, count in list(shape["extension_counts"].items())[:20]:
        print(f"- `{ext}`: {count}")
    print()

    print("### Top buckets")
    for item in shape["top_buckets_by_file_count"][:20]:
        print(f"- `{item['bucket']}`: {item['files']} files")
    print()

    def list_section(title: str, items: List[Any], limit: int = 30) -> None:
        print(f"### {title}")
        if not items:
            print("- none found")
        else:
            for item in items[:limit]:
                if isinstance(item, dict):
                    path = item.get("path", "")
                    rest = ", ".join(f"{k}={v}" for k, v in item.items() if k != "path")
                    print(f"- `{path}`" + (f" ({rest})" if rest else ""))
                else:
                    print(f"- `{item}`")
            if len(items) > limit:
                print(f"- ... {len(items) - limit} more")
        print()

    list_section("Manifests / build surfaces", shape["manifests"])
    list_section("Validation surfaces", shape["validation_surfaces"])
    list_section("Instruction surfaces", shape["instruction_surfaces"])
    list_section("Docs / ADR surfaces", shape["docs_and_adr_surfaces"])
    list_section("Generated or snapshot candidates", shape["generated_or_snapshot_candidates"])
    list_section("Commitment surface candidates", shape["commitment_surface_candidates"])
    list_section("Large files", shape["large_files"])
    list_section("Public export hotspots", shape["public_export_hotspots"])

    print("## Tests")
    print(f"Test file count: {shape['test_files_count']}")
    for path in shape["test_file_examples"][:30]:
        print(f"- `{path}`")
    print()

    deps = result["dependency_leads"]
    list_section("Top external imports", deps["top_external_imports"])
    list_section("Cross-bucket relative import edges", deps["cross_bucket_relative_edges"])
    list_section("Import examples", deps["import_examples"])
    list_section(f"Top churn files since {git.get('churn_since')}", git.get("top_churn_files") or [])


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only architecture context leads.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--path", action="append", default=[], help="Optional path(s) under root to focus. Can be repeated.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--max-files", type=int, default=5000)
    parser.add_argument("--max-large-files", type=int, default=25)
    parser.add_argument("--max-churn", type=int, default=25)
    parser.add_argument("--churn-since", default="180 days ago")
    parser.add_argument("--max-edges", type=int, default=50)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2

    if args.path:
        focus_roots: List[Path] = []
        for raw in args.path:
            p = (root / raw).resolve()
            if not p.exists():
                print(f"warning: focus path does not exist: {raw}", file=sys.stderr)
                continue
            if root not in p.parents and p != root:
                print(f"warning: focus path outside root ignored: {raw}", file=sys.stderr)
                continue
            focus_roots.append(p)
        if not focus_roots:
            return 2
    else:
        focus_roots = [root]

    all_files: List[Path] = []
    for focus in focus_roots:
        if focus.is_file():
            all_files.append(focus)
        else:
            all_files.extend(walk_files(focus, args.max_files - len(all_files)))
        if len(all_files) >= args.max_files:
            break
    all_files = sorted(set(all_files))

    ext_counts: Counter = Counter()
    bucket_counts: Counter = Counter()
    large_files: List[Dict[str, Any]] = []
    manifests: List[str] = []
    validation: List[str] = []
    instructions: List[str] = []
    docs: List[str] = []
    generated_candidates: List[str] = []
    commitment_candidates: List[str] = []
    test_files: List[str] = []
    public_export_files: List[Dict[str, Any]] = []

    for path in all_files:
        rel = relpath(path, root)
        ext_counts[path.suffix.lower() or "[no_ext]"] += 1
        bucket_counts[bucket_for(rel)] += 1
        lower_rel = rel.lower()

        if path.name in MANIFEST_NAMES:
            manifests.append(rel)
        if path.name in VALIDATION_NAMES or ".github/workflows/" in rel or rel.startswith(".github/workflows/"):
            validation.append(rel)
        if path.name in INSTRUCTION_NAMES:
            instructions.append(rel)
        if path.suffix.lower() in {".md", ".mdx"} and (rel.startswith("docs/") or "adr" in lower_rel or path.name.lower().startswith("readme")):
            docs.append(rel)
        if is_generated_or_snapshot_candidate(rel):
            generated_candidates.append(rel)
        if is_commitment_candidate(rel):
            commitment_candidates.append(rel)
        if re.search(r"(^|/)(test|tests|__tests__|spec|specs)(/|$)", lower_rel) or re.search(r"\.(test|spec)\.[tj]sx?$", lower_rel):
            test_files.append(rel)

        try:
            line_count = sum(1 for _ in path.open("r", encoding="utf-8", errors="replace"))
        except OSError:
            line_count = 0
        if line_count >= 250 and path.suffix.lower() not in {".json", ".lock"}:
            large_files.append({"path": rel, "lines": line_count})

        if path.suffix.lower() in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
            text = safe_read_text(path, max_bytes=160_000)
            if text:
                export_count = len(EXPORT_RE.findall(text))
                if export_count:
                    public_export_files.append({"path": rel, "export_statements": export_count})

    large_files.sort(key=lambda x: x["lines"], reverse=True)
    public_export_files.sort(key=lambda x: x["export_statements"], reverse=True)
    external_imports, bucket_edges, import_examples = collect_import_edges(root, all_files, args.max_edges)

    git_branch = run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    git_status = run_git(root, ["status", "--short", "--branch", "-uall"])
    churn = collect_churn(root, args.churn_since, args.max_churn)

    result: Dict[str, Any] = {
        "root": str(root),
        "focused_paths": [relpath(p, root) for p in focus_roots],
        "limits": {
            "max_files": args.max_files,
            "files_scanned": len(all_files),
            "truncated": len(all_files) >= args.max_files,
        },
        "git": {
            "branch": git_branch,
            "status_short_branch": git_status.splitlines()[:80] if git_status else [],
            "churn_since": args.churn_since,
            "top_churn_files": churn,
        },
        "repo_shape": {
            "extension_counts": dict(ext_counts.most_common()),
            "top_buckets_by_file_count": [{"bucket": k, "files": v} for k, v in bucket_counts.most_common(30)],
            "manifests": sorted(set(manifests))[:100],
            "validation_surfaces": sorted(set(validation))[:100],
            "instruction_surfaces": sorted(set(instructions))[:100],
            "docs_and_adr_surfaces": sorted(set(docs))[:100],
            "generated_or_snapshot_candidates": sorted(set(generated_candidates))[:100],
            "commitment_surface_candidates": sorted(set(commitment_candidates))[:100],
            "test_files_count": len(set(test_files)),
            "test_file_examples": sorted(set(test_files))[:40],
            "large_files": large_files[: args.max_large_files],
            "public_export_hotspots": public_export_files[:25],
        },
        "dependency_leads": {
            "top_external_imports": [{"name": k, "count": v} for k, v in external_imports.most_common(30)],
            "cross_bucket_relative_edges": [
                {"from_bucket": k[0], "to_bucket": k[1], "count": v} for k, v in bucket_edges.most_common(50)
            ],
            "import_examples": import_examples,
        },
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
