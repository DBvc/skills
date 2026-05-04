#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 dbx-decision-framing captured output 是否遵守分支契约。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

YAML_START = re.compile(r"\A```yaml\s*\ndecision_framing:\s*\n")
MODE_RE = re.compile(r"^\s*mode:\s*([a-z_]+)\s*$", re.MULTILINE)
GATE_RE = re.compile(r"^\s*(safety_ok|enough_context):\s*([a-z_]+)\s*$", re.MULTILINE)
FULL_REQUIRED_HEADINGS = [
    "## 结论",
    "## 我对问题的重新定义",
    "## 已知事实 / 假设 / 判断",
    "## 关键目标和约束",
    "## 可选方案比较",
    "## 关键思维方式",
    "## 推荐路径",
    "## 风险、反证和复盘",
]


def parse_gates(text: str) -> dict[str, str]:
    return {name: value for name, value in GATE_RE.findall(text)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file")
    parser.add_argument("--expected-mode", choices=["full_decision", "quick_decision", "clarification", "direct_answer", "safety_redirect"])
    args = parser.parse_args()

    text = Path(args.output_file).read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    mode_match = MODE_RE.search(text)
    detected_mode = mode_match.group(1) if mode_match else None
    gates = parse_gates(text)

    if args.expected_mode:
        if args.expected_mode == "direct_answer":
            if "decision_framing" in text:
                errors.append("direct_answer 不应输出 decision_framing YAML")
        else:
            if not YAML_START.search(text):
                errors.append(f"{args.expected_mode} 必须以 fenced YAML decision_framing 开头")
            if detected_mode != args.expected_mode:
                errors.append(f"mode 应为 {args.expected_mode}, 实际为 {detected_mode!r}")

    mode = args.expected_mode or detected_mode
    if mode == "quick_decision":
        for forbidden in ["已知事实 / 假设 / 判断", "可选方案比较", "深度决策备忘录"]:
            if forbidden in text:
                errors.append(f"quick_decision 过度展开，包含 {forbidden!r}")
    if mode == "clarification":
        for forbidden in ["我建议你读", "我建议你不读", "推荐：读", "推荐：不读", "你应该", "可能值得", "可能不值得", "如果目标是"]:
            if forbidden in text:
                errors.append(f"clarification 不应提前给结论，发现 {forbidden!r}")
        if "先确认" not in text and "关键信息" not in text:
            errors.append("clarification 应包含阻塞问题")
        if gates.get("enough_context") == "pass":
            errors.append("clarification 的 enough_context 不应为 pass")
    if mode == "full_decision":
        for required in FULL_REQUIRED_HEADINGS:
            if required not in text:
                errors.append(f"full_decision 缺少 {required!r}")
        if gates.get("enough_context") == "fail":
            errors.append("full_decision 的 enough_context 不应为 fail")
    if mode == "safety_redirect":
        if not YAML_START.search(text):
            errors.append("safety_redirect 必须先输出 YAML")
        if gates.get("safety_ok") != "fail":
            errors.append("safety_redirect 必须设置 safety_ok: fail")
        for required in ["## 不能按原请求执行", "## 安全替代方向"]:
            if required not in text:
                errors.append(f"safety_redirect 缺少固定标题 {required!r}")

    result = {"ok": not errors, "errors": errors, "warnings": warnings, "detected_mode": detected_mode}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
