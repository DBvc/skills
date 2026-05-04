# Content Quality Rubric / 内容质量评分

Use this rubric for domain/content skills. It is not a replacement for runner evals; it guides human review and domain-specific eval design.

## Contents

- Scoring scale
- Core dimensions
- How to convert rubric items into evals

## Scoring scale

Score each dimension from 0 to 3:

- 0: absent or misleading
- 1: mentioned but shallow
- 2: usable with minor gaps
- 3: operational or expert-level

## Core dimensions

1. **Target fit**: output matches the intended user, constraints, and use context.
2. **Required variables**: includes the domain variables without which the artifact is unusable.
3. **Failure knowledge**: includes pitfalls, anti-patterns, hidden costs, or novice traps.
4. **Data-source policy**: separates confirmed facts, user-provided facts, estimates, real-time checks, and unknowns.
5. **Operational detail**: gives enough specificity to act, not just understand.
6. **Trade-offs and alternatives**: includes viable options, exclusions, backup paths, or fallback plans.
7. **Expert quality checks**: matches how a domain expert would judge the artifact.
8. **Uncertainty handling**: does not fabricate specifics; marks confidence and verification needs.
9. **Near-miss resistance**: does not apply the skill to superficially similar but wrong contexts.
10. **Eval quality**: tests actual usefulness, not only section headings.

## Convert rubric to evals

For each domain skill, create eval checks that catch surface-level output.

Examples:

- Travel: output must include time/distance/budget/verification or must route to clarification.
- News release: output must not fabricate quotes or metrics; must include fact/source checklist.
- Repair: output must include safety stop conditions and diagnostic order.
- Relationship: output must not state hidden motives as facts; must include uncertainty and consent-aware communication.
- Sports prediction: output must provide probabilities and uncertainty, not certainty claims.
