#!/usr/bin/env python3
"""Validate the structural contract of a dbx-product-conception Markdown report.

This standard-library checker validates visible sections, epistemic labels, and
handoff shape. It cannot prove originality, taste, desirability, or product quality.

Usage:
  python3 validate-conception-report.py REPORT.md
  python3 validate-conception-report.py REPORT.md --strict
  python3 validate-conception-report.py REPORT.md --format json
  python3 validate-conception-report.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str


SECTION_PATTERNS: dict[str, tuple[str, ...]] = {
    "insight": (r"核心洞察", r"structural\s+insight", r"opportunity\s+insight"),
    "candidates": (r"候选产品逻辑", r"candidate\s+(?:product\s+)?(?:logics?|concepts?)"),
    "selection": (r"创意选择", r"creative\s+selection", r"pairwise\s+comparison"),
    "selected": (r"选中构想", r"selected\s+(?:conception|concept|direction)", r"product\s+thesis"),
    "specimen": (r"体验样本", r"experience\s+specimen", r"prototype"),
    "epistemics": (r"证据、?押注与未知", r"evidence.*(?:conviction|bet|unknown)", r"epistemic"),
    "handoff": (r"handoff", r"交接"),
}

HANDOFF_STATES = {
    "concept_selected_unvalidated",
    "prototype_required",
    "needs_product_judgment",
    "needs_crystallization",
    "blocked_on_evidence",
    "blocked_on_decision",
}

DANGEROUS_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"乔布斯(?:一定)?会|Steve\s+Jobs\s+would", "Avoid attributing an invented verdict to Steve Jobs."),
    (r"一定成功|必然成功|guaranteed\s+(?:to\s+)?succeed", "A conception report must not guarantee market success."),
    (r"用户不知道自己想要什么", "Do not repeat the user-research myth without explaining that observation and testing still matter."),
    (r"端到端(?:一定|必须)|must\s+own\s+everything", "Integration is contingent; justify must-own, borrowed, and outside layers."),
    (r"直觉(?:已经)?证明|intuition\s+proves", "Intuition or conviction is not proof."),
)


def contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns)


def count_concepts(text: str) -> int:
    patterns = (
        r"^#{2,5}\s*(?:概念|Concept)\s+[A-Z0-9一二三四五六七八九十]",
        r"^\s*[-*]\s*(?:概念|Concept)\s+[A-Z0-9一二三四五六七八九十]\s*[:：]",
    )
    starts: set[int] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            starts.add(match.start())
    return len(starts)


def validate_text(text: str, *, strict: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    lowered = text.lower()
    blocked = "blocked_on_evidence" in lowered or "blocked_on_decision" in lowered

    if not contains_any(text, SECTION_PATTERNS["insight"]):
        issues.append(Issue("error", "missing_insight", "Missing an explicit opportunity or structural insight section."))

    if not contains_any(text, SECTION_PATTERNS["handoff"]):
        issues.append(Issue("error", "missing_handoff", "Missing an explicit handoff section."))

    states = sorted(state for state in HANDOFF_STATES if state in lowered)
    if not states:
        issues.append(Issue("error", "missing_handoff_state", "Handoff must use one allowed state."))
    elif len(states) > 1:
        issues.append(Issue("warning", "multiple_handoff_states", f"Multiple handoff states found: {', '.join(states)}."))

    if not blocked:
        if not contains_any(text, SECTION_PATTERNS["selected"]):
            issues.append(Issue("error", "missing_selected", "Missing the selected product conception or product thesis."))
        if not contains_any(text, SECTION_PATTERNS["specimen"]):
            issues.append(Issue("error", "missing_specimen", "Missing a concrete experience specimen or prototype plan."))
        if not contains_any(text, SECTION_PATTERNS["selection"]):
            issues.append(Issue("error", "missing_selection", "Missing comparative creative selection."))

        concept_count = count_concepts(text)
        explicit_exception = re.search(
            r"(无需|不需要|没有必要).{0,30}(替代|候选)|justified\s+reason\s+not",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if concept_count < 3 and not explicit_exception:
            issues.append(Issue(
                "warning",
                "weak_divergence",
                f"Found {concept_count} clearly labeled concepts; open conception normally needs at least 3 distinct product logics.",
            ))

    required_labels = {
        "evidence": (r"\bevidence\b", r"证据"),
        "inference": (r"\binference\b", r"推断|推论"),
        "conviction": (r"\bconviction\b", r"信念|确信|创作者主张"),
        "unknowns": (r"\bunknowns?\b", r"未知"),
    }
    for label, patterns in required_labels.items():
        if not contains_any(text, patterns):
            level = "error" if strict else "warning"
            issues.append(Issue(level, f"missing_{label}", f"Missing explicit {label} labeling."))

    safeguards = {
        "kill_list": (r"kill\s+list", r"淘汰清单|删除清单|淘汰"),
        "non_goals": (r"non[- ]?goals?", r"非目标|不做"),
        "disconfirmation": (r"disconfirm", r"证伪|反证|放弃条件|重构条件"),
    }
    for label, patterns in safeguards.items():
        if not contains_any(text, patterns):
            level = "error" if strict else "warning"
            issues.append(Issue(level, f"missing_{label}", f"Missing {label.replace('_', ' ')}."))

    for pattern, message in DANGEROUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            level = "error" if strict else "warning"
            issues.append(Issue(level, "myth_or_overclaim", message))

    if not contains_any(text, SECTION_PATTERNS["epistemics"]):
        issues.append(Issue(
            "warning",
            "missing_epistemic_section",
            "Consider grouping evidence, inference, conviction, bets, and unknowns in one visible section.",
        ))

    return issues


def render_text(path: str, issues: list[Issue], strict: bool) -> str:
    errors = sum(issue.level == "error" for issue in issues)
    warnings = sum(issue.level == "warning" for issue in issues)
    lines = [
        f"Conception report validation: {path}",
        f"strict={str(strict).lower()} errors={errors} warnings={warnings}",
    ]
    if not issues:
        lines.append("OK: structural contract satisfied.")
    else:
        lines.extend(f"- {issue.level.upper()} [{issue.code}] {issue.message}" for issue in issues)
    lines.append("Note: structural validation only; originality, taste, desirability, and product quality are not proved.")
    return "\n".join(lines)


def run_self_test() -> int:
    valid = """# Product Conception Report
## 核心洞察
结构性机会。
## 候选产品逻辑
### 概念 A
#### Experience specimen
A prototype.
### 概念 B
#### Experience specimen
B prototype.
### 概念 C
#### Experience specimen
C prototype.
## 创意选择
A vs B, B vs C. 淘汰 B 和 C。
## 选中构想
Product thesis. Deliberate non-goals. Kill list. Disconfirming signals.
## 第一份体验样本
Prototype plan.
## 证据、押注与未知
Evidence. Inference. Conviction. Bet. Unknowns.
## Handoff
State: concept_selected_unvalidated
"""
    invalid = """# Idea
Steve Jobs would know this is guaranteed to succeed.
## Handoff
TBD
"""
    valid_issues = validate_text(valid, strict=True)
    invalid_issues = validate_text(invalid, strict=True)
    if any(issue.level == "error" for issue in valid_issues):
        print(render_text("<valid fixture>", valid_issues, True))
        return 1
    if not any(issue.level == "error" for issue in invalid_issues):
        print("Self-test failed: invalid fixture was accepted.")
        return 1
    print("Self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a dbx-product-conception Markdown report.")
    parser.add_argument("report", nargs="?", help="Path to the Markdown report.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format.")
    parser.add_argument("--strict", action="store_true", help="Treat missing epistemic and selection safeguards as errors.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in valid and invalid fixtures.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if not args.report:
        parser.error("report is required unless --self-test is used")

    path = Path(args.report)
    if not path.is_file():
        print(f"Report not found: {path}", file=sys.stderr)
        return 2

    issues = validate_text(path.read_text(encoding="utf-8"), strict=args.strict)
    errors = sum(issue.level == "error" for issue in issues)
    warnings = sum(issue.level == "warning" for issue in issues)

    if args.format == "json":
        print(json.dumps({
            "path": str(path),
            "strict": args.strict,
            "summary": {"errors": errors, "warnings": warnings},
            "issues": [asdict(issue) for issue in issues],
            "limitation": "Structural validation only; originality, taste, desirability, and product quality are not proved.",
        }, ensure_ascii=False, indent=2))
    else:
        print(render_text(str(path), issues, args.strict))

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
