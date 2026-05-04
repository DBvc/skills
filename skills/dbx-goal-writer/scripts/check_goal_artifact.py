#!/usr/bin/env python3
"""Check whether a Codex goal file or package has the expected sections."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Objective",
    "## Context",
    "## Target paths",
    "## Scope",
    "## Non-goals",
    "## Constraints",
    "## Acceptance criteria",
    "## Validation",
    "## Pause conditions",
    "## Budget and stop rules",
    "## Reporting",
]

PACKAGE_FILES = ["GOAL.md", "PLAN.md", "ACCEPTANCE.md", "VALIDATION.md", "STATUS.md"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a Codex goal file or package")
    parser.add_argument("path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    goal_path = path / "GOAL.md" if path.is_dir() else path

    issues: list[str] = []
    if not goal_path.exists():
        issues.append(f"Missing GOAL.md: {goal_path}")
    else:
        text = goal_path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                issues.append(f"GOAL.md missing section: {section}")
        if "/goal" not in text:
            issues.append("GOAL.md missing a Start command containing /goal")
        if "TODO" in text:
            issues.append("GOAL.md still contains TODO placeholders")

    if path.is_dir() and any((path / f).exists() for f in PACKAGE_FILES[1:]):
        for file in PACKAGE_FILES:
            if not (path / file).exists():
                issues.append(f"Package missing file: {file}")

    if issues:
        print("Goal artifact needs revision:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Goal artifact looks ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
