# Architecture health examples

These examples show the expected level of evidence. Adapt to the actual repository. Do not copy as boilerplate.

## Example 1: high-signal ownership finding

```markdown
1. [S1 high][OWN/PROOF] User status has three sources of truth
   - Evidence: `src/domain/user/status.ts` defines `Active | Suspended | Deleted`; `src/api/userDto.ts` accepts `active | disabled`; `src/features/billing/userStatus.ts` maps only `active` and `disabled`; no test covers status mapping completeness.
   - Impact: Adding a new user status requires synchronized edits across domain, API adapter, billing, and tests. A missed mapping can silently grant or block billing behavior for the wrong account state.
   - AI-coding failure mode: an agent changing the file nearest to the user story is likely to update one status union and mirror the local pattern, missing the other source-of-truth copies.
   - Fix: Choose `src/domain/user/status.ts` as the domain owner; derive or exhaustively map boundary DTO statuses; add a mapping contract test that fails when a status is unhandled.
   - Validation: Add an exhaustiveness/typecheck assertion or table-driven test that introduces an unmapped status and fails.
   - Confidence: high
```

Why this is good:
- exact files;
- root cause is ownership, not “duplication is bad”;
- future-change path is concrete;
- AI failure mode is specific;
- fix is bounded.

## Example 2: boundary and change-locality finding

```markdown
1. [S2 medium][LOC/CTX] `shared/` is becoming a feature-policy dumping ground
   - Evidence: `src/shared/tabs.ts`, `src/shared/paymentCopy.ts`, and `src/shared/onboardingFilters.ts` are used by only one feature each, but are exported from the public `src/shared/index.ts` barrel. Module docs say `shared/` is for cross-feature primitives.
   - Impact: Future feature edits will look globally reusable by default. Moving or changing a feature-private rule can become a repo-wide compatibility concern because consumers can import it through the shared barrel.
   - AI-coding failure mode: an agent will see the barrel export and likely add new feature config to `shared/`, expanding public surface instead of placing policy near the feature owner.
   - Fix: Move feature-private config next to the owning feature or mark it internal; reserve `shared/` for real cross-feature primitives; add a short README or lint/dependency rule if this pattern recurs.
   - Validation: Grep current importers before moving; typecheck; add/update dependency rule only if the team wants enforcement.
   - Confidence: medium
```

Why this is good:
- does not claim all shared code is bad;
- public surface and feature ownership are the real issue;
- fix begins with ownership placement, not a grand rewrite.

## Example 3: proof topology finding

```markdown
1. [S1 high][PROOF/EVO] Payment retry invariant is not executable
   - Evidence: `src/payments/retryPolicy.ts` encodes max retry count and backoff; `docs/payments.md` says failed payments must not be charged twice; tests cover successful retry but not idempotency under timeout or duplicate webhook.
   - Impact: Any agent or maintainer adjusting retry/backoff can preserve happy-path tests while breaking the no-double-charge invariant.
   - AI-coding failure mode: an agent asked to “make retries more robust” may add another retry path or webhook handler branch without testing duplicate external events.
   - Fix: Add an idempotency contract test around timeout + duplicate webhook before changing retry behavior; if the invariant owner is external, document the boundary and verify request idempotency keys.
   - Validation: Run the targeted payment retry/idempotency tests and typecheck/build if relevant.
   - Confidence: high
```

Why this is good:
- a missing test is tied to a named invariant;
- the finding is architectural because proof does not protect the change class.

## Example 4: context-control finding

```markdown
1. [S2 medium][CTX/OWN] Agent instructions point to stale architecture ownership
   - Evidence: `CLAUDE.md` says new API types belong in `src/types/api.ts`; current codegen writes API types to `src/generated/api/`; `src/types/api.ts` still exists with two handwritten legacy types.
   - Impact: Future AI-generated changes can resurrect or extend the legacy handwritten type file, creating a second API type source of truth.
   - AI-coding failure mode: an agent will likely follow `CLAUDE.md` because it is a top-level instruction file, even though current codegen has moved the source of truth.
   - Fix: Update `CLAUDE.md` to point to the generated source; mark `src/types/api.ts` deprecated or remove it after consumer scan; add generated-file header if missing.
   - Validation: Grep imports from `src/types/api.ts`; run typecheck; regenerate API types if the repo supports it.
   - Confidence: high
```

Why this is good:
- context issue is treated as architecture risk only because it can create a false source of truth.

## Anti-pattern: vague classic-principle finding

```markdown
[S2] This module violates DRY and Clean Architecture. Refactor it into services and repositories.
```

Problems:
- no concrete evidence;
- no root control;
- no future-change path;
- no AI failure mode;
- fix is pattern-driven and possibly harmful.

## Anti-pattern: fake health score precision

```markdown
Health Score: 73/100
```

A single score can be useful as a trend if backed by a stable rubric, but a one-off architecture health review should not pretend this number is objective. Prefer dimensional status:

```markdown
OWN: bad
LOC: watch
PROOF: bad
CTX: watch
EVO: unknown
```

## Anti-pattern: generated-code panic

```markdown
[S1] There is massive duplicate code under `src/generated`, so this repo has serious duplication debt.
```

Generated duplication is acceptable when there is a clear source of truth, generated files are marked, and stale generation is checked. The real finding, if any, is missing source-of-truth clarity or stale-generation proof.
