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

## finalize-plan 阶段

1. 运行 `scripts/issue-workflow.sh init <issue-id>` 创建中文 `plan.md` 和 `tasks.md` 模板。
2. 填写计划和任务。
3. 运行 `scripts/issue-workflow.sh seal <issue-id>` 写入 seal。
4. 根据 `.plan-first/config.toml` 自动提交或输出建议提交信息。

## implement-feature 阶段

1. 运行 `status` 或 `next` 确认当前任务。
2. 只实现第一个未完成 task。
3. 运行 `review-ready` 执行 task 验证、shared check、必要时 final validation，并生成 review snapshot。
4. 等用户 review 通过后运行 `complete`。
5. `complete` 写入中文证据文件，更新 `tasks.md`，并根据配置自动提交或输出建议提交信息。

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
- `git.mode = "manual-commit"` 且连续任务之间无法可靠隔离。

## Seal 规则

`seal` 会记录 `plan.md` 和 `tasks.md` hash。实现阶段发现 hash 不一致时必须停止。

`complete` 是唯一允许把当前 task 从 `[ ]` 改为 `[x]` 的流程动作。完成后脚本会更新 seal。
