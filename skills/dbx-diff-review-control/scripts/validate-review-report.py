#!/usr/bin/env python3
"""Validate the shape of a saved DBX diff review report.

This is a lightweight sanity checker. It does not judge technical correctness.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = ["核心判断", "Review 目标"]
FINDING_FIELDS = ["Evidence", "Impact", "Fix", "Confidence"]


def validate(text: str) -> dict[str, object]:
    warnings: list[str] = []
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\b", text, re.M):
            errors.append(f"missing section: {section}")

    severity_matches = re.findall(r"\[S[0-3]\s+(?:blocker|high|medium|low)\]", text)
    has_findings_section = bool(re.search(r"^##\s+主要发现\b", text, re.M))
    if has_findings_section and severity_matches:
        for field in FINDING_FIELDS:
            if field not in text:
                errors.append(f"finding field not found: {field}")
    elif has_findings_section and not severity_matches:
        warnings.append("主要发现 section exists but no [S0-S3 ...] severity markers were found")

    risky_claims = ["tests pass", "verified", "已验证", "测试通过", "build passed"]
    if any(claim in text.lower() for claim in risky_claims[:2]) or any(claim in text for claim in risky_claims[2:]):
        if not re.search(r"(Not run|未运行|未验证|Verification|验证建议|command|命令)", text):
            warnings.append("report may contain verification claims without validation context")

    if re.search(r"(感觉|可能吧|看起来不太好|code smell)", text, re.I) and "Evidence" not in text:
        warnings.append("possible vague finding without evidence")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "severity_count": len(severity_matches),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DBX diff review report shape.")
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
