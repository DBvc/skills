# 任务清单

用最终 task checklist 替换这个模板。

最终 `tasks.md` 只能包含：

- `- [ ] [<task-id>] ...` 或 `- [x] [<task-id>] ...` 形式的 task header。
- 每个 task 下方恰好一行 `验收:`。
- 每个 task 下方一行或多行 `验证:`。
- 可选且可重复的 `使用检查:` 行。
- 可选且可重复的 `依赖:` 行，或恰好一行 `依赖: none`。
- 可选且可重复的 `约束:` 行。
- 可选且最多一行 `提交类型:` 行，用于确定 commit subject 中的 `{commit_type}`。

新 task 的 task type 编码在 `验收:` 中，推荐写成 `任务类型=step; ...`。没有该 marker 的已有 task 默认为 `step`。支持类型：`step`、`loop-batch`、`gate`、`promote`。

最终文件中不要保留这段说明。
不要在模板文本或示例下面追加 task。

示例：

```text
- [ ] [settle-contract] 固定跨层契约和错误映射
验收: 任务类型=gate; request/response/error/auth mapping 已记录并被相关实现引用
验证: <项目原生验证命令>
提交类型: chore
使用检查: fast
依赖: none
约束: 不发明未被 source of truth 支持的字段、错误码或权限语义

- [ ] [implement-visible-behavior] 实现已确认的用户可见行为
验收: 任务类型=step; 目标 surface、关键状态和回归证据已覆盖
验证: <项目原生验证命令>
提交类型: feat
使用检查: fast
依赖: settle-contract
约束: 不改变 out-of-scope surface 或无关 public behavior

- [ ] [visual-review] 捕获目标状态的截图证据
验收: 任务类型=step; 目标 viewport/state 的截图或 review artifact 已记录
验证: # 无程序化验证: 该任务需要用户视觉 review
提交类型: chore
依赖: implement-visible-behavior
约束: 不重设计未在计划中确认的视觉方向
```

`依赖:` 行必须使用裸 task id，例如 `依赖: settle-contract`。
`提交类型:` 是确定性元数据，不允许在 complete 阶段临场猜。需要 `{commit_type}` 时，优先使用 task 的 `提交类型:`，否则使用 `.plan-first/config.toml` 的 `commit.default_type`；两者都没有就报错。
`约束:` 用于执行护栏，例如 non-goals、touched-surface limits、contract/data boundaries、design/content boundaries、review gates、batch limits、selection rules、retry/skip rules、no-full-rerun guards、worktree safety、prototype cleanup 和 write boundaries。不要在这里重复 task summary 或 `验收:` 行。
不要把普通实现任务拆成“实现代码”和“添加测试”两个 checklist item，除非测试工作本身就是独立交付物。
