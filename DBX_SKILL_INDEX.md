# DBX Skill Index

This file is the human-maintained map of the current DBX skill collection.

Update it when:

- a skill is added, renamed, deprecated, or removed;
- a trigger boundary changes;
- a skill gains or loses references, scripts, assets, or evals;
- routing relationships change;
- a compatibility or security risk changes.

## Maturity Scale

| Level | Meaning |
| --- | --- |
| L0 | Idea only. |
| L1 | Checklist or prompt. |
| L2 | Valid `SKILL.md`. |
| L3 | References/examples/rubrics separated. |
| L4 | Scripts/tools for fragile or deterministic work. |
| L5 | Trigger/output evals exist. |
| L6 | Baseline or old/new comparison exists. |
| L7 | Production regression, CI, compatibility, and release process. |

Maturity values below reflect current repository artifacts. All current stable skills include both `evals/triggers.json` and `evals/evals.json`, so they are listed as L5 unless a higher level is evidenced.

## Current Stable Skills

| Skill | Primary role | Shape | Maturity | Main risk | Routing note | Next useful improvement |
| --- | --- | --- | --- | --- | --- | --- |
| `dbx-open-source-commit-pr` | Public OSS commit/PR artifact writing. | procedure + writing | L5 | Diff facts still depend heavily on agent reading final change set. | Competes with `dbx-work-commit-pr`; use only for public/open-source context. | Add baseline comparison cases for no-skill/old-output behavior. |
| `dbx-work-commit-pr` | Internal/work commit and PR contract writing. | procedure + org workflow | L5 | Team-specific format and proof policy may not transfer. | Use for internal work artifacts; not for OSS PRs. | Parameterize team format in reference/config if reused outside current workflow. |
| `dbx-linus-review` | Strict pragmatic technical review. | review/procedure | L5 | Persona naming can invite tone drift; findings must stay evidence-based. | Precedes commit/PR skills when review and PR writing are both requested. | Consider eventual alias/name migration to `dbx-strict-pragmatic-review`; keep compatibility. |
| `dbx-skill-architect` | Create, critique, improve, evaluate, and triage skills. | meta | L5 | Context cost and over-engineering. | Precedes full skill creation; should not trigger for one-off prompt polish. | Add baseline comparison cases for old/no-skill skill-design outputs. |
| `dbx-conversation-align` | Diagnose stuck conversations and rewrite risky messages. | communication + safety + decision-lite | L5 | Over-triggering simple rewrites; over-structuring user-visible output. | Competes with `dbx-decision-framing`; use for wording, boundaries, relationship risk. | Add compact-output policy and near-miss evals for simple proofreading. |
| `dbx-decision-framing` | Frame high-impact real decisions. | decision | L5 | YAML/user-visible ceremony and over-analysis for low-stakes tasks. | Use before `dbx-goal-writer` when the task itself is not yet decided. | Hide boundary YAML by default for lightweight decisions; preserve internal self-check. |
| `dbx-subagent-context-control` | Control Codex subagent context inheritance. | coordination + host-specific | L5 | Codex feature drift and host portability. | Supports `dbx-goal-writer` only when Codex subagents or `fork_context` are explicit. | Keep `docs/DBX_CODEX_COMPATIBILITY.md` current. |
| `dbx-goal-writer` | Create, start, and audit Codex goal contracts. | procedure + host-specific | L5 | Codex `/goal` may be feature-gated or surface-dependent. | Use after decision is made; do not use for generic planning. | Add fixture tests for invented slash syntax and unsupported package mode. |

## Collection-Level Relationships

See `docs/DBX_ROUTING_MATRIX.md` and `docs/DBX_COLLECTION_DESIGN.md` for precedence and conflicts.

Important relationships:

- `dbx-linus-review` precedes commit/PR skills when review and PR writing are both requested.
- `dbx-decision-framing` precedes `dbx-goal-writer` when the work is not yet decided.
- `dbx-skill-architect` precedes new skill creation.
- `dbx-subagent-context-control` supports Codex planning only for explicit subagent context questions.
- `dbx-conversation-align` and `dbx-decision-framing` compete in some communication/choice scenarios; choose by primary intent.

## Future Skill Candidates

Do not add these until real repeated cases exist.

| Candidate | Why it may be useful | Evidence needed before creation |
| --- | --- | --- |
| `dbx-frontend-debug` | User has strong frontend background; ASCT includes a synthetic frontend-debug example; debugging has clear process/evidence/control surfaces. | 10 to 20 real bug cases showing baseline agent patch-stacking, weak root-cause loops, or false completion. |
| `dbx-project-memory` | Could preserve project glossary, ADRs, out-of-scope records, and agent briefs. | Repeated failures where agent forgets project terms or decisions despite current context. |
| `dbx-agent-handoff` | Could make long-running work transferable across agents/sessions. | Repeated handoff failures with missing state, validation, or next action. |

## Collection Priorities

1. Keep runtime skills lean and operational.
2. Improve evals by targeting historical failures, not marker-only structure.
3. Add scripts only for deterministic or fragile operations.
4. Maintain routing and compatibility docs when skills overlap or host behavior changes.
5. Avoid adding commands, hooks, or new skills until placement analysis shows they are the cheapest safe control.
