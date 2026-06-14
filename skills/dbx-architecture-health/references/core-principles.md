# Core principles for AI-coding-era architecture health

This reference defines the small set of questions used by `dbx-architecture-health`. It is not a checklist. The point is to find the few structural issues that actually make future AI-assisted changes unsafe, expensive, or hard to verify.

## Starting point

AI coding changes the cost structure of software work:

```text
code editing gets cheaper;
finding truth, proving behavior, reviewing changes, and avoiding misleading context do not get cheap at the same rate.
```

The architecture question becomes:

```text
Can a fallible coding agent and a bounded human reviewer make the next likely change safely, using small enough context and explicit proof?
```

Architecture health is therefore not “does this follow Clean Architecture?” or “is every file small?” It is whether the repository is shaped so that likely semantic changes can be made, checked, and corrected without heroic coordination.

## Review begins before principles

Before applying any principle, identify two things.

### 1. Likely change scenarios

Ask what changes this repository or module is expected to absorb:

- new product feature;
- new entity state or lifecycle rule;
- API/schema change;
- payment/auth/security rule;
- UI workflow change;
- dependency upgrade;
- migration or data shape change;
- package release;
- one-off prototype iteration.

No credible future change, no architecture finding.

### 2. Risk profile

Do not judge every codebase like a public platform.

Calibrate by:

- prototype vs internal tool vs product vs platform vs public library;
- number and type of users;
- persisted data;
- public API or SDK consumers;
- security, money, auth, compliance, or privacy paths;
- release/package expectations;
- migration history;
- expected lifetime.

Compatibility, migration, rollout, rollback, and versioning matter when the repo has real commitments. They are not universal obligations.

## Four core questions

### 1. [TRUTH] Where is the truth?

Primary question:

```text
What is true, who owns it, where is it enforced, and who is allowed to change it?
```

High-signal evidence:

- duplicate enums, schemas, state machines, permission rules, price formulas, status maps, feature flags, or lifecycle rules;
- API DTOs used as domain models;
- UI state treated as persisted/domain state;
- caches with unclear invalidation owner;
- fixture/example data acting as hidden domain source of truth;
- multiple modules writing the same state without a single owner;
- business names in code that do not match product/domain language.

AI-coding relevance:

- agents copy visible patterns and may update only one source of truth;
- agents often infer business rules from local code, fixtures, or DTOs;
- wrong ownership creates plausible patches that make the model more wrong.

Do not over-flag:

- separate bounded contexts may intentionally have similar names or concepts;
- DTOs are acceptable at boundaries when they are not treated as policy owners;
- simple CRUD flows may not need rich domain objects.

### 2. [LOCALITY] Can likely changes stay local?

Primary question:

```text
How much code, context, and coordination are required for one correct semantic change?
```

High-signal evidence:

- one business change requires edits across unrelated features, packages, configs, docs, generated artifacts, and tests;
- shared modules contain feature-specific policy;
- feature modules import each other directly;
- public exports grow without ownership or consumer awareness;
- circular dependencies or hidden bidirectional coupling;
- a stable-looking behavior becomes a de facto API through too much exposure.

AI-coding relevance:

- agents can modify many files quickly, but reviewers still need to verify semantic consistency;
- large blast radius makes omissions more likely and review less reliable;
- broad automatic changes can hide the one missed synchronized location.

Do not over-flag:

- multi-module changes are fine when boundaries, contracts, and validation make the change coherent;
- composition roots and adapter glue may legitimately connect many concrete implementations;
- fan-out alone is not decay if the dependency policy is explicit and enforced.

### 3. [PROOF] What proves important behavior?

Primary question:

```text
How does the repo prove that important invariants, contracts, and user paths still hold?
```

High-signal evidence:

- important rules exist only in prose, comments, screenshots, or old issue threads;
- public APIs, schemas, auth/permission flows, pricing, data lifecycles, or important migrations lack contract/regression tests;
- tests assert implementation wiring but not domain behavior;
- generated tests mirror the implementation and would pass with the same bug;
- lint/typecheck/CI do not cover the risk that actually matters;
- manual verification paths are undefined for high-risk flows.

AI-coding relevance:

- agents can produce code and tests that agree with each other while both violate the product invariant;
- executable proof is the main guardrail against confident but wrong code generation;
- tests should encode behavior and contracts, not merely satisfy coverage optics.

Do not over-flag:

- not every helper needs a test;
- coverage percentage is not proof quality;
- a missing test is a finding only when it leaves a named invariant, contract, or user path unprotected.

### 4. [CONTEXT] Will the repo context mislead humans or agents?

Primary question:

```text
Can humans and agents discover the right source of truth under bounded context?
```

High-signal evidence:

- `AGENTS.md`, `CLAUDE.md`, README, ADRs, module docs, examples, and code disagree;
- generated/vendor/snapshot code is not clearly marked;
- examples or fixtures are likely to be copied into production paths;
- module entrypoints and naming obscure ownership;
- key conventions exist only as tribal memory;
- repo instructions ask agents to obey rules that are not encoded in tests, lint, types, dependency checks, or docs close to the relevant module.

AI-coding relevance:

- the repo becomes part of the prompt;
- stale or conflicting context steers generation toward wrong local patterns;
- agent instructions are weaker than executable constraints, but they still influence future edits.

Do not over-flag:

- absence of long docs is not a problem if code/tests/contracts are self-explanatory;
- brief docs are better than large stale docs;
- context cleanup is lower priority than fixing broken ownership or missing proof.

## Commitments, not universal compatibility

Compatibility is important when the system has something to be compatible with:

- external consumers;
- public API or SDK;
- persisted data;
- release/package artifacts;
- long-lived user workflows;
- auth, money, security, privacy, or compliance paths;
- migration windows;
- explicit product promises.

When these exist, compatibility and rollback concerns can be severe. When they do not, forcing versioning, migration plans, feature flags, or elaborate rollout machinery can be architecture debt in disguise.

Use this rule:

```text
Do not demand compatibility. Identify commitments. Protect the commitments that exist.
```

## Proxy smells are not root principles

Many classic software-engineering concepts remain useful, but they should be treated as evidence, not the final diagnosis.

| Proxy smell or classic concept | Map it to | Why not primary |
|---|---|---|
| Cognitive overload | LOCALITY / CONTEXT / PROOF | It is often a symptom of unclear ownership, too much blast radius, or weak proof. |
| Dependency disorder | LOCALITY / TRUTH / risk profile | Direction matters because it changes ownership, locality, and commitment cost. |
| Knowledge duplication | TRUTH | Duplicated text is not always duplicated decision-making. |
| Accidental complexity | LOCALITY / PROOF / risk profile | Complexity is harmful when it increases change or proof cost relative to real risk. |
| Domain model distortion | TRUTH | The core issue is wrong truth ownership and invariant expression. |
| Generated-code quarantine | CONTEXT / TRUTH | It is a mechanism for context and source-of-truth clarity. |
| Architecture memory | CONTEXT | It is a maintenance surface, not a root architecture principle. |
| Reviewability | All four questions | It is an outcome of good truth, locality, proof, and context. |
| Clean/Hexagonal/DDD layering | TRUTH / LOCALITY | Patterns are useful only when they encode real ownership and volatility boundaries. |

## Anti-formalism rules

Use these rules to keep findings real:

1. No credible future change, no architecture finding.
2. No concrete owner, invariant, contract, proof, context, or boundary consequence, no finding.
3. No severity without impact.
4. No confidence without evidence.
5. Do not punish simple systems for staying simple.
6. Do not reward complex systems for naming abstractions.
7. Prefer one root-cause finding over five symptom findings.
8. Prefer executable guardrails over prose reminders.
9. Protect real commitments; do not invent compatibility duties.
10. If the best fix is “decide the owner”, say that before proposing refactors.
