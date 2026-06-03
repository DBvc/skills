---
name: dbx-software-plan-first-implement-feature
description: Manual trigger only. Use only when the user explicitly names `dbx-software-plan-first-implement-feature`, `$dbx-software-plan-first-implement-feature`, or asks to manually trigger this exact DBX Software Plan-First review-gated single-task implementation phase. Do not auto-trigger for ordinary implementation, tasks.md, next-task, or plan-first requests.
---

# DBX Software Plan-First Implement Feature

## DBX repository notes

- This repository uses the `dbx-` prefix for stable skills; use the prefixed skill names in handoffs and cross-skill routing.
- Keep this phase self-contained: load only the required references for the active phase, and do not pull sibling skill files unless the workflow explicitly hands off to that phase.

## Manual Trigger

- Manual trigger only.
- Use only when the user explicitly names `dbx-software-plan-first-implement-feature`, `$dbx-software-plan-first-implement-feature`, or says to use/trigger this exact skill.
- Do not auto-trigger for ordinary implementation, tasks.md, next-task, or plan-first requests.

用于按计划执行单个 task。

## 语义

- 每次只执行 `tasks.md` 中第一个未完成 task。
- 不跳 task，不静默改 plan，不手动把 task 标成完成。
- 实现前检查工作区安全。
- 实现后运行 `review-ready`，用户 review 通过后运行 `complete`。
- 所有沟通、证据和任务完成摘要使用中文。

## 必须读取

- `references/workflow-rules.md`
- `references/implement-notes.md`
- `references/worktree-safety.md`
- `references/review-checks.md`
- `references/feedback-and-proof.md`
- `references/impact-profiles.md`

## 工作流

1. 查看工作区：

```sh
git status --short --branch -uall
```

2. 查看当前 workflow 状态：

```sh
scripts/issue-workflow.sh status <issue-id>
scripts/issue-workflow.sh next <issue-id>
```

3. 只执行当前 task。
4. 如果发现计划假设错误、source of truth 缺失、验证模型不适用或 scope 需要扩大，停止并报告，不要继续实现。
5. 完成实现后运行：

```sh
scripts/issue-workflow.sh review-ready <issue-id>
```

6. 输出 `review-ready` 摘要，等待用户 review。
7. 用户确认通过后运行：

```sh
scripts/issue-workflow.sh complete <issue-id>
```

## 禁止事项

- 不执行非当前 task 的工作。
- 不手动改 `tasks.md` 完成状态。
- 不绕过失败验证。
- 不覆盖用户已有改动。
- 不在 review-ready 后继续改代码；如需改动，重新 review-ready。

## 输出

使用中文 `review-ready` 或 `complete` 摘要。
