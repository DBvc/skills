# `.plan-first/config.toml`

配置是为了适配团队流程，不是为了让工作流变成可编程章鱼。

默认配置等价于：

```toml
version = 1

[paths]
plan_root = "plans"
state_dir = ".plan-first"

[git]
mode = "auto-commit"      # auto-commit | manual-commit
plan_files = "tracked"    # tracked | local

[commit]
plan_subject = "plan: issue-{issue_id} 新增执行计划"
task_subject = "work: issue-{issue_id} 完成 {task_id}"
include_default_body = true

[project]
rules = [".plan-first/rules.md", "AGENTS.md", "README.md"]
```

## 字段

- `paths.plan_root`：当 `plan_files = "tracked"` 时，计划文件根目录。
- `paths.state_dir`：seal、review cache、本地计划文件和配置目录。
- `git.mode`：
  - `auto-commit`：workflow 自动提交计划和已完成 task。
  - `manual-commit`：workflow 不提交，只输出建议提交信息。
- `git.plan_files`：
  - `tracked`：`plan.md`、`tasks.md`、`runs/` 放到仓库计划目录。
  - `local`：这些过程产物放到 `.plan-first/issues/issue-<id>/`。
- `commit.plan_subject`：计划提交 subject 模板。
- `commit.task_subject`：任务提交 subject 模板。
- `commit.include_default_body`：是否生成默认中文 commit body。
- `project.rules`：`ground-plan` 应优先读取的项目规则文档候选。

## 模板变量

提交 subject 支持：

- `{issue_id}`
- `{task_id}`
- `{task_summary}`

## 不支持的复杂配置

初版刻意不支持：

- 任意 shell hook。
- 任意状态机配置。
- 每个 task 自定义 commit pipeline。
- 任意 validator/plugin。
- 动态 profile script。

项目特定规则请写在 `.plan-first/rules.md`、`AGENTS.md`、README、CI、架构文档、API/设计规范中。
