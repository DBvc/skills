#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""轻量 eval runner：校验 eval schema，并可对 captured output 做确定性检查。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED_KINDS = {"positive", "negative", "near_miss", "failure_mode", "safety"}
ALLOWED_CHECK_TYPES = {"must_contain", "must_not_contain", "regex"}
CHECK_GROUPS = ["trigger", "process", "output", "safety"]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(data: object) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["顶层必须是 JSON 对象"], warnings
    if "evals" not in data or not isinstance(data["evals"], list):
        return ["顶层必须包含 evals 数组"], warnings
    if "pass_threshold" in data and not isinstance(data["pass_threshold"], (int, float)):
        errors.append("pass_threshold 必须是数字")
    kinds = {k: 0 for k in ALLOWED_KINDS}
    for i, ev in enumerate(data["evals"]):
        prefix = f"evals[{i}]"
        if not isinstance(ev, dict):
            errors.append(f"{prefix} 必须是对象")
            continue
        for key in ["id", "kind", "prompt", "expected_behavior", "checks", "pass_criteria"]:
            if key not in ev:
                errors.append(f"{prefix} 缺少字段 {key}")
        kind = ev.get("kind")
        if kind not in ALLOWED_KINDS:
            errors.append(f"{prefix}.kind 非法: {kind!r}; 只允许 {sorted(ALLOWED_KINDS)}")
        else:
            kinds[kind] += 1
        checks = ev.get("checks")
        if not isinstance(checks, dict):
            errors.append(f"{prefix}.checks 必须是对象")
            continue
        for group in CHECK_GROUPS:
            arr = checks.get(group, [])
            if not isinstance(arr, list):
                errors.append(f"{prefix}.checks.{group} 必须是数组")
                continue
            for j, chk in enumerate(arr):
                cp = f"{prefix}.checks.{group}[{j}]"
                if not isinstance(chk, dict):
                    errors.append(f"{cp} 必须是对象，不能是 {type(chk).__name__}")
                    continue
                if chk.get("type") not in ALLOWED_CHECK_TYPES:
                    errors.append(f"{cp}.type 非法: {chk.get('type')!r}")
                if "value" not in chk:
                    errors.append(f"{cp} 缺少 value")
                if "required" in chk and not isinstance(chk["required"], bool):
                    errors.append(f"{cp}.required 必须是 boolean")
        pc = ev.get("pass_criteria")
        if not isinstance(pc, dict):
            errors.append(f"{prefix}.pass_criteria 必须是对象")
        else:
            if "all_required" in pc and not isinstance(pc["all_required"], bool):
                errors.append(f"{prefix}.pass_criteria.all_required 必须是 boolean")
            if "min_score" in pc and not isinstance(pc["min_score"], (int, float)):
                errors.append(f"{prefix}.pass_criteria.min_score 必须是数字")
    for required in ["positive", "negative", "near_miss", "failure_mode", "safety"]:
        if kinds[required] == 0:
            errors.append(f"至少需要一个 {required} eval")
    return errors, warnings


def find_output(outputs_dir: Path, eval_id: str) -> Path | None:
    for ext in [".md", ".txt"]:
        p = outputs_dir / f"{eval_id}{ext}"
        if p.exists():
            return p
    return None


def run_checks(data: dict, outputs_dir: Path) -> dict:
    results = []
    total_required = 0
    passed_required = 0
    for ev in data.get("evals", []):
        ev_id = ev.get("id", "unknown")
        out_path = find_output(outputs_dir, ev_id)
        if not out_path:
            results.append({"id": ev_id, "ok": False, "error": "缺少 captured output"})
            continue
        text = out_path.read_text(encoding="utf-8")
        case_errors = []
        for group in CHECK_GROUPS:
            for chk in ev.get("checks", {}).get(group, []):
                required = chk.get("required", True)
                if required:
                    total_required += 1
                typ = chk.get("type")
                value = str(chk.get("value", ""))
                ok = True
                if typ == "must_contain":
                    ok = value in text
                elif typ == "must_not_contain":
                    ok = value not in text
                elif typ == "regex":
                    ok = re.search(value, text, flags=re.MULTILINE) is not None
                else:
                    ok = False
                if ok and required:
                    passed_required += 1
                if not ok and required:
                    case_errors.append(f"{group}: {typ} {value!r} 未通过")
        results.append({"id": ev_id, "ok": not case_errors, "errors": case_errors})
    score = passed_required / total_required if total_required else 0.0
    return {"ok": all(r.get("ok") for r in results), "score": score, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evals_json")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--outputs-dir")
    args = parser.parse_args()

    path = Path(args.evals_json)
    try:
        data = load_json(path)
    except Exception as exc:
        print(json.dumps({"ok": False, "errors": [f"无法读取 JSON: {exc}"], "warnings": []}, ensure_ascii=False, indent=2))
        return 1

    errors, warnings = validate_schema(data)
    if errors or args.validate_only or not args.outputs_dir:
        result = {"ok": not errors, "errors": errors, "warnings": warnings, "mode": "validate-only" if args.validate_only else "schema-only"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    run_result = run_checks(data, Path(args.outputs_dir))
    result = {"ok": not errors and run_result["ok"], "schema_errors": errors, "warnings": warnings, "run": run_result}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
