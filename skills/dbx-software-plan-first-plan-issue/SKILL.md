---
name: dbx-software-plan-first-plan-issue
description: Manual trigger only. Use only when the user explicitly names `dbx-software-plan-first-plan-issue`, `$dbx-software-plan-first-plan-issue`, or asks to manually trigger this exact DBX Software Plan-First proposal-shaping phase. Do not auto-trigger for ordinary planning, Plan mode, repository exploration, or implementation requests.
---

# DBX Software Plan-First Plan Issue

## DBX repository notes

- This repository uses the `dbx-` prefix for stable skills; use the prefixed skill names in handoffs and cross-skill routing.
- Keep this phase self-contained: load only the required references for the active phase, and do not pull sibling skill files unless the workflow explicitly hands off to that phase.

## Manual Trigger

- Manual trigger only.
- Use only when the user explicitly names `dbx-software-plan-first-plan-issue`, `$dbx-software-plan-first-plan-issue`, or says to use/trigger this exact skill.
- Do not auto-trigger for ordinary planning, Plan mode, plan-first, or "do not code yet" requests.

用于在 Plan mode 中形成 `proposal-ready` 的软件工程计划。适用于前端、后端、全栈、工具链、文档、配置和通用软件项目。

## 语义

- 这是对话中的 proposal shaping 阶段，不是 `dbx-plan-convergence` controller，也不是仓库探索阶段。
- 不读取仓库，不写 `plan.md`，不写 `tasks.md`，不执行实现。
- 不调用写文件、改代码、格式化、安装依赖、迁移、codegen 或自动修复工具。
- 当决策不完整时，输出 `clarifying` 或 `blocked`。
- 当决策完整时，输出 `proposal-ready`，并说明是否需要 `dbx-software-plan-first-ground-plan`。
- 输出本阶段结果后停止，不在同一轮继续执行 sibling phase；即使用户要求“顺手”读仓库、finalize 或 implement，也只给下一阶段 handoff。
- 所有沟通、计划摘要和过程说明使用中文。

## 必须读取

- `references/output-format.md`
- `references/plan-issue-rules.md`
- `references/control-model.md`
- `references/impact-profiles.md`

## 按需读取

- `references/artifact-evidence-boundary.md`
- `references/feedback-and-proof.md`
- `references/config.md`

## 工作流

1. 判断当前是否是 plan-oriented 协作。如果宿主环境没有明确 Plan mode，不要声称自己切换了模式。
2. 收敛 Goal、Scope、Approach、Validation、Plan Strategy。
3. 选择 Impact Profile：`frontend`、`backend`、`fullstack` 或 `generic`。
4. 填写相关 Impact Boundary。
5. 对 loop/hybrid、generated artifact、migration、batch、formal/destructive write、prototype、screenshot/trace/report 证据，要求 Artifact/Evidence Boundary。
6. 如果需要仓库事实，停止在 chat proposal，交给 `dbx-software-plan-first-ground-plan`。
7. 如果当前上下文已经包含足够事实：
   - 父 workflow 已选择 DBX implementation-bound planning profile 时，交给 external `dbx-plan-convergence`；
   - 未选择该 profile，且用户明确确认计划已收敛时，交给 `dbx-software-plan-first-finalize-plan`。
8. 输出本阶段 handoff 后停止，不在同一轮运行 sibling phase 或 controller。

## 输出

严格遵循 `references/output-format.md`。
