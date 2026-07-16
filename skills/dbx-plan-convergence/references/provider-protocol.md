# Provider Protocol

The controller composes by protocol, not by provider name.

## 1. Roles

### Artifact provider

Produces or supplies the current plan artifact.

Minimum output:

```yaml
artifact:
  type: ""
  version: ""
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
  content_location: ""
```

### Reviewer provider

Finds material problems in the artifact. It does not decide whether the loop continues.

Preferred finding shape:

```yaml
finding:
  id: "F-001"
  severity: blocker | high | medium | low
  category: model | ownership | source_of_truth | compatibility | migration | validation | operability | complexity | evidence | decision | other
  evidence: ""
  impact: ""
  confidence: high | medium | low
  local_revision_signal: true | false | unknown
  evidence_gap_signal: true | false | unknown
  decision_gap_signal: true | false | unknown
  direction_failure_signal: true | false | unknown
  scope_expansion_signal: true | false | unknown
  verification_hint: ""
```

Signals are not controller decisions.

Human-readable review is acceptable. The controller may normalize it with lower parse confidence.

### Evidence provider

Supplies facts that can change the plan.

```yaml
evidence_item:
  id: "E-001"
  source: repo | documentation | test | log | measurement | stakeholder | other
  observation: ""
  supports_or_refutes: []
  freshness: ""
  confidence: high | medium | low
  limitation: ""
```

Keep observed facts separate from assumptions and judgments.

### Decision owner

Closes a branch that the controller or reviewer is not authorized to choose.

```yaml
decision:
  id: "D-001"
  question: ""
  choice: ""
  rationale: ""
  rejected_alternatives: []
  constraints_created: []
  owner: ""
  date: ""
```

### Revision provider

Receives only the revision contract plus the smallest necessary artifact context.

It returns:

```yaml
revision_result:
  artifact_version_before: ""
  artifact_version_after: ""
  accepted_findings_addressed: []
  changes_made: []
  assumptions_preserved: []
  could_not_complete: []
  scope_expanded: false
  anchor_changed: false
```

The reviser must stop rather than silently change direction.

## 2. Independence

Provider independence values:

- `independent`: reviewer did not receive the author's hidden reasoning or prior reviewer conclusion;
- `partially_independent`: separate role or context, but shares some history;
- `none`: same context performs author, reviewer, and controller roles;
- `unknown`.

Independent review is desirable for high-impact plans but is not always available.

Do not claim independence merely because the same model used a different prompt.

## 3. Review dimensions

Review breadth is about distinct risk surfaces, not reviewer count.

Common dimensions:

- direction, model, ownership, source of truth;
- compatibility, migration, rollout, rollback;
- validation, operability, observability, failure containment;
- security, privacy, identity, authorization;
- performance and capacity, only when material;
- implementation slicing, sequencing, and reversibility.

A single reviewer may cover multiple dimensions. Multiple reviewers repeating the same lens still count as one dimension.

## 4. Adapter rules

The controller must work when:

- only a plan and plain-text review are provided;
- the reviewer uses another schema;
- a human supplies decisions inline;
- evidence arrives after a round;
- one provider is unavailable;
- all roles run sequentially in one session.

Missing providers change confidence and next action. They do not justify inventing evidence or decisions.

## 5. No hidden coupling

Do not:

- require a particular skill name;
- assume a particular host feature;
- hard-code a model version;
- require a particular file format;
- make ordinary providers emit this schema unless convergence is explicitly requested;
- place provider-specific review knowledge inside the controller.

Optional collection-level commands or routing rules may choose local providers. Those choices stay outside this runtime skill.
