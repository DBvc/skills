# Severity and Evidence

Severity is impact plus likelihood. Confidence is evidence quality. Do not inflate severity because a finding sounds clever.

## Severity scale

- **S0 blocker**: data loss, security exposure, production outage, irreversible user harm, hard compatibility break, unsafe migration/release path, or a change that cannot be rolled back safely.
- **S1 high**: likely functional regression in an important user flow, wrong data/state ownership, broken invariant, auth/permission mistake, severe performance cliff, unsafe integration behavior, or a high-risk validation gap.
- **S2 medium**: real but bounded correctness or maintainability risk; incomplete handling of edge cases with plausible user impact; unnecessary complexity likely to cause future bugs.
- **S3 low**: local clarity, small cleanup, naming, test readability, or minor consistency. Report sparingly.

## Evidence quality

Strong evidence cites at least one of:

- changed file and function/line range;
- exact diff behavior;
- public API, schema, config, or persisted data change;
- data flow from input to state to output;
- user flow that fails under named conditions;
- failed or missing validation tied to a changed invariant;
- project rule from `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, docs, or CI.

Weak evidence looks like:

- “this feels complex”;
- “maybe risky”;
- “not clean”;
- “could be better”;
- “tests are missing” without naming the invariant.

Weak findings should be lowered in severity, converted to questions, or suppressed.

## Finding completeness

A reportable finding needs:

```text
Severity: S0/S1/S2/S3
Evidence: what changed and where
Impact: who or what breaks, under which condition
Fix: smallest useful repair direction
Confidence: high/medium/low
Verification: what was checked and what was not run
```

If you cannot fill Impact, it is probably not a finding.

If you cannot fill Evidence, it is not a finding.

If you cannot fill Fix, it may be a diagnostic question rather than a review comment.

## Calibration rules

- S0/S1 require concrete user, data, security, compatibility, or production impact.
- Style-only concerns are S3 unless they hide correctness or model risk.
- Maintainability can be S1/S2 only when the future failure path is concrete.
- Pre-existing issues are not findings unless the selected diff materially worsens or depends on them.
- Out-of-scope dirty files are not findings unless they make the selected target incomplete or unsafe to merge.

## High-signal examples

Good:

```text
[S1 high] Permission cache is keyed only by user id, but tenant id changed in this diff.
Evidence: `permissions.ts` now caches `Map<userId, Permission[]>`; `TenantSwitcher` can reuse the same user id across tenants.
Impact: user may see actions from the previous tenant after switching.
Fix: key cache by session/tenant boundary or clear on tenant switch.
Confidence: high.
```

Bad:

```text
[S1 high] This cache is scary.
```
