#!/usr/bin/env python3
"""Safe wrapper around `aliyun sls get-logs-v2`.

Goals:
- keep SLS log queries read-only;
- normalize time ranges;
- default to narrow windows;
- prevent huge raw result pulls by default;
- support dry-run;
- redact common secret-looking output.

This script does not manage credentials and does not read ~/.aliyun/config.json.
Configure Aliyun CLI outside chat.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
from typing import Iterable, Sequence


DEFAULT_RAW_MINUTES = 15
DEFAULT_MAX_RANGE_MINUTES = 60
MAX_RAW_LINE = 100

SECRET_PATTERNS = [
    re.compile(r"LTAI[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)((?:access[_ -]?key[_ -]?secret|secret|token|authorization|cookie|set-cookie|api[_ -]?key|password|passwd|pwd)\s*[:=]\s*)[^\s,}\]\"']+"),
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


def parse_time(value: str) -> int:
    """Parse Unix seconds or ISO-like datetime into Unix seconds."""
    value = value.strip()
    if re.fullmatch(r"\d{10,13}", value):
        number = int(value)
        return number // 1000 if number > 9_999_999_999 else number

    normalized = value.replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid time {value!r}; use Unix seconds or ISO format like 2026-06-29T10:00:00+08:00"
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return int(parsed.timestamp())


def is_sql_query(query: str) -> bool:
    return bool(re.search(r"\|\s*select\b", query, flags=re.IGNORECASE))


def shell_join(cmd: Sequence[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def build_command(args: argparse.Namespace, start: int, end: int) -> list[str]:
    cmd = [
        "aliyun",
        "sls",
        "get-logs-v2",
        "--project",
        args.project,
        "--logstore",
        args.logstore,
        "--from",
        str(start),
        "--to",
        str(end),
        "--query",
        args.query,
    ]

    if args.profile:
        cmd.extend(["--profile", args.profile])
    if args.region:
        cmd.extend(["--region", args.region])

    if is_sql_query(args.query):
        # SLS SQL should limit rows inside SQL. The API docs recommend line/offset 0 for SQL.
        cmd.extend(["--line", "0", "--offset", "0"])
    else:
        cmd.extend(["--line", str(args.line), "--offset", str(args.offset)])

    cmd.extend(["--reverse", "true" if args.reverse else "false"])
    return cmd


def resolve_time_range(args: argparse.Namespace) -> tuple[int, int, str]:
    now = int(time.time())

    if args.from_time and args.to_time:
        start = parse_time(args.from_time)
        end = parse_time(args.to_time)
        source = "explicit"
    elif args.from_time or args.to_time:
        raise SystemExit("--from and --to must be provided together.")
    else:
        minutes = args.last_minutes if args.last_minutes is not None else DEFAULT_RAW_MINUTES
        end = now
        start = now - minutes * 60
        source = f"last-{minutes}-minutes"

    if end <= start:
        raise SystemExit("--to must be greater than --from.")

    duration = end - start
    max_duration = args.max_range_minutes * 60
    if duration > max_duration and not args.allow_large_range:
        raise SystemExit(
            f"time range is {duration // 60} minutes, above the default {args.max_range_minutes} minute limit. "
            "Use --allow-large-range after explicit confirmation."
        )

    return start, end, source


def run_command(cmd: Sequence[str], timeout: int) -> dict:
    try:
        completed = subprocess.run(
            list(cmd),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        stdout = redact(completed.stdout)
        stderr = redact(completed.stderr)
        parsed_stdout = None
        try:
            parsed_stdout = json.loads(stdout) if stdout.strip() else None
        except json.JSONDecodeError:
            parsed_stdout = None

        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout_json": parsed_stdout,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": None,
            "stdout_json": None,
            "stdout": redact(exc.stdout or "").strip(),
            "stderr": "Command timed out.",
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a bounded read-only Aliyun SLS get-logs-v2 query.")
    parser.add_argument("--project", required=True, help="SLS project name.")
    parser.add_argument("--logstore", required=True, help="SLS logstore name.")
    parser.add_argument("--query", default="*", help="SLS index query, SQL query, or SPL query text.")
    parser.add_argument("--from", dest="from_time", help="Start time: Unix seconds/ms or ISO datetime.")
    parser.add_argument("--to", dest="to_time", help="End time: Unix seconds/ms or ISO datetime.")
    parser.add_argument("--last-minutes", type=int, help=f"Relative time window ending now. Default: {DEFAULT_RAW_MINUTES}.")
    parser.add_argument("--line", type=int, default=MAX_RAW_LINE, help=f"Raw log line limit. Max: {MAX_RAW_LINE}. Ignored for SQL mode.")
    parser.add_argument("--offset", type=int, default=0, help="Raw log offset. Ignored for SQL mode.")
    parser.add_argument("--reverse", dest="reverse", action="store_true", default=True, help="Return latest raw logs first. Default.")
    parser.add_argument("--forward", dest="reverse", action="store_false", help="Return logs in chronological order.")
    parser.add_argument("--profile", help="Optional Aliyun CLI profile for this command.")
    parser.add_argument("--region", help="Optional Aliyun CLI region for this command.")
    parser.add_argument("--max-range-minutes", type=int, default=DEFAULT_MAX_RANGE_MINUTES, help="Default max query window unless --allow-large-range is set.")
    parser.add_argument("--allow-large-range", action="store_true", help="Allow time range above --max-range-minutes after explicit approval.")
    parser.add_argument("--timeout", type=int, default=60, help="Subprocess timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Print command envelope without executing.")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.last_minutes is not None and args.last_minutes <= 0:
        raise SystemExit("--last-minutes must be positive.")
    if args.line < 0 or args.line > MAX_RAW_LINE:
        raise SystemExit(f"--line must be between 0 and {MAX_RAW_LINE}.")
    if args.offset < 0:
        raise SystemExit("--offset must be >= 0.")

    start, end, time_source = resolve_time_range(args)
    cmd = build_command(args, start, end)
    command_text = shell_join(cmd)

    envelope = {
        "tool": "dbx-aliyun-sls sls_query.py",
        "read_only": True,
        "dry_run": args.dry_run,
        "target": {
            "project": args.project,
            "logstore": args.logstore,
            "profile": args.profile,
            "region": args.region,
        },
        "time_range": {
            "from": start,
            "to": end,
            "duration_seconds": end - start,
            "source": time_source,
        },
        "query": {
            "text": args.query,
            "mode": "sql" if is_sql_query(args.query) else "raw_or_index",
            "line": 0 if is_sql_query(args.query) else args.line,
            "offset": 0 if is_sql_query(args.query) else args.offset,
            "reverse": args.reverse,
        },
        "command": redact(command_text),
    }

    if args.dry_run:
        envelope["result"] = None
        print(json.dumps(envelope, ensure_ascii=False, indent=2))
        return 0

    if shutil.which("aliyun") is None:
        envelope["result"] = {
            "ok": False,
            "returncode": None,
            "stdout_json": None,
            "stdout": "",
            "stderr": "aliyun CLI not found in PATH.",
        }
        print(json.dumps(envelope, ensure_ascii=False, indent=2))
        return 1

    envelope["result"] = run_command(cmd, timeout=args.timeout)
    print(json.dumps(envelope, ensure_ascii=False, indent=2))
    return 0 if envelope["result"]["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
