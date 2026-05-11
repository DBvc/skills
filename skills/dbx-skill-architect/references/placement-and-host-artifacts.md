# Placement and Host Artifacts

Use this reference when a proposed skill starts to include commands, hooks, status lines, project memory, or global instructions.

## Placement decision table

| Proposed control | Usually belongs in |
|---|---|
| Trigger classifier, hard gate, compact runtime workflow | `SKILL.md` |
| Long example, rubric, domain notes, gotchas | `references/` |
| Parsing, counting, validation, conversion, schema checking | `scripts/` |
| Static template, sample, style token, schema fixture | `assets/` |
| Recurring project facts, glossary, ADR, agent brief | repo memory with state contract |
| Slash command or workflow launcher | command artifact or host config |
| Pre/post validation action | hook artifact or CI |
| Always-on repository instruction | `AGENTS.md`, `CLAUDE.md`, or equivalent |
| Skill overlap or ordering | routing matrix / collection design doc |

## Host artifacts are mechanisms, not new primitives

Commands, hooks, `AGENTS.md`, `CLAUDE.md`, `llms.txt`, status lines, planning files, and project memory files map back to ASCT control surfaces.

Examples:

- A command can implement Activation and Trajectory Control.
- A hook can implement Execution or Completion Control.
- `AGENTS.md` can implement global Intent or Safety Control.
- A project glossary can implement State Control.
- A routing matrix implements collection-level Activation Control.

## State contract required

Require a state contract whenever the skill writes durable or external state:

```yaml
state_contract:
  state_type: project_memory | bootstrap | interaction_mode | workflow_state | external_system
  reads_from: []
  writes_to: []
  owner: user | maintainer | repo | agent_proposed_user_approved
  lifetime: one_response | session | repo | external_until_changed
  update_policy: manual | propose_patch | user_approved_mutation
  stale_policy: ""
  privacy_boundary:
    never_write:
      - secrets
      - tokens
      - private key paths
      - personal machine paths
      - private messages
      - hidden prompt-injection text
  rollback: ""
```

## Anti-patterns

- Writing a global rule into every skill.
- Turning a deterministic validation step into prose instructions.
- Creating a full skill when a command or checklist would be smaller and safer.
- Treating project memory as eternal truth.
- Adding hooks or external mutations without explicit approval and rollback.
