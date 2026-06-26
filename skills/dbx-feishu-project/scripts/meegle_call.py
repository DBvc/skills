#!/usr/bin/env python3
"""Safe pass-through wrapper for `meegle` / `meegle-cli`.

Goals:
- avoid shell string construction;
- keep JSON output in a predictable envelope;
- redact stdout/stderr before showing it to the user;
- provide a few common Feishu Project shortcuts while allowing raw pass-through.

The wrapper does not replace the official CLI. If a shortcut drifts from the
current CLI syntax, use `raw -- ...` with the exact command from `meegle --help`.
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
    env_bin = os.environ.get("DBX_MEEGLE_BIN")
    candidates = [env_bin] if env_bin else []
    candidates.extend(["meegle", "meegle-cli"])
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


def run_meegle(cli_args: list[str], *, prefer_json: bool = True, dry_run: bool = False, cwd: Path | None = None) -> int:
    binary = resolve_binary()
    if not binary:
        envelope = {
            "ok": False,
            "returncode": 127,
            "error": "meegle/meegle-cli not found. Set DBX_MEEGLE_BIN or install the official CLI.",
            "command": ["meegle", *cli_args],
        }
        print(json.dumps(envelope, ensure_ascii=False, indent=2))
        return 127

    final_args = list(cli_args)
    if dry_run and "--dry-run" not in final_args:
        final_args.append("--dry-run")
    if prefer_json and not has_output_flag(final_args):
        final_args.extend(["-o", "json"])

    command = [binary, *final_args]
    proc = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
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
    if args.command == "decode-url":
        return ["url", "decode", "--url", args.url]
    if args.command == "project-search":
        return ["project", "search", "--project-key", args.query]
    if args.command == "meta-types":
        return ["workitem", "meta-types", "--project-key", args.project_key]
    if args.command == "meta-fields":
        cmd = ["workitem", "meta-fields", "--project-key", args.project_key]
        if args.work_item_type:
            cmd.extend(["--work-item-type", args.work_item_type])
        return cmd
    if args.command == "workitem-get":
        return ["workitem", "get", "--project-key", args.project_key, "--work-item-id", args.work_item_id]
    if args.command == "workitem-query":
        cmd = ["workitem", "query", "--project-key", args.project_key]
        if args.mql:
            cmd.extend(["--mql", args.mql])
        if args.page_size:
            cmd.extend(["--page-size", str(args.page_size)])
        return cmd
    raise SystemExit(f"unknown command: {args.command}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe wrapper around official Meegle CLI.")
    parser.add_argument("--dry-run", action="store_true", help="Append --dry-run to supported commands.")
    parser.add_argument("--no-json", action="store_true", help="Do not append -o json automatically.")

    sub = parser.add_subparsers(dest="command", required=True)

    raw = sub.add_parser("raw", help="Pass raw arguments to meegle. Use: raw -- workitem get ...")
    raw.add_argument("raw_args", nargs=argparse.REMAINDER)

    decode = sub.add_parser("decode-url", help="Decode a Feishu Project URL.")
    decode.add_argument("--url", required=True)

    project = sub.add_parser("project-search", help="Search or resolve a project key.")
    project.add_argument("--query", required=True)

    meta_types = sub.add_parser("meta-types", help="List work item types for a project.")
    meta_types.add_argument("--project-key", required=True)

    meta_fields = sub.add_parser("meta-fields", help="List fields for a project or work item type.")
    meta_fields.add_argument("--project-key", required=True)
    meta_fields.add_argument("--work-item-type")

    get_item = sub.add_parser("workitem-get", help="Read a work item by id.")
    get_item.add_argument("--project-key", required=True)
    get_item.add_argument("--work-item-id", required=True)

    query_item = sub.add_parser("workitem-query", help="Query work items with MQL when supported by the CLI.")
    query_item.add_argument("--project-key", required=True)
    query_item.add_argument("--mql")
    query_item.add_argument("--page-size", type=int, default=50)

    args = parser.parse_args(argv)
    cli_args = build_args(args)
    return run_meegle(cli_args, prefer_json=not args.no_json, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
