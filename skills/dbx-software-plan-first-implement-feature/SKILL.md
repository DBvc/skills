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
- 用户显式进入本 implement phase，就已经授予当前 task 的代码写入权限；不要再问一次“是否开始写代码”。授权不扩大路径范围，写入仍严格限于当前 task 的 scope 与约束。
- Seal/document acceptance 之后先做一次 bounded implementation preflight：确认 current task、目标 surface/lookup、适用 owner/source of truth（局部无状态修改可由当前模块和测试满足）、不变量、验证、stop condition、seal identity、工作区和当前代码修改权限。通过后立即进入该 task 的代码实现，不再做普通 full plan review。
- 在第一次代码写入前由脚本封存 repo HEAD、task-start Git baseline 和机器可读 `allowed-path` / `required-path`。代码型 `step` / `loop-batch` 只有在验证前已存在 scope 内、命中全部 required target 的可归因实现 delta，且真实程序化验证至少成功一次时，才可进入 `review-ready`。验证不得改变 HEAD、index 或 Git 可见 workspace。`gate` / `promote` / `documentation-only` 只允许零 Git 可见实现 delta 完成。
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

3. 对当前 task 执行 bounded preflight。用户已显式调用本 phase，因此当前 task 的 `execution_authority` 直接为 `authorized`；不要重复索权。通过后运行下面的命令封存 repo HEAD、task-start Git baseline 和 task scope：

```sh
scripts/issue-workflow.sh begin-implementation <issue-id>
```

该命令重复调用时必须复用原 HEAD、baseline 和 task scope，不能在代码已修改后重置。随后立即只执行当前 task；不得触达 sealed `allowed-path` 外的文件，代码 task 必须命中全部 `required-path`。不要因为“再保险一次”回到方案评审。

4. 如果发现计划假设错误、source of truth 缺失、验证模型不适用或 scope 需要扩大，记录具体仓库证据并停止。

Preflight 只产生下面这个窄结果，不生成新计划：

```yaml
implementation_preflight:
  task_id: ""
  implementation_status: ready | blocked
  execution_authority: authorized
  checked: [task, seal, surface, scope, validation, worktree]
  contradictory_evidence: []
  next_action: implement_current_task | stop
```

`ready + authorized` 必须继续执行 `implement_current_task`，不能停在“可以开始”或要求再调用规划/review skill。

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
- 不把 review-only marker 当成代码型 task 的真实验证成功，不让零实现 delta、scope 外 delta 或漏掉 required target 的 `step` / `loop-batch` 进入 review-ready。
- 不让验证命令制造/改写实现 delta、stage 文件、commit，或突破总超时/总输出上限。
- 不让 `gate` / `promote` / `documentation-only` 携带 Git 可见实现 delta。
- 不覆盖用户已有改动。
- 不在 review-ready 后继续改代码；如需改动，重新 review-ready。

## 输出

使用中文 `review-ready` 或 `complete` 摘要，并说明 preflight 的 `implementation_status`。如果 blocked，给出具体证据；不要建议无条件再做 full plan review。
