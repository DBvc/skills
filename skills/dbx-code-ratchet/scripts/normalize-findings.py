#!/usr/bin/env python3
"""Normalize dbx-code-ratchet review findings.

This dependency-free helper extracts optional `ratchet_signals` JSON blocks from
review Markdown. If no block exists, it falls back to a conservative severity-line
parser so the ratchet controller can still reason about findings with lower
parse confidence.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SEVERITIES = {"S0", "S1", "S2", "S3"}

FENCE_RE = re.compile(
    r"```(?P<lang>ratchet_signals|json)?\s*\n(?P<body>[\s\S]*?)\n```",
    re.IGNORECASE,
)
SEVERITY_LINE_RE = re.compile(
    r"^(?:\s*\d+[.)]\s*)?\[(?P<severity>S[0-3])(?:\s+[^\]]+)?\]\s*(?P<title>.+?)\s*$",
    re.MULTILINE,
)


def load_text(path: Path) -> str:
    if str(path) == "-":
        return sys.stdin.read()
    return path.read_text(encoding="utf-8")


def stable_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index:03d}"


def normalize_bool_like(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "y"}:
            return True
        if lowered in {"false", "no", "n"}:
            return False
        if lowered in {"unknown", "null", "none", ""}:
            return "unknown"
    return value


def normalize_finding(raw: dict[str, Any], index: int, source_file: str, producer: str) -> dict[str, Any]:
    severity = str(raw.get("severity", "S2")).upper()
    if severity not in SEVERITIES:
        severity = "S2"

    finding_id = str(raw.get("id") or stable_id("F", index))
    title = str(raw.get("title") or raw.get("summary") or raw.get("name") or "Untitled finding").strip()

    return {
        "id": finding_id,
        "source_file": source_file,
        "source_skill": str(raw.get("source_skill") or raw.get("producer_skill") or producer),
        "severity": severity,
        "category": str(raw.get("category") or "other"),
        "title": title,
        "evidence": str(raw.get("evidence") or raw.get("why_local_repairs_are_risky") or "").strip(),
        "impact": str(raw.get("impact") or "").strip(),
        "fix_direction": str(raw.get("fix_direction") or raw.get("minimal_fix_hint") or raw.get("smaller_direction_hint") or "").strip(),
        "confidence": str(raw.get("confidence") or "unknown").lower(),
        "introduced_by_current_diff": normalize_bool_like(raw.get("introduced_by_current_diff", "unknown")),
        "local_fixable_signal": normalize_bool_like(raw.get("local_fixable_signal", "unknown")),
        "direction_symptom_signal": normalize_bool_like(raw.get("direction_symptom_signal", "unknown")),
        "scope_expansion_required_signal": normalize_bool_like(raw.get("scope_expansion_required_signal", "unknown")),
        "human_decision_required_signal": normalize_bool_like(raw.get("human_decision_required_signal", "unknown")),
        "verification_hint": str(raw.get("verification_hint") or "").strip(),
        "parse_confidence": str(raw.get("parse_confidence") or "high"),
    }


def extract_json_blocks(text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for match in FENCE_RE.finditer(text):
        body = match.group("body").strip()
        lang = (match.group("lang") or "").lower()
        if lang not in {"ratchet_signals", "json"}:
            continue
        if "ratchet_signals_version" not in body and '"findings"' not in body and '"direction_findings"' not in body:
            continue
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            blocks.append(parsed)
    return blocks


def findings_from_signal_block(block: dict[str, Any], source_file: str, producer_arg: str, start_index: int) -> list[dict[str, Any]]:
    producer = str(block.get("producer_skill") or producer_arg)
    result: list[dict[str, Any]] = []

    for key in ("findings", "direction_findings"):
        raw_items = block.get(key, [])
        if not isinstance(raw_items, list):
            continue
        for raw in raw_items:
            if not isinstance(raw, dict):
                continue
            item = dict(raw)
            if key == "direction_findings":
                item.setdefault("category", "direction")
                item.setdefault("direction_symptom_signal", True)
                item.setdefault("scope_expansion_required_signal", item.get("local_repair_recommended_signal") is False)
                item.setdefault("human_decision_required_signal", True)
            result.append(normalize_finding(item, start_index + len(result) + 1, source_file, producer))
    return result


def fallback_markdown_findings(text: str, source_file: str, producer: str, start_index: int) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for idx, match in enumerate(SEVERITY_LINE_RE.finditer(text), start=start_index + 1):
        raw = {
            "id": stable_id("F", idx),
            "severity": match.group("severity"),
            "title": match.group("title").strip(),
            "source_skill": producer,
            "parse_confidence": "medium",
            "confidence": "unknown",
        }
        result.append(normalize_finding(raw, idx, source_file, producer))
    return result


def normalize_inputs(paths: list[Path], producer: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    notes: list[str] = []
    source_files: list[str] = []

    for path in paths:
        source_file = str(path)
        source_files.append(source_file)
        text = load_text(path)
        before_count = len(findings)
        blocks = extract_json_blocks(text)
        for block in blocks:
            findings.extend(findings_from_signal_block(block, source_file, producer, len(findings)))
        if len(findings) == before_count:
            fallback = fallback_markdown_findings(text, source_file, producer, len(findings))
            findings.extend(fallback)
            if fallback:
                notes.append(f"{source_file}: used fallback Markdown severity parser; parse confidence is lower.")
            else:
                notes.append(f"{source_file}: no ratchet_signals block or severity findings found.")

    return {
        "normalized_findings_version": 1,
        "source_files": source_files,
        "producer_hint": producer,
        "findings": findings,
        "parse_notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize ratchet review findings from Markdown or ratchet_signals JSON blocks.")
    parser.add_argument("--input", "-i", action="append", required=True, help="Input review Markdown path. Use '-' for stdin. Repeatable.")
    parser.add_argument("--output", "-o", help="Output JSON path. Defaults to stdout.")
    parser.add_argument("--producer", default="unknown", help="Producer skill hint for fallback Markdown findings.")
    args = parser.parse_args()

    data = normalize_inputs([Path(item) for item in args.input], args.producer)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
