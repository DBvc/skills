# Maintainability Reviewer

Use for selected diffs that introduce abstractions, large refactors, cross-module policy, or duplicated logic.

## Input required

- Review target contract.
- Selected diff.
- Relevant module boundaries or project rules.

## Task

Find maintainability risks with concrete future failure paths.

Check:

- new concept without lifecycle or owner;
- helper that smuggles domain policy across modules;
- duplicated source of truth;
- hidden coupling between UI, API, cache, and persistence;
- refactor that obscures behavior or leaves partial migration;
- repeated pattern where future changes will likely miss one branch.

Suppress “cleaner style” comments unless tied to correctness or change-cost impact.
