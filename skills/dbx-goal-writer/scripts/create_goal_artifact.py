#!/usr/bin/env python3
"""Create a conservative Codex /goal artifact.

This helper creates placeholders. The agent should replace placeholders with
project-specific content before starting `/goal`.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "codex-goal"


def bullet(values: list[str], fallback: str) -> str:
    if not values:
        return f"- {fallback}"
    return "\n".join(f"- {v}" for v in values)


def command_block(commands: list[str]) -> str:
    if not commands:
        return "echo 'TODO: replace with confirmed validation commands'"
    return "\n".join(commands)


def shell_lines(commands: list[str]) -> str:
    return "\n".join(f"echo '+ {cmd}'\n{cmd}" for cmd in commands) + "\n"


def write_file(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def render_goal(args: argparse.Namespace, goal_path: str) -> str:
    short_objective = args.objective or args.title
    return f"""# Goal: {args.title}

## Objective

{args.objective or 'TODO: write the one-sentence outcome'}

## Context

{bullet(args.context, 'TODO: describe current behavior, evidence, and relevant references')}

## Target paths

{bullet(args.target_path, 'TODO: identify target files or discovery boundaries')}

## Scope

{bullet(args.scope, 'TODO: define allowed changes')}

## Non-goals

{bullet(args.non_goal, 'Do not change unrelated modules')}

## Constraints

{bullet(args.constraint, 'Keep public API and user-visible behavior compatible unless explicitly allowed')}

## Acceptance criteria

{bullet(args.acceptance, 'TODO: define observable completion criteria')}

## Validation

{bullet(args.validation_command, 'TODO: confirm validation commands')}

## Pause conditions

{bullet(args.pause_condition, 'Stop before adding dependencies, changing public APIs, broadening scope, or making unclear product or architecture decisions')}

## Budget and stop rules

{bullet(args.budget, 'If a token or time budget is configured, stop starting new substantive work when it is reached and summarize progress, remaining work, blockers, and the next concrete action')}

## Reporting

When the task is complete, report:

- Files changed
- Behavior changed
- Tests or checks run
- Known risks or follow-ups

## Start command

```text
/goal Execute {short_objective} according to {goal_path}. Read the goal contract before editing code. Respect Scope, Non-goals, Constraints, Acceptance Criteria, Validation, Budget and Stop Rules, and Pause Conditions. Completion requires all required validation to pass, or a clear explanation of why a check could not be run.
```
"""


def render_plan(args: argparse.Namespace) -> str:
    return f"""# Plan: {args.title}

## Milestones

1. Discover current behavior and relevant code paths.
2. Propose the smallest safe implementation approach.
3. Implement in small, reviewable steps.
4. Update or add regression coverage.
5. Run validation.
6. Summarize results and risks.

## Working rules

- Keep changes inside declared scope.
- Prefer local, reversible edits.
- Avoid broad rewrites unless explicitly authorized.
- Update STATUS.md after meaningful milestones.
"""


def render_acceptance(args: argparse.Namespace) -> str:
    return f"""# Acceptance: {args.title}

The goal is complete only when all required criteria are satisfied.

## Functional acceptance

{bullet(args.acceptance, 'TODO: define observable completion criteria')}

## Code acceptance

- The implementation is scoped and reviewable.
- No unrelated files are changed.
- Public API, exported types, and user-visible behavior remain compatible unless explicitly allowed.

## Validation acceptance

- Required commands in VALIDATION.md pass, or failures are explained with evidence and next steps.

## Review evidence

The final report includes summary, changed files, validation results, known risks, and follow-ups.
"""


def render_validation(args: argparse.Namespace) -> str:
    return f"""# Validation: {args.title}

## Required commands

```bash
{command_block(args.validation_command)}
```

## Manual checks

- Confirm changed behavior matches acceptance criteria.
- Confirm no unrelated UI, API, or build behavior changed.

## If validation cannot run

Explain which command could not run, why, what evidence was collected instead, and what the next human action should be.
"""


def render_status(args: argparse.Namespace) -> str:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return f"""# Status: {args.title}

## Current state

Not started.

## Progress log

| Time | Milestone | Notes |
| --- | --- | --- |
| {now} | Created goal package | Initial package created. |

## Decisions

- None yet.

## Blockers

- None yet.

## Validation results

- Not run yet.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Codex /goal file or package scaffold")
    parser.add_argument("--title", required=True)
    parser.add_argument("--objective", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--mode", choices=["file", "package"], default="file")
    parser.add_argument("--output-root", default=".codex/goals")
    parser.add_argument("--context", action="append", default=[])
    parser.add_argument("--target-path", action="append", default=[])
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--non-goal", action="append", default=[])
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--acceptance", action="append", default=[])
    parser.add_argument("--validation-command", action="append", default=[])
    parser.add_argument("--pause-condition", action="append", default=[])
    parser.add_argument("--budget", action="append", default=[], help="Budget or stop rule to include in GOAL.md")
    parser.add_argument("--with-validate-script", action="store_true", help="Create scripts/validate.sh for package mode")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    slug = args.slug or slugify(args.title)
    goal_dir = Path(args.output_root) / slug
    goal_path = goal_dir / "GOAL.md"
    display_goal_path = str(goal_path).replace(os.sep, "/")

    write_file(goal_path, render_goal(args, display_goal_path), args.overwrite)

    if args.mode == "package":
        write_file(goal_dir / "PLAN.md", render_plan(args), args.overwrite)
        write_file(goal_dir / "ACCEPTANCE.md", render_acceptance(args), args.overwrite)
        write_file(goal_dir / "VALIDATION.md", render_validation(args), args.overwrite)
        write_file(goal_dir / "STATUS.md", render_status(args), args.overwrite)
        if args.with_validate_script:
            validate_sh = goal_dir / "scripts" / "validate.sh"
            commands = shell_lines(args.validation_command) if args.validation_command else "echo 'TODO: replace with confirmed validation commands'\n"
            write_file(validate_sh, f"#!/usr/bin/env bash\nset -euo pipefail\n\n{commands}", args.overwrite)
            make_executable(validate_sh)

    print(f"Created goal artifacts in {goal_dir}")
    print()
    print("Start with:")
    print(f"/goal Execute {args.objective or args.title} according to {display_goal_path}. Read the goal contract before editing code. Respect Scope, Non-goals, Constraints, Acceptance Criteria, Validation, Budget and Stop Rules, and Pause Conditions. Completion requires all required validation to pass, or a clear explanation of why a check could not be run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
