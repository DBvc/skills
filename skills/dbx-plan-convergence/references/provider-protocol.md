# Provider Protocol

The controller composes by protocol, not by provider name.

## 1. Artifact provider

Produces or supplies the current plan artifact.

```yaml
artifact:
  type: ""
  version: ""
  fingerprint_scheme: null
  fingerprint: ""
  content_ref:
    kind: inline | path | current_context | file_bundle | null
    value: null
    plan: null
    tasks: null
  content_location: ""
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
```

### Identity rules

- `version` is required for persisted state, resume, multiple artifact versions, or multiple review passes.
- `fingerprint` is optional but recommended when the host can compute a stable content hash or content id.
- `strict_acceptance` requires the controller or artifact provider to hash the exact artifact bytes before review and declare a recognized scheme. A single artifact must use a readable `content_ref.kind: path` plus `exact-bytes-sha256`; an implementation bundle must use `file_bundle` plus the scheme below. `inline`, `current_context`, placeholders, malformed values, unknown schemes, unreadable paths, or values that cannot be recomputed fail as `obtain-artifact + needs-artifact`. They remain valid location forms for ordinary `handoff_ready` when its weaker identity rules are satisfied.
- `content_ref` is the canonical location contract. `content_location` is retained only for older v2 state and ordinary single-artifact compatibility; do not use it to infer a file bundle.
- In a single ephemeral turn, when artifact and its review are supplied together with no ambiguity, the controller may assign a session-local version such as `session-v1`.
- Do not claim a review applies to a changed artifact merely because the title is the same.

For `type: implementation_plan_bundle`, `fingerprint_scheme` must be `plan-first-bundle-sha256-v1` and `content_ref` must use `kind: file_bundle` with non-empty `plan` and `tasks` paths. Compute lowercase SHA-256 for those exact files, serialize their hashes with `json.dumps(files, ensure_ascii=True, sort_keys=True, separators=(",", ":"))`, UTF-8 encode that one-line JSON, and SHA-256 those bytes. The producer, controller, and reviewer preserve the same refs and scheme; a missing ref or unrecognized scheme returns `obtain-artifact + needs-artifact` before review.

## 2. Reviewer provider

Finds material problems. It does not decide whether the convergence loop continues.

Preferred review envelope:

```yaml
review_pass:
  id: "R1"
  artifact_type: ""
  artifact_version: "v1"
  artifact_fingerprint_scheme: null
  artifact_fingerprint: ""
  artifact_content_ref:
    kind: inline | path | current_context | file_bundle | null
    value: null
    plan: null
    tasks: null
  judgment: accept | accept_with_advisories | changes_required | reject | insufficient_evidence | null
  provider:
    id: ""
    type: human | agent | skill | tool | unknown
    capability: null | string
    independence: independent | partially_independent | none | unknown
  dimensions:
    - direction_model_ownership
  scope:
    kind: full | scoped
    contract_id: null | string
    accepted_finding_ids: []
    check_direct_regressions: false
    check_anchor_drift: false
    check_evidence_boundary: false
    check_scope_and_bloat: false
  parse_confidence: high | medium | low
  findings:
    - id: "F-001"
      source_review_id: "R1"
      severity: blocker | high | medium | low
      blocking: true | false
      residual: true | false
      decision_owner_required: true | false
      category: model | ownership | source_of_truth | compatibility | migration | validation | operability | complexity | evidence | decision | other
      evidence: ""
      impact: ""
      confidence: high | medium | low
      local_revision_signal: true | false | unknown
      evidence_gap_signal: true | false | unknown
      decision_gap_signal: true | false | unknown
      direction_failure_signal: true | false | unknown
      scope_expansion_signal: true | false | unknown
      verification_hint: ""
```

Signals are inputs to controller triage, not controller decisions.

Human-readable review remains acceptable. The controller wraps it in a review pass, assigns ids, records `parse_confidence`, and binds it to the artifact version it demonstrably reviewed. Ordinary reviewers do not need to emit this schema unless convergence is requested.

For `judgment`, consume the reviewer's explicit structured result when available. Clear approval with no finding is `accept`; `accept_with_advisories` requires every residual finding to be explicitly `blocking: false`; any blocking finding requires `changes_required`, `reject`, or `insufficient_evidence` as appropriate. Ambiguous wording remains `null` and cannot qualify for strict acceptance. The controller may map severity labels, but may not infer non-blocking status or accept risk.

### Stale review rule

A review is applicable only when one of these is true:

1. type, version, available fingerprint scheme/fingerprint, and structured content ref match the current artifact;
2. the review and artifact are supplied together in the same unambiguous context;
3. an external actor explicitly proves that changes since the review cannot affect its findings.

Otherwise choose:

```yaml
transition:
  next_action: obtain-review
  final_state: needs-review
```

Do not transplant old findings onto a new plan by intuition.

## 3. Evidence provider

Supplies facts that can change the plan.

```yaml
evidence_item:
  id: "E-001"
  source: repo | documentation | test | log | measurement | stakeholder | other
  observation: ""
  supports_or_refutes: []
  freshness: ""
  confidence: high | medium | low
  limitation: ""
```

Keep observed facts separate from assumptions and judgments. Evidence providers do not choose product or architecture policy.

## 4. Decision owner

Closes a branch that controller and reviewer are not authorized to choose.

```yaml
decision:
  id: "D-001"
  question: ""
  choice: ""
  rationale: ""
  rejected_alternatives: []
  constraints_created: []
  owner: ""
  date: ""
```

## 5. Revision provider

Receives only the revision contract plus the smallest necessary artifact context.

```yaml
revision_result:
  contract_id: "RC-E1-R1"
  artifact_type: "technical_plan"
  artifact_fingerprint_scheme: exact-bytes-sha256
  artifact_content_ref:
    kind: inline | path | current_context | file_bundle
    value: ""
    plan: null
    tasks: null
  artifact_version_before: "v1"
  artifact_fingerprint_before: ""
  artifact_version_after: "v2"
  artifact_fingerprint_after: ""
  accepted_findings_addressed: []
  changes_made: []
  assumptions_preserved: []
  could_not_complete: []
  scope_expanded: false
  anchor_changed: false
```

The reviser must preserve the contract's artifact type, fingerprint scheme, and content refs, then recompute the exact after-version/fingerprint. For `implementation_plan_bundle`, both `plan` and `tasks` refs are required and the provider recomputes `plan-first-bundle-sha256-v1` after modifying either file. Missing or changed ownership fields fail as `obtain-artifact + needs-artifact`. The reviser must stop rather than silently change direction, invent facts, resolve deferred findings, or broaden scope.

## 6. Per-review independence

Independence belongs to each review pass, not the global convergence state.

- `independent`: reviewer did not receive the author's hidden reasoning or prior reviewer conclusion;
- `partially_independent`: separate role or context, but shares some history;
- `none`: same context performs author and reviewer roles;
- `unknown`.

Do not claim independence merely because the same model used a different prompt. Different models do not automatically provide independent evidence either; shared assumptions and lenses still matter.

## 7. Review dimensions

Review breadth is about distinct risk surfaces, not reviewer count.

Common dimensions:

- direction, model, ownership, source of truth;
- compatibility, migration, rollout, rollback;
- validation, operability, observability, failure containment;
- security, privacy, identity, authorization;
- performance and capacity, only when material;
- implementation slicing, sequencing, and reversibility.

A single reviewer may cover multiple dimensions. Multiple reviewers repeating the same lens still count as one dimension.

## 8. Scoped re-review

A scoped review must bind to the revised artifact and reference the revision contract. `scope.contract_id` is required when `kind: scoped`. For a full review it may be omitted or `null`; the blank template serializes it as `null`:

```yaml
review_pass:
  id: "R2"
  artifact_type: ""
  artifact_version: "v2"
  artifact_fingerprint_scheme: null
  artifact_fingerprint: ""
  artifact_content_ref:
    kind: inline | path | current_context | file_bundle | null
    value: null
    plan: null
    tasks: null
  scope:
    kind: scoped
    contract_id: "RC-E1-R1"
    accepted_finding_ids:
      - "F-001"
    check_direct_regressions: true
    check_anchor_drift: true
    check_evidence_boundary: true
    check_scope_and_bloat: true
```

A re-review of v1 is not evidence that v2 closed the finding.

A scoped re-review can close accepted findings, but cannot issue strict acceptance. It must preserve the current structured content ref; bundle re-review cannot collapse two file refs into a directory or scalar path.

## 9. Final strict acceptance review

This section applies only when `completion_profile: strict_acceptance`.

A qualifying acceptance review must:

- receive a readable `content_ref.kind: path` for a single artifact, or a complete `file_bundle` for `implementation_plan_bundle`; `inline` and `current_context` are not qualifying strict-acceptance refs;
- use `scope.kind: full` and bind the current artifact type, recognized fingerprint scheme, version, structured content ref, and a recomputed fingerprint matching `^sha256:[0-9a-f]{64}$`;
- occur after the last artifact revision;
- use an `independent` reviewer pass;
- bind `review_pass.provider.id` to exactly one `provider_bindings.reviewers` entry and copy that entry's non-empty `capability` into `review_pass.provider.capability`; do not infer capability from a provider or skill name;
- receive only the current artifact, scope, evidence boundary, non-goals, and requested dimensions—not author hidden reasoning or prior reviewer conclusions;
- report `judgment: accept` or `accept_with_advisories` with no open `blocker` or `high` findings;
- either close each `medium` finding or have the reviewer explicitly retain it as a non-blocking residual finding. If it involves product, architecture, compatibility, or risk acceptance, the decision owner must also resolve it. The controller cannot downgrade severity or accept risk itself.

If the initial full review meets these rules and the artifact never changes, it may qualify without a duplicate review. Any artifact content change invalidates the prior acceptance basis and receipt. After a revision, scoped closure is followed by a fresh independent full review only when the artifact is again a completion candidate.

On success, issue:

```yaml
strict_acceptance_receipt:
  status: passed
  artifact_type: "technical_plan"
  artifact_version: "v3"
  artifact_fingerprint_scheme: exact-bytes-sha256
  artifact_fingerprint: "sha256:052e5fbfda6765a4d836a00d367fe2d7abb2967f72e72cdc69fdfdea28958c5b"
  artifact_content_ref:
    kind: path
    value: skills/dbx-plan-convergence/evals/fixtures/plan.md
    plan: null
    tasks: null
  review_id: "R-final-2"
  reviewer_capability: "strict_pragmatic_plan_review"
  scope: full
  independence: independent
  reviewed_after_last_revision: true
  open_blocker_high: 0
  review_judgment: accept | accept_with_advisories
  residual_findings: []
```

If the review finds new material problems, send them through normal triage. If the final-acceptance review budget is exhausted before success, choose `stop + stopped-budget`; never preserve an earlier PASS.

## 10. Provider bindings and delegated activation

A parent workflow may bind providers without changing controller semantics:

```yaml
provider_bindings:
  artifact_provider: null
  reviewers:
    - id: "dbx-linus-review"
      capability: "strict_pragmatic_plan_review"
  revision_provider: null
  evidence_provider: null
  decision_owner: null
  parent_workflow: null
```

Bindings identify who can perform a role. They do not import that provider's domain rubric into the controller.

For `strict_acceptance`, the review pass must identify one bound reviewer and carry that exact binding's capability. The receipt copies the same value. Missing, empty, ambiguous, or mismatched provider/capability provenance returns `obtain-review + needs-review` and cannot issue a passed receipt.

## 11. Adapter rules

The controller must work when:

- only a plan and plain-text review are provided;
- reviewer uses another schema;
- a human supplies decisions inline;
- evidence arrives after a paused round;
- one provider is unavailable;
- all roles run sequentially in one session;
- multiple reviewers assessed different artifact versions.

Missing providers change the transition or confidence. They do not justify inventing evidence or decisions.

## 12. No hidden coupling

Do not:

- require a particular skill name;
- assume a particular host feature;
- hard-code a model version;
- require a particular file format;
- make ordinary providers emit convergence schema outside convergence workflows;
- place provider-specific review knowledge inside controller;
- use reviewer voting as a substitute for evidence or decision ownership.

Collection-level commands, routing rules, or parent workflows may choose local providers. Those choices stay outside this runtime skill.
