---
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

## Domain content contract

Use this section for domain/content skills. If not applicable, state `not_applicable`.

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
```

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
- For domain/content skills: at least 2 content-quality checks for domain variables and hidden failure modes

Eval definitions must be runner-compatible with `scripts/run_skill_evals.py`.
