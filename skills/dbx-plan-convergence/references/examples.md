# Examples

## Example A: More than two rounds can be valid

Round 1 fixes ownership wording and splits implementation tasks.

Round 2 discovers a material compatibility decision and stops as `needs-decision`.

The API owner chooses backward compatibility and supplies the support window.

Round 3 is justified because it consumes a new decision. It updates migration and validation, then passes the progress gate.

The reason to continue is not “the plan is important.” The reason is “new material input changed the state.”

## Example B: Three rounds are still not enough

Round 1 adds a cache invalidation step.

Round 2 adds a user-switch hook.

Round 3 adds a permission-version flag.

The same stale-state problem keeps reopening. No new evidence exists. Complexity grows.

Correct result:

```yaml
phase: explore
finding: direction_failure
stop_state: pivot-required
reason: wrong state owner
```

## Example C: High-impact plan

A persistent data migration affects multiple services.

The controller selects `high_impact`:

- direction/model review;
- compatibility/migration/rollback review;
- operational validation and failure-containment review;
- human checkpoint before pivot;
- evidence required for current consumers and data volume.

The loop may use three rounds in one epoch, but each round needs a progress credit. A fourth wording-only round still stops.

## Example D: Reviewer disagreement

Reviewer A prefers a new abstraction. Reviewer B prefers a local adapter.

There is no evidence that future implementations exist, and the product support horizon is undecided.

Do not average the opinions.

```yaml
triage:
  reviewer_conflict:
    - abstraction versus local adapter
  evidence_gap:
    - expected number of implementations
  decision_gap:
    - support horizon
next_action:
  - gather-evidence
  - then request-decision
```

Only after those inputs exist should a direction be selected.

## Example E: Same-session fallback

The host cannot run independent agents.

The current agent can sequentially perform author, reviewer, and controller roles, but output must say:

```yaml
provider_independence: none
confidence_adjustment: lower_for_high_impact_direction_judgment
```

Use external repository evidence or a human checkpoint before finalizing a high-impact direction.
