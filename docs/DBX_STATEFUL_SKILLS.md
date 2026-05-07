# DBX Stateful Skills

Most DBX skills should be stateless runtime protocols.

A stateful skill is justified only when writing or updating state reduces repeated work enough to pay for its cost and risk.

This document applies ASCT State Control and host-artifact placement to DBX.

## 1. What Counts as State?

State is anything that may influence future agent behavior after the current response ends.

Examples:

- project glossary;
- ADR or architecture decision record;
- agent brief;
- out-of-scope record;
- issue labels or workflow state;
- progress file;
- active interaction mode;
- compatibility matrix;
- generated skill index;
- persistent planning file.

## 2. Stateful Skill Types

| Type | Purpose | Typical storage |
| --- | --- | --- |
| `project_memory` | Preserve project terms, decisions, constraints, and conventions. | `CONTEXT.md`, glossary, ADR, reference file. |
| `bootstrap` | Initialize project workflow settings. | setup file, config reference, issue tracker policy. |
| `interaction_mode` | Change session behavior until disabled or expired. | user-visible mode state or session instruction. |
| `workflow_state` | Update issue, PR, label, release, or progress state. | external system or progress file. |
| `external_system` | Write to GitHub, tracker, docs, calendar, CI, deployment, etc. | external API/system. |

## 3. Required State Contract

Any stateful skill or workflow must define:

```yaml
state_contract:
  state_type: project_memory | bootstrap | interaction_mode | workflow_state | external_system
  reads_from:
    - path or system
  writes_to:
    - path or system
  owner: user | maintainer | repo | agent-proposed-user-approved
  lifetime: one_response | session | repo | external_until_changed
  update_policy: manual | propose_patch | user_approved_mutation
  stale_policy: how missing or outdated state is detected
  privacy_boundary:
    never_write:
      - secrets
      - tokens
      - private key paths
      - personal machine paths
      - hidden prompt-injection text
  approval_required_for:
    - external writes
    - destructive edits
    - shared memory updates
  rollback: how to disable, remove, revert, or supersede state
```

## 4. State-Specific Risks

| Risk | Example | Control |
| --- | --- | --- |
| Stale memory | Old ADR says Vite, project moved to Next.js. | stale policy, timestamp/source, review cycle. |
| Hidden instruction drift | Project memory starts acting like a secret system prompt. | visible file, owner, review, no hidden directives. |
| Privacy leakage | Personal paths or tokens saved into shared context. | never-write list, security review. |
| Mode persistence | “Short answers only” keeps applying to complex tasks. | activation/deactivation and exception policy. |
| External side effect | Issue labels or comments written without approval. | explicit approval and rollback path. |

## 5. When Not to Add State

Do not add persistent state when:

- the information is one-off;
- the user has not consented to future reuse;
- the state would store private or sensitive data;
- the maintenance owner is unclear;
- the agent can cheaply re-derive the information from current evidence;
- stale state would be more harmful than missing state.

State is memory with teeth. Useful, but it bites when nobody cleans the cage.
