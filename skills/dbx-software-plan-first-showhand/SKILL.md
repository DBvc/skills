---
name: dbx-software-plan-first-showhand
description: Manual trigger only. Use only when the user explicitly names `dbx-software-plan-first-showhand`, `$dbx-software-plan-first-showhand`, or asks to manually trigger this exact DBX Software Plan-First safe automatic execution phase. Do not auto-trigger for ordinary automatic execution, do-it-all, showhand, or plan-first requests.
---

# DBX Software Plan-First Showhand

## DBX repository notes

- This repository uses the `dbx-` prefix for stable skills; use the prefixed skill names in handoffs and cross-skill routing.
- Keep this phase self-contained: load only the required references for the active phase, and do not pull sibling skill files unless the workflow explicitly hands off to that phase.

## Manual Trigger

- Manual trigger only.
- Use only when the user explicitly names `dbx-software-plan-first-showhand`, `$dbx-software-plan-first-showhand`, or says to use/trigger this exact skill.
- Do not auto-trigger for ordinary automatic execution, do-it-all, showhand, or plan-first requests.

用于在条件充分时，把完整计划自动执行到底。

## 语义

- 核心工作流不变：plan -> ground -> finalize -> implement -> review/complete。
- showhand 只是在安全条件满足时连续执行多个 task。
- 不降低 decision gate，不跳过 grounding，不跳过 seal，不跳过验证。
- 所有过程产物和沟通使用中文。

## 必须读取

- `references/workflow-rules.md`
- `references/plan-issue-rules.md`
- `references/control-model.md`
- `references/impact-profiles.md`
- `references/worktree-safety.md`
- `references/feedback-and-proof.md`
- `references/review-checks.md`
- `references/config.md`

## 允许使用的条件

- Goal、Scope、Approach、Validation、Plan Strategy、Impact Profile、Impact Boundary 完整。
- 所有 source of truth 明确。
- 验证命令或 review-only 证据明确。
- 工作区安全，没有不明用户改动。
- 每个 task 的完成条件可程序化或明确 review-only。
- 不涉及用户主观判断、设计方向未定、contract 未定、生产数据、destructive/formal write 或外部系统危险副作用。

## 自动执行流程

1. 必要时先执行只读 grounding。
2. 执行 finalize：`init`、写中文 `plan.md/tasks.md`、`seal`。
3. 循环执行：

```sh
scripts/issue-workflow.sh next <issue-id>
# 实现当前 task
scripts/issue-workflow.sh review-ready <issue-id>
scripts/issue-workflow.sh complete <issue-id>
```

4. 每个 task 都必须产生中文证据。
5. 最后输出中文完成摘要、验证结果和证据路径。

## 不要 showhand 的情况

- 用户需要逐步 review。
- `workspace.commit = "manual"` 且连续任务之间无法可靠隔离。
- contract、设计、文案、权限、数据、环境、验证或 source of truth 仍不完整。
- 任务涉及高风险写入、迁移、外部系统副作用、生产数据、formal/destructive write。

## 输出

用中文说明执行了哪些 task、每个 task 的证据、最终验证结果、是否还有未完成项。
