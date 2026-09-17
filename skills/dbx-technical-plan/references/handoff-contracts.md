# Handoff Contracts

A good technical plan should make the next step obvious. Use these contracts when handing off to another DBX skill or to an implementer.

## Handoff to implementation

Use when the plan is bounded and ready.

```yaml
implementation_handoff:
  status: pending_preflight
  next_action: implementation
  readiness_target: implementation_ready
  completion:
    document_status: accepted
    implementation_status: pending_preflight
    first_executable_slice: ""
    execution_authority: not_assessed | authorized | not_authorized
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

- Include only slices that are technically concrete enough for bounded implementation preflight.
- Do not hand off unresolved architecture decisions as coding tasks.
- State validation and stop conditions per slice when possible.
- `pending_preflight` means the plan has an executable first slice but repository/worktree/permission checks still belong to the implementer. Preflight is not another plan-review round.
- After preflight passes, the implementer may set `implementation_status: ready`; only current user or parent authority may set `execution_authority: authorized`.
- Preserve an explicit originating request to implement the feature as `execution_authority: authorized`. If preflight passes, the authorized parent/implementer continues with the first slice in the same task; do not ask the user to authorize the same code work again or route back to plan review.
- A bounded preflight checks only current repository/worktree/permission facts needed to enter the named first slice. It is not a reason to reopen general plan review.

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

Use only for an explicit standalone convergence/gate request. Follow that skill's current input contract; do not allocate or preserve its state here.

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
