# DBX Implementation-Bound Planning Workflow

This document defines the DBX collection-level policy for combining technical planning, strict plan review, bounded plan convergence, and Software Plan-First.

It is not a runtime skill. It does not replace the activation rules or internal contracts of any skill.

## 1. Purpose

DBX already has separate capabilities for:

- first-draft implementation planning: `dbx-technical-plan`;
- strict pragmatic review: `dbx-linus-review`;
- bounded review-revision control: `dbx-plan-convergence`;
- persistent review-gated execution: `dbx-software-plan-first-*`;
- concrete code review-repair: `dbx-code-ratchet`.

This workflow defines how the collection composes them when a technical plan is intended to guide implementation.

The policy is:

```text
No plan, no plan review.
Implementation-bound technical plan, one bounded Linus convergence by default.
```

This avoids forcing planning ceremony onto small direct changes while preserving the simplification value of strict review whenever a technical plan is created for implementation.

## 2. Control ownership

| Concern | Owner |
| --- | --- |
| Goal, scope, non-goals, success criteria | User or upstream contract |
| First technical plan | `dbx-technical-plan` or a Plan-First proposal provider |
| Strict critique | Reviewer provider, DBX default: `dbx-linus-review` |
| Finding triage, transition, revision contract, progress/stop gate | `dbx-plan-convergence` |
| Repository facts | Grounding/evidence provider |
| Product, architecture, compatibility, and risk decisions | Human decision owner |
| Plan text revision | Original plan author under `plan_text_only` authority |
| Implementation | Downstream implementation workflow |
| Persistent plan files, seal, task execution | `dbx-software-plan-first-*` |
| Cross-skill routing | Collection workflow or future command layer |

The planner must not approve its own critique. The reviewer must not revise the plan or choose the convergence transition. The controller must not invent repository evidence, replace the decision owner, or generate a pivot direction.

## 3. Activation authority

### 3.1 Direct skill use

A direct request for `dbx-technical-plan` produces a plan and an explicit handoff. It does not silently run every downstream provider.

A direct request for `dbx-plan-convergence` must satisfy that skill's explicit activation rules.

A direct request for strict/Linus review may invoke `dbx-linus-review` under its normal intent-based activation rules.

### 3.2 Delegated composition

An already user-authorized parent workflow may explicitly select this profile and delegate:

```yaml
delegation:
  originating_intent: "create and converge an implementation-bound technical plan"
  workflow_profile: dbx-implementation-bound-planning-v1
  artifact: {}
  scope: []
  provider_bindings: {}
  budget: {}
  modification_authority: plan_text_only
```

The parent must preserve the originating goal, scope, non-goals, permissions, and stop conditions. Delegation is not permission escalation.

Ordinary requests such as “帮我做方案” or “自动完成任务” do not automatically authorize the whole multi-skill workflow unless the parent workflow explicitly selects this profile.

## 4. Workflow paths

### 4.1 Direct low-risk path

```text
Goal
-> implementation
-> deterministic validation
-> concrete diff review or code ratchet when authorized
-> report
```

No technical plan means no plan convergence.

Use this path for local, reversible, low-risk changes whose behavior and validation are clear enough that a separate plan artifact would add more cost than control.

### 4.2 Stateless implementation-bound plan

```text
dbx-technical-plan
-> dbx-plan-convergence(mode=bounded_loop, completion_profile=strict_acceptance)
     -> initial reviewer: dbx-linus-review(plan_strict, full)
     -> bounded revision and scoped closure by the original plan author
     -> final acceptance: qualifying independent full review of the final artifact identity
          -> pass: identity-bound strict_acceptance_receipt
          -> new finding: bounded triage/revision/re-review
          -> no progress or exhausted budget: explicit stop state
-> ready-for-handoff with current receipt
-> implementation
```

Default budget:

```yaml
budget:
  initial_full_review_passes: 1
  local_revision_rounds: 2
  scoped_re_review_passes: 2
  final_acceptance_full_review_passes: 2
```

Generic `dbx-plan-convergence` still defaults to `handoff_ready`. This collection path explicitly selects `strict_acceptance`: scoped re-review closes accepted findings and direct regressions, but cannot authorize implementation. The initial independent full review may qualify when the artifact is unchanged; after any revision, final acceptance requires a fresh independent full review bound to the final type/scheme/version/fingerprint/content refs. A new material finding returns to the remaining bounded revision budget; exhausted budget stops the workflow without claiming acceptance.

When the exact `plan.md/tasks.md` bundle needs a local revision, the revision request/result preserve `implementation_plan_bundle`, `plan-first-bundle-sha256-v1`, both file refs, and the before/after identities. The provider recomputes the bundle fingerprint after editing; scoped closure and the final full review both bind that new identity.

### 4.3 Software Plan-First

```text
dbx-software-plan-first-plan-issue      # when proposal decisions are incomplete
-> dbx-software-plan-first-ground-plan  # when repository facts are needed
-> dbx-software-plan-first-finalize-plan # materialize unsealed plan.md/tasks.md
-> external dbx-plan-convergence gate   # strict review of the exact file bundle
-> dbx-software-plan-first-finalize-plan # verify the current bundle receipt
-> seal
-> implement-feature or showhand
```

The external convergence gate is not a new Plan-First phase. Selected-profile finalize is resumable: the first invocation materializes the final files and stops unsealed; the second passes the receipt identity into `seal`, which recomputes it before writing. Existing direct/manual seals remain compatible; selected seals add bundle identity fields. This does not change manual-only phase activation, implementation, or showhand semantics.

When a parent workflow selects this profile, the acceptance artifact is the exact `plan.md/tasks.md` bundle that implementation will consume. `scripts/issue-workflow.sh bundle-fingerprint <issue-id>` is the canonical producer for `plan-first-bundle-sha256-v1`: it hashes each file's exact bytes, serializes the two lowercase hashes as canonical one-line JSON, then hashes that JSON. `finalize-plan` may not seal until a current `ready-for-handoff` plus valid `strict_acceptance_receipt` bind that bundle type/scheme/version/fingerprint and the same structured plan/tasks refs. A proposal-level receipt may authorize no more than materialization; it cannot authorize the generated bundle. Any file change invalidates the bundle receipt.

Direct/manual `finalize-plan` remains compatible: a user may explicitly confirm that the plan is already converged, provided every existing decision, grounding, ownership, validation, and artifact-boundary gate is satisfied.

## 5. Default provider binding

`dbx-plan-convergence` remains provider-agnostic. DBX collection policy supplies this default binding:

```yaml
profile: dbx-implementation-bound-planning-v1

artifact_provider:
  capability: evidence_grounded_technical_planning
  preferred_dbx_skill: dbx-technical-plan

convergence_controller:
  capability: bounded_plan_convergence
  preferred_dbx_skill: dbx-plan-convergence
  mode: bounded_loop
  completion_profile: strict_acceptance

reviewer:
  capability: strict_pragmatic_plan_review
  preferred_dbx_skill: dbx-linus-review
  artifact_mode: plan_strict
  initial_scope: full
  final_acceptance_scope: full
  final_acceptance_independence: required
  write_access: none

reviser:
  role: original_plan_author
  modification_authority: plan_text_only

permissions:
  modify_plan_text: true
  modify_code: false
  commit: false
  push: false
  external_side_effects: false
```

Provider names belong to this collection profile, not to the generic controller kernel.

## 6. Technical-plan handoff

An implementation-bound technical plan should produce a handoff with enough identity and boundary information for convergence:

```yaml
plan_convergence_handoff:
  status: needs_plan_convergence
  originating_intent: ""
  completion_profile: strict_acceptance
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | implementation_proposal
    version: session-v1
    fingerprint_scheme: exact-bytes-sha256
    fingerprint: ""
    content_ref:
      kind: inline | path | current_context
      value: inline | path | current_response
      plan: null
      tasks: null
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
  evidence_boundary:
    repo_facts_read: []
    user_supplied_facts: []
    external_docs_or_versions: []
    assumptions: []
    unknowns: []
    not_read_or_not_run: []
  core_anchors:
    problem_goal: stable | unknown | conflicted | not_applicable
    source_of_truth: stable | unknown | conflicted | not_applicable
    state_or_data_owner: stable | unknown | conflicted | not_applicable
    public_contract: stable | unknown | conflicted | not_applicable
    migration_rollout_boundary: stable | unknown | conflicted | not_applicable
    critical_invariants: stable | unknown | conflicted | not_applicable
  risk_profile: standard | high_impact | irreversible
  reviewer_requirements:
    initial_scope: full
    final_acceptance_scope: full
    dimensions: []
    independence_required: required
  provider_bindings:
    reviewers:
      - id: dbx-linus-review
        capability: strict_pragmatic_plan_review
    revision_provider:
      id: original_plan_author
  budget:
    initial_full_review_passes: 1
    local_revision_rounds: 2
    scoped_re_review_passes: 2
    final_acceptance_full_review_passes: 2
  modification_authority: plan_text_only
  may_modify_code: false
  stop_on:
    - needs-artifact
    - needs-review
    - needs-evidence
    - needs-decision
    - needs-alternatives
    - pivot-required
    - blocked-state-mismatch
    - blocked-insufficient-history
    - stopped-flat
    - stopped-oscillating
    - stopped-bloat
    - stopped-budget
```

`session-v1` is sufficient for same-session inline composition. Resume, persistence, multiple versions, or multiple reviewers require explicit versioning and preferably a fingerprint.

Before delegation, materialize the exact artifact bytes, declare its structured content ref, and compute `sha256:<64 lowercase hex>` under `exact-bytes-sha256`. Blank, placeholder, malformed, unknown-scheme, missing-ref, or unverifiable values stop at `needs-artifact`. Do not invent non-applicable anchors merely to fill the contract.

The final acceptance pass returns an identity-bound receipt:

```yaml
strict_acceptance_receipt:
  status: passed
  artifact_type: technical_plan
  artifact_version: ""
  artifact_fingerprint_scheme: exact-bytes-sha256
  artifact_fingerprint: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  artifact_content_ref:
    kind: current_context
    value: current_response
    plan: null
    tasks: null
  review_id: ""
  reviewer_capability: strict_pragmatic_plan_review
  scope: full
  independence: independent
  reviewed_after_last_revision: true
  open_blocker_high: 0
  review_judgment: accept | accept_with_advisories
  residual_findings: []
```

The receipt is invalid after any artifact content change. A scoped review cannot issue it.

## 7. Reviewer delegation

A delegated Linus review must be read-only and receive:

```yaml
delegated_review:
  parent_controller: dbx-plan-convergence
  originating_intent: ""
  completion_profile: handoff_ready | strict_acceptance
  review_id: ""
  reviewer_provider_id: ""
  reviewer_capability: ""
  reviewer_independence: independent | partially_independent | none | unknown
  artifact:
    type: technical_plan | implementation_plan_bundle | architecture_proposal | migration_plan | adr | implementation_proposal | data_model | diff
    version: ""
    fingerprint_scheme: null | exact-bytes-sha256 | plan-first-bundle-sha256-v1
    fingerprint: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    content_ref:
      kind: inline | path | current_context | file_bundle
      value: null
      plan: null
      tasks: null
  review_scope:
    kind: full | scoped
    contract_id: null
    accepted_finding_ids: []
    check_direct_regressions: false
    check_anchor_drift: false
    check_evidence_boundary: false
    check_scope_and_bloat: false
  requested_dimensions: []
  evidence_boundary: {}
  non_goals: []
  write_prohibition:
    modify_artifact: false
    modify_code: false
    commit: false
    push: false
```

The reviewer returns the human review plus `delegated_review_result`, containing the assigned review id, reviewer provider id/capability copied from the binding, exact artifact type/scheme/version/fingerprint/content refs, scope, independence, judgment, and per-finding `blocking` / `residual` / `decision_owner_required` fields. It does not output convergence `next_action`, `final_state`, revision contracts, receipts, or completion state.

The DBX adapter maps `S0/S1/S2/S3` to `blocker/high/medium/low` but consumes structured `judgment` and blocking fields without downgrading them. `accept_with_advisories` is valid only when every residual is reviewer-declared non-blocking; policy or risk-acceptance S2 remains blocking until its decision owner resolves it. Missing or ambiguous structured fields cannot issue a receipt.

A scoped re-review must bind the current artifact type/scheme/version/fingerprint/content refs and revision contract id. It checks only accepted finding closure, direct regressions, anchor/evidence drift, scope/bloat, and material direction changes. It does not reopen a full review for new nits.

## 8. Transition routing

| Plan Convergence result | Collection action |
| --- | --- |
| `ready-for-handoff` | Under `strict_acceptance`, proceed only with a current identity-bound receipt; under generic `handoff_ready`, proceed according to the caller's normal completion policy |
| `needs-artifact` | Route to the artifact provider; the convergence controller must not draft the missing artifact |
| `needs-review` | Obtain a review bound to the current artifact version |
| `needs-evidence` | Route to repository grounding/evidence provider, then resume |
| `needs-decision` | Route to the human decision owner, then resume |
| `needs-alternatives` | Route to a planner to produce bounded candidate directions |
| `pivot-required` | Close the old direction; wait for an externally supplied new direction |
| `stopped-flat` | Stop repeated wording/local patches and report no progress |
| `stopped-oscillating` | Stop direction flipping and require evidence/decision |
| `stopped-bloat` | Stop because mechanism/document growth exceeds information gain |
| `stopped-budget` | Stop unless the user explicitly grants another bounded budget |
| `blocked-state-mismatch` | Supply matching artifact/state or create fresh review/state |
| `blocked-insufficient-history` | Stop the diagnostic path and request enough comparable history, or start a fresh bounded invocation with a current artifact/review |

The collection must not convert handoff states into hidden autonomous work. Evidence, decisions, alternatives, and pivots remain explicit boundaries.

## 9. Human interruption policy

Normal path:

- one authorization for the composite planning workflow;
- planner creates the artifact;
- reviewer performs the initial full strict review;
- controller triages findings;
- local plan revision and scoped re-review happen without a human confirmation round;
- the current qualifying independent full review issues the strict acceptance receipt; after a revision this must be a fresh full review, or the workflow returns to its remaining bounded budget;
- human receives the final plan, major simplifications, evidence boundary, and residual risks.

Interrupt the human only when:

- goal/scope/non-goals would change;
- product, architecture, compatibility, or risk acceptance needs a decision;
- required repository evidence is unavailable or contradictory;
- the direction needs alternatives or pivot;
- permissions would expand;
- progress/complexity/budget gates stop the loop;
- an irreversible or external action is proposed.

Linus review may be default for every implementation-bound technical plan without making human review mandatory after every reviewer message.

## 10. High-impact plans

Do not increase rigor by blindly repeating the same reviewer.

Prefer:

- more relevant review dimensions;
- stronger repository evidence;
- explicit compatibility/migration validation;
- honest reviewer independence;
- a human checkpoint for irreversible or policy decisions.

Multiple reviewers or models that repeat the same lens do not create independent evidence.

## 11. Cross-model extension

Future cross-model review is a provider extension:

```yaml
reviews:
  - provider: dbx-linus-review
    model: model-a
    dimensions:
      - direction_model_ownership
      - complexity_proportionality
  - provider: independent-reviewer
    model: model-b
    dimensions:
      - compatibility_migration
```

`dbx-plan-convergence` should merge findings by root cause, evidence, impact, and anchors. Do not use majority voting.

Cross-model execution is not part of profile v1.

## 12. Future Auto boundary

The collection currently has no macro command layer. `/dbx-auto` is not implemented by this document.

A future thin Auto may own:

- direct vs technical-plan vs Plan-First classification;
- provider binding;
- transition routing;
- inherited permissions;
- exception escalation.

It must not own planning knowledge, Linus review criteria, convergence gates, code repair, or Plan-First state/seal rules.

Build it only after real tasks show that this profile reliably reduces human interventions without increasing false readiness or implementation rework.

## 13. Evaluation

Compare the current manual workflow with this profile on real tasks:

```text
A: technical plan -> human invokes Linus -> human requests revision -> human re-invokes review
B: technical plan -> plan convergence with Linus provider
```

Primary metric:

```text
Human Interventions per Accepted Implementation-Bound Plan
```

Guardrails:

- false `ready-for-handoff` rate;
- fresh full-review rejection rate for an unchanged artifact after strict acceptance;
- scope drift;
- missing validation;
- implementation rework caused by plan defects;
- full-review reopen rate after local revision;
- evidence/decision/pivot misclassification;
- token, runtime, and document growth.

Use at least five real tasks before deciding whether a command or new meta-skill is justified.

## 14. Non-goals

This profile does not:

- force every code change to create a technical plan;
- silently activate from ordinary planning requests;
- modify code during plan convergence;
- add a Plan-First phase;
- generalize showhand;
- gather evidence inside the controller;
- replace decision owners;
- generate pivot directions inside the controller;
- implement cross-model voting;
- commit, push, merge, deploy, or perform external writes.
