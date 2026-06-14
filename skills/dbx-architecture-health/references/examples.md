# Architecture health examples

These examples show the expected level of evidence. Adapt to the actual repository. Do not copy as boilerplate.

## Example 1: high-signal truth finding

```markdown
1. [S1 high][TRUTH/PROOF] User status has three sources of truth
   - Evidence: `src/domain/user/status.ts` defines `Active | Suspended | Deleted`; `src/api/userDto.ts` accepts `active | disabled`; `src/features/billing/userStatus.ts` maps only `active` and `disabled`; no test covers status mapping completeness.
   - Future-change impact: Adding a new user status requires synchronized edits across domain, API adapter, billing, and tests. A missed mapping can silently grant or block billing behavior for the wrong account state.
   - AI-coding failure mode: an agent changing the file nearest to the user story is likely to update one status union and mirror the local pattern, missing the other source-of-truth copies.
   - Human-review impact: reviewer has to manually compare several files because no contract test or exhaustive mapping proves completeness.
   - Fix: Choose `src/domain/user/status.ts` as the domain owner; derive or exhaustively map boundary DTO statuses; add a mapping contract test that fails when a status is unhandled.
   - Validation: Add an exhaustiveness/typecheck assertion or table-driven test that introduces an unmapped status and fails.
   - Confidence: high
```

Why this is good:

- exact files;
- root cause is truth ownership, not “duplication is bad”;
- future-change path is concrete;
- AI failure mode is specific;
- fix is bounded.

## Example 2: boundary and change-locality finding

```markdown
1. [S2 medium][LOCALITY/CONTEXT] `shared/` is becoming a feature-policy dumping ground
   - Evidence: `src/shared/tabs.ts`, `src/shared/paymentCopy.ts`, and `src/shared/onboardingFilters.ts` are used by only one feature each, but are exported from the public `src/shared/index.ts` barrel. Module docs say `shared/` is for cross-feature primitives.
   - Future-change impact: Future feature edits will look globally reusable by default. Moving or changing a feature-private rule can become a repo-wide concern because consumers can import it through the shared barrel.
   - AI-coding failure mode: an agent will see the barrel export and likely add new feature config to `shared/`, expanding public surface instead of placing policy near the feature owner.
   - Human-review impact: reviewer must inspect importers and intent manually because folder structure says “shared” while actual ownership is feature-private.
   - Fix: Move feature-private config next to the owning feature or mark it internal; reserve `shared/` for real cross-feature primitives; add a short README or lint/dependency rule if this pattern recurs.
   - Validation: Grep current importers before moving; typecheck; add/update dependency rule only if the team wants enforcement.
   - Confidence: medium
```

Why this is good:

- does not claim all shared code is bad;
- public surface and feature ownership are the real issue;
- fix begins with ownership placement, not a grand rewrite.

## Example 3: proof finding with a real commitment

```markdown
1. [S1 high][PROOF/TRUTH] Payment retry invariant is not executable
   - Evidence: `src/payments/retryPolicy.ts` encodes max retry count and backoff; `docs/payments.md` says failed payments must not be charged twice; tests cover successful retry but not idempotency under timeout or duplicate webhook.
   - Future-change impact: Any agent or maintainer adjusting retry/backoff can preserve happy-path tests while breaking the no-double-charge invariant.
   - AI-coding failure mode: an agent asked to “make retries more robust” may add another retry path or webhook handler branch without testing duplicate external events.
   - Human-review impact: reviewer cannot prove safety from current tests because the important external commitment is idempotency, not retry success.
   - Fix: Add an idempotency contract test around timeout + duplicate webhook before changing retry behavior; if the invariant owner is external, document the boundary and verify request idempotency keys.
   - Validation: Run the targeted payment retry/idempotency tests and typecheck/build if relevant.
   - Confidence: high
```

Why this is good:

- a missing test is tied to a named invariant;
- severity is justified by a real money-path commitment;
- the finding is architectural because proof does not protect the change class.

## Example 4: context finding

```markdown
1. [S2 medium][CONTEXT/TRUTH] Agent instructions point to stale API type ownership
   - Evidence: `CLAUDE.md` says new API types belong in `src/types/api.ts`; current codegen writes API types to `src/generated/api/`; `src/types/api.ts` still exists with two handwritten legacy types.
   - Future-change impact: Future AI-generated changes can resurrect or extend the legacy handwritten type file, creating a second API type source of truth.
   - AI-coding failure mode: an agent will likely follow `CLAUDE.md` because it is a top-level instruction file, even though current codegen has moved the source of truth.
   - Human-review impact: reviewer has to know historical context to reject the wrong file; the repo itself points in two directions.
   - Fix: Update `CLAUDE.md` to point to the generated source; mark `src/types/api.ts` deprecated or remove it after consumer scan; add generated-file header if missing.
   - Validation: Grep imports from `src/types/api.ts`; run typecheck; regenerate API types if the repo supports it.
   - Confidence: high
```

Why this is good:

- context issue is treated as architecture risk only because it can create a false source of truth.

## Example 5: compatibility is not universal

```markdown
Not a main finding: this internal prototype route lacks API versioning.
```

Why this is suppressed:

- the repo is an internal two-week prototype;
- there are no external consumers, packages, persisted migrations, or public contracts;
- adding versioning would increase cost without protecting a real commitment.

A valid version of this finding would require evidence like:

```markdown
Evidence: `packages/sdk` is published, `api/users` is consumed by external clients, and changelog promises backwards compatibility. The route behavior changed without consumer scan or contract test.
```

## Anti-pattern: vague classic-principle finding

```markdown
[S2] This module violates DRY and Clean Architecture. Refactor it into services and repositories.
```

Problems:

- no concrete evidence;
- no root question;
- no future-change path;
- no AI failure mode;
- fix is pattern-driven and possibly harmful.

## Anti-pattern: fake health score precision

```markdown
Health Score: 73/100
```

A single score can be useful as a trend if backed by a stable rubric, but a one-off architecture health review should not pretend this number is objective.

Prefer dimensional status:

```markdown
TRUTH: bad
LOCALITY: watch
PROOF: bad
CONTEXT: watch
Compatibility relevance: not_applicable
```

## Anti-pattern: generated-code panic

```markdown
[S1] There is massive duplicate code under `src/generated`, so this repo has serious duplication debt.
```

Generated duplication is acceptable when there is a clear source of truth, generated files are marked, and stale generation is checked when it matters. The real finding, if any, is missing source-of-truth clarity or stale-generation proof.
