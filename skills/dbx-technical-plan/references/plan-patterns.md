# Plan Patterns

Use a plan shape that matches the task. Do not force every task into the same ceremony.

## Small feature

Shape:

```text
goal -> affected surface -> minimal vertical slice -> validation -> review focus
```

Use when the change is local, reversible, and low-risk.

Required checks:

- What user path or caller path changes?
- What is the smallest end-to-end slice?
- What behavior must not change?
- Which test or manual path proves the slice works?

Common failures:

- planning a framework when a local patch is enough;
- adding shared abstractions before two real call sites exist;
- skipping validation because the change feels small.

## Bug-fix strategy

Shape:

```text
repro -> observed behavior -> expected behavior -> hypotheses -> minimal patch -> regression test -> verification
```

Required checks:

- Can the bug be reproduced or logically traced?
- Which invariant is violated?
- Which hypothesis is most likely and cheapest to disprove?
- What regression test protects the fix?
- What adjacent cases might still fail?

Common failures:

- patching symptoms without identifying the source of truth;
- changing broad behavior to fix a narrow bug;
- treating a missing test as optional when it protects the broken invariant.

## Refactor

Shape:

```text
invariants -> current ownership -> target ownership -> small slices -> behavior-preserving validation -> cleanup
```

Required checks:

- Which behavior must be preserved exactly?
- Which source of truth or owner is being clarified?
- What is forbidden scope?
- Can each slice be reviewed independently?
- How will accidental behavior changes be detected?

Common failures:

- using “cleanup” to smuggle in feature changes;
- moving files without moving ownership;
- changing public contracts while calling the work internal.

## Migration

Shape:

```text
inventory -> partition -> compatibility -> batch execution -> validation -> rollback -> cleanup
```

Required checks:

- What must be inventoried before changes begin?
- Which call sites can be migrated mechanically?
- Which require manual judgment?
- Is a compatibility layer needed?
- What batch order reduces blast radius?
- What rollback path exists?
- When is old code removed?

Common failures:

- starting edits before inventory;
- mixing migration and redesign;
- no rollback path;
- passing typecheck while breaking runtime contracts.

## Architecture change

Shape:

```text
problem -> source-of-truth decision -> alternatives -> selected model -> migration path -> validation -> rollback
```

Generate alternatives only when they are genuinely viable.

Required checks:

- What is the actual modeling problem?
- What becomes the canonical owner?
- What public contracts change?
- Which current callers or users are affected?
- What evidence would prove the selected model is wrong?

Common failures:

- adding a concept to hide a bad data model;
- duplicating source of truth;
- underestimating compatibility;
- selecting a prettier abstraction with worse operational behavior.

## Tooling or infrastructure

Shape:

```text
compatibility matrix -> pilot -> migration guardrails -> CI validation -> fallback -> rollout
```

Required checks:

- Which runtimes, packages, environments, or CI paths are affected?
- What is the pilot scope?
- What must be measured before wider rollout?
- What fallback exists if CI or developer workflow breaks?

Common failures:

- optimizing local DX while breaking CI or release;
- ignoring generated code or package manager edge cases;
- no fallback when the new tool fails.

## Public API or contract

Shape:

```text
contract delta -> caller impact -> compatibility policy -> rollout/deprecation -> validation
```

Required checks:

- What exact contract changes?
- Is the change backwards compatible?
- Which callers are known and unknown?
- How will compatibility be validated?
- What deprecation or migration message is needed?

Common failures:

- changing exported types without considering downstream callers;
- treating internal consumers as proof there are no external consumers;
- making a clean break without a migration path.

## Frontend state or cache change

Shape:

```text
owner -> lifetime -> identity/key model -> async paths -> stale data paths -> validation flows
```

Required checks:

- Who owns the state?
- What is its lifetime?
- Which identity or cache key separates users, tabs, tenants, filters, or sessions?
- What happens on logout/login, refresh, retry, navigation, slow network, or permission downgrade?
- What manual path or automated test proves the invariant?

Common failures:

- duplicate editable state without reconciliation;
- stale cache after identity or permission change;
- optimistic update without rollback;
- hydration or navigation assumptions that only hold locally.

## Validation-only plan

Shape:

```text
risk inventory -> invariant map -> automated checks -> manual checks -> uncovered gaps -> release confidence
```

Required checks:

- What risks need evidence?
- Which can be covered by typecheck, lint, unit, integration, e2e, build, or manual checks?
- Which important risks remain review-only?
- What is explicitly not covered?

Common failures:

- running many checks that do not cover the changed invariant;
- saying “tests passed” without naming what they prove;
- hiding uncovered risk behind a green build.
