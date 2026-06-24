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
| `dbx-write` | Chinese-first viewpoint prose: technical blogs, personal essays, opinion articles, Markdown drafts, editing, and English transcreation. | taste + writing + evidence + light_tool | L5 | May over-trigger plain summaries, commit/PR text, product judgment, or interpersonal message rewriting; may also flatten author voice or invent facts/personal experience. | Use when the dominant artifact is viewpoint-driven prose; route commit/PR to commit skills, product/design judgment to judgment skills, interpersonal wording to `dbx-conversation-align`, and code/planning/review to software skills. | Add baseline comparisons from real drafts and tune anti-AI-smell cases after first 10 uses. |
| `dbx-read` | Source-grounded reading, extraction, deep read, comparison, and optional capture for explicit sources. | research + procedure + evidence + light_tool | L5 | Source extraction can be partial or host-dependent; can over-trigger `dbx-learn`, `dbx-write`, and attention routing. | Use for explicit source reading; route noisy queues to `dbx-attention-routing`, durable learning to `dbx-learn`, article writing to `dbx-write`, and concrete code/product/design decisions to matching DBX skills. | Add baseline cases after real URL/PDF/GitHub reading sessions; add host-specific ingestion scripts only when failure evidence justifies them. |
| `dbx-crystallize` | Pre-development requirement crystallization for fuzzy product/software ideas, feature requests, issue drafts, and stakeholder asks. | procedure + decision + coordination | L5 | Fake precision, over-questioning, and creep into product/design/technical judgment. | Use before product/design/technical planning when the primary task is clarifying requirements; route product-worth verdicts to `dbx-product-judgment`, UI/design correctness to `dbx-design-judgment`, technical implementation planning to `dbx-technical-plan`, and formal plan-first phases only when explicitly named. | Add baseline comparison after 10 real requirement discussions; tune blocking-question policy. |
| `dbx-diff-review` | Scoped concrete diff/PR/staged/commit/file review. | review/procedure + tool | L5 | Target ambiguity can still leak in if the user provides no artifact or mixed local state. | Use for ordinary concrete code-change review; establish target before any strict judgment or PR writing. | Add old/new baseline cases for staged-only and selected-file review. |
| `dbx-linus-review` | Strict pragmatic technical judgment for plans, models, over-engineering, and explicit hard reviews. | review/procedure | L5 | Persona naming can invite tone drift; findings must stay evidence-based and not displace ordinary diff target control. | Use for explicit strict/Linus/pragmatic critique; follows `dbx-diff-review` when strict judgment is requested on a concrete diff. | Consider eventual alias/name migration to `dbx-strict-pragmatic-review`; keep compatibility. |
| `dbx-technical-plan` | Evidence-grounded technical implementation planning before code changes. | planning/procedure + handoff | L5 | Can over-trigger into generic planning or invent repo facts when evidence is missing. | Use before implementation when the user asks for a technical plan; route strict critique to `dbx-linus-review`, concrete diffs to `dbx-diff-review`, and formal stateful plan-first work to `dbx-software-plan-first-*`. | Add baseline comparison cases after real planning sessions. |
| `dbx-code-ratchet` | 有界 concrete diff review-repair-revalidation 元技能。 | meta + workflow + tool | L5 | 自动修复可能放大错误方向，因此 direction/progress gates 必须优先于 repair。 | Use only when explicitly asked for code ratchet / 棘轮自修; composes `dbx-diff-review`, conditionally `dbx-linus-review`, and Codex subagent context isolation. | Add baseline old/new evals from real failed AI repair loops after trial use. |
| `dbx-architecture-health` | Read-only repository/module architecture health audit for long-term decay, state ownership drift, validation topology, and AI-coding operability. | architecture audit + evidence map + tool | L5 | Can over-trigger into concrete PR review or generic architecture advice if scope/evidence gates are skipped. | Use for repo/module health and anti-decay roadmap; route concrete diffs to `dbx-diff-review`, strict plan critique to `dbx-linus-review`, implementation planning to `dbx-technical-plan`, and bounded repair to `dbx-code-ratchet`. | Add baseline comparison cases after real repo audits. |
| `dbx-skill-architect` | Create, critique, improve, evaluate, and triage skills. | meta | L5 | Context cost and over-engineering. | Precedes full skill creation; should not trigger for one-off prompt polish. | Add baseline comparison cases for old/no-skill skill-design outputs. |
| `dbx-skill-portfolio-auditor` | Audit installed skill portfolios and recommend global, project, explicit-only, disable, uninstall, or merge placement. | meta + collection workflow + tool | L5 | Usage evidence and privacy boundaries can be weak if the user does not provide data. | Explicit/manual trigger for portfolio optimization; routes single-skill creation or critique to `dbx-skill-architect`. | Add baseline comparison with a real local portfolio audit after first use. |
| `dbx-product-judgment` | Evidence-bounded judgment of whether a product, feature, PRD, live UX, IA, interaction, content, implementation, roadmap, or competitor position is product-correct. | decision + product audit + research + implementation alignment | L5 | Unsupported certainty when target user, product artifact, or evidence boundary is missing. | Use for product/feature correctness judgment; hand off ordinary concrete diff review to `dbx-diff-review` and high-impact go/no-go trade-offs to `dbx-decision-framing` when product artifacts do not dominate. | Add baseline comparison cases after several real audits. |
| `dbx-design-judgment` | Evidence-bounded design judgment, audit, critique, PRD-to-design brief, screenshot review, code-backed interface alignment, and design system review. | design audit + taste/craft + handoff | L5 | Role creep into implementation, unsupported taste claims, and product-strategy overreach. | Use when a UI/flow/screenshot/prototype/PRD/design system/interface design surface dominates; route product viability to `dbx-product-judgment` and implementation/code changes to coding/frontend workflows. | Add baseline comparison cases after several real design reviews. |
| `dbx-attention-routing` | Mixed inbox / information / idea / task attention routing | Stable kernel routes: `act_now`, `build`, `test`, `track`, `store`, `incubate`, `drop`, `guard`, `clarify`; optional profile and adapter mapping | L5 | Product-specific tags, collectors, and productivity methods can leak into the kernel if adapter/profile boundaries are not enforced. | Use before product-specific tagging or task/note metadata changes; dry-run external writes. | Add baseline comparison cases for noisy inbox routing without profile vs profile-assisted routing. |
| `dbx-learn` | Durable learning, source-grounded study, practice reps, review, and optional learning records. | learning + research + interaction + state-lite | L5 | Over-triggering ordinary explanations or summaries; state drift if learning records are written too eagerly. | Use when the user wants capability change, practice, review, or a learning workspace; route skill creation to `dbx-skill-architect`, mixed content routing to `dbx-attention-routing`, and direct implementation/review to coding skills. | Add baseline comparisons after real learning sessions. |
| `dbx-conversation-align` | Diagnose stuck conversations and rewrite risky messages. | communication + safety + decision-lite | L5 | Over-triggering simple rewrites; over-structuring user-visible output. | Competes with `dbx-decision-framing`; use for wording, boundaries, relationship risk. | Add compact-output policy and near-miss evals for simple proofreading. |
| `dbx-decision-framing` | Frame high-impact real decisions. | decision | L5 | YAML/user-visible ceremony and over-analysis for low-stakes tasks. | Use before `dbx-goal-writer` when the task itself is not yet decided. | Hide boundary YAML by default for lightweight decisions; preserve internal self-check. |
| `dbx-subagent-context` | Set Codex subagent context inheritance strategy. | coordination + host-specific | L5 | Codex feature drift and host portability. | Supports `dbx-goal-writer` only when Codex subagents or `fork_context` are explicit. | Keep `docs/DBX_CODEX_COMPATIBILITY.md` current. |
| `dbx-goal-writer` | Create, start, and audit Codex goal contracts. | procedure + host-specific | L5 | Codex `/goal` may be feature-gated or surface-dependent. | Use after decision is made; do not use for generic planning. | Add fixture tests for invented slash syntax and unsupported package mode. |
| `dbx-agent-handoff` | Create restart handoffs for future AI agent sessions. | coordination + handoff | L5 | Ambiguous "handoff" requests can be confused with human workplace handoff docs; stale or overbroad context can mislead the next agent. | Use only for AI agent/session continuation; ask one clarification on ambiguous handoff requests; not for human status docs. | Add regression cases from real session resumes. |
| `dbx-software-plan-first-plan-issue` | Manual-only Software Plan-First chat convergence before repository grounding. | procedure + coordination + stateful workflow | L5 | Wrong trigger could turn ordinary planning into ceremonial workflow. | Use only when explicitly named; precedes `dbx-software-plan-first-ground-plan` or `dbx-software-plan-first-finalize-plan`. | Add baseline comparison after first real issue workflow. |
| `dbx-software-plan-first-ground-plan` | Manual-only read-only grounding of project facts, rules, source-of-truth, surfaces, and validation. | procedure + knowledge + tool | L5 | Scanner hints may be mistaken for verified facts. | Follows `dbx-software-plan-first-plan-issue`; hands off to `dbx-software-plan-first-finalize-plan`. | Add fixture repo for grounding output regression. |
| `dbx-software-plan-first-finalize-plan` | Manual-only writing of Chinese `plan.md` and `tasks.md`, plus workflow seal. | procedure + stateful workflow + tool | L5 | Incomplete decisions may be sealed as if final. | Follows plan convergence and grounding; precedes implementation. | Add structural checker for generated `plan.md` / `tasks.md` examples. |
| `dbx-software-plan-first-implement-feature` | Manual-only review-gated execution of exactly one current unfinished task. | procedure + tool + stateful workflow | L5 | Scope creep across tasks or bypassed validation/review. | Follows sealed plan; use instead of showhand when user review is needed after each task. | Add fixture workflow with failed validation and dirty worktree cases. |
| `dbx-software-plan-first-showhand` | Manual-only safe automatic execution of the full plan-first workflow when all gates pass. | procedure + coordination + stateful workflow | L5 | Automation may continue through subjective, destructive, or under-specified work. | Use only when explicitly named and all decision/source-of-truth/validation/worktree gates pass. | Add safety evals for destructive writes and product/design uncertainty. |

## Collection-Level Relationships

See `docs/DBX_ROUTING_MATRIX.md` and `docs/DBX_COLLECTION_DESIGN.md` for precedence and conflicts.

Important relationships:

- `dbx-code-ratchet` is explicit-only and may modify code. It composes `dbx-diff-review` for primary review/re-review and conditionally `dbx-linus-review` for direction/complexity gates. It should not replace read-only review or open-ended implementation workflows.
- `dbx-architecture-health` diagnoses repository/module architecture decay as a read-only audit. It hands off concrete diffs to `dbx-diff-review`, strict proposal critique to `dbx-linus-review`, implementation plans to `dbx-technical-plan`, and bounded repair to `dbx-code-ratchet`.
- `dbx-technical-plan` handles lightweight, stateless technical planning before implementation; route existing-plan critique to `dbx-linus-review`, concrete diffs to `dbx-diff-review`, and formal persistent workflows to `dbx-software-plan-first-*`.
- `dbx-diff-review` handles ordinary concrete diff/PR/staged/commit/file review and precedes commit/PR skills when review and PR writing are both requested.
- `dbx-linus-review` handles explicit strict pragmatic critique; for concrete diffs, establish scope with `dbx-diff-review` first when target ambiguity matters.
- `dbx-write` handles viewpoint-driven prose artifacts. It should not preempt commit/PR skills, product/design judgment, conversation alignment, code review, technical planning, or plain summarization. If factual/current claims dominate the writing task, it must use current sources or mark claims unverified.
- `dbx-read` handles explicit source-bound reading, extraction, comparison, deep-read, and optional local capture. It can precede `dbx-learn`, `dbx-write`, or judgment/planning skills when a source digest is needed, but should not replace their dominant artifacts.
- `dbx-crystallize` turns fuzzy product/software intent into a bounded requirement contract before product/design/technical planning or implementation. It should hand off product-worth verdicts to `dbx-product-judgment`, design correctness to `dbx-design-judgment`, technical implementation planning to `dbx-technical-plan`, and formal plan-first phases only when explicitly named.
- `dbx-decision-framing` precedes `dbx-goal-writer` when the work is not yet decided.
- `dbx-skill-architect` precedes new skill creation.
- `dbx-skill-portfolio-auditor` handles installed-skill portfolio optimization; hand off single-skill design, critique, or improvement to `dbx-skill-architect`.
- `dbx-product-judgment` handles product-correctness judgment when a product artifact, target user/job, evidence boundary, or product decision is in scope; route ordinary code diff review to `dbx-diff-review` and non-product high-impact trade-offs to `dbx-decision-framing`.
- `dbx-design-judgment` handles design-correctness judgment when a UI surface, flow, screenshot, prototype, PRD-to-design brief, design system, or code-backed interface design question is in scope; it is design-only and should hand off implementation without editing files.
- `dbx-attention-routing` handles mixed inbox/information/idea/task attention routing before product-specific tagging or external metadata writes.
- `dbx-learn` handles durable learning, source-grounded study, practice reps, review, and optional learning records. It should not replace ordinary summarization, direct coding/debugging/review, skill creation, or mixed inbox routing.
- `dbx-subagent-context` supports Codex planning only for explicit subagent context questions.
- `dbx-agent-handoff` handles AI agent/session continuation packets; do not use it for human workplace handoff docs or general summaries.
- `dbx-conversation-align` and `dbx-decision-framing` compete in some communication/choice scenarios; choose by primary intent.
- `dbx-software-plan-first-*` skills form a manual-only phase chain: plan issue -> ground plan -> finalize plan -> implement one task, with showhand as the gated automation variant.
- Do not route ordinary planning, repository reading, or implementation into `dbx-software-plan-first-*` unless the user explicitly names the DBX-prefixed phase skill.

## Future Skill Candidates

Do not add these until real repeated cases exist.

| Candidate | Why it may be useful | Evidence needed before creation |
| --- | --- | --- |
| `dbx-frontend-debug` | User has strong frontend background; ASCT includes a synthetic frontend-debug example; debugging has clear process/evidence/control surfaces. | 10 to 20 real bug cases showing baseline agent patch-stacking, weak root-cause loops, or false completion. |
| `dbx-project-memory` | Could preserve project glossary, ADRs, out-of-scope records, and agent briefs. | Repeated failures where agent forgets project terms or decisions despite current context. |

## Collection Priorities

1. Keep runtime skills lean and operational.
2. Improve evals by targeting historical failures, not marker-only structure.
3. Add scripts only for deterministic or fragile operations.
4. Maintain routing and compatibility docs when skills overlap or host behavior changes.
5. Avoid adding commands, hooks, or new skills until placement analysis shows they are the cheapest safe control.
