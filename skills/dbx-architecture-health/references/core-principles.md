# Core principles for AI-coding-era architecture health

This reference defines the small set of root controls used by `dbx-architecture-health`.

Do not treat this as a decorative checklist. The point is to find the controls that actually reduce architecture decay when code is increasingly produced, edited, and refactored by AI agents under human review.

## Fundamental thesis

AI coding changes the cost structure of software work:

```text
code generation cost decreases
but semantic ownership, invariant proof, review, migration, rollback, and context grounding costs remain
```

The architecture question becomes:

```text
Can a fallible coding agent and a bounded human reviewer make the next likely change safely, with small context and executable proof?
```

Architecture health is therefore not “does this follow Clean Architecture?” or “is every file small?” It is whether the repository is a controlled change system.

## Primary controls

### 1. [OWN] Ownership and invariant control

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

### 2. [LOC] Change locality and blast-radius control

Primary question:

```text
How much code, context, and coordination are required for one correct semantic change?
```

High-signal evidence:
- one business change requires edits across unrelated features, packages, configs, docs, generated artifacts, and tests;
- shared modules contain feature-specific policy;
- feature modules import each other directly;
- public exports grow without ownership or compatibility policy;
- circular dependencies or hidden bidirectional coupling;
- a stable-looking behavior becomes a de facto API through too much exposure.

AI-coding relevance:
- agents can modify many files quickly, but reviewers still need to verify semantic consistency;
- large blast radius makes omissions more likely and review less reliable;
- broad automatic changes can hide the one missed synchronized location.

Do not over-flag:
- multi-module changes are fine when boundaries, contracts, and validation make the change coherent;
- composition roots and adapter glue may legitimately connect many concrete implementations;
- fan-out alone is not decay if dependency policy is explicit and enforced.

### 3. [PROOF] Executable proof and validation topology

Primary question:

```text
How does the repo prove that important invariants, contracts, and user paths still hold?
```

High-signal evidence:
- important rules exist only in prose, comments, screenshots, or old issue threads;
- public APIs, schemas, migrations, auth/permission flows, pricing, or data lifecycles lack contract/regression tests;
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

### 4. [CTX] Context and control-surface integrity

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
- the repo becomes the prompt;
- stale or conflicting context steers generation toward wrong local patterns;
- agent instructions are weak control compared with executable constraints, but they are still part of the architecture's operational surface.

Do not over-flag:
- absence of long docs is not a problem if code/tests/contracts are self-explanatory;
- brief docs are better than large stale docs;
- context cleanup is lower priority than fixing broken ownership or missing proof.

### 5. [EVO] Evolution, compatibility, and reversibility control

Primary question:

```text
Can the system evolve, migrate, roll back, and absorb dependency/API changes without heroic coordination?
```

High-signal evidence:
- irreversible migrations without rollback or compatibility window;
- public API behavior changes without deprecation, versioning, or consumer scan;
- dependency versions and generated clients drift across packages;
- feature flags exist but cannot isolate the actual risk;
- release/package artifacts are not tied to source or validation;
- long-lived compatibility branches accumulate with no retirement path.

AI-coding relevance:
- agents are good at local code edits and weak at rollout semantics;
- architecture must bound failure when generated changes are wrong;
- reversibility turns AI speed from a hazard into a safer iteration loop.

Do not over-flag:
- not every internal change needs rollout machinery;
- small reversible changes can be merged without heavyweight migration plans;
- compatibility cost should match the public surface and blast radius.

## Proxy smells are not root principles

Many classic software-engineering concepts remain useful, but they should be treated as evidence, not the final diagnosis.

| Proxy smell or classic concept | Map it to | Why not primary |
|---|---|---|
| Cognitive overload | LOC / CTX / PROOF | It is often a symptom of unclear ownership, too much blast radius, or poor proof. |
| Dependency disorder | LOC / OWN / EVO | Direction matters because it changes ownership, locality, upgrade, and rollback costs. |
| Knowledge duplication | OWN | Duplicated text is not always duplicated decision-making. |
| Accidental complexity | LOC / PROOF / EVO | Complexity is harmful when it increases change, proof, or evolution cost. |
| Domain model distortion | OWN | The core issue is wrong truth ownership and invariant expression. |
| Generated-code quarantine | CTX / OWN | It is a mechanism for context and source-of-truth clarity. |
| Architecture memory | CTX / EVO | It is a maintenance surface, not a root architecture principle. |
| Reviewability | All five controls | It is an outcome of good ownership, locality, proof, context, and reversibility. |
| Clean/Hexagonal/DDD layering | OWN / LOC / EVO | Patterns are useful only when they encode real ownership and volatility boundaries. |

## The anti-formalism rules

Use these rules to keep findings real:

1. No credible future change, no architecture finding.
2. No concrete owner, invariant, contract, proof, or boundary consequence, no finding.
3. No severity without impact.
4. No confidence without evidence.
5. Do not punish simple systems for staying simple.
6. Do not reward complex systems for naming abstractions.
7. Prefer one root-cause finding over five symptom findings.
8. Prefer executable guardrails over prose reminders.
9. Prefer reversible small moves over heroic rewrites.
10. If the best fix is “decide the owner”, say that before proposing refactors.
