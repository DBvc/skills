# `.plan-first/config.toml`

配置只描述外部约定。workflow 状态目录、文件名和 issue 目录结构是内部模型，不开放配置。

## Root 规则

workspace root 的解析顺序：

1. 命令行 `--root <dir>`。
2. 环境变量 `PLAN_FIRST_ROOT`。
3. 从当前目录向上查找最近的 `.plan-first/config.toml`，其父目录就是 workspace root。
4. 如果没有配置文件且当前目录在 Git 仓库中，使用当前 Git root。

`init` 会在 workspace root 创建最小 `.plan-first/config.toml` 作为 root marker。虚拟多仓 workspace 首次初始化时：

- 在 workspace root 当前目录运行裸 `init`，脚本会用当前目录 bootstrap。
- 在任一子 repo 里首次初始化时，必须传 `--root <workspace-root>`，否则脚本不能可靠推断父级 workspace。

虚拟多仓 workspace 初始化后，从任一子 repo 继续运行命令都必须解析回同一个 workspace root。

workspace root 可以是 Git 仓库，也可以是普通目录。Git 单仓只是 workspace root 恰好也是 Git repo；虚拟多仓是 workspace root 下有多个 Git repo。

## 固定 artifact 结构

所有 plan-first 过程产物固定写在：

```text
<workspace-root>/
  .plan-first/
    config.toml
    issues/
      <issue-id>/
        plan.md
        tasks.md
        runs/
          task-001-<task-id>.md
        state/
          seal.json
          review-ready.json
          complete-pending.json
          validation.log
```

不要配置这些路径，也不要把它们当提交产物。`plan.md`、`tasks.md`、`runs/`、seal、review snapshot 和验证日志都是本地 workflow 状态。

## 默认配置

```toml
version = 1

[workspace]
commit = "manual"      # none | manual | auto

[commit]
task_subject = "work: issue-{issue_id} 完成 {task_id}"
default_type = "chore"
include_body = true
body_template = """
中文 plan-first 任务完成。

Issue: {issue_id}
Task: {task_id}
Evidence: {evidence_file}
"""
```

## 字段

- `workspace.commit`：
  - `none`：不 stage、不 commit、不生成提交建议；仍记录完整 review snapshot。
  - `manual`：不 stage、不 commit；输出建议提交信息，并记录整个 workspace 已发现 repo 的 review snapshot。
  - `auto`：自动 stage/commit。单 repo 可直接使用；多 repo workspace 下 `review-ready` 必须显式传 `--repo <name>`。
- `commit.task_subject`：任务提交 subject 的确定性模板。
- `commit.default_type`：当模板使用 `{commit_type}` 且 task 没有 `提交类型:` 时的默认值。可以设为空字符串；为空时缺失类型会报错。
- `commit.include_body`：是否生成 commit body。
- `commit.body_template`：commit body 的确定性模板。

## 模板变量

`commit.task_subject` 和 `commit.body_template` 支持：

- `{issue_id}`
- `{task_id}`
- `{task_summary}`
- `{commit_type}`
- `{evidence_file}`
- `{validation_log}`
- `{changed_files}`

`{commit_type}` 的来源：

1. 当前 task 的 `提交类型:` 行。
2. `commit.default_type`。
3. 如果两者都没有，且模板使用 `{commit_type}`，workflow 必须报错，不允许猜。

## Git repo 发现

workflow 不配置 repo 列表。

- 如果 workspace root 本身是 Git repo，只使用该 repo。
- 如果 workspace root 不是 Git repo，扫描 root 下一层；若下一层不是 Git repo，再扫描一层子目录。
- `node_modules`、`.plan-first`、`dist`、`build`、`coverage`、`.venv`、`vendor`、`target` 等目录会跳过。

验证命令总是在 workspace root 下执行。多仓任务必须在 `tasks.md` 中显式写 cwd，例如：

```text
验证: cd web-app && yarn lint
验证: cd api-service && npm run test:ci
```

不要让 workflow 猜某条验证命令属于哪个 repo。

## Review snapshot 规则

- `manual` / `none` 模式必须 review 整个 workspace；`--repo` 只允许 `auto` 模式使用。
- `review-ready` 记录被 review repo 的完整当前 diff 边界，包括当时无变更的 repo。
- `complete` 会重新计算被 review repo 的完整 diff 边界；`manual` / `none` 还会比对完整 repo manifest。只要新增文件、新增 dirty repo、新增/删除 repo、文件内容变化、repo 路径变化或提交模式变化，就必须重新 `review-ready`。
- `complete` 会在写 `tasks.md`、runs、seal 之前先完成提交模板、snapshot 和 staged 文件安全检查；`auto` 模式会用本地 `complete-pending.json` 支持提交失败后的重试。

## 不支持的复杂配置

刻意不支持：

- 自定义 artifact 路径、文件名或 issue 目录格式。
- 常驻 `vcs.repos` 列表。
- LLM commit prompt。
- 任意 shell hook。
- 任意状态机配置。
- 每个 task 自定义 commit pipeline。
- 任意 validator/plugin。
- 动态 profile script。

项目特定规则请写在 `.plan-first/rules.md`、`AGENTS.md`、README、CI、架构文档、API/设计规范中。
