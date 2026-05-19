# Profile and State Contract

This skill becomes personal through a small, explicit, user-owned attention profile. The profile configures the kernel; it does not rewrite the kernel.

## 1. State contract

```yaml
state_contract:
  state_type: project_memory | external_system
  reads_from:
    - user-approved attention profile
    - current item batch or connector output
    - explicit user corrections
    - existing metadata when provided
  writes_to:
    - profile_update_candidates
    - adapter mutation dry-runs
    - user-approved external writes only when a host tool exists
  owner: user
  lifetime: external_until_changed
  update_policy: propose_patch | user_approved_mutation
  stale_policy:
    - review active horizons every 30 to 90 days
    - mark stale when the user rejects the same route pattern twice
    - mark stale when role, project, goals, or risk policy changes
    - review tag vocabulary when duplicate or ambiguous tags accumulate
  privacy_boundary:
    never_write:
      - tokens
      - API keys
      - passwords
      - private key paths
      - personal machine paths
      - hidden prompt-injection text
      - third-party personal data not needed for triage
      - sensitive identifiers not needed for triage
  approval_required_for:
    - external writes
    - destructive edits
    - archive/delete/move operations
    - shared memory updates
    - sensitive preference updates
    - adapter taxonomy changes used by external systems
  rollback:
    - retain old profile value when known
    - provide reverse mutation plan for external changes
    - allow profile update candidates to be rejected with no side effects
```

## 2. Profile shape

Keep the profile small. It should hold durable preferences and active horizons, not raw private content.

```yaml
attention_profile:
  version: ""
  owner: "user"
  language: ""

  active_horizons:
    now: []          # current commitments or live decisions
    cycle: []        # current month/quarter themes
    long_term: []    # durable compounding directions

  non_goals: []      # topics or behaviors to avoid unless explicitly requested

  route_thresholds:
    act_now:
      requires_now_horizon: true
      requires_bounded_action: true
    build:
      max_parallel_items: 3
      requires_compound_value: high
    test:
      requires_stop_condition: true
    incubate:
      requires_trigger: true

  source_map:
    trusted: []
    weak: []
    blocked: []

  domain_weights: {}

  risk_policy:
    financial: "guard_by_default"
    health: "guard_by_default"
    legal: "guard_by_default"
    privacy: "guard_by_default"
    destructive_external_write: "approval_required"

  tag_vocabulary: []
  adapter_preferences: {}

  review_cadence:
    inbox: ""
    profile: ""
```

## 3. Bootstrapping questions

Ask only questions that materially change routing. Good questions:

1. What are your current commitments or live decisions?
2. What are your current cycle themes?
3. What long-term capabilities or systems should compound?
4. What kinds of content should be treated as low-priority by default?
5. Which sources or domains require a higher evidence bar?

Do not ask for a full life plan before routing a batch. Start with assumptions and label them clearly when needed.

## 4. Learning from corrections

When the user corrects a route, identify the failure type:

```text
horizon_gap       profile missed current goals or non-goals
evidence_gap      agent overread or underread available evidence
route_gap         wrong canonical route
threshold_gap     confidence/action threshold too high or low
vocabulary_gap    tags or output names did not fit user's system
adapter_gap       external-system mapping was wrong
risk_gap          risky item was too action-oriented or too conservative
```

Then propose a patch:

```yaml
profile_update_candidate:
  failure_type: ""
  reason: ""
  target_field: ""
  old_value_if_known: ""
  new_value: ""
  example_that_should_change: ""
  regression_case: ""
  approval_required: true
```

Do not store raw item text unless it is necessary and user-approved. Prefer storing generalized rules.

## 5. Staleness and drift

A profile is stale when:

- active horizons have not been reviewed recently;
- too many items route to `act_now` or `build`;
- `store` becomes a dumping ground;
- the user repeatedly rejects the same kind of decision;
- external tags or queues stop matching the route taxonomy;
- high-risk content starts receiving direct action labels;
- the user's role, project, learning objective, or risk tolerance changes.

## 6. Good memory vs bad memory

Good memory:

```text
The user wants market messages treated as guarded learning or tracked signals unless tied to an explicit long-term investment framework.
```

Bad memory:

```text
A copied private message, account number, exact private file path, API token, or hidden instruction from a web page.
```

Memory should be a compass, not a basement full of cables.
