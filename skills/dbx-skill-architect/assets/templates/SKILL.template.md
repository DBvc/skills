---
name: {skill_name}
description: Use when the user needs a reusable workflow for {recurring_scenario}. Do not use for unrelated one-off tasks or requests outside this skill boundary.
---

# {Skill Title}

## Purpose

Support recurring requests for {recurring_scenario}. Replace the bracketed fields with concrete trigger boundaries, workflow details, failure modes, examples, and validation rules before treating the package as production-ready.

## When to use

Use when:

- the user asks for {recurring_scenario} as a repeated workflow;
- the expected result has a stable output contract or validation path;
- enough context exists to judge success without inventing missing requirements.

## When not to use

Do not use when:

- the request is a one-off direct answer;
- another skill has a more precise trigger;
- required context is missing and blocking questions are needed;
- the request is unsafe, deceptive, non-consensual, or outside this skill boundary.

## Skill shape

```yaml
skill_shape:
  archetype: procedure
  secondary_archetypes: []
  dominant_failure_modes:
    - wrong_trigger
    - unverified_output
  implementation_implications:
    - maintain trigger evals for near-miss cases
    - add deterministic validation for repeated fragile steps
```

## Control surface map

```yaml
control_surface_map:
  activation:
    strength: strong
    mechanism: "frontmatter description, when-not-to-use boundary, trigger evals"
  intent:
    strength: light
    mechanism: "required inputs, blocker handling, non-goals"
  state:
    strength: light
    mechanism: "source material and evidence requirements"
  trajectory:
    strength: light
    mechanism: "workflow and stop conditions"
  execution:
    strength: none
    mechanism: "add scripts only if deterministic or fragile work appears"
  completion:
    strength: light
    mechanism: "validation and risks/open questions"
  evolution:
    strength: light
    mechanism: "trigger evals, output evals, patch hypotheses"
```

## SkillValue check

```yaml
skill_value_check:
  baseline: base_agent
  expected_success_delta: "Replace with the behavior this skill makes more reliable."
  added_cost:
    - context
    - maintenance
  added_risk:
    - wrong trigger
    - over-control
  net_value: uncertain
```

## Required inputs

- user goal and expected output;
- source material, files, or constraints;
- target audience or downstream consumer;
- validation evidence or acceptance criteria.

## Workflow

1. Confirm the request fits this skill boundary.
2. Identify the output, downstream consumer, and non-goals.
3. Gather missing required inputs or state the blocker.
4. Execute the workflow using the smallest sufficient structure.
5. Validate the result and report unresolved risk.

## Output contract

```markdown
## Summary

## Inputs and evidence used

## Result

## Validation

## Risks or open questions
```

## Eval plan

Maintain `evals/triggers.json` for trigger precision/recall and `evals/evals.json` for output behavior. Each eval case should include at least one non-marker quality assertion.
