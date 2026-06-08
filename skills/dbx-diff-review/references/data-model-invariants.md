# Data Model and Invariant Review

Use this reference when the diff changes state, schema, API contracts, caches, derived data, frontend stores, reducers, selectors, backend models, DTOs, migrations, or persistence.

## Core questions

1. What are the core entities?
2. What is the identity of each entity?
3. Who owns the state?
4. What is persisted vs derived?
5. What is cached, and what invalidates it?
6. What invariant must always hold?
7. Which boundary transforms the data?
8. What happens on partial failure, retry, rollback, user switch, tenant switch, logout, permission downgrade, or refresh?

## Common bad models

### Wrong identity boundary

Symptoms:

- cache keyed by `userId` but behavior depends on `tenantId`, `sessionId`, `locale`, `permissionSet`, or feature flag;
- list items keyed by array index when order can change;
- optimistic updates keyed by temporary ids that are not reconciled.

Review finding shape:

```text
The identity boundary is too small. The system treats X as unique, but the behavior depends on Y too.
```

### Two sources of truth

Symptoms:

- local component state and global store both own the same field;
- API response is copied into a mutable model and later patched separately;
- derived flags are stored and can drift from source values.

Ask whether one source can derive the other.

### Cache without lifecycle

Symptoms:

- no invalidation on logout/login/user switch/tenant switch/permission downgrade;
- cache survives feature flag or config changes;
- mutation does not update or invalidate reads;
- stale cache is hidden by optimistic UI.

### Schema or DTO mismatch

Symptoms:

- field renamed in API response but frontend type/mapper not updated;
- optionality changes but callers assume required;
- enum grows but switch/exhaustive handling does not;
- migration changes persisted data without rollback or compatibility path.

### Special-case patches

Symptoms:

- branches multiply around one entity state;
- boolean flags encode multiple states;
- error handling differs by caller because the model cannot express a common rule;
- new adapter only exists to compensate for previous incorrect representation.

Good fix direction: change representation so the common path is simple.

## Frontend-specific invariants

- State owner: component, URL, server cache, global store, form library, or storage.
- Lifetime: render frame, route lifetime, session, tab, user, tenant, app install.
- Async safety: stale closures, request races, cancellation, double submit, optimistic rollback.
- Hydration: server/client value mismatch, localStorage-dependent first render.
- Accessibility/user flow: disabled/loading/error states and focus/keyboard behavior.

## Backend-specific invariants

- Transaction boundary and idempotency.
- Authorization before mutation and after lookup.
- Input validation before trust-boundary crossing.
- Consistent schema/version handling.
- Retry and duplicate event handling.
- Migration compatibility and rollback.

## Review smell

If you are about to write five comments about small branches, stop and ask: “Is there one wrong state model causing all of these?”
