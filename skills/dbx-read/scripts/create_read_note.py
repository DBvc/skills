#!/usr/bin/env python3
"""Create a safe local Markdown reading note.

This script has no network access and uses only the Python standard library.
It writes a Markdown file from stdin or a content file, avoids silent overwrite,
and emits structured JSON to stdout.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


def slugify(title: str, fallback_seed: str) -> str:
    text = title.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    if text:
        return text[:80].strip("-")
    digest = hashlib.sha1(fallback_seed.encode("utf-8", errors="ignore")).hexdigest()[:8]
    return f"read-note-{digest}"


def read_content(path: str | None) -> str:
    if path is None or path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def parse_tags(raw_tags: list[str] | None) -> list[str]:
    if not raw_tags:
        return []
    tags: list[str] = []
    for raw in raw_tags:
        for part in raw.split(","):
            tag = part.strip()
            if tag:
                tags.append(tag)
    return tags


def yaml_scalar(value: str) -> str:
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def build_frontmatter(args: argparse.Namespace, retrieved: str, tags: list[str]) -> str:
    tag_text = "[" + ", ".join(yaml_scalar(tag) for tag in tags) + "]"
    lines = [
        "---",
        f"title: {yaml_scalar(args.title)}",
        f"source: {yaml_scalar(args.source or '')}",
        f"source_type: {yaml_scalar(args.source_type)}",
        f"author: {yaml_scalar(args.author or '')}",
        f"published: {yaml_scalar(args.published or '')}",
        f"retrieved: {yaml_scalar(retrieved)}",
        f"reading_mode: {yaml_scalar(args.mode)}",
        f"coverage: {yaml_scalar(args.coverage)}",
        f"confidence: {yaml_scalar(args.confidence)}",
        f"caveats: {yaml_scalar(args.caveats or '')}",
        f"tags: {tag_text}",
        "---",
        "",
    ]
    return "\n".join(lines)


def choose_path(output_dir: Path, base_name: str, overwrite: bool) -> tuple[Path, bool]:
    candidate = output_dir / f"{base_name}.md"
    if overwrite or not candidate.exists():
        return candidate, False
    for index in range(2, 1000):
        alt = output_dir / f"{base_name}-{index}.md"
        if not alt.exists():
            return alt, True
    raise RuntimeError("Could not find a non-conflicting filename after 999 attempts.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a safe local Markdown reading note.")
    parser.add_argument("--title", required=True, help="Note title.")
    parser.add_argument("--source", default="", help="Source URL, path, or description.")
    parser.add_argument("--source-type", default="unknown", help="url, pdf, github, doc, local_file, pasted_text, mixed, unknown.")
    parser.add_argument("--author", default="", help="Source author, if known.")
    parser.add_argument("--published", default="", help="Source publication date, if known.")
    parser.add_argument("--mode", default="capture_note", help="Reading mode.")
    parser.add_argument("--coverage", default="unknown", help="full, partial, selected, failed, unknown.")
    parser.add_argument("--confidence", default="medium", help="high, medium, low.")
    parser.add_argument("--caveats", default="", help="Important extraction or evidence caveats.")
    parser.add_argument("--tag", action="append", help="Tag. May be repeated or comma-separated.")
    parser.add_argument("--output-dir", default="notes/read", help="Directory for the note. Default: notes/read.")
    parser.add_argument("--content-file", default="-", help="Markdown body file, or '-' / omitted for stdin.")
    parser.add_argument("--date", default="", help="Date prefix YYYY-MM-DD. Default: today in local timezone.")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting exact generated path.")
    parser.add_argument("--dry-run", action="store_true", help="Return the planned path and metadata without writing.")
    args = parser.parse_args(argv)

    body = read_content(args.content_file).strip() + "\n"
    if not body.strip():
        print(json.dumps({"ok": False, "error": "empty_content"}, ensure_ascii=False), file=sys.stdout)
        return 2

    date_prefix = args.date or dt.date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_prefix):
        print(json.dumps({"ok": False, "error": "invalid_date", "date": date_prefix}, ensure_ascii=False), file=sys.stdout)
        return 2

    output_dir = Path(args.output_dir)
    slug = slugify(args.title, args.source or args.title)
    base_name = f"{date_prefix}-{slug}"
    path, deconflicted = choose_path(output_dir, base_name, args.overwrite)
    tags = parse_tags(args.tag)
    retrieved = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    content = build_frontmatter(args, retrieved, tags) + body

    result: dict[str, Any] = {
        "ok": True,
        "dry_run": bool(args.dry_run),
        "path": str(path),
        "output_dir": str(output_dir),
        "deconflicted": deconflicted,
        "overwrite": bool(args.overwrite),
        "bytes": len(content.encode("utf-8")),
        "title": args.title,
        "source": args.source,
        "mode": args.mode,
        "coverage": args.coverage,
        "confidence": args.confidence,
    }

    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stdout)
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    if path.exists() and not args.overwrite:
        print(json.dumps({"ok": False, "error": "path_exists", "path": str(path)}, ensure_ascii=False), file=sys.stdout)
        return 3
    path.write_text(content, encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
