# Finding calibration

Use this reference to calibrate severity, confidence, evidence class, and false-positive guards for architecture health findings.

## Required finding shape

A real architecture health finding must have all of these:

```text
root control: OWN | LOC | PROOF | CTX | EVO
observed evidence: concrete repo artifact or user-provided architecture fact
future-change failure path: what becomes unsafe, expensive, or unverifiable
AI-coding failure mode: what a coding agent is likely to copy, miss, or misread
bounded fix direction: a minimum useful anti-decay move
validation path: how to prove the fix reduced risk
confidence: high | medium | low
```

If any field is missing, demote the item to residual risk, investigation note, or omit it.

## Evidence classes

| Class | Evidence | Typical use |
|---|---|---|
| E0 observed failure | failing test, production incident, command output, bug report, CI failure, explicit user evidence | Can support S0/S1 if impact is high. |
| E1 direct structural evidence | conflicting files, duplicate source of truth, import path, public export, schema mismatch, missing contract test for named invariant | Can support S1/S2. |
| E2 topology or trend evidence | churn hotspot, fan-out, large shared surface, repeated pattern, generated/vendor ambiguity | Usually S2 unless tied to direct impact. |
| E3 docs/context evidence | stale docs, conflicting instructions, missing README, weak agent guidance | Usually S2/S3 unless it demonstrably causes wrong changes. |
| E4 inference only | plausible hypothesis without inspected repo evidence | Not a finding. Put in unknowns. |

S0/S1 findings should normally require E0 or E1. E2 can become S1 only when the blast radius is critical and the future-change path is concrete.

## Severity calibration

### [S0 blocker]

Use only when architecture creates an immediate or near-immediate high-impact failure mode:
- unsafe migration path likely to corrupt or lose data;
- auth/permission ownership split likely to expose data;
- production-critical public contract cannot be changed safely;
- rollback impossible for an active high-risk change;
- CI/release path cannot verify a critical generated artifact or package output.

S0 must include direct evidence and a validation/mitigation gate.

### [S1 high]

Use when a root decay mechanism is likely to cause real regressions or dangerous future changes:
- duplicated source of truth for a core business rule;
- wrong state owner or cache owner in a critical flow;
- domain model represented by boundary DTOs across many modules;
- public API or schema evolution with no compatibility/consumer policy;
- important invariant lacks executable proof and is actively changed;
- AI context is actively steering code generation toward wrong owner or wrong pattern.

### [S2 medium]

Use when decay is concrete but bounded:
- shared module is growing into a dumping ground but impact is localized;
- tests cover happy path but not named edge invariants;
- docs/context are stale around a non-critical module;
- import direction creates future coupling but no current critical flow is exposed;
- generated artifacts are mixed with handwritten code but source of truth can still be found.

### [S3 low]

Use sparingly:
- local boundary clarification;
- small context/doc cleanup;
- minor source-of-truth naming issue;
- low-risk generated-code marker or README improvement.

Do not fill the report with S3 items unless the user asks for a full backlog.

## Confidence calibration

- `high`: exact paths and artifacts show the issue; impact path is concrete; likely false-positive guards were checked.
- `medium`: evidence is concrete, but impact depends on likely future changes or missing runtime details.
- `low`: useful suspicion. Do not present as a main finding unless the user asked for hypotheses.

Severity and confidence are independent. A possible catastrophic issue with weak evidence is `high impact / low confidence`, not automatically S0.

## Root-cause grouping

When several symptoms share one root cause, group them:

```markdown
Root cause: user status ownership split between domain, API adapter, and UI store
Mapped controls: OWN, LOC, PROOF
Symptoms:
- `src/domain/user/status.ts` and `src/api/userDto.ts` define different status sets
- UI has a local `editableStatus` union
- tests cover rendering but not status transition compatibility
Primary fix:
- choose domain status as owner, generate/derive boundary mappings, add transition contract test
```

Do not write separate findings for each duplicate enum, mapping, and missing test when one ownership decision fixes them.

## False-positive guards

Check these before reporting.

### Simple system guard

A small CRUD app, internal script, prototype, or one-off tool may not need layered architecture, rich domain modeling, or extensive rollout machinery. Flag only real future-change or correctness risk.

### Bounded-context duplication guard

Similar terms in different bounded contexts are not automatically duplicated decisions. Ask whether they have independent lifecycles and domain meanings.

### Generated projection guard

Repeated code generated from a single schema/source is acceptable if:
- the source is obvious;
- generated files are marked;
- generated artifacts are not manually edited;
- validation catches stale generation.

### Adapter glue guard

Adapters, composition roots, test fixtures, and integration glue may legitimately import concrete details. Flag only when policy or source-of-truth ownership leaks through the adapter.

### Migration window guard

Temporary duplication during an active migration is acceptable when:
- the old and new paths are labeled;
- compatibility behavior is defined;
- removal/retirement path exists;
- validation covers both paths.

### Public API guard

Public surface is not bad by itself. It becomes risk when it lacks owner, compatibility policy, consumer scan, versioning, or proof.

### Documentation guard

Missing docs are not automatically CTX risk. Stale or conflicting docs are more dangerous than sparse docs. Prefer docs close to the source of truth and backed by tests/contracts.

## Bad finding patterns

Avoid these:

```markdown
[S2] This file is too long.
```

No root cause, no future-change path.

```markdown
[S1] Violates Clean Architecture because domain imports infra.
```

Could be true, but needs impact, ownership, and evidence.

```markdown
[S2] Add more tests.
```

Name the unprotected invariant or omit it.

```markdown
[S1] Rewrite the module using DDD.
```

Pattern worship. Specify the ownership/invariant failure and the smallest useful change.

## Good finding test

A good finding should pass this sentence:

```text
Because of [observed evidence], the next likely change [change class] will require [unsafe/expensive/unverifiable coordination], and an AI coding agent is likely to [specific failure mode]. The smallest useful fix is [bounded action], proven by [validation].
```
