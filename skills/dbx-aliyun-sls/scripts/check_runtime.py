#!/usr/bin/env python3
"""Check local Aliyun CLI / SLS runtime readiness without reading secret files.

This script is intentionally conservative:
- It uses command discovery and normal CLI commands only.
- It does not open ~/.aliyun/config.json.
- It redacts common secret-looking output before printing.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from typing import Sequence


SECRET_PATTERNS = [
    re.compile(r"LTAI[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)((?:access[_ -]?key[_ -]?secret|secret|token|authorization|cookie|set-cookie)\s*[:=]\s*)[^\s,}\]\"']+"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{12,}"),
]


def redact(text: str) -> str:
    out = text
    for pattern in SECRET_PATTERNS:
        if pattern.groups >= 1:
            out = pattern.sub(lambda m: m.group(1) + "<REDACTED>", out)
        else:
            out = pattern.sub("<REDACTED>", out)
    return out


def run(cmd: Sequence[str], timeout: int = 20) -> dict:
    try:
        completed = subprocess.run(
            list(cmd),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": list(cmd),
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": redact(completed.stdout.strip()),
            "stderr": redact(completed.stderr.strip()),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": list(cmd),
            "ok": False,
            "returncode": None,
            "stdout": redact(exc.stdout or ""),
            "stderr": "Command timed out.",
        }
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        return {
            "command": list(cmd),
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }


def main() -> int:
    aliyun_path = shutil.which("aliyun")
    report = {
        "tool": "dbx-aliyun-sls runtime check",
        "aliyun_found": bool(aliyun_path),
        "aliyun_path": aliyun_path,
        "checks": [],
        "summary": [],
    }

    if not aliyun_path:
        report["summary"].append("aliyun CLI not found in PATH.")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    commands = [
        ["aliyun", "version"],
        ["aliyun", "plugin", "list"],
        ["aliyun", "sls", "--help"],
        ["aliyun", "configure", "list"],
    ]

    for cmd in commands:
        result = run(cmd)
        report["checks"].append(result)

    sls_help_ok = any(
        c.get("command") == ["aliyun", "sls", "--help"] and c.get("ok")
        for c in report["checks"]
    )
    if sls_help_ok:
        report["summary"].append("aliyun CLI is available and `aliyun sls --help` succeeded.")
    else:
        report["summary"].append("aliyun CLI is available, but SLS plugin/help check did not succeed. Try `aliyun plugin install --names sls`.")

    configure_ok = any(
        c.get("command") == ["aliyun", "configure", "list"] and c.get("ok")
        for c in report["checks"]
    )
    if configure_ok:
        report["summary"].append("A CLI profile list was returned. Check that the intended profile/region is active.")
    else:
        report["summary"].append("Could not list CLI profiles. Configure credentials outside chat before querying.")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if sls_help_ok and configure_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
