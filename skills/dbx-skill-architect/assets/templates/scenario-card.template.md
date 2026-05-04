# Scenario Card

## Basic scenario

```text
Scenario name:
Primary user:
Context of use:
Real job to be done:
Typical inputs:
Expected outputs:
Recurring failure modes:
Evidence sources:
Hard constraints:
Non-goals:
Success criteria:
```

## Hard gates

```yaml
hard_gates:
  repeatability: pass | fail | unknown
  stable_job: pass | fail | unknown
  evaluability: pass | fail | unknown
  safety_legitimacy: pass | fail | unknown
```

## Domain substance gates

Use for domain/content skills.

```yaml
domain_substance_gates:
  target_user_defined: pass | fail | unknown | not_applicable
  output_depth_defined: pass | fail | unknown | not_applicable
  domain_variables_identified: pass | fail | unknown | not_applicable
  data_source_policy_defined: pass | fail | unknown | not_applicable
  failure_knowledge_identified: pass | fail | unknown | not_applicable
  expert_quality_rubric_defined: pass | fail | unknown | not_applicable
  worked_example_available: pass | fail | unknown | not_applicable
```

## Domain content contract

```yaml
domain_content_contract:
  target_user: ""
  artifact_type: ""
  output_depth: "quick | standard | deep | operational"
  required_variables: []
  hidden_failure_modes: []
  expert_quality_checks: []
  data_source_policy:
    realtime_required: []
    user_provided_required: []
    can_estimate_with_label: []
    must_not_fabricate: []
  uncertainty_policy: []
  must_not_omit: []
  worked_examples_needed: []
  domain_eval_cases: []
```
