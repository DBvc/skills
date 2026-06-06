# Direction Gate

The direction gate prevents the loop from treating every review finding as a todo item.

## Stop when symptoms share a root cause

Examples:

```text
F-001 logout cache is stale
F-002 user switch sees old permission state
F-003 permission downgrade needs manual invalidation
```

This may be one wrong state owner, not three local bugs. Stop and escalate before adding more cache invalidation branches.

## Stop when local repairs grow the model

Stop if the minimal repair wants to add:

- new dependency
- new public API
- schema or migration
- new cross-module state owner
- broad adapter layer
- global mutable state
- generalized abstraction with one implementation
- feature flag or config to hide uncertain behavior
- performance optimization without measurement

## Stop when repair makes more problems

Stop with `stopped-diverging` if after repair:

- new S0/S1 appears
- risk score does not decrease
- accepted findings remain open and complexity increases
- validation gets worse
- S2 count increases more than accepted S2 count decreases
- changed file set expands outside the repair contract

## Continue only on monotonic movement

A safe ratchet step should satisfy most of these:

```yaml
risk_score_after < risk_score_before
accepted_open_findings_after < accepted_open_findings_before
new_s0_or_s1: false
scope_expanded: false
complexity_budget_exceeded: false
validation_worse: false
direction_health: ok
```

If two rounds are not enough, the likely missing ingredient is direction judgment, not a third turn of patching paint onto wet concrete.
