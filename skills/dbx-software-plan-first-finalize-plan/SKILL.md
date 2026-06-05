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
- 写入中文 `plan.md` 和 `tasks.md`。
- 运行 `scripts/issue-workflow.sh seal <issue-id>` 建立 seal。
- 计划过程产物固定写入 `.plan-first/issues/<issue-id>/`，不作为提交产物。
- 是否自动提交以及提交格式由 `.plan-first/config.toml` 控制。

## 必须读取

- `references/workflow-rules.md`
- `references/plan-template.md`
- `references/tasks-template.md`
- `references/config.md`
- `references/impact-profiles.md`
- `references/artifact-evidence-boundary.md`

## 工作流

1. 运行：

```sh
scripts/issue-workflow.sh init <issue-id>
```

2. 用中文填写 `plan.md` 和 `tasks.md`。
3. 确认 `tasks.md` 每个任务包含：`验收:`、`验证:`，以及必要的 `使用检查:`、`依赖:`、`约束:`。
4. 运行：

```sh
scripts/issue-workflow.sh seal <issue-id>
```

5. 报告 workspace root、计划文件位置、配置模式、任务数量和下一步执行命令。

## 禁止事项

- 不在决策不完整时写计划。
- 不把项目特定规则写进通用 skill；只把本仓库 grounding 到的规则写进本 issue 计划。
- 不跳过 seal。
- 不在 finalize 阶段实现代码。

## 输出

用中文说明：workspace root、计划文件位置、任务数量、影响画像、验证模型、配置模式、下一步执行命令。
