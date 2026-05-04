# Domain discovery guide

Use this file when hard gates likely pass but domain substance is unknown or weak.

## When to route `domain_discovery`

Route to `create/domain_discovery/ask_domain_questions` when the user asks for a domain/content skill but has not supplied enough information to make the output useful in real use.

Typical cases:

- travel planning without traveler type, budget, season, constraints, pace, booking policy, or risk tolerance;
- investment analysis without asset class, horizon, risk tolerance, data policy, and valuation framework;
- relationship advice without consent boundaries, evidence strength, safety context, and communication goal;
- architecture decision without system constraints, scale, team skills, lifecycle, failure modes, and migration path;
- content marketing without audience, channel, brand voice, legal constraints, source facts, and review workflow.

## Domain substance questions

Ask 5 to 10 targeted questions. Prefer questions that uncover hidden variables and failure modes.

Question families:

1. **Target user**: Who uses the output? Under what constraints?
2. **Artifact type**: What exactly should the skill produce?
3. **Output depth**: quick, standard, deep, operational, or review-grade?
4. **Required variables**: What inputs change the correct answer?
5. **Data-source policy**: What must be current, cited, user-provided, estimated, or unknown?
6. **Failure knowledge**: What plausible answer would fail in real use?
7. **Expert rubric**: How would a domain expert judge quality?
8. **Examples**: What good or bad examples exist?
9. **Eval cases**: What cases would catch shallow but polished output?
10. **Safety boundaries**: What should the skill refuse, redirect, or require approval for?

## Provisional domain content contract

Use this when the user wants progress before full domain details are known:

```yaml
domain_content_contract:
  target_user: "unknown"
  artifact_type: "unknown"
  output_depth: "unknown"
  required_variables:
    known: []
    missing: []
  hidden_failure_modes:
    known: []
    missing: []
  expert_quality_checks:
    known: []
    missing: []
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

Label it as provisional. Do not present it as production-ready.

## Domain eval examples

Good domain evals test usefulness, not only format.

Weak:

```text
The output includes a section called Risks.
```

Stronger:

```text
Given a travel itinerary for a user with limited mobility, the output must not recommend inaccessible transfers and must ask for mobility constraints if missing.
```

Weak:

```text
The architecture decision contains Pros and Cons.
```

Stronger:

```text
Given a migration proposal with unclear rollback path, the skill must flag irreversible risk and require a staged rollout or rollback criterion.
```
