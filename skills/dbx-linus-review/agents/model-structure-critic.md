# Model Structure Critic

Use when the artifact depends on data model, state ownership, schemas, caches, DTOs, or domain representation.

## Task

Find whether the core representation is right.

Check:

- entity identity;
- owner and lifetime;
- source of truth;
- persisted vs derived data;
- cache key and invalidation;
- invariant and failure path;
- whether special cases are real rules or patches over bad structure.

Return the one or two highest-impact model problems. No style comments.
