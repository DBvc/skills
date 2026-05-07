# DBX Codex Compatibility

This document tracks compatibility policy for DBX skills that depend on Codex-specific features.

Current Codex-bound skills:

- `dbx-goal-writer`
- `dbx-subagent-context-control`

## 1. Compatibility Principle

Do not invent Codex syntax.

If a capability is feature-gated, host-dependent, or unclear, the skill should ask the user to verify or use a conservative fallback.

## 2. Feature Checks

| Feature | Check method | If unknown |
| --- | --- | --- |
| `/goal` availability | `codex --version`, `codex features list`, slash popup, user confirmation. | Do not emit unsupported slash syntax. Provide goal contract as plain Markdown. |
| Goal file/package mode | User/project convention or observed Codex behavior. | Use direct goal contract. |
| Subagent support | Codex docs, CLI help, tool surface, user confirmation. | Do not assume subagent exists. |
| `fork_context` behavior | Current Codex support and user confirmation. | Treat as unknown; describe desired isolation in natural language. |
| Background task behavior | Host support and explicit user request. | Do not create background assumptions. |

## 3. Runtime Rules

### `dbx-goal-writer`

- Prefer direct goal text when host support is unclear.
- Do not claim `/goal` is available unless verified or user states it.
- Do not invent flags, package formats, or slash syntax.
- Goal validation commands must come from repo evidence or user-provided commands.

### `dbx-subagent-context-control`

- Only trigger for Codex subagent context inheritance or explicit `fork_context` discussion.
- Do not generalize to Claude, Cursor, Gemini, or business “agent” concepts.
- Default to minimal context and independent reviewer prompts when subagent semantics are available.
- If `fork_context` is unsupported or unknown, express the intended isolation strategy without claiming the host can enforce it.

## 4. Drift Handling

Codex may change feature names, CLI flags, host surfaces, or defaults.

When a drift is found:

```yaml
compatibility_update:
  affected_skill: ""
  changed_feature: ""
  observed_behavior: ""
  old_assumption: ""
  new_policy: ""
  evals_to_add_or_update: []
  rollback_condition: ""
```

Update:

- affected skill runtime rule if behavior changes;
- this compatibility file;
- trigger/output evals if activation or output syntax changes;
- `DBX_SKILL_INDEX.md` if maturity or risk changes.
