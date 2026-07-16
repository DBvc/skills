# Provider Protocol

The controller composes by protocol, not by provider name.

## 1. Artifact provider

Produces or supplies the current plan artifact.

```yaml
artifact:
  type: ""
  version: ""
  fingerprint: ""
  content_location: ""
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
```

### Identity rules

- `version` is required for persisted state, resume, multiple artifact versions, or multiple review passes.
- `fingerprint` is optional but recommended when the host can compute a stable content hash or content id.
- In a single ephemeral turn, when artifact and its review are supplied together with no ambiguity, the controller may assign a session-local version such as `session-v1`.
- Do not claim a review applies to a changed artifact merely because the title is the same.

## 2. Reviewer provider

Finds material problems. It does not decide whether the convergence loop continues.

Preferred review envelope:

```yaml
review_pass:
  id: "R1"
  artifact_version: "v1"
  artifact_fingerprint: ""
  provider:
    id: ""
    type: human | agent | skill | tool | unknown
    independence: independent | partially_independent | none | unknown
  dimensions:
    - direction_model_ownership
  scope:
    kind: full | scoped
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

### Stale review rule

A review is applicable only when one of these is true:

1. version and available fingerprint match the current artifact;
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

The reviser must stop rather than silently change direction, invent facts, resolve deferred findings, or broaden scope.

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

A scoped review must bind to the revised artifact and reference the revision contract:

```yaml
review_pass:
  id: "R2"
  artifact_version: "v2"
  artifact_fingerprint: ""
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

## 9. Provider bindings and delegated activation

A parent workflow may bind providers without changing controller semantics:

```yaml
provider_bindings:
  artifact_provider: null
  reviewers: []
  revision_provider: null
  evidence_provider: null
  decision_owner: null
  parent_workflow: null
```

Bindings identify who can perform a role. They do not import that provider's domain rubric into the controller.

## 10. Adapter rules

The controller must work when:

- only a plan and plain-text review are provided;
- reviewer uses another schema;
- a human supplies decisions inline;
- evidence arrives after a paused round;
- one provider is unavailable;
- all roles run sequentially in one session;
- multiple reviewers assessed different artifact versions.

Missing providers change the transition or confidence. They do not justify inventing evidence or decisions.

## 11. No hidden coupling

Do not:

- require a particular skill name;
- assume a particular host feature;
- hard-code a model version;
- require a particular file format;
- make ordinary providers emit convergence schema outside convergence workflows;
- place provider-specific review knowledge inside controller;
- use reviewer voting as a substitute for evidence or decision ownership.

Collection-level commands, routing rules, or parent workflows may choose local providers. Those choices stay outside this runtime skill.
