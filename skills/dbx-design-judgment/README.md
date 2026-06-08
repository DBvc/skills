# dbx-design-judgment

A DBX skill for evidence-bounded design judgment and design shaping.

This skill answers a narrow question:

```text
Does this design support the target user, task, context, and product promise with clear structure, interaction, visual language, and system consistency?
```

It deliberately does **not** implement code. It may read code as design evidence, but it does not edit files, write patches, install dependencies, or claim implementation is complete.

## Repository Status

This skill is already integrated in this repository at:

```text
skills/dbx-design-judgment/
```

Run repository checks from the repo root after changing it:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

Run this skill's local report checker with:

```bash
python3 skills/dbx-design-judgment/scripts/validate-design-report.py path/to/report.md
```

The checker validates report shape and evidence markers. It does not validate whether the design judgment is true.

## Shape

```yaml
skill_shape:
  primary: design_judgment
  secondary:
    - design_audit
    - prd_to_design_brief
    - screenshot_review
    - code_design_alignment
    - design_system_review
  core_thesis: "Design judgment turns product intent into evidence-bounded interface decisions, without taking over implementation."
  dominant_failure_modes:
    - generic_design_advice
    - unsupported_taste_claim
    - role_creep_into_code_editing
    - product_strategy_scope_creep
    - screenshot_not_grounded
    - visual_issue_overgeneralized
    - missing_interaction_states
    - design_system_drift_ignored
    - responsive_accessibility_blind_spots
    - over_redesign_instead_of_minimal_fix_direction
    - brand_product_register_confusion
    - ai_template_reflex
    - unverified_completion
  implementation_implication: "Keep SKILL.md as a compact control loop, move rubrics and playbooks to references, use scripts only for deterministic report-shape validation."
```

## Why this is not a design encyclopedia

The runtime controller has one core path:

```text
design artifact + evidence
-> design frame
-> five-lens judgment
-> P-level findings
-> design handoff
```

The five lenses are the minimum useful kernel:

1. Task support.
2. Information structure.
3. Interaction and states.
4. Visual language and system.
5. Trust, accessibility, and handoff readiness.

Everything else is conditional reference material.

## Why P0-P3 instead of D0-D3

Use P0-P3 to stay aligned with DBX product judgment. In this skill, P means design-impact severity, not implementation order. Fix order is derived from severity plus confidence, cost, and blast radius.

## Routing

Use for evidence-bounded design judgment and design shaping.

Route elsewhere when:

- The request is pure product viability or product strategy: `dbx-product-judgment`.
- The request is code implementation, CSS fixes, or patch generation: the appropriate coding/frontend skill.
- The request is ordinary diff review unrelated to design impact: `dbx-diff-review`, if available.

## Evaluation philosophy

This skill is not proven by sounding complete. It should be evaluated by whether it reduces these observable failures:

- The agent gives taste claims without evidence.
- The agent skips user/task/context.
- The agent jumps from PRD to UI suggestions without IA and state model.
- The agent reviews screenshots with vague adjectives rather than visible facts.
- The agent reads code and becomes a generic code reviewer.
- The agent edits code despite a design-only role.
- The agent claims verification that it did not run.

See `evals/` for starter trigger and output checks.
