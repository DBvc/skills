#!/usr/bin/env python3
"""Create a compliant starter skill package.

Use --domain for domain/content skills so the package includes a domain content
contract and starter content-quality evals.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

SKILL_TEMPLATE = '''---
name: {name}
description: {description}
---

# {title}

## Purpose

This skill handles a recurring scenario where <primary user> needs to <stable job>. It improves <target outcome> by enforcing a bounded workflow, evidence policy, domain content contract when relevant, output contract, and eval plan.

## When to use

- Use when <trigger context 1>.
- Use when <trigger context 2>.

## When not to use

- Do not use for one-off tasks with no reusable workflow.
- Do not use for unsafe, deceptive, privacy-invasive, or out-of-scope requests.
- Do not use when required inputs are missing and assumptions would be unsafe or misleading.
- Do not use for superficially similar requests that lack this skill's stable job or required domain variables.

## Hard gates or required inputs

```yaml
hard_gates:
  repeatability: "<why this scenario repeats or is reusable>"
  stable_job: "<stable job-to-be-done>"
  evaluability: "<how success is checked>"
  safety_legitimacy: "<safety/privacy/legal boundary>"
required_inputs:
  - "<required input>"
optional_inputs:
  - "<optional input>"
assumptions_if_missing:
  - "<safe assumption, if any>"
```

{domain_contract}

## IR summary

```yaml
objects: []
states_or_results: []
events_or_actions: []
evidence: []
hypotheses: []
constraints: []
risky_boundaries: []
reasoning_mode: []
type_errors_to_prevent: []
```

## Workflow

1. Validate required inputs, hard gates, and domain variables when relevant.
2. Compile the request into the IR.
3. Execute the domain workflow with bounded freedom.
4. Produce the output contract.
5. Mark missing information, confidence, blockers, next actions, and verification needs.

## Evidence and confidence policy

- Confirmed: directly supported by provided or validated evidence.
- Probable: supported by multiple signals but not fully confirmed.
- Weak: plausible but under-supported.
- Unknown: insufficient evidence.

Never state conclusions stronger than the available evidence. For real-time facts, separate confirmed, estimated-with-label, and needs-verification.

## Output contract

Use this exact structure unless the user requests another format:

```yaml
summary: ""
inputs_used: []
evidence:
  confirmed: []
  probable: []
  weak: []
missing_information: []
assumptions: []
result:
  domain_specific_fields: []
confidence: high | medium | low
blockers: []
next_actions: []
verification_needed: []
```

## Failure and escalation rules

- Stop and ask when required inputs or domain variables are missing and assumptions would change the result.
- Refuse or redesign unsafe, deceptive, privacy-invasive, or coercive goals.
- Use a checklist or direct answer instead of this skill when the scenario is not reusable.
- For domain/content skills, fail the output if it is well-formatted but lacks required domain variables, hidden pitfalls, or data-source policy.

## References and scripts

- Add `references/<file>.md` for long domain guidance, rubrics, examples, and hidden failure modes.
- Add `scripts/<script>.py` for deterministic parsing, validation, transformation, scoring, or fragile operations.

## Eval plan

At minimum include:

- 2 positive cases
- 1 negative case
- 1 near-miss case
- 1 failure_mode or safety case
{domain_eval_line}

Eval definitions must be runner-compatible with `scripts/run_skill_evals.py`.
'''

DOMAIN_CONTRACT = '''## Domain content contract

This section is required for domain/content skills. Replace placeholders before treating this package as production-ready.

```yaml
domain_content_contract:
  target_user: ""
  artifact_type: ""
  output_depth: "quick | standard | deep | operational"
  required_variables: []
  hidden_failure_modes: []
  expert_quality_checks: []
  data_source_policy:
    realtime_required: []
    user_provided_required: []
    can_estimate_with_label: []
    must_not_fabricate: []
  uncertainty_policy: []
  must_not_omit: []
  worked_examples_needed: []
  domain_eval_cases: []
```'''

NON_DOMAIN_CONTRACT = '''## Domain content contract

```yaml
domain_content_contract: not_applicable
```'''


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def check(kind: str, value: str, required: bool = True) -> dict:
    return {"type": kind, "value": value, "required": required}


def make_evals(name: str, domain: bool) -> dict:
    evals = [
        {
            "id": "positive-primary-1",
            "kind": "positive",
            "prompt": "Use this skill for its primary recurring scenario with enough required inputs.",
            "expected_behavior": "Use the workflow and output contract.",
            "checks": {"trigger": [], "process": [check("must_contain", "summary", False)], "output": [check("must_contain", "confidence", False)], "safety": []},
            "pass_criteria": {"all_required": True, "min_score": 0.85},
        },
        {
            "id": "positive-primary-2",
            "kind": "positive",
            "prompt": "Apply the skill to another realistic recurring input in the same scenario family.",
            "expected_behavior": "Use the same bounded workflow and mark missing information.",
            "checks": {"trigger": [], "process": [check("must_contain", "missing", False)], "output": [check("must_contain", "next", False)], "safety": []},
            "pass_criteria": {"all_required": True, "min_score": 0.85},
        },
        {
            "id": "negative-one-off-task",
            "kind": "negative",
            "prompt": "Handle a one-off task that does not match the reusable scenario.",
            "expected_behavior": "Do not over-trigger the skill or fabricate a reusable workflow.",
            "checks": {"trigger": [check("must_not_contain", "SKILL.md", True)], "process": [], "output": [], "safety": []},
            "pass_criteria": {"all_required": True, "min_score": 0.85},
        },
        {
            "id": "near-miss-similar-but-wrong-context",
            "kind": "near_miss",
            "prompt": "A superficially similar request that lacks the skill's required inputs or stable job.",
            "expected_behavior": "Ask for missing inputs or route smaller instead of forcing the skill.",
            "checks": {"trigger": [], "process": [check("must_contain", "missing", False)], "output": [check("must_not_contain", "confirmed", False)], "safety": []},
            "pass_criteria": {"all_required": True, "min_score": 0.85},
        },
        {
            "id": "failure-mode-overconfident-output",
            "kind": "failure_mode",
            "prompt": "Use the skill with weak evidence and ask for a definitive conclusion.",
            "expected_behavior": "Do not exceed evidence; state uncertainty, blockers, and next actions.",
            "checks": {"trigger": [], "process": [check("must_contain", "evidence", False)], "output": [check("must_contain", "unknown", False), check("must_not_contain", "definitely", False)], "safety": []},
            "pass_criteria": {"all_required": True, "min_score": 0.85},
        },
    ]
    if domain:
        evals.append({
            "id": "failure-mode-surface-level-domain-output",
            "kind": "failure_mode",
            "prompt": "Use the skill for a domain-specific request but omit concrete variables, pitfalls, and data-source policy.",
            "expected_behavior": "Detect shallow output and include required domain variables, hidden failure modes, and verification needs.",
            "checks": {"trigger": [], "process": [check("must_contain", "hidden", False), check("must_contain", "required", False)], "output": [check("must_contain", "verification", False)], "safety": []},
            "pass_criteria": {"all_required": True, "min_score": 0.85},
        })
    return {"skill_name": name, "pass_threshold": 0.85, "evals": evals}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--description", required=True)
    parser.add_argument("--domain", action="store_true", help="include domain content contract and content-quality eval")
    args = parser.parse_args()
    name = args.name.strip()
    if not NAME_RE.match(name):
        raise SystemExit("name must be lowercase letters/numbers/hyphens and <=64 chars")
    skill_dir = args.output_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "evals").mkdir(exist_ok=True)
    domain_contract = DOMAIN_CONTRACT if args.domain else NON_DOMAIN_CONTRACT
    domain_eval_line = "- For domain/content skills: at least 2 content-quality checks for domain variables and hidden failure modes" if args.domain else ""
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, title=title_from_name(name), description=args.description.strip(), domain_contract=domain_contract, domain_eval_line=domain_eval_line),
        encoding="utf-8",
    )
    (skill_dir / "evals" / "evals.json").write_text(json.dumps(make_evals(name, args.domain), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
