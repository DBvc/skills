# Progress and Stop Gates

## 1. Progress is not document delta

A revision is useful only when it changes the decision or execution state.

### Strong progress credits

- A material unknown becomes a fact with source.
- A decision owner resolves a branch.
- A blocker is removed without introducing an equal or larger blocker.
- The implementation path becomes smaller, more reversible, or easier to validate.
- Risk-to-validation mapping gains a missing critical path.
- Rollout, rollback, containment, or observability becomes executable.
- A bad direction is rejected with evidence and does not remain as an ambiguous fallback.

### Weak or zero progress

- More prose, diagrams, headings, or alternatives with no decision effect.
- Review comments copied into the plan as disclaimers.
- A finding is “addressed” only by saying it will be considered during implementation.
- The same reviewer rephrases the same concern.
- A new abstraction, adapter, flag, or compatibility layer hides a direction problem.
- Unknown facts are replaced by confident wording.

## 2. Flat gate

Stop as `stopped-flat` after one round without a strong progress credit.

Typical signs:

```yaml
blockers_after: same_as_before
material_unknowns_after: same_as_before
decisions_resolved: 0
new_external_evidence: 0
actionability_delta: none
document_size_delta: positive
```

Do not spend another round hoping wording will turn into evidence.

## 3. Oscillation gate

Stop as `stopped-oscillating` when:

- the same core anchor flips twice without new evidence or decision;
- a rejected direction returns only because a reviewer changed wording;
- findings repeatedly close and reopen around the same root cause;
- each round changes the architecture shape but not the constraints;
- the author and reviewer trade incompatible preferences without an owner or experiment.

Resolution requires one of:

- new evidence;
- explicit decision ownership;
- a reversible experiment;
- a smaller scope;
- acceptance of residual risk.

## 4. Bloat gate

Stop as `stopped-bloat` when added complexity exceeds added certainty.

Watch signals:

- more layers, adapters, caches, flags, synchronization paths, compatibility branches, or configuration;
- more implementation slices but weaker ownership;
- more alternatives without a decision rule;
- larger validation matrix caused by accidental design complexity;
- repeated “future-proofing” without a concrete requirement;
- plan length grows while blocker and unknown counts do not fall.

Bloat is a direction signal, not a formatting complaint.

## 5. Direction gate

Classify as `direction_failure` when multiple findings share a root cause in:

- wrong source of truth;
- wrong state or data owner;
- wrong identity or lifecycle boundary;
- wrong public contract;
- wrong migration or compatibility model;
- invented problem or disproportionate solution;
- architecture that only works by adding many synchronization or exception paths.

Do not generate a local revision contract for a direction failure.

## 6. Evidence and decision gates

Use `needs-evidence` when a fact could flip the plan.

Examples:

- actual framework or runtime version;
- existing owner or source of truth;
- real call sites or data volume;
- compatibility consumers;
- current tests, CI, operational constraints;
- measured performance or reliability characteristics.

Use `needs-decision` when the missing item is not discoverable as fact.

Examples:

- breaking versus backward-compatible API;
- migration window;
- acceptable risk and rollback threshold;
- product semantics;
- ownership boundary;
- rollout order or support policy.

## 7. Scoped re-review

After a local revision, re-review only:

1. accepted finding closure;
2. direct regressions;
3. core anchor drift;
4. evidence boundary drift;
5. scope and bloat.

A full re-review is justified only when the revision materially changed direction, scope, contract, ownership, migration, or validation topology. In that case the controller should usually open a new epoch rather than pretending it was local.

## 8. Ready gate

`ready-for-handoff` requires:

```yaml
direction_failures_open: 0
material_decision_gaps_open: 0
plan_flipping_evidence_gaps_open: 0
core_anchors: stable
implementation_path: actionable
critical_risks_mapped_to_validation: true
rollout_rollback_or_containment: adequate_for_profile
residual_risks_explicit: true
flat_signal: false
oscillation_signal: false
bloat_signal: false
```

Ready is relative to the evidence boundary. It is not proof that implementation will succeed.
