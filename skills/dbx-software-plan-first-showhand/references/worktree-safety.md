# Worktree 安全规则

执行实现前，必须把 Git 工作区当作用户资产，而不是 agent 草稿纸。

## 基础规则

- 先查看 `git status --short --branch -uall`。
- 未经当前回合明确批准，不要运行 `git reset`、`git clean`、`git stash`、`git checkout`、`git switch` 来处理用户已有改动。
- 不要覆盖不属于当前 task 的 modified、staged、untracked 文件。
- 自动提交模式只提交当前 review snapshot 和 workflow 产物，不吞掉无关 staged 文件。
- 如果工作区已经有不明改动，先报告并请求用户确认边界；不能假设它们属于当前任务。

## 实现中

- 每个 task 只改它的 `Accept:` 和 `Constraint:` 允许的范围。
- 发现计划边界不对时停止，不要顺手扩范围。
- 发现项目规则、命令、contract、设计或验证与计划冲突时，回到 `finalize-plan` 或请求 reseal。

## 完成前

- `review-ready` 必须生成或记录验证结果。
- `complete` 只能完成已经 `review-ready` 的同一个 task。
- review 之后、complete 之前，不能再改代码；否则必须重新 `review-ready`。
