# Artifact Playbooks

Use the smallest playbook that matches the available artifact.

## PRD review

Inspect:

- Target user, scenario, problem, current alternative.
- Product promise and desired state change.
- Non-goals and constraints.
- Success metrics and guardrails.
- Scope boundaries and launch stage.
- Main flow, edge states, error states, empty/loading states.
- Data, permissions, privacy, compliance, and support implications.
- Dependencies, rollout, rollback, and validation plan.

Common findings:

- Problem statement is solution-shaped.
- Target user is too broad.
- Metrics measure activity but not user progress.
- Acceptance criteria describe UI screens but not outcome.
- Risks are listed but not turned into product or technical guardrails.
- Edge cases are pushed to implementation without product decisions.

## Live product walkthrough

Procedure:

1. State the path you will inspect.
2. Start from the likely first user moment.
3. Record what the product teaches before asking for commitment.
4. Follow the critical path until the first value moment or blocker.
5. Capture screenshots when visual hierarchy, state, or interaction evidence matters.
6. Inspect failure, empty, loading, pricing, trust, privacy, and support surfaces where reachable.
7. Do not create accounts, submit forms, pay, invite others, upload files, or change settings without explicit approval.

Look for:

- Clear promise above the fold or first screen.
- User segment recognition.
- Next action clarity.
- Input burden before value.
- Feedback and recoverability.
- Trust signals and hidden costs.
- Accessibility and responsive basics.
- Consistency between marketing promise and product path.

## Screenshot or prototype review

Inspect visible evidence only:

- Main task and hierarchy.
- Labels, affordances, grouping, visual weight.
- What information the user needs next.
- Missing states and implied flow gaps.
- Contrast, density, spacing, focus, and accessibility risks.
- Whether visual choices support trust and comprehension.

Do not infer backend behavior, real adoption, or hidden business logic.

## Feature review

Procedure:

1. Define who uses the feature and at which moment.
2. Identify the before-state and after-state.
3. Reconstruct the shortest value path.
4. Compare against current alternatives, including doing nothing.
5. Check interaction, information, trust, technical, and validation risks.
6. Decide whether to build, cut, narrow, prototype, or measure.

Feature questions:

- Is this a real user job or an internal wish?
- Does it belong in the product’s core model?
- Does it introduce new objects, states, permissions, or support load?
- Can a smaller version validate the assumption?
- What would make us kill or expand it?

## Information architecture and content

Inspect:

- Object model: what things exist, how they relate, who owns them, how they change over time.
- Navigation: whether it follows user tasks or internal departments/modules.
- Naming: whether terms are distinct, stable, user-understandable, and domain-correct.
- Content: whether copy answers user decisions, risk, next step, and recovery.
- Progressive disclosure: whether advanced concepts appear only when useful.

Common risks:

- Two names for one object.
- One name for two objects.
- Lifecycle states hidden in labels.
- Permission or role concepts leak into ordinary paths.
- Empty states sell the product but do not help the user start.

## Implementation alignment

Inspect:

- Core entities and identifiers.
- State ownership, cache keys, persistence, lifecycle, and invalidation.
- API contracts, validation, permissions, privacy, feature flags.
- Error handling, retries, idempotency, slow network, duplicate submit.
- Telemetry for core success and guardrail metrics.
- Tests or validation for product-critical invariants.

Product-relevant technical smells:

- Duplicate source of truth creates UI inconsistency.
- Wrong identity boundary creates permission or personalization bugs.
- Domain rules scattered across UI branches create hidden divergence.
- Missing telemetry makes product learning impossible.
- Incomplete error states make users lose trust.

## Competitor-informed judgment

Procedure:

1. Define competitors by the user’s alternative, not only by category label.
2. Research current positioning and capabilities using current sources.
3. Compare by user job, first value moment, switching cost, trust, price/risk, workflow fit, and distribution.
4. Identify table-stakes capabilities versus differentiators.
5. Avoid feature-count scoreboards unless feature breadth is the user’s actual decision criterion.

Output should answer:

- What alternative does the user currently use?
- Why would the user switch?
- What must be table-stakes?
- What wedge could make the product meaningfully better?
- What evidence would prove the wedge is real?

## Analytics or user-feedback review

Ask or inspect:

- Segment and time period.
- Sample size and collection method.
- Funnel step definitions.
- Cohort differences.
- Qualitative quotes tied to behavior.
- Support issues, rage clicks, repeated cancellations, search failures, manual workarounds.

Avoid:

- Treating anecdotes as population truth.
- Treating aggregate metrics as explanation.
- Optimizing a step without understanding user intent.
