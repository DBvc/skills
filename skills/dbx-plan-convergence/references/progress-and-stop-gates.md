# Progress and Stop Gates

## 1. Review applicability gate

Before triage, verify that each review pass applies to the current artifact.

Pass when:

- artifact version matches;
- fingerprint matches when both are present;
- or the artifact and review were supplied together in an unambiguous single-turn context.

Stop or hand off when:

- review targets an older known version;
- current artifact changed after review and affected scope is unknown;
- resume state names a different artifact version/fingerprint;
- scoped re-review inspected the pre-revision artifact.

Transitions:

```yaml
stale_review:
  next_action: obtain-review
  final_state: needs-review

resume_identity_mismatch:
  next_action: stop
  final_state: blocked-state-mismatch
```

A stale review is not low-confidence review. It is inapplicable evidence.

## 2. Progress is not document delta

A revision is useful only when it changes decision or execution state.

### Strong progress credits

- A material unknown becomes a sourced fact.
- A decision owner resolves a branch.
- A blocker is removed without introducing an equal or larger blocker.
- The implementation path becomes smaller, more reversible, or easier to validate.
- Risk-to-validation mapping gains a missing critical path.
- Applicable rollout, rollback, containment, or observability becomes executable.
- A bad direction is rejected with evidence and no longer remains as ambiguous fallback.
- A missing review dimension is covered against the current artifact version.

### Weak or zero progress

- More prose, diagrams, headings, or alternatives with no decision effect.
- Review comments copied into the plan as disclaimers.
- A finding is “addressed” only by saying it will be considered during implementation.
- Same reviewer rephrases the same concern.
- A new abstraction, adapter, flag, or compatibility layer hides a direction problem.
- Unknown facts are replaced by confident wording.
- Review is repeated against the wrong artifact version.

## 3. Flat gate

Stop as `stopped-flat` after one revision transition without a strong progress credit.

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

Flat diagnosis requires at least a before and after state. One isolated artifact is insufficient.

## 4. Oscillation gate

Stop as `stopped-oscillating` when:

- the same core anchor flips twice without new evidence or decision;
- a rejected direction returns only because a reviewer changed wording;
- findings repeatedly close and reopen around the same root cause;
- each round changes architecture shape but not constraints;
- author and reviewer trade incompatible preferences without an owner or experiment.

Oscillation diagnosis normally requires at least two anchor flips or three comparable snapshots.

Resolution requires one of:

- new evidence;
- explicit decision ownership;
- a reversible experiment;
- smaller scope;
- acceptance of residual risk.

## 5. Bloat gate

Stop as `stopped-bloat` when added complexity exceeds added certainty.

Watch signals:

- more layers, adapters, caches, flags, synchronization paths, compatibility branches, or configuration;
- more implementation slices but weaker ownership;
- more alternatives without a decision rule;
- larger validation matrix caused by accidental design complexity;
- repeated future-proofing without a concrete requirement;
- plan length grows while blocker and unknown counts do not fall;
- non-applicable rollout, migration, or contract sections are generated to satisfy a template.

Bloat is a direction signal, not a formatting complaint.

## 6. Direction gate

Classify as `direction_failure` when multiple findings share a root cause in:

- wrong source of truth;
- wrong state or data owner;
- wrong identity or lifecycle boundary;
- wrong public contract;
- wrong migration or compatibility model;
- invented problem or disproportionate solution;
- architecture that works only by adding many synchronization or exception paths.

Transition:

```yaml
transition:
  next_action: initiate-pivot
  final_state: pivot-required
```

Do not generate a local revision contract. Close the old epoch with a rejection reason, then hand off. A new epoch starts only after an external provider or human supplies a new candidate.

## 7. Alternatives gate

Use `needs-alternatives` when the current direction is not yet selected but has not been disproved.

Examples:

- multiple viable ownership models need comparison;
- scope can be solved by either migration or compatibility strategy, but selection criteria are missing;
- current proposal is only one candidate and review found no decisive rejection evidence.

Transition:

```yaml
transition:
  next_action: explore-alternatives
  final_state: needs-alternatives
```

Do not mark this as `pivot-required`; that would invent a direction failure.

## 8. Evidence and decision gates

Use `needs-evidence` when a discoverable fact could flip the plan.

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
- ownership boundary as organizational policy;
- rollout order or support policy.

When both exist, select the action that can reduce uncertainty first. Record any later action as `follow_up_if` rather than an action list.

## 9. Scoped re-review

After a local revision, re-review only:

1. accepted finding closure;
2. direct regressions;
3. core anchor drift;
4. evidence boundary drift;
5. scope and bloat.

The review pass must bind to the revised artifact version/fingerprint and reference the revision contract.

A full re-review is justified only when revision materially changed direction, scope, contract, ownership, migration, or validation topology. Such a change usually means the previous revision was not local and should be reclassified or moved to a new epoch.

## 10. Budget gate

Soft budget is a checkpoint. Continue beyond it only with progress credit and no disqualifier.

Hard budget ends the current run:

```yaml
transition:
  next_action: stop
  final_state: stopped-budget
```

An override requires an explicit new bounded budget. “继续直到完美” is invalid.

## 11. Ready gate

`ready-for-handoff` requires:

```yaml
direction_failures_open: 0
material_decision_gaps_open: 0
plan_flipping_evidence_gaps_open: 0
applicable_core_anchors: stable
non_applicable_anchors: explicitly_marked
implementation_path: actionable
critical_risks_mapped_to_validation: true
rollout_rollback_or_containment: adequate_for_profile_when_applicable
current_artifact_reviewed: true
review_breadth: adequate_for_profile
residual_risks_explicit: true
flat_signal: false
oscillation_signal: false
bloat_signal: false
```

A non-directional implementation unknown may remain only when it is explicit, bounded, and paired with a stop condition before affected work.

Ready is relative to evidence boundary. It is not proof that implementation will succeed.
