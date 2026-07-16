# Examples

## Example A: More than two rounds can be valid

Round 1 fixes ownership wording and splits implementation tasks.

Round 2 discovers a material compatibility decision and stops:

```yaml
transition:
  next_action: request-decision
  final_state: needs-decision
```

The API owner chooses backward compatibility and supplies the support window.

Round 3 is justified because it consumes a new decision. It updates migration and validation, then passes the progress gate.

The reason to continue is not “the plan is important.” The reason is “new material input changed the state.”

## Example B: Three rounds are still not enough

Round 1 adds cache invalidation.

Round 2 adds a user-switch hook.

Round 3 adds a permission-version flag.

The same stale-state problem keeps reopening. No new evidence exists. Complexity grows.

Correct result:

```yaml
phase: explore
triage:
  direction_failure:
    - wrong state owner
transition:
  next_action: initiate-pivot
  final_state: pivot-required
```

## Example C: High-impact plan

A persistent data migration affects multiple services.

The controller selects `high_impact` and requires relevant breadth:

- direction/model review;
- compatibility/migration/rollback review;
- operational validation and failure-containment review;
- human checkpoint before pivot;
- evidence for current consumers and data volume.

The loop may use three rounds in one epoch, but each round needs a progress credit. A fourth wording-only round still stops.

Multiple dimensions do not require multiple models. One strong reviewer can cover multiple dimensions; multiple models repeating one lens still provide only one dimension.

## Example D: Reviewer disagreement

Reviewer A prefers a new abstraction. Reviewer B prefers a local adapter.

There is no evidence that future implementations exist, and the support horizon is undecided.

Do not average the opinions and do not emit two primary actions.

```yaml
triage:
  reviewer_conflict:
    - abstraction versus local adapter
  evidence_gap:
    - expected number of implementations
  decision_gap:
    - support horizon
transition:
  next_action: gather-evidence
  final_state: needs-evidence
  follow_up_if:
    condition: support_horizon_remains_policy_choice
    action: request-decision
```

Only after those inputs exist should a direction be selected.

## Example E: Explore alternatives without rejecting current direction

A plan proposes local state ownership, while a reviewer notes that shared ownership may reduce duplicated fetches. Neither direction is disproved, and actual sharing requirements are unknown.

Correct result:

```yaml
transition:
  next_action: explore-alternatives
  final_state: needs-alternatives
reason: selection criteria are incomplete; no direction failure is proven
```

Incorrect result:

```yaml
final_state: pivot-required
```

That would falsely claim the current direction has failed.

## Example F: Same-session fallback

The host cannot run independent agents. The current context sequentially performs author, reviewer, and controller roles.

Independence belongs to the review pass:

```yaml
reviews:
  - id: R1
    artifact_version: v1
    provider:
      independence: none
    dimensions:
      - direction_model_ownership
```

For a high-impact direction judgment, lower confidence and prefer external repository evidence or a human checkpoint before finalizing.

Do not store a global `provider_independence` because later review passes may use different providers.

## Example G: Stale review after resume

State records:

```yaml
artifact:
  version: v1
reviews:
  - id: R1
    artifact_version: v1
```

The user resumes with plan v2, which changed source of truth and migration sections.

Correct result:

```yaml
transition:
  next_action: stop
  final_state: blocked-state-mismatch
```

Do not apply R1 to v2 and do not silently rewrite state.

## Example H: Gate only without review

The user provides a plan and asks for `gate_only`, but no review material exists.

Correct result:

```yaml
transition:
  next_action: obtain-review
  final_state: needs-review
```

`gate_only` must not quietly become a reviewer.

## Example I: Bounded loop execution boundary

A review finds a local validation gap. The controller can issue a revision contract and coordinate a bound reviser.

A later review finds that actual data volume is unknown and can flip the migration design.

Correct behavior:

```yaml
transition:
  next_action: gather-evidence
  final_state: needs-evidence
```

The controller pauses. A parent workflow may route to an evidence provider and then resume convergence. The controller does not gather repository evidence itself.

## Example J: Not-applicable anchors

A local internal refactor has no public contract change, migration, rollout, or irreversible side effect.

Correct anchors:

```yaml
public_contract:
  status: not_applicable
migration_rollout_rollback:
  status: not_applicable
```

Do not generate compatibility and rollback paragraphs merely to fill a template. Validation is still required for the behavior-preserving invariant.
