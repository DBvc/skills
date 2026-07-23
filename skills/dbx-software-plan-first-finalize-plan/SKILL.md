---
name: dbx-software-plan-first-finalize-plan
description: Manual trigger only. Use only when the user explicitly names `dbx-software-plan-first-finalize-plan`, `$dbx-software-plan-first-finalize-plan`, or asks to manually trigger this exact DBX Software Plan-First plan finalization phase. Do not auto-trigger for ordinary plan writing, finalize, seal, or implementation requests.
---

# DBX Software Plan-First Finalize Plan

## DBX repository notes

- This repository uses the `dbx-` prefix for stable skills; use the prefixed skill names in handoffs and cross-skill routing.
- Keep this phase self-contained: load only the required references for the active phase, and do not pull sibling skill files unless the workflow explicitly hands off to that phase.

## Manual Trigger

- Manual trigger only.
- Use only when the user explicitly names `dbx-software-plan-first-finalize-plan`, `$dbx-software-plan-first-finalize-plan`, or says to use/trigger this exact skill.
- Do not auto-trigger for ordinary plan writing, `plan.md/tasks.md`, finalize, seal, or plan-first requests.

用于把已经收敛的计划写入过程产物，并建立 workflow seal。

## 语义

- 只能在 Goal、Scope、Approach、Validation、Plan Strategy、Impact Profile、Impact Boundary 已完整时使用。
- 如果需要仓库事实但尚未 grounding，先交给 `dbx-software-plan-first-ground-plan`。
- 如果当前调用来自已选择 DBX implementation-bound planning profile 的父 workflow，必须提供与当前 proposal version/fingerprint 匹配的 `dbx-plan-convergence` `ready-for-handoff` 结果，才可写 `plan.md`、`tasks.md` 和 seal。
- 如果用户直接显式调用本 skill，且明确确认当前计划已经收敛，现有 Mandatory Decision Gate、grounding、ownership、validation 和 artifact boundary 全部满足，则不强制制造新的 convergence run。
- 如果计划会新增、移动或固定 source/config/test/doc 产物，产物归属必须已经由项目事实或用户确认支持；归属未定时不要 seal，先返回 grounding 或澄清。
- 写入中文 `plan.md` 和 `tasks.md`。
- 运行 `scripts/issue-workflow.sh seal <issue-id>` 建立 seal。
- 计划过程产物固定写入 `.plan-first/issues/<issue-id>/`，不作为提交产物；若 `.plan-first/config.toml` 显式配置 `plan_docs.mode = "tracked"`，只提交同步到项目文档路径的 `plan.md` 和 `tasks.md` 副本。
- 是否自动提交以及提交格式由 `.plan-first/config.toml` 控制。

## 必须读取

- `references/workflow-rules.md`
- `references/plan-template.md`
- `references/tasks-template.md`
- `references/config.md`
- `references/impact-profiles.md`
- `references/artifact-evidence-boundary.md`

## 工作流

1. 如果父 workflow 选择了 implementation-bound planning profile，先校验 convergence receipt 与当前 proposal identity 匹配；缺失、stale 或 mismatch 时不运行 `init`、不写文件、不 seal，返回 external `dbx-plan-convergence`。
2. 运行：

```sh
scripts/issue-workflow.sh init <issue-id>
```

3. 用中文填写 `plan.md` 和 `tasks.md`。
4. 确认 `tasks.md` 每个任务包含：`验收:`、`验证:`，以及必要的 `使用检查:`、`依赖:`、`约束:`。会新增或迁移产物的任务，必须在 `约束:` 中写明产物归属、依据和禁止误放的边界。
5. 运行：

```sh
scripts/issue-workflow.sh seal <issue-id>
```

6. 报告 workspace root、计划文件位置、配置模式、任务数量和下一步执行命令。

## 禁止事项

- 不在决策不完整时写计划。
- 不在 selected profile 的 current convergence receipt 缺失、stale 或 identity mismatch 时写计划或 seal。
- 不把项目特定规则写进通用 skill；只把本仓库 grounding 到的规则写进本 issue 计划。
- 不跳过 seal。
- 不在 finalize 阶段实现代码。

## 输出

用中文说明：workspace root、计划文件位置、任务数量、影响画像、验证模型、配置模式、下一步执行命令。
