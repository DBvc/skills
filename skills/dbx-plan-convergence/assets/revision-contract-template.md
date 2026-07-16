# Revision Contract Template

```yaml
revision_contract:
  convergence_run_id: ""
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | adr | implementation_proposal | other
    version_before: ""
    version_after_expected: ""
  epoch:
    id: "E1"
    direction_summary: ""
  round: 1
  purpose: ""
  accepted_findings:
    - id: "F-001"
      type: local_revision | validation_gap
      evidence: ""
      impact: ""
      required_change: ""
      verification_hint: ""
  frozen_anchors:
    - name: goal
      value: ""
    - name: source_of_truth
      value: ""
  allowed_changes: []
  forbidden_changes:
    - change_core_direction_without_new_evidence_or_decision
    - invent_repo_or_runtime_facts
    - expand_scope_without_controller_approval
    - resolve_deferred_findings
    - add_defensive_prose_without_actionability_gain
    - weaken_validation_rollout_or_rollback
  facts_to_preserve: []
  assumptions_to_keep_explicit: []
  required_validation_updates: []
  re_review_scope:
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
```
