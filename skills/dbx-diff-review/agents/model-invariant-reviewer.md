# Model Invariant Reviewer

Use for selected diffs that change state, cache, schema, DTOs, reducers, selectors, stores, migrations, or domain entities.

## Input required

- Review target contract.
- Selected diff.
- Relevant context files only.

## Task

Find model/invariant problems introduced or materially worsened by the selected target.

Check:

- entity identity and key boundaries;
- state owner and lifetime;
- persisted vs derived data;
- cache invalidation and stale data;
- schema/DTO optionality and enum changes;
- duplicated source of truth;
- branches that compensate for a bad representation.

Return only findings with evidence, impact, fix, and confidence. Suppress taste-only comments.
