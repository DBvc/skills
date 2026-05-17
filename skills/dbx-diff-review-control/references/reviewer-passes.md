# Reviewer Passes

Use this file to run specialist passes without losing the main target contract.

## Base pass

The base pass always runs:

1. Target selection.
2. Intent/scope drift.
3. User-impact correctness.
4. Data model/invariant review.
5. Compatibility/contracts.
6. Maintainability with concrete failure path.
7. Validation gaps.
8. Verifier pass.

## Specialist activation

Activate specialists only when the selected target needs them.

| Specialist | Activate when |
| --- | --- |
| user-impact reviewer | UI, route, workflow, product behavior, permissions, forms, user-visible API behavior |
| model-invariant reviewer | state, store, cache, schema, DTO, migration, domain entity, reducer, selector |
| maintainability reviewer | new abstraction, cross-module coupling, duplicated policy, large refactor |
| verifier | always, but especially for S0/S1 candidates |

## Parallel or sequential

If the host supports subagents, run activated specialists in parallel with the same review target contract and selected diff. If not, run the passes sequentially.

Do not let specialists expand the target. They may request context files, but they must label context separately from reviewed target files.

## Verifier protocol

For each candidate finding, ask:

1. Is this introduced or materially worsened by the selected target?
2. Is there concrete evidence?
3. Is the impact user-visible, data/model-breaking, compatibility-breaking, or materially maintainability-relevant?
4. Is there a smaller fix direction?
5. Could a type checker, linter, existing test, or project rule already catch it?
6. Is it actually out of scope?
7. What would make this false?

Suppress candidates that fail the verifier. Lower confidence instead of overclaiming.

## Adversarial pass

For deep review, ask:

```text
If I wanted this selected change set to fail in production, what path would I use?
```

Angles:

- assumption violation;
- stale data or stale session;
- partial failure and retry;
- concurrent actions;
- unauthorized boundary crossing;
- schema or contract skew;
- rollback/release mismatch.

Suppress anything below medium confidence.
