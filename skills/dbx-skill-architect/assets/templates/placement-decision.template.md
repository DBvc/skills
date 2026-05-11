# Placement Decision

Use this before adding a new control to a skill package.

```yaml
placement_decision:
  proposed_control: ""
  failure_it_targets: ""
  candidate_locations:
    - SKILL.md
    - references/
    - scripts/
    - assets/
    - evals/
    - repo_memory
    - command
    - hook
    - global_instruction
    - routing_matrix
  chosen_location: ""
  reason: ""
  rejected_locations:
    - location: ""
      reason: ""
  added_cost:
    - context
    - maintenance
    - runtime
    - safety
  validation_signal: ""
  rollback_condition: ""
```
