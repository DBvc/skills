# Repair Contract Template

```yaml
repair_contract:
  ratchet_run_id: ""
  target:
    source: staged | unstaged | local | branch | commit_range | selected_files | pasted_patch
    included_files: []
    out_of_scope_dirty_files: []
  accepted_findings:
    - id: F-001
      severity: S1
      title: ""
      evidence: ""
      impact: ""
      required_fix: ""
      verification_hint: ""
  forbidden_findings: []
  allowed_files: []
  forbidden_files: []
  allowed_change_types:
    - local_correctness_fix
    - focused_regression_test
  forbidden_change_types:
    - new_dependency_without_user_approval
    - public_api_change_without_user_approval
    - schema_or_migration_without_user_approval
    - unrelated_cleanup
    - deferred_finding_fix
    - test_deletion_or_weakening
    - broad_refactor
  stop_if_minimal_fix_not_possible: true
```
