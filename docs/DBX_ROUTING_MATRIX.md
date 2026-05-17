# DBX Routing Matrix

This document is the repository-level routing policy for `DBvc/skills`.

It implements ASCT Activation Control and collection-level conflict resolution. It is not a normal README overview, and it is not loaded by every runtime skill.

Read it when:

- creating or modifying a skill;
- writing trigger evals;
- reviewing overlap between skills;
- answering “which skill should handle this?”;
- designing a multi-skill workflow.

## 1. Primary Intent Routing

| User primary intent | Prefer | Do not use first |
| --- | --- | --- |
| Write open-source commit/PR artifact | `dbx-open-source-commit-pr` | `dbx-linus-review`, unless review is requested. |
| Write work/internal commit/PR artifact | `dbx-work-commit-pr` | `dbx-open-source-commit-pr`. |
| Review concrete PR/diff/staged/commit/file changes | `dbx-diff-review-control` | `dbx-linus-review`, unless strict pragmatic critique is explicit. |
| Judge architecture plans, data models, over-engineering, or explicit strict technical risk | `dbx-linus-review` | `dbx-diff-review-control`, unless a concrete diff target must be selected first. |
| Make a high-impact real decision | `dbx-decision-framing` | `dbx-linus-review`, unless code/design evidence dominates. |
| Rewrite risky conversation or boundary message | `dbx-conversation-align` | `dbx-decision-framing`, unless real action trade-off dominates. |
| Create/review/improve/evaluate a skill | `dbx-skill-architect` | other runtime skills. |
| Create/start/audit Codex `/goal` contract | `dbx-goal-writer` | `dbx-skill-architect`, unless designing a reusable skill. |
| Control Codex subagent context inheritance | `dbx-subagent-context-control` | generic coordination advice. |
| Establish project memory, ADR, glossary, or agent brief | No current runtime skill; direct answer or design one with `dbx-skill-architect`. | `dbx-goal-writer`, unless writing a Codex goal. |
| Explicit multi-skill macro workflow | No current command layer; use this matrix and direct orchestration. | A single overloaded skill. |

## 2. Skill Graph Rules

```text
precedes: A should run before B
requires: B depends on output from A
competes: A and B are alternatives
fallback: use B if A cannot proceed
handoff: A produces a contract for B
```

Current graph:

| Relationship | Rule |
| --- | --- |
| `dbx-diff-review-control` precedes commit/PR skills | Review concrete code-change risk before writing the final PR artifact when both are requested. |
| `dbx-diff-review-control` precedes `dbx-linus-review` for ambiguous concrete diffs | Establish staged/unstaged/branch/commit/file scope before applying strict pragmatic judgment. |
| `dbx-linus-review` handles explicit strict critique | Use it when the user asks for Linus-style, harsh, over-engineering, model, or merge/readiness judgment. |
| `dbx-decision-framing` precedes `dbx-goal-writer` | Decide whether/what to do before writing a Codex execution contract. |
| `dbx-skill-architect` precedes new skill creation | Triage repeatability, stable task distribution, evaluability, safety, and placement. |
| `dbx-subagent-context-control` supports Codex planning | Use only when Codex subagents or `fork_context` are explicit. |
| `dbx-conversation-align` competes with `dbx-decision-framing` | Communication wording vs real-world trade-off. |
| `dbx-open-source-commit-pr` competes with `dbx-work-commit-pr` | Public OSS artifact vs internal work artifact. |

## 3. Chaining Rules

### Review before PR writing

If the user asks to review concrete code changes and write PR text, run `dbx-diff-review-control` first, then write commit/PR artifacts from the final diff and accepted findings. If the user explicitly asks for strict pragmatic judgment, establish the diff target first and then apply `dbx-linus-review`.

### Decision before execution contract

If the user is unsure whether to do the work, use decision framing before writing a Codex goal.

### Skill triage before skill creation

If the user asks to turn a one-off prompt into a skill, use skill-architect triage before full skill creation.

### Conversation safety before wording

If there are threats, coercion, privacy invasion, legal/HR escalation, or severe power imbalance, use `dbx-conversation-align` safety path before any rewrite.

### Host verification before host-specific syntax

If the task depends on Codex `/goal`, subagents, or `fork_context`, consult `docs/DBX_CODEX_COMPATIBILITY.md` and avoid inventing syntax.

## 4. Near-Miss Examples

| Prompt | Route |
| --- | --- |
| “帮我解释一下这个 PR 改了什么。” | Direct answer, not commit/PR skill unless artifact requested. |
| “帮我普通 review 一下 staged diff。” | `dbx-diff-review-control`. |
| “用 Linus 风格严厉判断这个 staged diff 能不能合。” | `dbx-diff-review-control` to establish target, then `dbx-linus-review`. |
| “帮我审一下这个架构方案有没有明显问题。” | `dbx-linus-review` if evidence/code/design risk dominates; `dbx-decision-framing` if trade-off dominates. |
| “我该不该做这个项目？” | `dbx-decision-framing`. |
| “帮我把这个 prompt 写好一点，只用一次。” | Direct answer, not `dbx-skill-architect` full skill. |
| “帮我写一句不那么冲的回复。” | `dbx-conversation-align` compact rewrite, not full diagnosis. |
| “我要开一个持续极简回答模式。” | Interaction-mode/stateful pattern; no current DBX runtime skill. Need activation/deactivation/lifetime. |
| “帮我做一个项目术语表，以后 agent 都按这个理解。” | Stateful project-memory pattern; direct artifact or future skill, not normal decision framing. |

## 5. Adding a New Skill

Before adding a skill, update this matrix if the new skill:

- overlaps with an existing skill;
- should precede or follow an existing skill;
- introduces host-specific commands or hooks;
- adds persistent state;
- changes install scope;
- deprecates or replaces another skill.

If you cannot state how the new skill interacts with the existing collection, you are not done designing it.
