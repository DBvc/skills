#!/usr/bin/env python3
"""Validate the shape of a saved strict pragmatic review report.

This checks structure only. It does not judge technical correctness.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def validate(text: str) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not re.search(r"^##\s+核心判断\b", text, re.M):
        errors.append("missing section: 核心判断")

    has_findings = bool(re.search(r"^##\s+(主要发现|主要风险)\b", text, re.M))
    severity_count = len(re.findall(r"\[S[0-3]\s+(?:blocker|high|medium|low)\]", text))
    if has_findings and severity_count == 0:
        warnings.append("findings/risks section exists but no severity markers were found")

    for field in ["Evidence", "Impact", "Fix", "Confidence"]:
        if severity_count and field not in text:
            errors.append(f"missing finding field: {field}")

    forbidden = ["我是 Linus", "Linus Torvalds 在这里", "你这个人", "废物", "垃圾人"]
    for value in forbidden:
        if value in text:
            errors.append(f"forbidden persona/personal-attack wording found: {value}")

    if re.search(r"(重写所有|全部推倒|rewrite everything)", text, re.I) and not re.search(r"(Evidence|为什么|模型|数据结构)", text):
        warnings.append("rewrite recommendation may lack evidence")

    if re.search(r"(测试通过|tests pass|verified|已验证)", text, re.I) and not re.search(r"(命令|command|未运行|Not run|输出|log)", text):
        warnings.append("verification claim may lack command/output context")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "severity_count": severity_count}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate strict pragmatic review report shape.")
    parser.add_argument("file", help="Markdown report file to validate.")
    parser.add_argument("--json", action="store_true", help="Print JSON result.")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"error: file does not exist: {path}", file=sys.stderr)
        return 2

    result = validate(path.read_text(encoding="utf-8", errors="ignore"))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("ok:" if result["ok"] else "not ok:", result["ok"])
        for err in result["errors"]:
            print(f"error: {err}")
        for warn in result["warnings"]:
            print(f"warning: {warn}")
        print(f"severity_count: {result['severity_count']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
