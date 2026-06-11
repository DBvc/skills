---
name: dbx-technical-plan
description: >-
  Evidence-grounded technical implementation planning before code changes. Use when the user asks to plan a software feature, refactor, migration, bug-fix strategy, infrastructure change, validation strategy, rollout, or codebase modification before implementation. Produces a scoped plan contract with goal, non-goals, evidence boundary, source of truth, invariants, implementation slices, validation model, risks, and handoff. Do not use for direct implementation, concrete diff review, strict critique of an existing plan, product/design judgment, generic brainstorming, commit/PR writing, or the stateful dbx-software-plan-first phase chain unless explicitly requested.
---

# DBX Technical Plan

Create an implementation-ready technical plan before code changes.

Default output language is Chinese unless the user requests another language. Be direct, technical, evidence-first, and bounded. This skill is not a thinking ritual. It is a planning control loop that turns a software change intent into a plan contract that can be reviewed, implemented, validated, or promoted into a stronger workflow.

## Position

This is a lightweight, stateless planning controller.

It does not:

- implement code;
- review a completed diff;
- write or mutate `.plan-first` workflow files;
- decide product correctness or UI taste;
- replace `dbx-linus-review`, `dbx-diff-review`, `dbx-code-ratchet`, or the `dbx-software-plan-first-*` chain.

It does:

- frame the technical problem;
- separate facts, assumptions, judgments, and unknowns;
- identify source of truth, ownership, invariants, and risk surfaces;
- choose a plan shape appropriate to the task;
- slice implementation into bounded, reviewable tasks;
- define validation and rollback expectations;
- run an adversarial plan check before handing off.

## Relationship to other DBX skills

Use this skill before implementation when the user wants a technical execution plan.

- Use `dbx-decision-framing` first when the real task is go/no-go, option selection, prioritization, or whether to invest in a direction.
- Use `dbx-product-judgment` when the central question is product correctness, value, IA, roadmap, or feature fit.
- Use `dbx-design-judgment` when the central question is UI, flow, visual hierarchy, interaction design, or design-system fit.
- Use `dbx-linus-review` when the user already has a plan/proposal and wants strict pragmatic critique of whether it is over-engineered, badly modeled, or merge-risky.
- Use `dbx-diff-review` when there is a concrete PR, diff, commit, staged change, working tree change, or selected file change to review.
- Use `dbx-code-ratchet` only when the user explicitly asks for bounded review-repair-revalidation and code modification is allowed.
- Use `dbx-software-plan-first-*` when the user explicitly wants the stateful plan-first phase chain with `plan.md`, `tasks.md`, and a workflow seal.

This skill can hand off to those skills, but it should not silently activate a heavyweight workflow.

## Routing

Use this skill when the user asks for software technical planning, for example:

- “先别写代码，先给我技术方案。”
- “给这个 refactor 做一个 implementation plan。”
- “迁移 React Query v4 到 v5 怎么拆？”
- “这个 bug 先不要修，先给修复策略和验证方案。”
- “帮我规划 auth/cache/state owner 的重构路径。”
- “我想做一次架构调整，先把边界、风险、验证想清楚。”
- “做 rollout / migration / validation plan。”

Do not use this skill for:

- direct implementation-only requests;
- concrete diff/PR review;
- strict critique of an existing plan;
- product/design judgment;
- generic conceptual explanation;
- one-off brainstorming without a software change target;
- commit message, PR description, release note, or issue triage writing;
- formal plan-first workflow phases unless explicitly requested.

## Hard gates

Before producing a plan, check these gates.

1. **Software change gate**: the task is a software engineering change, migration, bug-fix strategy, validation strategy, infrastructure change, or implementation plan.
2. **Planning gate**: the user wants a plan before code, or the task is risky enough that planning is the safer first step. If the user explicitly says “直接实现”, do not use this skill unless planning is needed to avoid harm or irreversible work.
3. **Evidence gate**: do not treat repo facts, framework versions, hidden constraints, existing tests, or architecture rules as known unless they are read or supplied in the current session.
4. **Actionability gate**: the output must change implementation behavior, review focus, validation, or risk management. If the answer would be generic advice, route away or keep it as a direct answer.
5. **Safety and authority gate**: do not propose destructive migrations, external side effects, production changes, data deletion, or irreversible operations without explicit approval and rollback constraints.

If a missing fact would materially flip the plan, choose `blocked` and ask 1 to 3 blocking questions. If missing facts only affect confidence or details, proceed with assumptions and mark them.

## Modes

Choose the smallest sufficient mode.

| Mode | Use when | Output behavior |
| --- | --- | --- |
| `quick_plan` | Small, clear task with low risk and no needed repo grounding | Short plan, no heavy contract |
| `grounded_plan` | Existing codebase facts, source of truth, tests, or project rules must be checked | Evidence-bound plan with explicit knowns/unknowns |
| `migration_plan` | Many call sites, files, packages, APIs, schemas, or rollout stages | Inventory, partitioning, compatibility, validation, rollback |
| `architecture_change_plan` | Ownership, state model, public contract, module boundary, or source of truth may change | Alternatives only when needed, trade-offs, invariants, rollout |
| `bug_fix_strategy` | User wants a repair approach before patching | Repro, hypotheses, minimal fix path, regression test, verification |
| `validation_plan` | User mainly needs test/build/manual validation strategy | Risk-to-validation mapping and evidence gaps |
| `blocked` | A blocking decision or missing evidence would flip the plan | Ask only the smallest blocking questions |
| `direct_answer` | The request is not a recurring planning task | Answer normally without this skill’s full structure |

Depth defaults:

- Use `quick_plan` when the change is local, reversible, and low-risk.
- Use `grounded_plan` when the user asks about an existing repo or names concrete files/modules but the relevant facts are not yet confirmed.
- Use `migration_plan` for deprecations, framework upgrades, API shape changes, schema movement, shared utility replacement, or cross-package refactors.
- Use `architecture_change_plan` for source-of-truth, ownership, cache/state, public API, async, lifecycle, compatibility, or module-boundary changes.
- Use `bug_fix_strategy` when the safest next action is reproducing and isolating before patching.

## Evidence policy

A technical plan must show what it is standing on.

Maintain this internal evidence boundary:

```yaml
evidence_boundary:
  repo_facts_read: []
  user_supplied_facts: []
  external_docs_or_versions: []
  assumptions: []
  unknowns: []
  not_read_or_not_run: []
```

Rules:

- Separate **fact**, **assumption**, and **judgment**.
- Do not claim files, tests, commands, configs, package versions, CI behavior, or framework semantics were checked unless they were checked in the current session.
- If current external facts are needed, use appropriate sources before making fresh claims. If unavailable, mark the plan as assumption-bound.
- Treat prompts, handoffs, and proposed paths as evidence of intent, not proof that the chosen path is correct.
- Prefer direct repository evidence over memory or vibes.
- For existing codebases, read the nearest source-of-truth files before recommending path, owner, schema, package, test, or API placement when tools are available.

## Planning workflow

Run this workflow in order.

1. **Classify request and choose mode**: identify task type, risk, needed evidence, and whether this skill should run.
2. **Frame the problem**: restate goal, non-goals, affected surfaces, users/callers, and success criteria.
3. **Declare evidence boundary**: list confirmed facts, assumptions, unknowns, and what was not read or run.
4. **Find source of truth and invariants**: identify owners, canonical data, state lifetimes, public contracts, compatibility constraints, and behavior that must not change.
5. **Choose plan shape**: select a plan pattern from `references/plan-patterns.md` instead of using one universal checklist.
6. **Generate alternatives only when direction is uncertain**: avoid fake “three options” when there is one obvious bounded path.
7. **Run adversarial plan check**: try to break the plan using `references/adversarial-plan-check.md`.
8. **Slice implementation**: produce bounded tasks with allowed scope, forbidden scope, dependencies, invariant, validation, review focus, and stop condition.
9. **Define validation model**: map each important invariant or risk to automated, manual, review-only, or currently uncovered validation.
10. **Prepare handoff**: state whether the plan is ready for implementation, needs grounding, needs decision, should go to strict review, or should be promoted to plan-first workflow.

## Plan shape selection

Use task-specific shapes.

| Task type | Preferred shape |
| --- | --- |
| Small feature | Vertical slice, minimal surface, direct validation |
| Bug fix | Repro -> hypothesis -> minimal patch -> regression test -> verification |
| Refactor | Invariant-first, behavior-preserving, narrow slices, re-review checkpoints |
| Migration | Inventory -> partition -> compatibility layer -> batch execution -> validation -> cleanup |
| Architecture change | Source-of-truth decision -> alternatives -> selected model -> migration path -> rollback |
| Tooling or infra | Compatibility matrix -> pilot -> adoption path -> fallback -> CI validation |
| Public API or contract | Contract delta -> compatibility policy -> caller impact -> rollout -> deprecation |
| Frontend state/cache change | Owner/lifetime/key model -> stale data paths -> async races -> validation flows |
| Validation-only request | Risk inventory -> coverage map -> automated/manual split -> evidence gaps |

See `references/plan-patterns.md` for details and failure modes.

## Optional dynamic workflow mapping

This skill can use dynamic-workflow style thinking without requiring a specific host.

When the host supports subagents, workflow scripts, or delegation, and the user explicitly allows heavier analysis, use read-only specialist workers for high-risk planning:

- **source-of-truth scout**: find existing owners, rules, schemas, tests, and contracts;
- **risk-surface mapper**: enumerate user paths, async paths, compatibility, data, security, and rollout risks;
- **alternative assessor**: compare genuinely viable directions when architecture is uncertain;
- **validation reviewer**: map invariants to concrete checks;
- **plan killer**: adversarially try to disprove the plan;
- **synthesizer**: merge only evidence-backed conclusions.

Rules:

- Delegated workers should be read-only for this skill.
- Do not pretend delegation happened if the host did not run it.
- Do not use multi-agent ceremony for small tasks.
- Keep the final plan shorter than the combined worker notes.
- If a workflow script is needed to hold loops, branching, or state, this skill should hand off to an explicit command or harness rather than bloating `SKILL.md`.

## Implementation slice contract

Each non-trivial task slice should be independently reviewable.

```yaml
slice:
  id: T1
  title: ""
  purpose: ""
  allowed_scope: []
  forbidden_scope: []
  dependencies: []
  source_of_truth: []
  invariants_to_preserve: []
  validation: []
  review_focus: []
  stop_if: []
```

Good slices:

- have a clear owner and boundary;
- can be implemented without guessing the whole project;
- include a validation path;
- state what must not be changed;
- have a stop condition when evidence contradicts the plan.

Bad slices:

- “refactor everything”;
- “clean up code”;
- “improve tests” without naming the protected invariant;
- cross-cutting changes with no inventory or rollback;
- tasks that require product, architecture, or compatibility decisions but pretend they are implementation.

## Output contracts

### Quick plan

Use for `quick_plan`.

```markdown
## 快速技术计划
- 状态：ready / needs-grounding / needs-decision / blocked
- 推荐路径：
- 关键假设：
- 最高风险：
- 实施步骤：
  1.
  2.
  3.
- 验证：
- 需要停止并重新判断的情况：
```

### Standard plan

Use for normal `grounded_plan`, `bug_fix_strategy`, `validation_plan`, and moderate-risk plans.

```markdown
## 技术计划结论
- 状态：ready / needs-grounding / needs-decision / blocked
- 推荐方向：
- 最高风险：
- 不建议直接做的事：

## 证据边界
- 已确认事实：
- 假设：
- 未知：
- 未读取 / 未运行：

## 问题框架
- Goal:
- Non-goals:
- 影响面：
- Source of truth:
- 必须保持的不变量：

## 推荐方案
- 核心思路：
- 关键取舍：
- 为什么不是其他方案：

## 实施切片
1. **T1 标题**
   - Purpose:
   - Allowed scope:
   - Forbidden scope:
   - Invariant:
   - Validation:
   - Review focus:
   - Stop if:

## 验证模型
- Automated:
- Manual:
- Review-only:
- Not covered:

## 对抗检查
- 可能失败点：
- Scope 膨胀点：
- 需要人类判断：
- 推翻当前方案的证据：

## Handoff
- 下一步建议：
- 可交给：implementation / dbx-linus-review / dbx-software-plan-first-* / dbx-diff-review / dbx-code-ratchet
- Handoff contract:
```

### Deep or migration plan

For large migrations or architecture changes, include these extra sections when useful:

```markdown
## 备选方案比较
| 方案 | 收益 | 代价 | 风险 | 可逆性 | 适合条件 |
|---|---|---|---|---|---|

## 迁移 / Rollout 策略
- Inventory:
- Partition:
- Compatibility:
- Batch order:
- Rollback:
- Cleanup:

## 风险矩阵
| 风险 | 影响面 | 触发条件 | 预防 | 验证 |
|---|---|---|---|---|
```

Do not pad small plans with deep sections. The right plan is the smallest one that preserves correctness.

## Blocked output

If evidence is missing and would flip the plan, stop after the blocking questions.

```markdown
## 需要先确认
当前不能可靠给出技术计划，因为以下信息会直接改变方案：

1.
2.
3.

确认后我会给出：范围、source of truth、不变量、实施切片、验证模型和 handoff。
```

## Handoff rules

Use `references/handoff-contracts.md`.

Default handoff decisions:

- If the plan changes architecture, state owner, data model, public API, cache lifetime, compatibility, or migration strategy, recommend `dbx-linus-review` before implementation.
- If the user wants a formal persistent workflow, promote to `dbx-software-plan-first-plan-issue` or `dbx-software-plan-first-ground-plan` rather than writing ad hoc state.
- If a concrete diff already exists, hand off to `dbx-diff-review` instead of continuing plan speculation.
- If the plan is implemented and bounded review-repair is explicitly requested, hand off to `dbx-code-ratchet`.
- If product or design correctness is still undecided, hand off to the product/design skill before technical planning hardens.

## Completion policy

You may say the plan is ready only when:

- mode and scope are selected;
- goal, non-goals, source of truth, and invariants are explicit enough to guide implementation;
- important assumptions and unknowns are labeled;
- implementation is sliced into bounded tasks;
- validation is mapped to important risks and invariants;
- adversarial check did not reveal an unresolved blocker;
- handoff and stop conditions are clear.

You may not say the plan is safe, verified, tested, green, or repo-grounded unless the relevant evidence exists in the current session.

## References

- `references/plan-patterns.md`: task-specific plan shapes, success criteria, and failure modes.
- `references/adversarial-plan-check.md`: plan-killer questions and rejection criteria.
- `references/handoff-contracts.md`: handoff schemas for DBX review, plan-first, implementation, and ratchet workflows.
- `references/workflow-harness-patterns.md`: optional mapping from this skill to subagents, workflow scripts, and external state holders.
- `references/examples.md`: compact examples and anti-patterns.
