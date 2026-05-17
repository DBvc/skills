# Strict Data Model and Invariant Review

Use this reference when the artifact is mostly about data structures, state ownership, schemas, caches, or domain model.

## The brutal checklist

1. What is the entity?
2. What is its identity?
3. Who owns it?
4. What is its lifetime?
5. What is persisted vs derived?
6. What invalidates it?
7. What can observe or mutate it?
8. What user/caller path breaks when the invariant fails?

## Red flags

- A cache key omits a boundary that changes behavior.
- A boolean flag encodes multiple states.
- A DTO is copied into mutable UI/domain state without a mapper or invariant boundary.
- A model exists only because callers disagree about ownership.
- A migration changes shape without compatibility or rollback.
- A helper hides policy decisions that belong at a domain boundary.
- A plan introduces multiple managers/stores/buses/reconcilers for one state problem.
- The system needs many special cases to explain the “normal” path.

## What to say

Lead with the model, not the syntax.

Good:

```text
The bug is not the missing null check. The bug is that draft ownership is split between URL params, local form state, and DraftStore. The null check only hides one symptom.
```

Bad:

```text
This function is ugly.
```

## Simpler direction patterns

- Collapse derived state back to a source of truth.
- Key caches by the actual boundary: session, tenant, locale, feature flag, permission set.
- Move policy to the domain boundary instead of leaking it through UI helpers.
- Replace several booleans with one explicit state enum when the domain has states.
- Make migration compatibility explicit before changing persisted shape.
