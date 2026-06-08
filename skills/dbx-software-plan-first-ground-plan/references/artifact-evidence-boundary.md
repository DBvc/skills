# 产物和证据边界

普通源码编辑可以只依赖 `plan.md`、`tasks.md` 和验证命令。以下情况必须额外明确 Artifact/Evidence Boundary：

- loop-exploration 或 hybrid 计划。
- 生成代码、导入导出、批处理、迁移、数据写入。
- 截图、trace、report、baseline、benchmark、浏览器证据。
- 设计原型、throwaway prototype、视觉对比。
- formal/destructive write、会改变真实环境或外部系统的操作。
- 任何证据本身就是交付物的任务。

## 必须说明

- Source-of-truth refs：真实存在的 issue、spec、contract、design、PRD、conversation、grounding handoff。不要枚举不存在的来源。
- Artifact paths：每个产物的位置，是 committed、local、gitignored、transient、prototype-only 还是 production source。
- Evidence paths：截图、日志、报告、trace、run record、baseline、review artifact 的位置和是否提交。
- State policy：缓存、浏览器 storage、数据库状态、临时目录、环境变量、cleanup、rollback。
- Validation gates：task-local、shared、final、manual/review-only 的边界。
- Metadata/provenance：commit、baseline、schema、fixture、设计来源、viewport、browser、环境、批次信息。
- Batch/write boundary：batch selection、batch size、stop/skip/retry、no-full-rerun、promotion、destructive/formal write 规则。

## 提交流程

默认 `plan_docs.mode = "local"` 时，`.plan-first/` 是本地 workflow 状态。配置、计划文件、任务文件、runs、seal、review snapshot 和验证日志都不作为任务提交产物：

```text
.plan-first/
```

local 模式下，commit message 不应引用这些本地过程路径；脚本会拒绝在提交模板里使用 `{evidence_file}`、`{validation_log}`、`{plan_file}` 或 `{tasks_file}`。

如果团队需要把计划纳入仓库，必须显式使用 `plan_docs.mode = "tracked"`，并把 `plan.md` 和 `tasks.md` 同步到配置的项目文档路径。tracked 模式提交的是这些同步后的项目文档，不是 `.plan-first/` 本体。

local 模式下，提交策略只影响代码变更：

- `workspace.commit = "none"`：不 stage、不 commit、不生成提交建议。
- `workspace.commit = "manual"`：输出建议提交信息，记录整个 workspace 已发现 repo 的 review snapshot。
- `workspace.commit = "auto"`：单 repo 可自动提交；多 repo 必须在 `review-ready` 显式传 `--repo <name>`。

`manual` / `none` 模式下不能用 `--repo` 缩窄 review 范围。`review-ready` 后、`complete` 前，任何被 review repo 的 diff 边界变化都会导致 complete 失败。

tracked 模式下，提交策略也会影响同步后的 plan/task 文档；`workspace.commit = "auto"` 要求 tracked 文档和当前 task 变更位于同一个被 review 的 repo。无论哪种 plan docs 模式，都必须保留 seal、review snapshot、验证日志和证据记录；这些记录仍然是本地 workflow 状态，不进入 task commit。

tracked 文档虽然由 workflow 同步，但一旦写入项目文档路径，就按用户工作区资产处理。同步前如果发现目标文档已有未提交且不同的内容，或目标文档被删除 / staged 删除，必须停止并要求用户先处理冲突或确认删除意图，不能静默覆盖或重建。

tracked 文档路径必须能稳定进入 review snapshot 和 task commit 边界；不能写入 `.git/`、`.plan-first/` 或被 Git ignore 的未跟踪路径。`review-ready` 会锁定 `plan_docs` 模式、渲染路径和 repo 文件映射；`complete` 前这些边界变化时必须重新 review。
