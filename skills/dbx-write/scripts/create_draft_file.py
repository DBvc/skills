#!/usr/bin/env python3
"""Create a Markdown draft file for dbx-write.

The script is intentionally small and dependency-free. It writes Markdown
content to a safe filename and returns structured JSON so an agent can report
the exact artifact path.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path


def slugify(text: str) -> str:
    text = text.strip().lower()
    # Keep ASCII letters/numbers/hyphens. Non-ASCII titles fall back to date slug.
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:80] or "draft"


def read_content(content_file: str | None) -> str:
    if not content_file:
        return ""
    if content_file == "-":
        return sys.stdin.read()
    return Path(content_file).read_text(encoding="utf-8")


def build_frontmatter(title: str, lang: str, status: str, created: str) -> str:
    safe_title = title.replace('"', '\\"')
    return (
        "---\n"
        f'title: "{safe_title}"\n'
        f"lang: {lang}\n"
        f"status: {status}\n"
        f"created: {created}\n"
        "skill: dbx-write\n"
        "---\n\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a dbx-write Markdown draft file."
    )
    parser.add_argument("--title", required=True, help="Draft title.")
    parser.add_argument(
        "--output-dir",
        default="drafts",
        help="Directory to write the draft into. Default: drafts.",
    )
    parser.add_argument(
        "--slug",
        help="Optional ASCII filename slug. Defaults to a slugified title or draft.",
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en", "bilingual"],
        default="zh",
        help="Language metadata. Default: zh.",
    )
    parser.add_argument(
        "--status",
        default="draft",
        help="Status metadata. Default: draft.",
    )
    parser.add_argument(
        "--content-file",
        help="Markdown content file, or '-' to read from stdin. If omitted, only a starter draft is created.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting an existing file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the target path and metadata without writing.",
    )
    args = parser.parse_args()

    created = _dt.date.today().isoformat()
    slug = slugify(args.slug or args.title)
    filename = f"{created}-{slug}.md"

    output_dir = Path(args.output_dir).expanduser()
    path = output_dir / filename

    content = read_content(args.content_file).strip()
    if content.startswith("---\n"):
        body = content + "\n"
    else:
        body = build_frontmatter(args.title, args.lang, args.status, created)
        if content:
            body += content + "\n"
        else:
            body += f"# {args.title}\n\n"

    result = {
        "path": str(path),
        "created": created,
        "lang": args.lang,
        "status": args.status,
        "dry_run": bool(args.dry_run),
        "overwritten": bool(path.exists() and args.overwrite),
    }

    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if path.exists() and not args.overwrite:
        print(
            json.dumps(
                {
                    "error": "file_exists",
                    "path": str(path),
                    "hint": "Use --overwrite to replace the file.",
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
