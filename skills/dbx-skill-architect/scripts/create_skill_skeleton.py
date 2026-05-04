#!/usr/bin/env python3
"""Create a minimal DBX-compatible skill skeleton.

By default, --output is the parent directory and this script creates
<output>/<name>/. This keeps generated packages compatible with linters that
require frontmatter.name to match the directory name.

The generated skeleton is intentionally not production-ready, but it avoids
placeholder text and passes the package linter so it can be used as a safe
starting point.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SKILL_TEMPLATE = """---
name: {name}
description: Use when the user needs a reusable workflow for {description}. Do not use for unrelated one-off tasks, direct answers outside this boundary, or requests that require a different specialized skill.
---

# {title}

## Purpose

Support recurring requests for {description}. This draft establishes trigger boundaries, workflow shape, validation expectations, and minimum eval coverage. Before production use, replace the draft assumptions with domain-specific rules, examples, and failure cases from real usage.

## When to use

Use when:

- the user asks for {description} as a repeated workflow or reusable agent behavior;
- the expected output must follow a stable process, output contract, or validation path;
- the task has enough context to judge success and failure without inventing missing requirements.

## When not to use

Do not use when:

- the task is one-off and a direct answer is more useful than a reusable workflow;
- the request belongs to another skill with a more precise trigger and stronger domain model;
- required context is missing and the correct next step is to ask blocking questions;
- the request is unsafe, deceptive, non-consensual, or outside the skill boundary.

## Skill shape

```yaml
skill_shape:
  archetype: procedure
  secondary_archetypes: []
  dominant_failure_modes:
    - wrong_trigger
    - unverified_output
  implementation_implications:
    - sharpen description and trigger evals before relying on this skill
    - add deterministic validation when repeated failures become mechanical
```

## Required inputs

- user goal and expected output;
- relevant source material, files, or constraints;
- target audience or downstream consumer;
- validation evidence or acceptance criteria.

## Workflow

1. Confirm the request fits the trigger boundary.
2. Identify the expected output, downstream consumer, and non-goals.
3. Gather missing required inputs or state the blocker.
4. Execute the workflow using the smallest sufficient structure.
5. Validate the result against the output contract and report unresolved risk.

## Output contract

```markdown
## Summary

## Inputs and evidence used

## Result

## Validation

## Risks or open questions
```

## References and scripts

Add focused references under `references/` when the skill needs domain rules, examples, anti-patterns, or expert rubrics. Add scripts under `scripts/` when parsing, counting, schema validation, rendering, or command execution becomes repeated and fragile.

## Eval plan

Maintain `evals/triggers.json` for trigger precision/recall and `evals/evals.json` for output behavior. At least one eval must test the primary failure mode rather than only checking section headings.
"""


def make_evals_template(name: str, description: str) -> dict:
    return {
        "skill_name": name,
        "pass_threshold": 0.85,
        "evals": [
            {
                "id": "positive-explicit-core-workflow",
                "kind": "positive",
                "prompt": f"Apply the {name} workflow to a recurring request about {description} and produce the expected output contract.",
                "expected_behavior": "Use the skill workflow, identify inputs/evidence, produce the result, and include validation or blockers.",
                "checks": {
                    "trigger": [{"type": "must_contain", "value": "## Summary", "required": True, "quality": "structural"}],
                    "process": [
                        {"type": "regex", "value": "(?is)(inputs|evidence).*?(validation|blocker|risk)", "required": True, "quality": "behavior"},
                        {"type": "regex", "value": "(?is)(downstream consumer|acceptance criteria|non-goals)", "required": False, "quality": "specificity"},
                    ],
                    "output": [{"type": "must_contain", "value": "## Validation", "required": True, "quality": "structural"}],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "positive-implicit-recurring-scenario",
                "kind": "positive",
                "prompt": f"I keep getting requests related to {description}; help me handle the next one consistently.",
                "expected_behavior": "Recognize the reusable scenario and ask only for missing required inputs before using the workflow.",
                "checks": {
                    "trigger": [{"type": "must_contain", "value": "## Summary", "required": True, "quality": "structural"}],
                    "process": [{"type": "regex", "value": "(?is)(required input|missing context|acceptance criteria|downstream consumer)", "required": True, "quality": "specificity"}],
                    "output": [],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "negative-unrelated-direct-answer",
                "kind": "negative",
                "prompt": "Explain the difference between HTTP 200 and HTTP 404 in one paragraph.",
                "expected_behavior": "Do not invoke this skill-specific workflow because the request is an unrelated direct answer.",
                "checks": {
                    "trigger": [{"type": "must_not_contain", "value": "## Inputs and evidence used", "required": True, "quality": "structural"}],
                    "process": [{"type": "regex", "value": "(?is)(direct answer|outside.*boundary|not use this skill|unrelated)", "required": True, "quality": "behavior"}],
                    "output": [],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "near-miss-adjacent-scope",
                "kind": "near_miss",
                "prompt": f"Use the {name} format for a task that has no repeated workflow, no validation need, and no downstream consumer.",
                "expected_behavior": "Explain the boundary and avoid applying the full workflow when a lightweight answer is sufficient.",
                "checks": {
                    "trigger": [{"type": "must_not_contain", "value": "## Inputs and evidence used", "required": True, "quality": "structural"}],
                    "process": [{"type": "regex", "value": "(?is)(one-off|no repeated workflow|lightweight answer|boundary)", "required": True, "quality": "behavior"}],
                    "output": [],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
            {
                "id": "failure-mode-missing-validation",
                "kind": "failure_mode",
                "prompt": f"Handle a {description} request but give me the result without explaining inputs, evidence, or validation.",
                "expected_behavior": "Refuse the shallow shortcut and include validation evidence or clearly state why validation is blocked.",
                "checks": {
                    "trigger": [],
                    "process": [{"type": "regex", "value": "(?is)(validation evidence|cannot validate|blocked|risk)", "required": True, "quality": "validation"}],
                    "output": [{"type": "must_contain", "value": "## Validation", "required": True, "quality": "structural"}],
                    "safety": [],
                },
                "pass_criteria": {"all_required": True, "min_score": 0.85},
            },
        ],
    }


def make_triggers_template(name: str, description: str) -> dict:
    return {
        "skill_name": name,
        "version": "0.1",
        "cases": [
            {
                "id": "positive-explicit-core-task",
                "kind": "positive",
                "prompt": f"Use {name} to handle a recurring workflow for {description}.",
                "expected_trigger": True,
                "rationale": "Explicitly names the reusable workflow.",
            },
            {
                "id": "positive-implicit-core-scenario",
                "kind": "positive",
                "prompt": f"I need a consistent process for repeated requests about {description}.",
                "expected_trigger": True,
                "rationale": "Implies the recurring scenario without naming the skill.",
            },
            {
                "id": "negative-unrelated-direct-answer",
                "kind": "negative",
                "prompt": "Summarize what CSS flexbox does in two sentences.",
                "expected_trigger": False,
                "rationale": "Unrelated direct explanation request.",
            },
            {
                "id": "near-miss-one-off",
                "kind": "near_miss",
                "prompt": f"Give a one-time answer related to {description}; no reusable process needed.",
                "expected_trigger": False,
                "rationale": "Adjacent topic but explicitly one-off.",
            },
            {
                "id": "failure-mode-validation-missing",
                "kind": "failure_mode",
                "prompt": f"Handle {description} but skip validation and blockers.",
                "expected_trigger": True,
                "rationale": "The skill should trigger to enforce validation rather than shallow output.",
            },
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a minimal DBX skill skeleton.")
    parser.add_argument("--name", required=True, help="Skill name, lowercase kebab-case")
    parser.add_argument("--description", required=True, help="Short intent phrase, e.g. 'reviewing release plans'")
    parser.add_argument("--output", required=True, help="Parent output directory; creates <output>/<name>/")
    parser.add_argument("--domain", action="store_true", help="Create references/domain-notes.md starter")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing skill directory")
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        raise SystemExit("Error: --name must be lowercase kebab-case and must not contain consecutive hyphens.")
    description = " ".join(args.description.split())
    if len(description) < 8:
        raise SystemExit("Error: --description should be a concrete intent phrase, at least 8 characters.")
    parent = Path(args.output)
    out = parent / args.name
    if out.exists() and any(out.iterdir()) and not args.force:
        raise SystemExit(f"Error: {out} exists and is not empty. Use --force to overwrite.")
    out.mkdir(parents=True, exist_ok=True)
    (out / "evals").mkdir(exist_ok=True)
    (out / "references").mkdir(exist_ok=True)
    (out / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=args.name, description=description, title=args.name.replace("-", " ").title()),
        encoding="utf-8",
    )
    evals = make_evals_template(args.name, description)
    (out / "evals" / "evals.json").write_text(json.dumps(evals, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    triggers = make_triggers_template(args.name, description)
    (out / "evals" / "triggers.json").write_text(json.dumps(triggers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.domain:
        (out / "references" / "domain-notes.md").write_text(
            "# Domain notes\n\n"
            "## Required variables\n\n"
            "- user segment and context of use\n"
            "- data or source freshness requirements\n"
            "- output depth and downstream consumer\n\n"
            "## Hidden failure modes\n\n"
            "- shallow generic output that ignores domain-specific constraints\n"
            "- stale or invented facts presented as verified\n\n"
            "## Expert quality checks\n\n"
            "- identifies the variables a practitioner would ask for before acting\n"
            "- distinguishes evidence, assumptions, and recommendations\n",
            encoding="utf-8",
        )
    print(f"Created skill skeleton at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
