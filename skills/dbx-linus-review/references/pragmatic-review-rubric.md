# Pragmatic Review Rubric

Use this file when the review needs stricter structure.

## Severity

- **S0 blocker**: data loss, security exposure, hard compatibility break, production outage path, unsafe migration without rollback, irreversible user harm.
- **S1 high**: likely regression, broken core flow, severe performance cliff, incorrect ownership model, unsafe concurrency, auth/permission error, missing validation for high-risk change.
- **S2 medium**: maintainability or correctness risk that is real but bounded; unnecessary complexity likely to cause future bugs; incomplete handling of a plausible edge case.
- **S3 low**: naming, style, local simplification, test clarity, minor consistency.

## Evidence quality

A finding is strong when it cites at least one of:

- file and line/function/component;
- exact diff behavior;
- proposal section, assumption, interface, or migration claim;
- public API or schema change;
- persisted data or migration path;
- failed or missing validation tied to a changed invariant;
- concrete user path or caller path.

A finding is weak when it only says:

- “this feels complex”;
- “maybe risky”;
- “not clean”;
- “could be better”.

Weak findings should be lowered in severity, turned into questions, or suppressed.

## Good review questions

- What is the core data model?
- Who owns this state?
- What invariant is being preserved?
- What existing user path breaks?
- What happens on retry, partial failure, concurrency, stale cache, rollback, or migration failure?
- Which branch is a real rule and which is compensating for a bad representation?
- What is the smallest change that solves the real problem?
- What can be deleted without losing value?

## Anti-patterns

- Persona performance instead of technical evidence.
- Full rewrite recommendation without proving why local change cannot work.
- Listing ten style nits while missing the data model bug.
- Calling something S1 without showing user impact.
- Ignoring compatibility because the new design is “cleaner”.
- Treating a plan as good because it is elaborate.
- Treating a diff as safe because it is small.
