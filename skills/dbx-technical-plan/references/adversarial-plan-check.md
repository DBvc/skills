# Adversarial Plan Check

Run this check before finalizing any non-trivial technical plan. The goal is not to sound skeptical. The goal is to remove plans that cannot survive implementation pressure.

## Core questions

### Source of truth

- Does the plan introduce a second source of truth?
- Does it move data without moving ownership?
- Does it rely on derived state without defining reconciliation?
- Does it put feature-private rules into shared/global surfaces?
- Does a proposed new abstraction represent a real domain concept or just hide branching?

### Scope

- Is the plan secretly larger than the user’s request?
- Are unrelated cleanups mixed with behavior changes?
- Are migration, redesign, and validation bundled into one giant task?
- Can each slice be reviewed independently?
- Is there a clear forbidden scope?

### Compatibility

- Does any exported type, API route, schema, event, config, feature flag, cache key, CLI behavior, or persisted value change?
- Are known callers covered?
- Are unknown callers acknowledged?
- Is there a compatibility layer, deprecation path, or rollback when needed?

### Runtime behavior

- What happens under retry, partial failure, slow network, logout/login, user switch, permission downgrade, refresh, navigation, duplicate submit, offline mode, or rollback?
- Does the plan preserve ordering, idempotency, cancellation, cleanup, and lifecycle behavior?
- Could a green typecheck still miss the real failure?

### Validation

- Which invariant is protected by each proposed check?
- Are tests proposed because they prove behavior, or because “add tests” sounds responsible?
- Is any critical behavior only review-checked?
- What will remain unverified?
- What command or manual flow would catch the most likely regression?

### Cost and reversibility

- Is the plan overbuilding for a one-off problem?
- Does it create long-lived abstractions before usage is proven?
- What is the rollback path?
- What is the smallest reversible step that reduces uncertainty?
- What evidence would cause the plan to stop?

## Rejection criteria

Mark the plan `needs-decision`, `needs-grounding`, or `blocked` when any of these are true:

- source of truth is unclear;
- implementation slices require guessing project facts;
- validation cannot observe the key invariant;
- public compatibility may break and caller impact is unknown;
- rollback is required but absent;
- the plan requires product, design, architecture, or data migration approval that has not been made;
- the “technical plan” is actually a broad redesign disguised as a local change;
- the plan’s success depends on tests or commands that were not identified.

## False-positive guard

Do not over-escalate every unknown. Some unknowns are non-blocking.

A missing fact is blocking only when it would change the recommended direction, scope, source of truth, compatibility policy, rollout, or validation model.

If the missing fact only affects confidence or implementation details, proceed with an explicit assumption and add a stop condition.
