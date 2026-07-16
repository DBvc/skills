# Convergence Model

## 1. Controlled target

Plan text is not expected to improve monotonically.

The controlled target is:

```text
decision reliability
+ evidence clarity
+ review provenance
+ anchor stability
+ implementation actionability
+ risk-to-validation coverage
- unresolved blockers
- material unknowns
- accidental complexity
- oscillation
```

A shorter plan can be progress. A rejected direction can be progress. A stop requiring evidence or human decision can be progress. The controller must not confuse document completion with decision quality.

## 2. Action and state are different axes

A convergence gate answers two questions:

```text
next_action  What should happen next?
final_state  Does this invocation pause, complete, or stop?
```

Example:

```yaml
transition:
  next_action: revise-local
  final_state: null
```

This means the direction is locally repairable and the workflow may continue.

```yaml
transition:
  next_action: gather-evidence
  final_state: needs-evidence
```

This means the current invocation ends with an external handoff. It can resume after evidence arrives.

Do not use a state name as a vague action. In particular:

- `initiate-pivot` is an action;
- `pivot-required` is the outcome state;
- `explore-alternatives` does not imply `pivot-required`.

## 3. Why “two rounds” exists

Two rounds is a default soft checkpoint because repeated review-revision often has diminishing information return:

1. The first revision closes obvious structural and evidence issues.
2. The second reveals whether the direction can absorb critique without growing accidental complexity.
3. A third pass by the same author and same reviewer often becomes correlated polishing rather than new learning.

This is not a claim that important plans deserve only two reviews. It is a claim that more repetitions of the same loop are weak evidence of quality.

When a plan is important, increase rigor through:

- stronger evidence grounding;
- multiple review dimensions;
- independent review where practical;
- explicit decision ownership;
- migration, rollout, rollback, observability, and containment checks where applicable;
- prototype, spike, benchmark, or reversible experiment when uncertainty is empirical.

More importance should buy more independent information, not merely more turns.

## 4. Direction epoch versus revision round

A revision round assumes core direction is stable:

```text
same direction
  -> bounded local revision
  -> scoped review of revised artifact
  -> progress gate
```

A direction failure is different:

```text
direction failure
  -> initiate-pivot
  -> close old epoch with rejection reason
  -> hand off for evidence, decision, or alternatives
  -> receive a new candidate
  -> open a new epoch
```

The controller does not generate the new direction itself.

The new epoch may receive a fresh per-epoch soft budget because it is a new candidate. However:

- total revision rounds remain counted;
- direction epochs remain bounded;
- rejected directions and reasons remain visible;
- a return to an old direction requires new evidence or an explicit decision.

This prevents both premature lock-in and endless zigzagging.

## 5. When a third or later round is justified

Beyond the soft checkpoint, continue only when the new round consumes material input that was not available before.

Valid reasons:

- repository evidence disproves an earlier assumption;
- an owner decides compatibility or migration policy;
- a prototype or benchmark resolves feasibility;
- a new review dimension finds a material risk;
- a blocker is closed and the implementation path becomes more bounded;
- an externally supplied pivot creates a materially different candidate.

Weak reasons:

- “再润色一遍”；
- same reviewer repeats the same concern with different wording;
- headings, diagrams, or prose become longer;
- the plan adds adapters, flags, layers, or exceptions to preserve a suspect direction;
- the author keeps flipping a core decision without new evidence.

## 6. Review provenance is part of state

A finding is meaningful only relative to the artifact it reviewed.

```text
plan v1 -> review R1 of v1 -> revision contract -> plan v2 -> scoped review R2 of v2
```

The controller must not apply R1 to v2 unless unchanged applicability is demonstrated. Each review pass carries its own provider independence and dimensions because these properties can differ by pass.

This matters even in a single-model workflow:

- resume can receive stale findings;
- two reviewers may have seen different plan versions;
- scoped review may accidentally inspect the pre-revision artifact;
- a same-session reviewer is not independent merely because its prompt changed.

## 7. Explore alternatives is not always a pivot

`explore-alternatives` means the direction is not yet sufficiently chosen. Examples:

- two candidates remain viable and trade-offs are unresolved;
- the current proposal is incomplete rather than disproved;
- a decision framing step is needed before local revision.

`initiate-pivot` means the current direction is rejected because its model, owner, source of truth, contract, or route is wrong.

Conflating them creates false certainty and prematurely closes viable options.

## 8. High-impact plans

A plan is high impact when errors have wide blast radius or expensive correction, for example:

- public API or protocol changes;
- persistent data, schema, or migration changes;
- cross-module ownership or source-of-truth changes;
- security, privacy, identity, authorization, or financial behavior;
- infrastructure, rollout, operational, or reliability changes;
- long-lived platform abstractions;
- changes difficult to roll back.

High impact does not mean unlimited rounds. It means:

- soft budget may be larger;
- relevant review breadth is required;
- evidence gaps block finalization more often;
- pivots require stronger rationale;
- human checkpoints become mandatory for material decisions;
- ready status requires explicit residual risk and applicable rollback or containment.

## 9. Compact output, full internal rigor

Runtime state may contain review provenance, epochs, revisions, anchor snapshots, credits, and disqualifiers. Normal bounded-loop output should expose only the pieces needed to act.

Compact output must still reveal:

- selected transition;
- why it was selected;
- non-empty blockers or gaps;
- owner of next step;
- evidence boundary and residual risks.

Diagnostic output is appropriate for gate-only analysis, stall diagnosis, resume mismatch, direction failure, or user-requested introspection.

## 10. Skill shape

```yaml
skill_shape:
  primary: coordination
  secondary:
    - decision
    - interaction_mode
  dominant_failure_modes:
    - action_state_ambiguity
    - stale_review_application
    - false_local_repair
    - evidence_invention
    - decision_substitution
    - oscillation
    - document_bloat
    - collection_coupling
  implementation_implication: >-
    Keep provider knowledge outside the controller; enforce artifact identity,
    transition gates, bounded revision contracts, and explicit handoff states.
```
