# Patch Hypothesis

Use this before non-trivial skill changes.

```yaml
patch_hypothesis:
  target_skill: ""
  change_type: repo_architecture | architect_skill | individual_skill
  target_failure:
    - ""
  proposed_change: ""
  expected_benefit:
    - ""
  expected_cost:
    - ""
  affected_files:
    - ""
  evals_to_add_or_update:
    - ""
  validation_plan:
    - ""
  regression_risk:
    - ""
  rollback_condition:
    - ""
```

## Review Questions

1. What specific failure does this patch reduce?
2. Does the patch add context cost, tool dependency, or user-visible ceremony?
3. What old behavior must not regress?
4. What eval or manual check would falsify the improvement claim?
5. Can this be a smaller patch?
