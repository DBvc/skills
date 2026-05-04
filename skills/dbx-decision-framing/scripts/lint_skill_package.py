#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dbx-decision-framing skill 包静态检查器。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED_NAME = "dbx-decision-framing"
ALLOWED_KINDS = {"positive", "negative", "near_miss", "failure_mode", "safety"}
REQUIRED_SECTIONS = [
    "## 1. 硬门禁",
    "## 2. 五个分支的强制输出规则",
    "## 3. YAML 边界块",
    "## 5. 标准输出契约：full_decision",
    "## 6. quick_decision 专用模板",
    "## 7. clarification 专用模板",
    "## 8. safety_redirect 专用模板",
    "## 13. 结束前自检",
]
REQUIRED_EXAMPLES = ["clarification", "quick_decision", "direct_answer", "safety_redirect"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    block = text[4:end].strip().splitlines()
    data: dict[str, str] = {}
    for line in block:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"')
    return data


def validate_evals(evals_path: Path, errors: list[str], warnings: list[str]) -> None:
    if not evals_path.exists():
        errors.append("缺少 evals/evals.json")
        return
    try:
        data = json.loads(read(evals_path))
    except Exception as exc:
        errors.append(f"evals/evals.json 不是合法 JSON: {exc}")
        return

    if not isinstance(data, dict) or not isinstance(data.get("evals"), list):
        errors.append("evals/evals.json 顶层必须包含 evals 数组")
        return
    if data.get("skill_name") != EXPECTED_NAME:
        errors.append(f"evals/evals.json skill_name 必须是 {EXPECTED_NAME}")

    kinds: dict[str, int] = {k: 0 for k in ALLOWED_KINDS}
    for i, ev in enumerate(data["evals"]):
        prefix = f"evals[{i}]"
        if not isinstance(ev, dict):
            errors.append(f"{prefix} 必须是对象")
            continue
        kind = ev.get("kind")
        if kind not in ALLOWED_KINDS:
            errors.append(f"{prefix}.kind 非法: {kind!r}；只允许 {sorted(ALLOWED_KINDS)}")
        else:
            kinds[kind] += 1
        for key in ["id", "prompt", "expected_behavior", "checks", "pass_criteria"]:
            if key not in ev:
                errors.append(f"{prefix} 缺少字段 {key}")
        checks = ev.get("checks", {})
        if not isinstance(checks, dict):
            errors.append(f"{prefix}.checks 必须是对象")
            continue
        for group in ["trigger", "process", "output", "safety"]:
            arr = checks.get(group, [])
            if not isinstance(arr, list):
                errors.append(f"{prefix}.checks.{group} 必须是数组")
                continue
            for j, chk in enumerate(arr):
                if not isinstance(chk, dict):
                    errors.append(f"{prefix}.checks.{group}[{j}] 必须是对象")
                    continue
                if chk.get("type") not in {"must_contain", "must_not_contain", "regex"}:
                    errors.append(f"{prefix}.checks.{group}[{j}].type 非法")
                if "value" not in chk:
                    errors.append(f"{prefix}.checks.{group}[{j}] 缺少 value")
                if "required" in chk and not isinstance(chk["required"], bool):
                    errors.append(f"{prefix}.checks.{group}[{j}].required 必须是 boolean")
        pc = ev.get("pass_criteria")
        if not isinstance(pc, dict):
            errors.append(f"{prefix}.pass_criteria 必须是对象")
        elif "all_required" in pc and not isinstance(pc["all_required"], bool):
            errors.append(f"{prefix}.pass_criteria.all_required 必须是 boolean")

    if len(data["evals"]) < 10:
        warnings.append("建议至少 10 个 eval，覆盖 positive/negative/near_miss/failure_mode/safety")
    for required in ["positive", "negative", "near_miss", "failure_mode", "safety"]:
        if kinds[required] == 0:
            errors.append(f"evals/evals.json 至少需要一个 {required} case")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        errors.append("缺少 SKILL.md")
    else:
        text = read(skill_md)
        fm = parse_frontmatter(text)
        if fm.get("name") != EXPECTED_NAME:
            errors.append(f"frontmatter.name 必须是 {EXPECTED_NAME}")
        if not fm.get("description"):
            errors.append("frontmatter.description 不能为空")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"SKILL.md 缺少必要章节: {section}")
        for phrase in ["mode: clarification", "mode: quick_decision", "mode: safety_redirect", "direct_answer"]:
            if phrase not in text:
                errors.append(f"SKILL.md 缺少分支约束: {phrase}")
        if "即使开头是拒绝，也不能省略 YAML" not in text:
            errors.append("SKILL.md 必须强调 safety_redirect 不能省略 YAML")
        if len(text.splitlines()) > 520:
            warnings.append("SKILL.md 行数超过 520，建议继续瘦身")

    for p in ["references/model-catalog.md", "references/domain-adapters.md", "references/output-contracts.md", "references/worked-examples.md"]:
        f = root / p
        if not f.exists():
            errors.append(f"缺少 {p}")
            continue
        txt = read(f)
        if len(txt.splitlines()) > 120 and "## 目录" not in txt:
            errors.append(f"长 reference 缺少目录: {p}")

    examples = root / "references" / "worked-examples.md"
    if examples.exists():
        ex_text = read(examples)
        for ex in REQUIRED_EXAMPLES:
            if ex not in ex_text:
                errors.append(f"worked-examples.md 缺少 {ex} 示例")

    validate_evals(root / "evals" / "evals.json", errors, warnings)

    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
