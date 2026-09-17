# 实现阶段注意事项

## 基本动作

- 运行 `scripts/issue-workflow.sh status <issue-id>` 查看状态。
- 运行 `scripts/issue-workflow.sh next <issue-id>` 查看当前 task。
- 用户显式进入 implement phase 已经授权当前 task 的代码写入；不重复索权，路径仍限于 task scope。
- 第一次写代码前运行 `scripts/issue-workflow.sh begin-implementation <issue-id>`，封存 repo HEAD、task-start Git baseline，以及 task 的 `allowed-path` / `required-path`。
- 只实现第一个未完成 task。
- 任务完成后运行 `scripts/issue-workflow.sh review-ready <issue-id>`。
- 用户 review 通过后运行 `scripts/issue-workflow.sh complete <issue-id>`。

## 遇到计划不对

停止，不要边改边修 plan。需要说明：

- 哪个计划假设不成立。
- 影响哪个 Impact Boundary。
- 是否需要重新 grounding。
- 是否需要重新 finalize 和 seal。

## 验证失败

不要绕过验证。先判断：

- 是实现错误。
- 是测试命令或环境前置条件缺失。
- 是计划的验证模型不适用。
- 是项目已有失败，与当前任务无关。

只有用户明确接受时，才能把可执行验证改成 review-only marker。

代码型 `step` / `loop-batch` 不接受 review-only-only 的完成证据：必须在运行验证前已经存在 task-start 后可归因的实现 delta，全部 delta 位于 sealed `allowed-path`，每个 `required-path` 都被命中，并至少有一次真实程序化验证成功。验证执行有总超时和总输出上限，且不得改变 HEAD、index 或 Git 可见 workspace。

`gate` / `promote` / `documentation-only` 只能零 Git 可见实现 delta 完成。若任务需要写项目文件，把 task type 改为 `step` / `loop-batch` 并应用完整代码门禁。

## 过程产物语言

用户要求中文版时，计划、任务、证据、运行说明、review 摘要、完成摘要都用中文。技术标识、命令、文件名、代码符号可以保留原文。
