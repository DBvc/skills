# Workflow 规则

本工作流的门控顺序固定，但入口按已满足的证据门选择。不要把它理解成每次都必须从 `plan-issue` 跑满到 `implement-feature`。

DBX implementation-bound planning profile 可以在 grounding 与 finalize 之间插入 external `dbx-plan-convergence` gate。该 gate 不是 Plan-First phase，不改变 phase skill 的 manual-only activation，也不改变 seal、implement 或 showhand 语义。

```text
dbx-software-plan-first-plan-issue（仅当决策未收敛）
  -> dbx-software-plan-first-ground-plan（仅当需要仓库事实）
  -> [external dbx-plan-convergence，只有父 workflow/用户显式选择时]
  -> dbx-software-plan-first-finalize-plan（需要完整决策和必要证据）
  -> dbx-software-plan-first-implement-feature（需要 sealed plan/tasks）
  -> dbx-software-plan-first-showhand（只在适合自动化时使用）
```

## Phase Entry Matrix

| 目标阶段 | 可以进入的前提 | 必须停止或回退的情况 |
| --- | --- | --- |
| `plan-issue` | Goal、Scope、Approach、Validation、Plan Strategy、Impact Profile 或 Impact Boundary 尚未收敛，需要先在对话中定边界 | 用户要求读仓库、写文件、seal 或实现；本阶段只能输出 `clarifying`、`blocked` 或 `proposal-ready` |
| `ground-plan` | 计划或用户输入需要仓库事实来确认路径、项目规则、source of truth、契约、验证命令、ownership 或 protected/generated 区域 | 用户要求在 grounding 阶段写计划文件或实现代码；只输出 `grounding-handoff` |
| `finalize-plan` | Mandatory Decision Gate 已完整，且所有会影响计划的仓库事实已由 grounding、当前上下文或用户确认支持；implementation-bound profile 下还必须有匹配 current artifact 的 `ready-for-handoff` | 缺少验证、source of truth、artifact/evidence boundary、产物归属或项目事实；selected profile 的 receipt 缺失、stale 或 identity mismatch；先回到 `plan-issue`、`ground-plan` 或 external `dbx-plan-convergence` |
| `implement-feature` | 已有 sealed `plan.md` / `tasks.md`，workflow status/next 指向第一个未完成 task，工作区安全 | 没有 seal、seal hash 不一致、计划假设错误、验证模型不适用、scope 需要扩大或用户改动不明 |
| `showhand` | `implement-feature` 的所有前提成立，且 showhand 条件全部满足 | 需要主观判断、高风险写入、外部副作用、source of truth 缺失或工作区不安全 |

入口可以跳过已经满足的上游阶段，但不能跳过对应证据门：决策未完整不能 finalize；需要仓库事实但未确认不能 seal；没有 sealed task 不能 implement。

Direct/manual `finalize-plan` 保持兼容：用户显式确认当前计划已经收敛，且所有现有证据门都满足时，可以不提供外部 convergence receipt。

## 脚本命令

所有技能目录都带有同一个 workflow wrapper：

```sh
scripts/issue-workflow.sh init <issue-id>
scripts/issue-workflow.sh seal <issue-id>
scripts/issue-workflow.sh status <issue-id>
scripts/issue-workflow.sh next <issue-id>
scripts/issue-workflow.sh notes-template <issue-id>
scripts/issue-workflow.sh review-ready <issue-id>
scripts/issue-workflow.sh complete <issue-id>
```

通用参数：

```sh
scripts/issue-workflow.sh --root <workspace-root> status <issue-id>
scripts/issue-workflow.sh --repo <repo-name> review-ready <issue-id>
```

默认 root 解析顺序：`--root`、`PLAN_FIRST_ROOT`、向上查找 `.plan-first/config.toml`、当前 Git root。`init` 会创建最小 `.plan-first/config.toml` 作为 workspace root marker；非 Git workspace 首次裸 `init` 必须在 workspace root 当前目录运行，或显式传 `--root <workspace-root>`。

`--repo` 只允许 `workspace.commit = "auto"` 使用。`manual` / `none` 模式必须 review 整个 workspace，不能缩窄 repo snapshot。

## finalize-plan 阶段

1. 运行 `scripts/issue-workflow.sh init <issue-id>` 创建中文 `plan.md` 和 `tasks.md` 模板。
2. 填写计划和任务。
3. 运行 `scripts/issue-workflow.sh seal <issue-id>` 写入 seal。
4. 报告本地计划文件位置、任务数量、workspace root、plan docs 模式和提交模式。计划过程产物固定写在 `.plan-first/issues/<issue-id>/`；默认 `plan_docs.mode = "local"` 时不自动提交。`plan_docs.mode = "tracked"` 时，同步后的 `plan.md` 和 `tasks.md` 会写入配置的项目文档路径。

## implement-feature 阶段

1. 运行 `status` 或 `next` 确认当前任务。
2. 只实现第一个未完成 task。
3. 运行 `review-ready` 执行 task 验证、shared check、必要时 final validation，并生成完整 review snapshot。
4. 等用户 review 通过后运行 `complete`。
5. `complete` 先确认 review 后 diff 边界、提交模式、提交模板和 staged 文件仍一致，再写中文证据文件、更新本地 `tasks.md`；tracked 模式会同步项目文档 `tasks.md`。之后根据 `workspace.commit` 自动提交或输出建议提交信息。`auto` 模式若提交中断，会保留本地 `complete-pending.json`，下次 `complete` 会优先恢复。

多仓 workspace 下，验证命令必须显式写 cwd，例如 `cd web-app && yarn lint`。workflow 不猜验证命令归属。

`workspace.commit = "auto"` 且发现多个 Git repo 时，`review-ready` 必须显式传 `--repo <name>`，避免一次 task 自动提交多个仓库。

`workspace.commit = "none"` 不生成提交建议。`workspace.commit = "manual"` 输出 deterministic commit subject/body；提交类型来自 task 的 `提交类型:` 或 `commit.default_type`，不能从 diff 猜。

`plan_docs.mode = "local"` 时，提交模板不能引用本地过程路径。`plan_docs.mode = "tracked"` 时，`review-ready` 会把同步后的 `plan.md` 和 `tasks.md` 纳入 review snapshot；`workspace.commit = "auto"` 要求 tracked 文档位于被 review 的同一个 repo 中。

## showhand 阶段

showhand 只能在下列条件全部成立时使用：

- Mandatory Decision Gate 已完整。
- Impact Boundary 已完整。
- 所有 source of truth 已明确。
- 验证命令或 review-only 证据明确。
- 工作区安全。
- 风险不需要用户在每个任务之间做主观判断。

以下情况不要 showhand：

- contract、设计、文案、权限、数据写入或环境仍不明确。
- 需要用户视觉判断或业务判断。
- 任务涉及 destructive/formal write、migration、生产数据、外部系统副作用。
- 当前仓库有不明用户改动。
- `workspace.commit = "manual"` 且连续任务之间无法可靠隔离。

## Seal 规则

`seal` 会记录 `plan.md` 和 `tasks.md` hash。实现阶段发现 hash 不一致时必须停止。

`complete` 是唯一允许把当前 task 从 `[ ]` 改为 `[x]` 的流程动作。完成后脚本会更新 seal。

`review-ready` 后、`complete` 前不能新增 dirty 文件、改动已 review 文件、改变提交模式或切换 repo 边界。`manual` / `none` 模式下，新增、删除、重命名或移动 discovered repo 也会导致 `complete` 失败；发生任何一种变化都必须重新 `review-ready`。
