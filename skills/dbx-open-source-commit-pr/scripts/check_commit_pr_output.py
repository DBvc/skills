#!/usr/bin/env python3
"""Check public/open-source commit and PR text for common DBX quality issues."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VAGUE_VALIDATION = [
    r"tested locally",
    r"verified it works",
    r"works as expected",
    r"should be fine",
    r"looks good",
    r"basic testing",
]

PROCESS_CHATTER = [
    r"first tried",
    r"initially tried",
    r"after feedback",
    r"review comments?",
    r"chat discussion",
    r"debugging session",
    r"temporary workaround",
    r"reverted approach",
    r"Slack",
    r"internal ticket",
]

PRIVATE_BLOCKERS = [
    r"\bM-\d+\b",
    r"\bJIRA-[A-Z0-9]+\b",
    r"customer secret",
    r"access token",
    r"\bapi[_ -]?key\b",
    r"\bapi[_ -]?token\b",
    r"secret[_ -]?key",
    r"personal access token",
]

PRIVATE_WARNINGS = [
    r"Linear ticket",
]

REQUIRED_PR_SECTIONS = ["Summary", "Why", "Validation"]
KNOWN_PR_SECTIONS = REQUIRED_PR_SECTIONS + ["Risks", "Risk", "Testing", "Tests", "Test plan", "Notes"]


def read_input(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    return sys.stdin.read()


def has_section(text: str, name: str) -> bool:
    return section_heading_re(name).search(text) is not None


def section_heading_re(name: str) -> re.Pattern[str]:
    escaped = re.escape(name)
    return re.compile(rf"(?im)^\s*(?:#{{1,6}}\s+{escaped}\s*:?|{escaped}\s*:)\s*$")


def section_body(text: str, name: str) -> str:
    match = section_heading_re(name).search(text)
    if not match:
        return ""
    tail = text[match.end() :]
    known_sections = "|".join(re.escape(section) for section in KNOWN_PR_SECTIONS)
    next_section = re.search(
        rf"(?im)^\s*(?:#{{1,6}}\s+\S.*|(?:{known_sections})\s*:)\s*$",
        tail,
    )
    if next_section:
        return tail[: next_section.start()]
    return tail


def find_patterns(text: str, patterns: list[str]) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check open-source commit/PR text for vague validation, process chatter, and missing public PR sections.",
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

    vague = find_patterns(text, VAGUE_VALIDATION)
    if vague:
        errors.append("vague validation wording found: " + ", ".join(vague))

    chatter = find_patterns(text, PROCESS_CHATTER)
    if chatter:
        warnings.append("possible implementation-journey or internal-process chatter: " + ", ".join(chatter))

    private_blockers = find_patterns(text, PRIVATE_BLOCKERS)
    if private_blockers:
        errors.append("private/internal marker found in public text: " + ", ".join(private_blockers))

    private_warnings = find_patterns(text, PRIVATE_WARNINGS)
    if private_warnings:
        warnings.append("possible private/internal marker in public text: " + ", ".join(private_warnings))

    if args.artifact in {"pr", "both"}:
        for section in REQUIRED_PR_SECTIONS:
            if not has_section(text, section):
                errors.append(f"missing PR section: {section}:")
        if has_section(text, "Validation"):
            validation_body = section_body(text, "Validation")
            if not re.search(r"(?im)^\s*-?\s*(Automated|Manual|Not run)\s*:", validation_body):
                errors.append("Validation section should include Automated, Manual, or Not run evidence lines")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "artifact": args.artifact,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "OK" if result["ok"] else "FAIL"
        print(status)
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
