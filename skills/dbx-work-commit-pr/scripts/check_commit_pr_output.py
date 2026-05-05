#!/usr/bin/env python3
"""Check DBX work commit/PR text for vague proof and contract-shape issues."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VAGUE_PROOF = [
    r"Proof\s*[:：]\s*已测试",
    r"Proof\s*[:：]\s*测试通过",
    r"Proof\s*[:：]\s*本地测过",
    r"证明它可行\s*[:：]\s*验证通过",
    r"证明它可行\s*[:：]\s*本地测试通过",
    r"已验证",
    r"测试没问题",
]

PROCESS_CHATTER = [
    r"讨论过程",
    r"失败尝试",
    r"被否决方案",
    r"临时调试",
    r"review 往返",
    r"先试了",
    r"后来改成",
]

REQUIRED_PR_SECTIONS = [
    "做了什么/为什么",
    "证明它可行",
    "风险与 AI 参与",
    "评审关注点",
]

COMMIT_TITLE_RE = re.compile(r"(?m)^M-[A-Za-z0-9_-]+\((feat|fix|inf|chore|test|docs)\): \S.+$")


def read_input(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    return sys.stdin.read()


def contains_heading(text: str, heading: str) -> bool:
    return re.search(rf"(?im)^\s*#+\s*{re.escape(heading)}\s*$", text) is not None


def find_patterns(text: str, patterns: list[str]) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, re.IGNORECASE)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Chinese work commit/PR text for vague proof, missing four-block PR sections, and process leakage.",
    )
    parser.add_argument("--file", help="Read output text from this file. Defaults to stdin.")
    parser.add_argument("--artifact", choices=["commit", "pr", "both"], default="both")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()

    text = read_input(args)
    errors: list[str] = []
    warnings: list[str] = []

    if not text.strip():
        errors.append("output is empty")

    vague = find_patterns(text, VAGUE_PROOF)
    if vague:
        errors.append("vague proof wording found: " + ", ".join(vague))

    chatter = find_patterns(text, PROCESS_CHATTER)
    if chatter:
        warnings.append("possible process chatter: " + ", ".join(chatter))

    if args.artifact in {"commit", "both"} and not COMMIT_TITLE_RE.search(text):
        errors.append("missing commit title matching M-xxx(type): title with an allowed type")

    if args.artifact in {"pr", "both"}:
        for section in REQUIRED_PR_SECTIONS:
            if not contains_heading(text, section):
                errors.append(f"missing PR section: {section}")
        if "证明它可行" in text and not re.search(r"(自动验证|手动验证|未验证)\s*[:：]", text):
            errors.append("proof section should include 自动验证、手动验证 or 未验证 evidence")
        if "风险与 AI 参与" in text and not re.search(r"AI\s*参与\s*[:：]", text):
            errors.append("risk section should state AI 参与")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "artifact": args.artifact,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("OK" if result["ok"] else "FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
