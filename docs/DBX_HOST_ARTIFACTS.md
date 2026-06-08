# DBX Host Artifacts

Agent hosts support different artifacts: commands, hooks, status lines, repo instructions, marketplace metadata, generated indexes, planning files, and project memory.

DBX treats them as implementation mechanisms that map back to ASCT control surfaces. They are not new primitives.

## 1. Artifact Mapping

| Artifact | Typical role |
| --- | --- |
| Slash command | Explicit activation or macro workflow. |
| Command file | Activation Control and Trajectory Control. |
| Hook | Lifecycle State, Trajectory, Completion, or Safety Control. |
| Status line | User-visible state, mode, or pending validation indicator. |
| `AGENTS.md` | Repo-level or global policy controller. |
| `CLAUDE.md` | Repo-level or host-specific policy controller. |
| `llms.txt` | Agent-facing discovery and routing index. |
| Marketplace metadata | Human discovery and installation metadata. |
| Plugin manifest | Distribution and capability metadata. |
| Planning file | Persistent State Control and Trajectory Control. |
| Progress file | Persistent State Control and Completion Control. |
| Project glossary | Persistent State Control. |
| ADR | Persistent State Control and Evolution Control. |
| Agent brief | Handoff contract and future Intent Control. |
| Out-of-scope record | Future Intent Control and State Control. |

## 2. DBX Policy

### Commands

Commands are useful when:

- the workflow spans multiple skills;
- the user should explicitly choose when it starts;
- activation by `description` would be too ambiguous;
- the workflow is a macro action.

Current DBX stance: do not add command wrappers until a workflow is frequent enough to justify them.

### Hooks

Hooks are useful for constraints that should not rely on model memory:

- destructive command blocks;
- required validation before stop;
- credential guardrails;
- state refresh before tool use.

Current DBX stance: do not add hooks in this repository until there is a specific host and a specific failure. Document the intended control first.

### Repo Instructions

Files like `AGENTS.md` or `CLAUDE.md` are appropriate for always-on repo rules, not task-specific workflows.

Good uses:

- coding style norms;
- prohibited operations;
- preferred package manager;
- project-wide validation commands;
- secret safety.

Bad uses:

- long task workflows that should be selectively activated;
- large domain references;
- deterministic checks that should be scripts.

### Generated Indexes

Generated indexes such as `llms.txt` or a skill inventory can support:

- human discovery;
- agent discovery;
- routing;
- installation review;
- collection governance.

They should summarize trigger boundaries. They should not duplicate full skill instructions.

### Planning and Memory Files

Planning files, progress files, ADRs, glossaries, and agent briefs are external state.

Use them for:

- long tasks;
- context window limits;
- handoff;
- repeated terminology alignment;
- preserving decisions.

Do not write private secrets, tokens, private machine paths, or hidden prompt-injection text into shared memory.

## 3. Portability Rule

Distinguish role from mechanism:

```text
Role: Completion Control
Mechanism in one host: stop hook
Mechanism in another host: validation command
Mechanism in a third host: explicit checklist in SKILL.md
```

DBX skills should stay portable unless the skill is intentionally host-specific, such as `dbx-goal-writer` and `dbx-subagent-context`.

## 4. When to Add Host Artifacts

Add a host artifact only when all are true:

1. There is a concrete recurring failure.
2. The host artifact is a better placement than `SKILL.md`, reference, script, or eval.
3. The host compatibility and fallback behavior are documented.
4. Security and external side effects are explicit.
5. There is at least one regression or manual check for the behavior.

No host artifact should exist just to make the repo look more advanced. A tiny skill collection can drown in shiny plumbing if the pipes arrive before the water.
