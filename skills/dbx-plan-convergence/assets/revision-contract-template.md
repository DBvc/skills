# Revision Contract Template

```yaml
revision_contract:
  id: "RC-E1-R1"
  convergence_run_id: ""
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | adr | implementation_proposal | other
    version_before: ""
    fingerprint_before: ""
    version_after_expected: ""
  source_reviews:
    - review_id: "R1"
      artifact_version: ""
      artifact_fingerprint: ""
  epoch:
    id: "E1"
    direction_summary: ""
  round: 1
  purpose: ""
  accepted_findings:
    - id: "F-001"
      source_review_id: "R1"
      type: local_revision | validation_gap
      evidence: ""
      impact: ""
      required_change: ""
      verification_hint: ""
  frozen_anchors:
    - name: goal
      value: ""
      status: stable
    - name: source_of_truth
      value: ""
      status: stable
  allowed_changes: []
  forbidden_changes:
    - change_core_direction_without_new_evidence_or_decision
    - invent_repo_or_runtime_facts
    - expand_scope_without_controller_approval
    - resolve_deferred_findings
    - add_defensive_prose_without_actionability_gain
    - weaken_validation_or_applicable_rollout_rollback_containment
    - apply_findings_from_a_stale_review
  facts_to_preserve: []
  assumptions_to_keep_explicit: []
  required_validation_updates: []
  re_review_scope:
    contract_id: "RC-E1-R1"
    artifact_version_after: ""
    artifact_fingerprint_after: ""
    accepted_finding_ids: []
    check_direct_regressions: true
    check_anchor_drift: true
    check_evidence_boundary: true
    check_scope_and_bloat: true
  stop_if:
    - minimal_local_revision_not_possible
    - direction_change_required
    - new_material_decision_required
    - new_external_evidence_required
    - scope_expansion_required
    - artifact_identity_cannot_be_established
```
