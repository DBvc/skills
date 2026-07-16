# State Migration: v1 to v2

`convergence_state_version: 2` fixes action/state ambiguity and adds review provenance.

## 1. Top-level transition

### v1

```yaml
next_action: revise-local
final_state: in-progress
```

### v2

```yaml
transition:
  next_action: revise-local
  final_state: null
  reason: ""
  owner_role: revision_provider
  follow_up_if: null
```

Rules:

- Replace v1 `final_state: in-progress` with `null`.
- Move `next_action` and `final_state` under `transition`.
- Keep one primary action only.
- Convert action arrays into one action plus `follow_up_if`.

## 2. Pivot terminology

### v1

```yaml
next_action: pivot-required
final_state: pivot-required
```

### v2

```yaml
transition:
  next_action: initiate-pivot
  final_state: pivot-required
```

`explore-alternatives` now maps to `needs-alternatives`, not `pivot-required`.

## 3. Missing artifact

v1 `blocked-artifact` becomes:

```yaml
transition:
  next_action: obtain-artifact
  final_state: needs-artifact
```

## 4. Provider independence

Remove the v1 global field:

```yaml
provider_independence: unknown
```

Record independence on every review pass:

```yaml
reviews:
  - id: R1
    artifact_version: v1
    provider:
      id: ""
      independence: unknown
```

This allows one review to be independent and another to share author context.

## 5. Review provenance

Wrap existing findings in a review pass:

```yaml
reviews:
  - id: R1
    artifact_version: v1
    artifact_fingerprint: ""
    provider:
      id: "legacy-review"
      type: unknown
      independence: unknown
    dimensions: []
    scope:
      kind: full
    parse_confidence: low
    findings:
      - id: F-001
        source_review_id: R1
```

If the reviewed artifact version cannot be established and multiple versions exist, do not migrate findings as applicable. Return `needs-review`.

## 6. Artifact identity

Add:

```yaml
artifact:
  version: v1
  fingerprint: ""
  content_location: ""
```

A fingerprint is optional. Version is mandatory for resume and multi-version histories.

## 7. Anchor status

Allowed v2 statuses:

```text
unknown
stable
conflicted
not_applicable
```

Migrate empty optional anchors such as public contract or migration to `not_applicable` only when the task truly does not involve them. Otherwise keep `unknown`.

## 8. Reviews, revisions, and history

Add arrays:

```yaml
reviews: []
revisions: []
history:
  artifact_versions: []
  anchor_snapshots: []
  rejected_directions: []
  transition_summaries: []
```

Do not fabricate historical entries. If history is unavailable, leave arrays empty and do not run `diagnose_stall` claims that require them.

## 9. Output mode

Add:

```yaml
output_mode: diagnostic
```

Defaults:

- `gate_only`: diagnostic
- `bounded_loop`: compact
- `resume`: compact
- `diagnose_stall`: diagnostic

Output mode changes presentation only. It must not discard internal state or hide a blocker.

## 10. Migration safety

When a v1 state has ambiguous artifact identity, mixed action/state values, or findings from unknown versions:

1. preserve the old state as read-only evidence;
2. do not guess the intended transition;
3. request the current artifact and applicable review;
4. create a fresh v2 state.
