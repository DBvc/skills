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
-> dbx-plan-convergence(mode=bounded_loop)
     -> reviewer: dbx-linus-review(plan_strict, full)
     -> reviser: original plan author
     -> optional scoped re-review
-> ready-for-handoff
-> implementation
```

Default budget:

```yaml
budget:
  full_review_passes: 1
  local_revision_rounds: 1
  scoped_re_review_passes: 1
```

The full review is default whenever a technical plan is intended for implementation. A second full review is not default. After a bounded local revision, re-review only the accepted findings, direct regressions, anchor drift, evidence-boundary drift, scope growth, and bloat.

### 4.3 Software Plan-First

```text
dbx-software-plan-first-plan-issue      # when proposal decisions are incomplete
-> dbx-software-plan-first-ground-plan  # when repository facts are needed
-> external dbx-plan-convergence gate   # when this profile is explicitly selected
-> dbx-software-plan-first-finalize-plan
-> seal
-> implement-feature or showhand
```

The external convergence gate is not a new Plan-First phase. It does not change manual-only phase activation, the seal format, implementation scripts, or showhand semantics.

When a parent workflow selects this profile, `finalize-plan` should require a current `ready-for-handoff` result bound to the proposal version/fingerprint.

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

reviewer:
  capability: strict_pragmatic_plan_review
  preferred_dbx_skill: dbx-linus-review
  artifact_mode: plan_strict
  initial_scope: full
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
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | implementation_proposal
    version: session-v1
    fingerprint: null
    content_ref: inline | path | current_response
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
    dimensions: []
    independence_required: none | preferred | required
  provider_requirements:
    reviewer_role: strict_pragmatic_plan_reviewer
    reviser_role: original_plan_author
  budget:
    full_review_passes: 1
    local_revision_rounds: 1
    scoped_re_review_passes: 1
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

Do not invent non-applicable anchors merely to fill the contract.

## 7. Reviewer delegation

A delegated Linus review must be read-only and receive:

```yaml
delegated_review:
  parent_controller: dbx-plan-convergence
  originating_intent: ""
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | adr | implementation_proposal | data_model | diff
    version: ""
    fingerprint: null
    content_ref: inline | path | current_context
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

The reviewer returns findings, severity, evidence, impact, fix direction, confidence, and relevant direction/complexity judgment. It does not output convergence `next_action`, `final_state`, revision contracts, or completion state.

A scoped re-review must bind the current artifact version and revision contract id. It checks only accepted finding closure, direct regressions, anchor/evidence drift, scope/bloat, and material direction changes. It does not reopen a full review for new nits.

## 8. Transition routing

| Plan Convergence result | Collection action |
| --- | --- |
| `ready-for-handoff` | Proceed to implementation or Plan-First finalize/seal |
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
- reviewer performs full strict review;
- controller triages findings;
- local plan revision and scoped re-review happen without a human confirmation round;
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
