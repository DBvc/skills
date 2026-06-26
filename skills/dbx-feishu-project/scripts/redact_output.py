#!/usr/bin/env python3
"""Redact secrets from Feishu/Lark/Meegle command output.

This script is intentionally dependency-free so it can run inside agent skill
sandboxes and local developer machines.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SENSITIVE_KEY_RE = re.compile(
    r"(?i)(secret|token|authorization|cookie|session|password|credential|device[_-]?code|refresh[_-]?token|access[_-]?token|app[_-]?secret)"
)

TEXT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)(Authorization\s*:\s*Bearer\s+)[A-Za-z0-9._\-+/=]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9._\-+/=]{12,}"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(app[_-]?secret\s*[=:]\s*)['\"]?[^'\"\s,}]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)((?:user|tenant|refresh|access)[_-]?token\s*[=:]\s*)['\"]?[^'\"\s,}]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(cookie\s*[=:]\s*)['\"]?[^'\"\r\n]+"), r"\1[REDACTED]"),
]


def redact_text(text: str) -> str:
    redacted = text
    for pattern, replacement in TEXT_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def redact_json(value: Any) -> Any:
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if SENSITIVE_KEY_RE.search(str(key)):
                out[key] = "[REDACTED]"
            else:
                out[key] = redact_json(item)
        return out
    if isinstance(value, list):
        return [redact_json(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_maybe_json(text: str) -> str:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return redact_text(text)
    return json.dumps(redact_json(parsed), ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Redact secret-like values from stdin, a file, or an argument string.")
    parser.add_argument("value", nargs="?", help="Text to redact. If omitted, stdin is used.")
    parser.add_argument("--file", type=Path, help="File to redact.")
    parser.add_argument("--json", action="store_true", help="Parse JSON and redact recursively when possible.")
    args = parser.parse_args()

    if args.file:
        text = args.file.read_text(encoding="utf-8")
    elif args.value is not None:
        text = args.value
    else:
        text = sys.stdin.read()

    if args.json:
        print(redact_maybe_json(text))
    else:
        print(redact_text(text), end="" if text.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
