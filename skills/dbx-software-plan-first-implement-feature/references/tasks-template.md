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

如果 task 会新增、移动或固定 source/config/test/doc 产物，必须至少有一行 `约束:` 写明产物归属、依据和禁止误放的边界。上游 prompt、计划草稿或 handoff 中出现的候选路径不是批准。

每个代码型 task 还必须用可重复的 `约束:` 封存机器可读路径：

- `约束: allowed-path=<workspace 相对路径>`：实现 delta 允许触达的文件。目录范围必须以 `/` 结尾；不支持 glob。
- `约束: required-path=<workspace 相对路径>`：本 task 必须实际命中的目标文件或目录。每个 required path 必须被某个 allowed path 覆盖。

路径使用 POSIX `/`，不能包含空段、`.`、`..`、`.git` 或 `.plan-first`。`review-ready` 会拒绝 allowed scope 外的任何 task-attributable delta，并要求每个 required target 至少命中一次。

新 task 的 task type 编码在 `验收:` 中，推荐写成 `任务类型=step; ...`。没有该 marker 的已有 task 默认为 `step`。支持类型：`step`、`loop-batch`、`gate`、`promote`、`documentation-only`。

- `step`、`loop-batch` 是代码型 task：进入 implement phase 时必须先封存 repo HEAD、task-start Git baseline、allowed paths 和 required paths；`review-ready` 必须同时看到验证前已存在且命中 required targets 的 scope 内实现 delta，以及至少一条真实程序化验证成功记录。
- `gate`、`promote`、`documentation-only` 只能在没有 Git 可见实现 delta 时完成；仍要执行声明的验证，允许使用有具体理由的 review-only marker。需要写项目文件时改用代码型 task 和完整代码门禁。

最终文件中不要保留这段说明。
不要在模板文本或示例下面追加 task。

示例：

```text
- [ ] [settle-contract] 固定跨层契约和错误映射
验收: 任务类型=gate; request/response/error/auth mapping 的 review 结论已记录在本地 evidence
验证: # 无程序化验证: 该 gate 只确认现有契约，不写项目文件
提交类型: chore
依赖: none
约束: 不发明未被 source of truth 支持的字段、错误码或权限语义

- [ ] [implement-visible-behavior] 实现已确认的用户可见行为
验收: 任务类型=step; 目标 surface、关键状态和回归证据已覆盖
验证: <项目原生验证命令>
提交类型: feat
使用检查: fast
依赖: settle-contract
约束: 不改变 out-of-scope surface 或无关 public behavior
约束: allowed-path=src/feature/
约束: required-path=src/feature/entrypoint.ts

- [ ] [visual-review] 捕获目标状态的截图证据
验收: 任务类型=documentation-only; 目标 viewport/state 的截图或 review artifact 已记录
验证: # 无程序化验证: 该任务需要用户视觉 review
提交类型: chore
依赖: implement-visible-behavior
约束: 不重设计未在计划中确认的视觉方向
```

`依赖:` 行必须使用裸 task id，例如 `依赖: settle-contract`。
`提交类型:` 是确定性元数据，不允许在 complete 阶段临场猜。需要 `{commit_type}` 时，优先使用 task 的 `提交类型:`，否则使用 `.plan-first/config.toml` 的 `commit.default_type`；两者都没有就报错。
`约束:` 用于执行护栏，例如 non-goals、touched-surface limits、artifact ownership、contract/data boundaries、design/content boundaries、review gates、batch limits、selection rules、retry/skip rules、no-full-rerun guards、worktree safety、prototype cleanup 和 write boundaries。不要在这里重复 task summary 或 `验收:` 行。
不要把普通实现任务拆成“实现代码”和“添加测试”两个 checklist item，除非测试工作本身就是独立交付物。
