#!/usr/bin/env python3
"""Score dbx-code-ratchet progress from normalized findings.

The score is intentionally coarse. It supports the ratchet progress gate; it is
not a substitute for human engineering judgment.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

WEIGHTS = {"S0": 100, "S1": 25, "S2": 5, "S3": 1}
CLOSED_STATUSES = {"fixed", "closed", "resolved", "reject_false_positive", "defer_not_worth", "deferred", "rejected"}


def load_json(path: Path) -> Any:
    if str(path) == "-":
        return json.loads(sys.stdin.read())
    return json.loads(path.read_text(encoding="utf-8"))


def get_findings(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        if isinstance(data.get("findings"), list):
            return [item for item in data["findings"] if isinstance(item, dict)]
        if isinstance(data.get("open_findings"), list):
            return [item for item in data["open_findings"] if isinstance(item, dict)]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def severity_of(item: dict[str, Any]) -> str:
    severity = str(item.get("severity", "S2")).upper()
    return severity if severity in WEIGHTS else "S2"


def is_open(item: dict[str, Any]) -> bool:
    status = str(item.get("status") or item.get("triage_status") or item.get("resolution") or "open").lower()
    return status not in CLOSED_STATUSES


def summarize(items: list[dict[str, Any]]) -> dict[str, Any]:
    open_items = [item for item in items if is_open(item)]
    counts = {key: 0 for key in WEIGHTS}
    for item in open_items:
        counts[severity_of(item)] += 1
    score = sum(counts[sev] * weight for sev, weight in WEIGHTS.items())
    ids = [str(item.get("id") or item.get("title") or "") for item in open_items]
    return {
        "open_counts": counts,
        "open_risk_score": score,
        "open_count": len(open_items),
        "open_ids": ids,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score before/after ratchet findings and emit a progress-gate hint.")
    parser.add_argument("--before", required=True, help="Before findings JSON path.")
    parser.add_argument("--after", required=True, help="After findings JSON path.")
    parser.add_argument("--output", "-o", help="Output JSON path. Defaults to stdout.")
    parser.add_argument("--complexity-exceeded", action="store_true", help="Mark complexity budget as exceeded.")
    parser.add_argument("--validation-worse", action="store_true", help="Mark validation as worse after repair.")
    parser.add_argument("--scope-expanded", action="store_true", help="Mark scope as expanded after repair.")
    parser.add_argument("--direction-health", choices=["ok", "suspect", "failed"], default="ok", help="Direction health after repair.")
    args = parser.parse_args()

    before_items = get_findings(load_json(Path(args.before)))
    after_items = get_findings(load_json(Path(args.after)))
    before = summarize(before_items)
    after = summarize(after_items)

    new_high_risk = after["open_counts"]["S0"] > before["open_counts"]["S0"] or after["open_counts"]["S1"] > before["open_counts"]["S1"]
    risk_decreased = after["open_risk_score"] < before["open_risk_score"]
    open_decreased = after["open_count"] < before["open_count"]

    should_continue = (
        (risk_decreased or after["open_count"] == 0)
        and not new_high_risk
        and not args.complexity_exceeded
        and not args.validation_worse
        and not args.scope_expanded
        and args.direction_health != "failed"
    )

    if args.direction_health == "failed":
        gate = "stopped-direction-failure"
    elif new_high_risk or args.complexity_exceeded or args.validation_worse or args.scope_expanded or not (risk_decreased or after["open_count"] == 0):
        gate = "stopped-diverging"
    elif after["open_count"] == 0:
        gate = "pass-ready"
    elif should_continue:
        gate = "continue-if-round-budget-remains"
    else:
        gate = "needs-human-decision"

    result = {
        "ratchet_progress_score_version": 1,
        "before": before,
        "after": after,
        "delta_risk_score": after["open_risk_score"] - before["open_risk_score"],
        "risk_decreased": risk_decreased,
        "open_count_decreased": open_decreased,
        "new_s0_or_s1": new_high_risk,
        "complexity_budget_exceeded": args.complexity_exceeded,
        "validation_worse": args.validation_worse,
        "scope_expanded": args.scope_expanded,
        "direction_health": args.direction_health,
        "gate_hint": gate,
    }

    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
