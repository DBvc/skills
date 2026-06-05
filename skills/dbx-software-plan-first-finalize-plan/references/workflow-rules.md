# Workflow 规则

五段式工作流固定不变：

```text
dbx-software-plan-first-plan-issue
  -> dbx-software-plan-first-ground-plan
  -> dbx-software-plan-first-finalize-plan
  -> dbx-software-plan-first-implement-feature
  -> dbx-software-plan-first-showhand（只在适合自动化时使用）
```

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
4. 报告本地计划文件位置、任务数量、workspace root 和提交模式。计划过程产物固定写在 `.plan-first/issues/<issue-id>/`，不自动提交。

## implement-feature 阶段

1. 运行 `status` 或 `next` 确认当前任务。
2. 只实现第一个未完成 task。
3. 运行 `review-ready` 执行 task 验证、shared check、必要时 final validation，并生成完整 review snapshot。
4. 等用户 review 通过后运行 `complete`。
5. `complete` 先确认 review 后 diff 边界、提交模式、提交模板和 staged 文件仍一致，再写中文证据文件、更新 `tasks.md`，并根据 `workspace.commit` 自动提交或输出建议提交信息。`auto` 模式若提交中断，会保留本地 `complete-pending.json`，下次 `complete` 会优先恢复。

多仓 workspace 下，验证命令必须显式写 cwd，例如 `cd web-app && yarn lint`。workflow 不猜验证命令归属。

`workspace.commit = "auto"` 且发现多个 Git repo 时，`review-ready` 必须显式传 `--repo <name>`，避免一次 task 自动提交多个仓库。

`workspace.commit = "none"` 不生成提交建议。`workspace.commit = "manual"` 输出 deterministic commit subject/body；提交类型来自 task 的 `提交类型:` 或 `commit.default_type`，不能从 diff 猜。

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
