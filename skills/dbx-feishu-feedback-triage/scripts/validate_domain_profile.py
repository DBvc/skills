#!/usr/bin/env python3
"""Lightweight domain profile checker for dbx-feishu-feedback-triage.

This script intentionally avoids PyYAML so it can run in minimal agent hosts.
It checks for required top-level keys and obvious placeholder/security issues.
It is not a full YAML validator.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "domain_id",
    "domain_name",
    "timezone",
    "scope",
    "default_chats",
    "knowledge_sources",
    "read_policy",
    "memory_policy",
    "report_profile",
]

SECRET_PATTERNS = [
    re.compile(r"(?i)(access[_-]?key|secret|token|cookie|authorization)\s*[:=]\s*[^\s<]+"),
    re.compile(r"(?i)(AKIA[0-9A-Z]{16})"),
]


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def top_level_present(text: str, key: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}\s*:", text) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a feedback-triage domain profile skeleton.")
    parser.add_argument("profile", help="Path to domain-profile YAML/JSON/text file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    path = Path(args.profile)
    if not path.exists():
        print(json.dumps({"ok": False, "errors": [f"file not found: {path}"]}, ensure_ascii=False, indent=2))
        return 2

    text = load_text(path)
    errors: list[str] = []
    warnings: list[str] = []

    missing = [key for key in REQUIRED_TOP_LEVEL if not top_level_present(text, key)]
    if missing:
        errors.append("missing required top-level keys: " + ", ".join(missing))

    if "<" in text and ">" in text:
        warnings.append("profile still contains angle-bracket placeholders")

    if not re.search(r"oc_[A-Za-z0-9]+|chat_id\s*:\s*\"?unknown\"?", text):
        warnings.append("no obvious Feishu chat_id like oc_xxx found")

    if not re.search(r"https?://|feishu|larksuite|local path|<Feishu", text, re.I):
        warnings.append("no obvious document/source URL or placeholder found")

    for pat in SECRET_PATTERNS:
        if pat.search(text):
            errors.append("possible secret-like value found; remove credentials from domain profile")
            break

    result = {
        "ok": not errors and not (args.strict and warnings),
        "profile": str(path),
        "required_keys_found": [key for key in REQUIRED_TOP_LEVEL if top_level_present(text, key)],
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
