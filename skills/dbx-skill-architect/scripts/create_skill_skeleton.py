#!/usr/bin/env python3
"""Create a minimal DBX skill skeleton.

`--output` is the parent directory. The script creates `<output>/<name>/`.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite {path}; pass --force")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def skill_md(name: str, description: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {name}

Use this skill for a recurring scenario where the base agent needs explicit trigger boundaries, a stable workflow, evidence policy, output contract, and regression cases.

## Use when

- The user asks for this recurring workflow by name or describes its characteristic inputs and outputs.
- The task is repeated enough to justify a reusable controller.
- The output can be evaluated by examples, assertions, validation commands, or human review criteria.

## Do not use when

- The request is one-off and a direct answer would be cheaper and clearer.
- The user is asking for a different skill's primary job.
- Required facts are missing and the right action is clarification.
- The task is unsafe, non-consensual, deceptive, or requires irreversible external action without approval.

## Workflow

1. Confirm the task fits this skill's trigger boundary.
2. Identify the evidence source and the expected output artifact.
3. Follow the smallest workflow that can produce a usable result.
4. State validation, limitations, or missing evidence before claiming success.

## Output contract

Return:

- result or recommendation;
- evidence or input basis;
- validation performed or explicitly not performed;
- risks, unknowns, or next action.

## Quality bar

A good output is specific to the user's actual input, avoids generic filler, and can be used by the next human, agent, reviewer, or tool without guessing the missing contract.
"""


def evals_json(name: str) -> str:
    data = {
        "skill_name": name,
        "pass_threshold": 0.85,
        "evals": [
            {
                "id": "positive-explicit-recurring-task",
                "kind": "positive",
                "prompt": "Use this recurring workflow on a realistic input that matches the skill boundary.",
                "expected_behavior": "The skill should trigger, identify the input basis, follow the workflow, and return the contracted output with validation or limitations.",
                "checks": {
                    "trigger": [
                        {"type": "must_contain", "value": "Use when", "required": False, "quality": "structural"}
                    ],
                    "process": [
                        {"type": "regex", "value": "(?is)(evidence|input basis|source).*?(workflow|steps|validation)", "required": True, "quality": "behavior"}
                    ],
                    "output": [
                        {"type": "regex", "value": "(?is)(result|recommendation).*?(validation|limitations|unknowns)", "required": True, "quality": "validation"}
                    ],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "positive-validation-aware-output",
                "kind": "positive",
                "prompt": "Handle a matching request where validation can only be partially performed.",
                "expected_behavior": "The output should not overclaim success and should explicitly separate performed validation from missing validation.",
                "checks": {
                    "trigger": [],
                    "process": [
                        {"type": "regex", "value": "(?is)(performed|checked|validated).*?(not performed|not verified|missing|limitation)", "required": True, "quality": "validation"}
                    ],
                    "output": [
                        {"type": "regex", "value": "(?is)(cannot claim|not verified|limitation|unknown)", "required": True, "quality": "behavior"}
                    ],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "negative-one-off-request",
                "kind": "negative",
                "prompt": "Ask for a one-off answer that does not need this reusable workflow.",
                "expected_behavior": "The skill should not force its workflow and should either stay inactive or provide a compact direct answer.",
                "checks": {
                    "trigger": [
                        {"type": "must_not_contain", "value": "full reusable workflow", "required": True, "quality": "behavior"}
                    ],
                    "process": [],
                    "output": [
                        {"type": "regex", "value": "(?is)(direct answer|one-off|not necessary|lighter)", "required": True, "quality": "specificity"}
                    ],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "near-miss-adjacent-skill",
                "kind": "near_miss",
                "prompt": "Ask for an adjacent workflow that belongs to another skill or direct answer.",
                "expected_behavior": "The skill should reject or reroute the near miss rather than stretching its boundary.",
                "checks": {
                    "trigger": [],
                    "process": [
                        {"type": "regex", "value": "(?is)(near.?miss|different skill|outside this skill|reroute|not this workflow)", "required": True, "quality": "behavior"}
                    ],
                    "output": [
                        {"type": "regex", "value": "(?is)(use .* instead|direct answer|clarify)", "required": True, "quality": "specificity"}
                    ],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "failure-mode-evidence-free-success-claim",
                "kind": "failure_mode",
                "prompt": "Ask the skill to claim completion without evidence or validation.",
                "expected_behavior": "The skill should refuse to overclaim and should state the missing evidence or validation path.",
                "checks": {
                    "trigger": [],
                    "process": [
                        {"type": "regex", "value": "(?is)(evidence|validation|proof).*?(missing|not available|cannot verify)", "required": True, "quality": "validation"}
                    ],
                    "output": [
                        {"type": "must_not_contain", "value": "fully verified", "required": True, "quality": "safety"}
                    ],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def triggers_json(name: str) -> str:
    data = {
        "skill_name": name,
        "cases": [
            {
                "id": "positive-explicit-request",
                "kind": "positive",
                "prompt": f"Please use {name} for this recurring workflow.",
                "expected_trigger": True,
                "rationale": "Explicitly requests the skill by name.",
            },
            {
                "id": "positive-implicit-recurring-scenario",
                "kind": "positive",
                "prompt": "I keep doing this same workflow and want a reusable agent routine with validation.",
                "expected_trigger": True,
                "rationale": "Recurring workflow with validation need.",
            },
            {
                "id": "negative-one-off",
                "kind": "negative",
                "prompt": "Answer this one-time question directly.",
                "expected_trigger": False,
                "rationale": "One-off direct answer should not trigger a reusable workflow skill.",
            },
            {
                "id": "near-miss-adjacent-task",
                "kind": "near_miss",
                "prompt": "Do a nearby task that belongs to a different skill.",
                "expected_trigger": False,
                "rationale": "Near-miss should be rejected or routed elsewhere.",
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a DBX skill skeleton.")
    parser.add_argument("--name", required=True, help="Skill directory/frontmatter name, e.g. dbx-example-skill")
    parser.add_argument("--description", required=True, help="Specific trigger-oriented description, at least 40 chars")
    parser.add_argument("--output", required=True, help="Parent output directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated directory")
    args = parser.parse_args()

    name = args.name.strip()
    if not NAME_RE.match(name):
        raise SystemExit("--name must be lowercase kebab-case")
    if len(args.description.strip()) < 40:
        raise SystemExit("--description must be at least 40 characters and trigger-oriented")

    parent = Path(args.output).expanduser().resolve()
    root = parent / name
    if root.exists() and args.force:
        shutil.rmtree(root)
    elif root.exists():
        raise SystemExit(f"{root} already exists; pass --force")

    write(root / "SKILL.md", skill_md(name, args.description.strip()), args.force)
    write(root / "evals" / "evals.json", evals_json(name), args.force)
    write(root / "evals" / "triggers.json", triggers_json(name), args.force)
    write(
        root / "references" / "gotchas.md",
        "# Gotchas\n\n- Add real failure cases observed from use.\n- Replace this line only after you have a concrete failure to prevent.\n",
        args.force,
    )
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
