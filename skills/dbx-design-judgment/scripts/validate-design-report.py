#!/usr/bin/env python3
"""Validate the handoff shape of a DBX design judgment Markdown report.

This script is intentionally conservative. It checks whether a saved report contains
expected sections, P0-P3 findings, evidence markers, impact markers, fix markers,
validation markers, confidence markers, and uncertainty markers. It also warns when
implementation-edit language appears.

It does not judge whether the design analysis is true.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_SECTIONS = [
    r"核心判断|判断|Design Judgment|Verdict",
    r"范围和证据|证据|Scope|Evidence|可见事实",
    r"设计模型|Design model|设计目标|Design read|目标用户|User",
]

REPORT_SHAPES = {
    "standard": [
        r"核心判断|Design Judgment|Verdict",
        r"范围和证据|Scope|Evidence",
        r"设计模型|Design model|目标用户|User",
    ],
    "compact": [
        r"判断|Verdict",
        r"最关键的问题|Key issue|主要问题",
        r"下一步|Next step|最小修正",
    ],
    "screenshot_review": [
        r"截图判断|Screenshot review",
        r"可见事实|Visible facts",
        r"截图无法证明|Cannot prove|无法证明",
    ],
    "design_brief": [
        r"Design read|需求理解",
        r"设计目标|Design goals",
        r"状态设计|States|状态",
        r"交付给实现者|Handoff",
    ],
    "code_design_alignment": [
        r"设计与代码是否对齐|code.*design|design.*code",
        r"设计系统观察|tokens|components|states",
    ],
    "insufficient_context": [
        r"暂不能下结论|信息不足|insufficient context|cannot judge",
        r"需要补充的最少问题|blocking questions|minimal questions",
    ],
}

UNCERTAINTY_MARKERS = [
    r"未验证|not verified|not run|未查看|unknown|假设|assumption|仍需确认|缺少|无法证明",
]

FORBIDDEN_IMPLEMENTATION_PATTERNS = [
    r"(?m)^diff --git\b",
    r"(?m)^\+\+\+ b/",
    r"(?m)^--- a/",
    r"apply_patch",
    r"I changed|I've changed|I modified|我已经修改|已修改文件|改了文件",
    r"npm install|pnpm add|yarn add|bun add",
    r"git commit|committed",
]

OVERCONFIDENT_PATTERNS = [
    r"一定会|保证|肯定转化|完全合规|符合\s*WCAG|测试已通过|验证通过|可以上线|用户一定",
]

HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
FINDING_RE = re.compile(
    r"(?m)^\s*(?:\d+\.|-)?\s*\[(P[0-3])\s+(blocker|high|medium|low)\]\s*.*$",
    re.I,
)

FINDING_FIELDS = {
    "Evidence": r"(?m)^\s*[-*]\s*(Evidence|证据|看到什么)\s*[:：]",
    "Impact": r"(?m)^\s*[-*]\s*(Impact|Design impact|Product impact|影响|为什么重要|风险)\s*[:：]",
    "Fix": r"(?m)^\s*[-*]\s*(Fix|修正|建议|改法|Recommendation|Direction)\s*[:：]",
    "Validation": r"(?m)^\s*[-*]\s*(Validation|验证|如何验证|实验|测试)\s*[:：]",
    "Confidence": r"(?m)^\s*[-*]\s*(Confidence|置信度)\s*[:：]",
}


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def has_pattern(text: str, pattern: str) -> bool:
    return re.search(pattern, text, re.I | re.S) is not None


def collect_headings(text: str) -> list[str]:
    return [match.group(1).strip() for match in HEADING_RE.finditer(text)]


def has_heading(headings: list[str], pattern: str) -> bool:
    return any(re.search(pattern, heading, re.I) for heading in headings)


def matched_report_shapes(headings: list[str]) -> list[str]:
    matches: list[str] = []
    for name, patterns in REPORT_SHAPES.items():
        if all(has_heading(headings, pattern) for pattern in patterns):
            matches.append(name)
    return matches


def finding_block(text: str, match: re.Match[str]) -> str:
    following = text[match.end():]
    next_finding = FINDING_RE.search(following)
    next_heading = re.search(r"(?m)^#{1,6}\s+", following)
    end_candidates = [
        match.end() + next_match.start()
        for next_match in (next_finding, next_heading)
        if next_match is not None
    ]
    end = min(end_candidates) if end_candidates else len(text)
    return text[match.start():end]


def validate_report(text: str) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    metrics: dict[str, Any] = {}

    headings = collect_headings(text)
    shapes = matched_report_shapes(headings)
    metrics["matched_shapes"] = shapes

    if not shapes:
        issues.append({
            "level": "error",
            "message": "Report does not match a known design judgment shape via Markdown headings.",
        })

    insufficient_context = has_pattern(text, r"暂不能下结论|信息不足|insufficient context|cannot judge")

    if not insufficient_context:
        for pattern in REQUIRED_SECTIONS:
            if not has_heading(headings, pattern):
                issues.append({"level": "error", "message": f"Missing required heading matching: {pattern}"})

    findings = list(FINDING_RE.finditer(text))
    metrics["finding_count"] = len(findings)
    metrics["severities"] = [m.group(1).upper() for m in findings]

    no_major_findings = has_pattern(text, r"未发现|no major findings|no blocking|没有.*阻止")
    if not findings and not insufficient_context and not no_major_findings:
        issues.append({
            "level": "warning",
            "message": "No P0-P3 findings found. This is okay only for insufficient-context or no-major-findings reports.",
        })

    if findings:
        for index, match in enumerate(findings, start=1):
            block = finding_block(text, match)
            for label, pattern in FINDING_FIELDS.items():
                if not has_pattern(block, pattern):
                    issues.append({"level": "error", "message": f"Finding {index} should include {label}."})

    if not any(has_pattern(text, p) for p in UNCERTAINTY_MARKERS):
        issues.append({
            "level": "warning",
            "message": "Report should disclose unknowns, assumptions, not-viewed artifacts, or not-verified checks.",
        })

    for pattern in FORBIDDEN_IMPLEMENTATION_PATTERNS:
        if has_pattern(text, pattern):
            issues.append({
                "level": "error",
                "message": f"Report appears to contain implementation/editing output matching: {pattern}",
            })

    for pattern in OVERCONFIDENT_PATTERNS:
        if has_pattern(text, pattern):
            issues.append({
                "level": "warning",
                "message": f"Report may contain overconfident wording matching: {pattern}. Ensure claims are tied to evidence.",
            })

    ok = not any(i["level"] == "error" for i in issues)
    return {"ok": ok, "issues": issues, "metrics": metrics}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a DBX design judgment Markdown report shape.")
    parser.add_argument("report", help="Path to Markdown report, or '-' for stdin.")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format. Default: json.")
    args = parser.parse_args()

    try:
        text = read_input(args.report)
    except OSError as exc:
        print(f"error: could not read report: {exc}", file=sys.stderr)
        return 2

    result = validate_report(text)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("OK" if result["ok"] else "FAILED")
        for issue in result["issues"]:
            print(f"[{issue['level']}] {issue['message']}")
        print(f"findings: {result['metrics']['finding_count']}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
