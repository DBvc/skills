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
| Review concrete PR/diff/staged/commit/file changes | `dbx-diff-review` | `dbx-linus-review`, unless strict pragmatic critique is explicit. |
| Run explicit bounded review-repair-revalidation on concrete code changes | `dbx-code-ratchet` | Read-only review skills or open-ended implementation workflows. |
| Audit repository/module architecture health, long-term decay, AI-coding operability, or anti-decay roadmap | `dbx-architecture-health` | `dbx-diff-review` for concrete changes; `dbx-technical-plan` for implementation planning; `dbx-linus-review` for strict proposal critique. |
| Judge architecture plans, data models, over-engineering, or explicit strict technical risk | `dbx-linus-review` | `dbx-diff-review`, unless a concrete diff target must be selected first. |
| Judge product, feature, PRD, UX, IA, content, implementation alignment, roadmap, or competitor correctness | `dbx-product-judgment` | `dbx-diff-review`, unless ordinary code-change review is primary; `dbx-decision-framing`, unless non-product trade-off dominates. |
| Judge or shape UI, flow, screenshot, prototype, PRD-to-design brief, component, design system, or code-backed interface design | `dbx-design-judgment` | Implementation/frontend coding skills when the user asks to edit files; `dbx-product-judgment` when product viability or business correctness dominates. |
| Make a high-impact real decision | `dbx-decision-framing` | `dbx-linus-review`, unless code/design evidence dominates. |
| Route noisy mixed inbox, saved content, tasks, ideas, signals, courses, tools, notes, or external-system metadata | `dbx-attention-routing` | Product-specific tagging/write workflows, unless adapter dry-run is requested. |
| Rewrite risky conversation or boundary message | `dbx-conversation-align` | `dbx-decision-framing`, unless real action trade-off dominates. |
| Create/review/improve/evaluate a skill | `dbx-skill-architect` | other runtime skills. |
| Audit installed or repository skill portfolios and recommend global/repo/explicit-only/disable/uninstall placement | Ask whether to manually run `dbx-skill-portfolio-auditor`; use it only when explicitly named or launched. | `dbx-skill-architect` for one skill's design or critique. |
| Create/start/audit Codex `/goal` contract | `dbx-goal-writer` | `dbx-skill-architect`, unless designing a reusable skill. |
| Set Codex subagent context inheritance strategy | `dbx-subagent-context` | generic coordination advice. |
| Create an AI agent/session restart packet for a future agent | `dbx-agent-handoff` | Human workplace handoff docs, onboarding docs, status reports, or meeting summaries. |
| Manually execute a Software Plan-First phase | The explicitly named `dbx-software-plan-first-*` phase skill | Any phase skill when the request is only ordinary planning, repo reading, or implementation. |
| Establish project memory, ADR, glossary, or long-lived project agent brief | No current runtime skill; direct answer or design one with `dbx-skill-architect`. | `dbx-agent-handoff`, unless the request is current-session continuation. |
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
| `dbx-diff-review` precedes commit/PR skills | Review concrete code-change risk before writing the final PR artifact when both are requested. |
| `dbx-diff-review` precedes `dbx-linus-review` for ambiguous concrete diffs | Establish staged/unstaged/branch/commit/file scope before applying strict pragmatic judgment. |
| `dbx-code-ratchet` composes `dbx-diff-review` and conditionally `dbx-linus-review` | Use only when the user explicitly asks for code ratchet or automatic review-repair-revalidation; it may modify code and must stop on direction failure or diverging risk. |
| `dbx-architecture-health` hands off to plan/review/repair skills | Use for read-only architecture decay diagnosis and anti-decay roadmap; do not silently switch to implementation planning, concrete diff review, or code changes. |
| `dbx-linus-review` handles explicit strict critique | Use it when the user asks for Linus-style, harsh, over-engineering, model, or merge/readiness judgment. |
| `dbx-product-judgment` handles product correctness judgment | Use it when a product artifact, target user/job, evidence boundary, or product decision dominates; route ordinary code diffs to `dbx-diff-review` and non-product trade-offs to `dbx-decision-framing`. |
| `dbx-design-judgment` handles design correctness and design shaping | Use it when a design surface, task path, IA, visual hierarchy, interaction states, visual system, accessibility, responsive behavior, or design handoff dominates; it may read code as design evidence but must not edit files. |
| `dbx-decision-framing` precedes `dbx-goal-writer` | Decide whether/what to do before writing a Codex execution contract. |
| `dbx-skill-architect` precedes new skill creation | Triage repeatability, stable task distribution, evaluability, safety, and placement. |
| `dbx-skill-portfolio-auditor` supports collection placement decisions | Use only after explicit/manual invocation for installed-skill portfolio audits; hand off single-skill creation, critique, or improvement to `dbx-skill-architect`. |
| `dbx-attention-routing` precedes product-specific tagging/write workflows | Route mixed inputs through the stable kernel before mapping to tags, task fields, note metadata, queues, or other external systems. |
| `dbx-subagent-context` supports Codex planning | Use only when Codex subagents or `fork_context` are explicit. |
| `dbx-agent-handoff` produces restart packets | Use for AI agent/session continuation, especially context compaction or "next session continues"; do not use for human-facing handoff documents. |
| `dbx-conversation-align` competes with `dbx-decision-framing` | Communication wording vs real-world trade-off. |
| `dbx-open-source-commit-pr` competes with `dbx-work-commit-pr` | Public OSS artifact vs internal work artifact. |
| `dbx-software-plan-first-plan-issue` handoff to `dbx-software-plan-first-ground-plan` | Use only after explicit invocation and only when repository facts are needed before finalizing a plan. |
| `dbx-software-plan-first-ground-plan` handoff to `dbx-software-plan-first-finalize-plan` | Grounding output supplies verified facts, source-of-truth boundaries, and validation candidates for plan finalization. |
| `dbx-software-plan-first-finalize-plan` precedes `dbx-software-plan-first-implement-feature` | A sealed `plan.md` / `tasks.md` workflow is required before review-gated implementation. |
| `dbx-software-plan-first-showhand` is the gated automation variant | It may continue across tasks only when decision completeness, grounding, validation, source-of-truth, and worktree-safety gates pass. |

## 3. Chaining Rules

### Review before PR writing

If the user asks to review concrete code changes and write PR text, run `dbx-diff-review` first, then write commit/PR artifacts from the final diff and accepted findings. If the user explicitly asks for strict pragmatic judgment, establish the diff target first and then apply `dbx-linus-review`.

### Code ratchet

Use `dbx-code-ratchet` only when the user explicitly asks for code ratchet, 棘轮自修, or automatic review-repair-revalidation on a concrete diff target. It is a bounded modifying workflow: it delegates review to `dbx-diff-review`, invokes `dbx-linus-review` for direction/complexity gates when needed, repairs only accepted local findings, and stops rather than continuing if direction or progress gates fail.

### Architecture health

Use `dbx-architecture-health` when the user asks for repository or module architecture health, long-term architecture decay, state/source-of-truth drift, validation topology gaps, or whether the repo is agent-operable for AI coding. It is read-only: route concrete PR/diff review to `dbx-diff-review`, strict critique of a proposed architecture plan to `dbx-linus-review`, implementation planning to `dbx-technical-plan`, and explicit bounded repair to `dbx-code-ratchet`.

### Decision before execution contract

If the user is unsure whether to do the work, use decision framing before writing a Codex goal.

### Product judgment

Use `dbx-product-judgment` when product correctness is the primary question: whether a product, feature, PRD, UX flow, IA, content, implementation, roadmap, or competitor position is coherent, valuable, usable, or worth building. If the task turns into ordinary concrete diff review, route that part to `dbx-diff-review`; if it turns into a high-impact non-product go/no-go decision, route to `dbx-decision-framing`.

### Design judgment

Use `dbx-design-judgment` when the design surface is the primary question: UI, flow, screenshot, prototype, PRD-to-design brief, component, design system, visual hierarchy, interaction states, responsive behavior, accessibility, or code-backed interface consistency. It is read-only and design-only: if the user asks to patch CSS/React or implement the design, route that execution to the appropriate coding/frontend workflow after producing a handoff. If the question is mainly product viability, business value, roadmap, or market positioning, route to `dbx-product-judgment`.

### Skill triage before skill creation

If the user asks to turn a one-off prompt into a skill, use skill-architect triage before full skill creation.

### Skill portfolio audit

`dbx-skill-portfolio-auditor` is explicit/manual-only. For generic cleanup or portfolio questions, ask whether the user wants to run it. Use it directly only when the user names the skill or launches it from the skill UI.

### Agent handoff

Use `dbx-agent-handoff` for AI-to-AI or session-to-session continuation packets. Ambiguous "handoff" or "交接文档" requests should get one clarification question because human workplace handoffs are out of scope.

### Conversation safety before wording

If there are threats, coercion, privacy invasion, legal/HR escalation, or severe power imbalance, use `dbx-conversation-align` safety path before any rewrite.

### Host verification before host-specific syntax

If the task depends on Codex `/goal`, subagents, or `fork_context`, consult `docs/DBX_CODEX_COMPATIBILITY.md` and avoid inventing syntax.

### Software Plan-First phases

The `dbx-software-plan-first-*` skills are manual-only and phase-specific. Do not infer them from phrases like "先计划", "plan-first", "读一下仓库", "按 tasks.md 做", or "一路做完" unless the user explicitly names the DBX-prefixed skill. When invoked, preserve the phase order: plan issue -> ground plan -> finalize plan -> implement feature, with showhand only as a stricter automation path.

## 4. Near-Miss Examples

| Prompt | Route |
| --- | --- |
| “帮我解释一下这个 PR 改了什么。” | Direct answer, not commit/PR skill unless artifact requested. |
| “帮我普通 review 一下 staged diff。” | `dbx-diff-review`. |
| “对 staged changes 跑 L2 代码棘轮，明确问题可以自动修，不要 commit。” | `dbx-code-ratchet`. |
| “帮我对这个仓库做一次架构健康体检，重点看长期腐化和 AI agent 风险。” | `dbx-architecture-health`. |
| “给 auth/cache 架构问题写具体 implementation plan。” | `dbx-technical-plan`, unless an architecture health audit is explicitly requested first. |
| “用 Linus 风格严厉判断这个 staged diff 能不能合。” | `dbx-diff-review` to establish target, then `dbx-linus-review`. |
| “帮我审一下这个架构方案有没有明显问题。” | `dbx-linus-review` if evidence/code/design risk dominates; `dbx-decision-framing` if trade-off dominates. |
| “这个功能从产品上到底对不对？” | `dbx-product-judgment`. |
| “这个截图为什么看起来很乱？只做设计评审，不要改代码。” | `dbx-design-judgment`. |
| “读这个 PRD，给我 IA、交互状态和设计交接，不要实现。” | `dbx-design-judgment`. |
| “我该不该做这个项目？” | `dbx-decision-framing`. |
| “帮我把这一堆收藏、课程、想法和任务分一下：哪些做、哪些存、哪些丢。” | `dbx-attention-routing`. |
| “帮我把这个 prompt 写好一点，只用一次。” | Direct answer, not `dbx-skill-architect` full skill. |
| “请使用 $dbx-skill-portfolio-auditor 审计我装的 skills。” | `dbx-skill-portfolio-auditor`. |
| “我装了太多 skills，帮我看看哪些该清理。” | Ask whether to manually run `dbx-skill-portfolio-auditor`; do not invoke it implicitly. |
| “下个 session 继续，帮我做个交接包。” | `dbx-agent-handoff`. |
| “帮我写一份给同事的项目交接文档。” | Direct workplace handoff doc, not `dbx-agent-handoff`. |
| “帮我写一句不那么冲的回复。” | `dbx-conversation-align` compact rewrite, not full diagnosis. |
| “这个需求先 plan-first 一下，别急着写代码。” | Direct planning or Plan mode behavior, not `dbx-software-plan-first-*` unless explicitly named. |
| “使用 $dbx-software-plan-first-ground-plan，只读确认仓库事实。” | `dbx-software-plan-first-ground-plan`. |
| “按 tasks.md 做下一个任务。” | Direct implementation unless `$dbx-software-plan-first-implement-feature` is explicitly named. |
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

## dbx-attention-routing routing note

Use `dbx-attention-routing` when the user asks to route a noisy collection of mixed inputs or build a reusable attention profile. It should run before any product-specific metadata/tagging/task/note write workflow.

Do not route ordinary summaries, explanations, recommendations, coding tasks, or single-topic research through this skill unless the user explicitly asks for attention allocation.

Product names and productivity methods are examples unless the user explicitly requests an adapter. Keep them in adapter manifests or profile config, not in the kernel.
