# Convergence Model

## 1. Why “two rounds” exists

Two rounds is useful as a default **soft checkpoint** because repeated review-revision usually has diminishing information return:

1. The first revision closes obvious structural and evidence issues.
2. The second revision reveals whether the chosen direction can actually absorb critique without growing accidental complexity.
3. A third pass by the same author and same reviewer often becomes correlated polishing rather than new learning.

This is not a claim that important plans only deserve two reviews. It is a claim that **more repetitions of the same loop are weak evidence of quality**.

When a plan is important, increase rigor through:

- stronger evidence grounding;
- multiple review dimensions;
- independent reviewers where practical;
- explicit decision ownership;
- migration, rollout, rollback, observability, and failure-containment checks;
- prototype, spike, benchmark, or reversible experiment where uncertainty is empirical.

More importance should buy more independent information, not merely more turns.

## 2. Direction epoch versus revision round

A revision round assumes the core direction is stable.

```text
same direction
  -> bounded local revision
  -> scoped re-evaluation
  -> progress gate
```

A pivot is different:

```text
direction failure
  -> close old epoch with rejection reason
  -> gather evidence or decision
  -> open a new direction epoch
```

The new epoch may receive a fresh per-epoch soft budget because it is a new candidate. However:

- total revision rounds remain counted;
- the number of direction epochs remains bounded;
- rejected directions and reasons remain visible;
- a return to an old direction requires new evidence or an explicit decision.

This prevents both premature lock-in and endless zigzagging.

## 3. When a third or later round is justified

Beyond the soft checkpoint, continue only when the new round consumes a material input that was not available before.

Valid reasons:

- repository evidence disproves an earlier assumption;
- an owner decides compatibility or migration policy;
- a prototype or benchmark resolves a feasibility question;
- a new review dimension finds a material risk;
- a blocker is closed and the revised implementation path becomes more bounded;
- a pivot creates a materially different candidate.

Weak reasons:

- “再润色一遍”；
- same reviewer repeats the same concern with different wording;
- headings, diagrams, or prose become longer;
- the plan adds adapters, flags, layers, or exceptions to preserve a suspect direction;
- the author keeps flipping a core decision without new evidence.

## 4. High-impact plans

A plan is `high_impact` when errors have wide blast radius or expensive correction, for example:

- public API or protocol changes;
- persistent data, schema, or migration changes;
- cross-module ownership or source-of-truth changes;
- security, privacy, identity, authorization, or financial behavior;
- infrastructure, rollout, operational, or reliability changes;
- long-lived platform abstractions;
- changes that are difficult to roll back.

High-impact does not mean unlimited rounds. It means:

- soft budget may be larger;
- independent review breadth is required;
- evidence gaps block finalization more often;
- pivots require stronger rationale;
- human checkpoints become mandatory for material decisions;
- ready status requires explicit residual risk and rollback / containment.

## 5. The real monotonic target

Plan text is not expected to improve monotonically.

The controlled target is:

```text
decision reliability
+ evidence clarity
+ anchor stability
+ implementation actionability
+ risk-to-validation coverage
- unresolved blockers
- material unknowns
- accidental complexity
- oscillation
```

A shorter plan can be progress. A rejected plan can be progress. A stop requiring human decision can be progress. The controller must not confuse document completion with decision quality.
