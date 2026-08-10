# Handoff Contracts

A good technical plan should make the next step obvious. Use these contracts when handing off to another DBX skill or to an implementer.

## Handoff to implementation

Use when the plan is bounded and ready.

```yaml
implementation_handoff:
  status: ready
  goal: ""
  non_goals: []
  allowed_scope: []
  forbidden_scope: []
  source_of_truth: []
  invariants: []
  task_slices: []
  validation_required: []
  stop_conditions: []
  review_focus: []
```

Rules:

- Include only implementation-ready slices.
- Do not hand off unresolved architecture decisions as coding tasks.
- State validation and stop conditions per slice when possible.

## Handoff to `dbx-linus-review`

Use when the plan changes modeling, ownership, compatibility, public contracts, cache/state lifetime, architecture, or migration strategy.

```yaml
linus_review_handoff:
  status: needs_strict_review
  plan_summary: ""
  selected_model: ""
  alternatives_considered: []
  source_of_truth: []
  invariants: []
  highest_risk: ""
  suspicious_complexity: []
  compatibility_risks: []
  questions_for_review: []
```

Ask the reviewer to judge whether the plan is real simplification or abstraction fog.

## Handoff to `dbx-plan-convergence`

Use when a generated technical plan is intended to guide implementation and should receive bounded convergence before coding.

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

Rules:

- `session-v1` is acceptable for same-session inline composition. Resume, persistence, multiple artifact versions, or multiple reviewers require an explicit version and preferably a fingerprint.
- Before delegation, the parent workflow must materialize the exact plan bytes, compute `sha256:<64 lowercase hex>` under `exact-bytes-sha256`, and fill the identity plus structured content ref. Blank, placeholder, malformed, unknown-scheme, missing-ref, or unverifiable values are not a valid handoff.
- Generic plan convergence defaults to `completion_profile: handoff_ready`. This implementation-bound technical-plan handoff must request `strict_acceptance`.
- The handoff binds `dbx-linus-review` for the DBX collection path and declares required dimensions; the generic controller remains provider-agnostic.
- An unchanged initial independent full review may qualify for strict acceptance. After any local revision and scoped closure, strict acceptance requires a fresh independent full review bound to the final artifact identity.
- `ready-for-handoff` under this profile requires a current `strict_acceptance_receipt`. A failed final review returns to bounded triage/revision while budget remains; otherwise it stops without claiming acceptance.
- This handoff does not authorize code modification.
- Do not populate anchors that are not applicable merely to satisfy the template.

## Handoff to `dbx-diff-review`

Use when a concrete implementation exists.

```yaml
diff_review_handoff:
  status: implemented_needs_review
  original_plan_goal: ""
  expected_changed_surfaces: []
  invariants_to_check: []
  validation_expected: []
  known_residual_risks: []
  review_focus: []
```

Do not continue plan speculation when there is a real diff to inspect.

## Handoff to `dbx-code-ratchet`

Use only when the user explicitly asks for bounded repair and code modification is allowed.

```yaml
ratchet_handoff:
  status: eligible_for_bounded_repair | not_eligible
  review_findings_available: true | false
  local_fixable_scope: []
  forbidden_scope: []
  validation_required: []
  stop_conditions: []
```

Rules:

- One writer at a time.
- Repair must be local and bounded.
- Direction failures should stop, not patch around architecture trouble.

## Handoff to `dbx-software-plan-first-*`

Use when the user wants a persistent, review-gated workflow with plan files.

```yaml
plan_first_handoff:
  status: promote_to_stateful_plan_first
  recommended_phase: plan_issue | ground_plan | finalize_plan | implement_feature | showhand
  reason: ""
  current_plan_summary: ""
  evidence_needed_before_seal: []
  candidate_tasks: []
```

Rules:

- Do not write `.plan-first` files from this skill.
- Do not invent a workflow seal.
- Promote only when persistent state reduces risk or repeated work.

## Handoff back to product, design, or decision

Use when technical planning is premature.

```yaml
upstream_handoff:
  status: needs_product_design_or_decision
  blocking_question: ""
  why_it_blocks_technical_plan: ""
  suggested_skill: dbx-decision-framing | dbx-product-judgment | dbx-design-judgment
```

Examples:

- Product behavior is undecided.
- UI flow is not settled.
- Architecture direction depends on go/no-go or trade-off choice.
- Compatibility policy requires human or team decision.
