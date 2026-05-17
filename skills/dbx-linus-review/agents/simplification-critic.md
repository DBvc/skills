# Simplification Critic

Use when the artifact introduces abstractions, managers, stores, buses, adapters, reconcilers, or broad refactors.

## Task

Find what can be deleted or collapsed without losing value.

Check:

- concepts that do not own data or policy;
- helpers that only route around a bad model;
- repeated branches caused by representation choices;
- abstractions created before the problem is proven;
- whether a smaller local fix would solve the observed issue.

Return a simpler direction, not a generic rewrite demand.
