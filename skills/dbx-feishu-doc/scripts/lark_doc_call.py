#!/usr/bin/env python3
"""Safe pass-through wrapper for `lark` / `lark-cli` document commands.

Goals:
- avoid shell string construction;
- default document shortcuts to api-version v2;
- redact stdout/stderr;
- return predictable JSON envelopes;
- keep raw pass-through available when official CLI syntax drifts.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from redact_output import redact_json, redact_text  # noqa: E402


def resolve_binary() -> str | None:
    env_bin = os.environ.get("DBX_LARK_BIN")
    candidates = [env_bin] if env_bin else []
    candidates.extend(["lark", "lark-cli"])
    for candidate in candidates:
        if not candidate:
            continue
        if os.path.isabs(candidate) or "/" in candidate:
            if Path(candidate).exists() and os.access(candidate, os.X_OK):
                return candidate
        else:
            found = shutil.which(candidate)
            if found:
                return found
    return None


def parse_json_maybe(text: str) -> Any | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def has_output_flag(args: list[str]) -> bool:
    return any(arg in {"-o", "--output", "--format"} or arg.startswith("--output=") or arg.startswith("--format=") for arg in args)


def has_api_version(args: list[str]) -> bool:
    return any(arg == "--api-version" or arg.startswith("--api-version=") for arg in args)


def read_content_arg(args: argparse.Namespace) -> str | None:
    if getattr(args, "content_file", None):
        return Path(args.content_file).read_text(encoding="utf-8")
    return getattr(args, "content", None)


def run_lark(cli_args: list[str], *, prefer_json: bool = True, dry_run: bool = False) -> int:
    binary = resolve_binary()
    if not binary:
        envelope = {
            "ok": False,
            "returncode": 127,
            "error": "lark/lark-cli not found. Set DBX_LARK_BIN or install the official CLI.",
            "command": ["lark", *cli_args],
        }
        print(json.dumps(envelope, ensure_ascii=False, indent=2))
        return 127

    final_args = list(cli_args)
    if len(final_args) >= 2 and final_args[0] == "docs" and not has_api_version(final_args):
        final_args.extend(["--api-version", "v2"])
    if dry_run and "--dry-run" not in final_args:
        final_args.append("--dry-run")
    if prefer_json and not has_output_flag(final_args):
        final_args.extend(["-o", "json"])

    command = [binary, *final_args]
    proc = subprocess.run(
        command,
        text=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    stdout = redact_text(proc.stdout)
    stderr = redact_text(proc.stderr)
    parsed = parse_json_maybe(stdout)

    envelope: dict[str, Any] = {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "command": redact_json(command),
        "stdout_json": redact_json(parsed) if parsed is not None else None,
        "stdout": None if parsed is not None else stdout,
        "stderr": stderr,
    }
    print(json.dumps(envelope, ensure_ascii=False, indent=2))
    return proc.returncode


def build_args(args: argparse.Namespace) -> list[str]:
    if args.command == "raw":
        if not args.raw_args:
            raise SystemExit("raw requires arguments after --")
        return args.raw_args
    if args.command == "fetch":
        cmd = ["docs", "+fetch", "--doc", args.doc]
        if args.with_ids:
            cmd.append("--with-ids")
        if args.extra:
            cmd.extend(args.extra)
        return cmd
    if args.command == "create":
        cmd = ["docs", "+create", "--title", args.title]
        content = read_content_arg(args)
        if content is not None:
            cmd.extend(["--content", content])
        if args.extra:
            cmd.extend(args.extra)
        return cmd
    if args.command == "update":
        cmd = ["docs", "+update", "--doc", args.doc]
        content = read_content_arg(args)
        if content is not None:
            cmd.extend(["--content", content])
        if args.extra:
            cmd.extend(args.extra)
        return cmd
    raise SystemExit(f"unknown command: {args.command}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe wrapper around official Lark/Feishu CLI document commands.")
    parser.add_argument("--dry-run", action="store_true", help="Append --dry-run to supported commands.")
    parser.add_argument("--no-json", action="store_true", help="Do not append -o json automatically.")

    sub = parser.add_subparsers(dest="command", required=True)

    raw = sub.add_parser("raw", help="Pass raw arguments to lark. Use: raw -- docs +fetch ...")
    raw.add_argument("raw_args", nargs=argparse.REMAINDER)

    fetch = sub.add_parser("fetch", help="Fetch a document through docs +fetch.")
    fetch.add_argument("--doc", required=True)
    fetch.add_argument("--with-ids", action="store_true")
    fetch.add_argument("extra", nargs=argparse.REMAINDER)

    create = sub.add_parser("create", help="Create a document through docs +create.")
    create.add_argument("--title", required=True)
    create.add_argument("--content")
    create.add_argument("--content-file")
    create.add_argument("extra", nargs=argparse.REMAINDER)

    update = sub.add_parser("update", help="Update a document through docs +update.")
    update.add_argument("--doc", required=True)
    update.add_argument("--content")
    update.add_argument("--content-file")
    update.add_argument("extra", nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)
    cli_args = build_args(args)
    return run_lark(cli_args, prefer_json=not args.no_json, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
