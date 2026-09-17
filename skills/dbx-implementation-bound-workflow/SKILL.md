---
name: dbx-implementation-bound-workflow
description: Manual-only controller for an explicitly invoked, already-authorized feature request that genuinely needs one bounded technical-plan review before continuing into its first code slice. Use only through $dbx-implementation-bound-workflow. Do not use for ordinary direct implementation, plan-only requests, standalone review, or Plan-First phase commands.
---

# DBX Implementation-Bound Workflow

Move one explicit implementation request from a real draft operation to an attributable first code slice. This is an isolated prototype. `scripts/planning_workflow.py` owns the run, transitions, correction budget, authority, and frozen host-validation handoff. It does not own validation execution or implementation completion.

## Activation

Run only when all are true:

- the user explicitly invokes `$dbx-implementation-bound-workflow`;
- the requested outcome includes implementation;
- a technical plan is genuinely needed before the first edit;
- current trusted context already grants code-write authority with explicit repository-relative paths.

Otherwise route to ordinary direct implementation, plan-only work, standalone review, or the already-selected Plan-First phase. Invocation does not create missing write authority.

## Start and resume

Give `start` one stable, trusted runtime directory outside the Git worktree. It must be owner-only. `origin_ref` must identify the originating trusted request, not a model-generated retry.

```text
planning_workflow.py start --runtime-dir <private-outside-repo-dir> --workspace <repo> \
  --origin-ref <trusted-event-ref> --goal <implementation-goal> \
  --authority-source-ref <grant-ref> --authority-path <repo-relative-path>
```

The helper derives the state and plan paths from `origin_ref`. Repeating identical start input in the same runtime directory returns the existing run; conflicting input fails. This prevents budget reset inside that runtime registry, not global feature identity across arbitrary directories. Reuse the returned `state_path` for every later command.

Start requires the derived plan file not to exist. Its first `next` action is `begin draft`. State and plan remain outside the worktree under `0700`/`0600` protection.

## Execute only returned actions

Every mutating command needs a stable unique `--event-id`. A `record` uses the matching begin ID as `--operation-id`. Identical event replay is idempotent; conflicting reuse fails.

- `draft`: ask `dbx-technical-plan` to write the returned plan path, then record a JSON file containing exactly one `workflow_plan_result`.
- `initial_review`: pass the exact persisted `delegated_review` envelope returned by the helper to one independent, read-only `dbx-linus-review` worker, then record its exact `delegated_review_result` JSON.
- `correction_cycle`: revise all persisted blocking finding IDs in one batch. The provider result must close exactly that set without changing the frozen artifact type or first-slice contract; the helper permits at most one begin.
- `final_review`: perform one final full independent review. Any new blocker terminates `blocked`; there is no second correction.
- `implementation`: begin first verifies the Git workspace did not change during planning, then implement the declared first slice in the current task. `record implemented` only moves to `host_validation`; it never executes planner-supplied argv.
- `host_validation`: begin captures the first-slice-present pre-validation snapshot, rejects out-of-scope/missing-target/index/HEAD changes, freezes one exact host validation request, and terminates at `needs_host_validation`. This package does not accept caller-written host result JSON and cannot transition to validated/completed.

Never edit state JSON, reset a run, infer a transition from prose, stage, commit, or delegate write authority through reviewer text.

## Planner result

The path-backed JSON must use this exact payload shape. `bounded_revision` uses the same shape with `consumed_revision_rounds: 1` and the exact persisted `closed_finding_ids`.

```yaml
workflow_plan_result:
  correlation_id: <run_id>
  provider_id: dbx-technical-plan
  purpose: draft | bounded_revision
  status: produced
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | implementation_proposal
    version: <non-empty>
    fingerprint_scheme: exact-bytes-sha256
    fingerprint: sha256:<exact-file-bytes>
    content_ref: {kind: path, value: <derived-plan-path>}
  first_slice:
    id: <non-empty>
    summary: <non-empty>
    target_paths: [<inside-start-authority>]
    validation_argv: [<executable>, <arg>]
  closed_finding_ids: []
  consumed_revision_rounds: 0
  unresolved_blockers: []
```

The helper recomputes the file hash, validates provider/correlation/purpose, freezes target paths and validation argv, and rejects targets outside start-time authority. Once correction starts, artifact type and the entire normalized first-slice contract are frozen; only plan bytes/version and closure of the persisted finding set may change.

## Reviewer result

Record the canonical generic `delegated_review_result` from `dbx-linus-review`; do not add experiment-specific result fields. The workflow persists the full generic request envelope. Its deterministic `review_id` binds the run, review purpose, provider capability, scope, requested dimensions, evidence boundary, non-goals, write prohibition, and exact artifact identity. The result must echo that ID plus the fixed provider/capability/scope/independence and exact current artifact path/version/hash.

`accept` requires no findings. `accept_with_advisories` permits only non-blocking residual findings. `changes_required` requires blocking finding IDs. A finding with `decision_owner_required: true` is terminal `blocked`; it never enters automatic correction. Other initial blocking IDs become the sole correction contract; final blocking findings stop the run.

## Host validation handoff

The helper never executes `validation_argv`. `begin host_validation` freezes all of these into one fingerprinted request:

- repository-root `cwd` and the exact argv plus command hash;
- the implementation baseline and controller-captured pre-validation snapshot;
- current plan, accepted review, first-slice, target, and authority identities;
- a fixed 300-second timeout and 1 MiB combined stdout/stderr capture limit;
- `external_side_effect_policy: forbidden_without_separate_host_approval`.

Before emitting that request, the controller requires:

- current review still matches current plan bytes and version;
- a real delta already present before host validation, including executable-bit or file/symlink type changes;
- every changed path inside start-time authority;
- at least one changed path inside the declared first-slice target surface.

Git compares only Git-relevant regular-file mode (`100644` versus `100755`, based on owner execute); permission hardening such as `0644` to `0600` and group/other-only execute changes are not code deltas.

`needs_host_validation` is terminal for this prototype and always reports:

- `first_slice_present: true`;
- `validation_status: not_run_by_controller`;
- `implementation_completion_claim: false`.

A platform-owned trusted host may separately approve, execute, limit, and inspect the frozen request, including a post-validation workspace snapshot. That channel and its completion decision are outside this package. Do not turn a caller-written JSON file, non-empty approval reference, document acceptance, or handoff claim into validation or implementation completion evidence.

`evals/evals.json` covers activation and response boundaries only; executable truth lives in `tests/test_planning_workflow.py` and `tests/test_git_evidence.py`.
