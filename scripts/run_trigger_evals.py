#!/usr/bin/env python3
"""Validate and package trigger evals.

This does not run an agent. It validates `evals/triggers.json` files and can emit
an agent/manual testing pack.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CANONICAL_KINDS = {"positive", "negative", "near_miss", "failure_mode", "safety"}


def load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def validate_file(path: Path, expected_skill_name: str) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}
    data, err = load_json(path)
    if err:
        return [f"{path}: invalid JSON: {err}"], warnings, counts
    if not isinstance(data, dict):
        return [f"{path}: root must be an object"], warnings, counts
    if data.get("skill_name") != expected_skill_name:
        warnings.append(f"{path}: skill_name is {data.get('skill_name')!r}, expected {expected_skill_name!r}")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return [f"{path}: cases must be a non-empty array"], warnings, counts
    seen: set[str] = set()
    for idx, case in enumerate(cases):
        prefix = f"{path}#{idx}"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: case must be an object")
            continue
        case_id = case.get("id")
        kind = case.get("kind")
        counts[str(kind)] = counts.get(str(kind), 0) + 1
        if not case_id:
            errors.append(f"{prefix}: missing id")
        elif case_id in seen:
            errors.append(f"{prefix}: duplicate id {case_id!r}")
        else:
            seen.add(str(case_id))
        if kind not in CANONICAL_KINDS:
            errors.append(f"{prefix}: kind must be one of {sorted(CANONICAL_KINDS)}")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{prefix}: prompt must be a non-empty string")
        if not isinstance(case.get("expected_trigger"), bool):
            errors.append(f"{prefix}: expected_trigger must be true or false")
        if not isinstance(case.get("rationale", ""), str):
            errors.append(f"{prefix}: rationale must be a string if present")
    for needed in ["positive", "negative", "near_miss"]:
        if counts.get(needed, 0) == 0:
            warnings.append(f"{path}: consider adding at least one {needed} case")
    return errors, warnings, counts


def discover(root: Path) -> list[tuple[str, Path]]:
    skills_dir = root / "skills"
    if not skills_dir.exists():
        return []
    result: list[tuple[str, Path]] = []
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        path = skill_dir / "evals" / "triggers.json"
        if path.exists():
            result.append((skill_dir.name, path))
    return result


def emit_agent_pack(root: Path, output: Path) -> None:
    chunks: list[str] = [
        "# DBX Trigger Eval Pack",
        "",
        "Use each case to check whether the target skill should trigger. Record actual_trigger, evidence, and notes.",
        "",
    ]
    for skill_name, path in discover(root):
        data, err = load_json(path)
        if err or not isinstance(data, dict):
            continue
        chunks.extend([f"## {skill_name}", ""])
        for case in data.get("cases", []):
            if not isinstance(case, dict):
                continue
            chunks.append(f"### {case.get('id', 'unnamed')}")
            chunks.append("")
            chunks.append(f"Kind: `{case.get('kind')}`")
            chunks.append(f"Expected trigger: `{case.get('expected_trigger')}`")
            chunks.append("")
            chunks.append("Prompt:")
            chunks.append("")
            chunks.append("```text")
            chunks.append(str(case.get("prompt", "")))
            chunks.append("```")
            chunks.append("")
            chunks.append("Result:")
            chunks.append("")
            chunks.append("```yaml")
            chunks.append("actual_trigger: true | false")
            chunks.append("evidence: \"\"")
            chunks.append("notes: \"\"")
            chunks.append("```")
            chunks.append("")
    output.write_text("\n".join(chunks), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DBX trigger eval files and emit manual test packs.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--validate-only", action="store_true", help="Only validate schemas. This is the default if no emit option is used.")
    parser.add_argument("--emit-agent-pack", help="Write a Markdown pack of trigger eval prompts to this file.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format for validation results.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    entries = discover(root)
    results = []
    total_errors: list[str] = []
    total_warnings: list[str] = []
    for skill_name, path in entries:
        errors, warnings, counts = validate_file(path, skill_name)
        total_errors.extend(errors)
        total_warnings.extend(warnings)
        results.append({"skill_name": skill_name, "path": str(path.relative_to(root)), "errors": errors, "warnings": warnings, "counts": counts})

    missing = []
    skills_dir = root / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            if not (skill_dir / "evals" / "triggers.json").exists():
                missing.append(skill_dir.name)
                total_warnings.append(f"{skill_dir.name}: missing evals/triggers.json")

    if args.emit_agent_pack:
        emit_agent_pack(root, Path(args.emit_agent_pack))

    summary = {"trigger_eval_files": len(entries), "missing": missing, "errors": len(total_errors), "warnings": len(total_warnings)}
    if args.format == "json":
        print(json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(f"Trigger eval validation: {summary['trigger_eval_files']} files, {summary['errors']} errors, {summary['warnings']} warnings")
        for result in results:
            status = "ERROR" if result["errors"] else "WARN" if result["warnings"] else "OK"
            print(f"[{status}] {result['skill_name']} | {result['path']} | counts={result['counts']}")
            for err in result["errors"]:
                print(f"  - ERROR: {err}")
            for warning in result["warnings"]:
                print(f"  - WARNING: {warning}")
        for skill in missing:
            print(f"[MISSING] {skill}: evals/triggers.json")
        if args.emit_agent_pack:
            print(f"Wrote trigger eval pack: {args.emit_agent_pack}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
