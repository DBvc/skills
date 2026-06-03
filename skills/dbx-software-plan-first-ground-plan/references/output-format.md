# 输出格式

本技能的用户沟通默认使用中文。除非项目已有明确要求，否则不要把计划、任务、证据、执行说明写成英文。

## `clarifying`

当缺少会影响计划或执行的信息时使用。

```text
状态：clarifying

还需要确认：
- <会改变目标、范围、方案、验证、影响边界或证据模型的问题>

当前已确定：
- <已经稳定的信息>

建议下一步：
- <需要用户确认的最小问题>
```

## `blocked`

当当前信息不足以安全推进，或存在必须由用户/项目给出的 source of truth 时使用。

```text
状态：blocked

阻塞原因：
- <为什么不能继续>

缺失的 source of truth：
- <合同/API/设计/权限/数据/环境/项目规则等>

可继续的条件：
- <用户提供什么之后可以继续>
```

## `proposal-ready`

当计划已经能交给 `ground-plan` 或 `finalize-plan` 时使用。

```text
状态：proposal-ready

目标：
- <具体交付结果>

范围：
- In-scope: <本次要做什么>
- Out-of-scope: <本次不做什么>

方案：
- <高层实现策略>

计划策略：
- Plan Strategy: step-execution | loop-exploration | hybrid

影响画像：
- Primary: frontend | backend | fullstack | generic
- Why: <为什么这样分类>

影响边界：
- Target surfaces: <目标 surface>
- User/system-visible behavior: <用户或系统可见行为>
- Contract/data/state boundary: <契约、数据、状态边界>
- Composition/ownership boundary: <模块、组件、服务、所有权边界>
- Runtime/operational boundary: <运行时、部署、回滚、环境边界>
- Content/design boundary: <文案、设计、内容来源边界>
- Feedback/evidence boundary: <反馈和证据模型>
- Artifact/evidence boundary: <产物、证据、写入边界；无关可省略>

验证：
- Task-local: <每个任务本地验证>
- Shared: <可复用验证>
- Final: <最终整体验证>
- Review-only: <无法程序化验证时的明确原因和证据>

Grounding producer：
- dbx-software-plan-first-ground-plan | none | <项目指定 producer>

非阻塞问题：
- <不会改变执行路径的问题；没有则写“无”>
```

## `grounding-handoff`

`ground-plan` 完成只读仓库确认后使用。

```text
状态：grounding-handoff

已确认的项目事实：
- <事实 + 文件/命令/路径依据>

项目规则来源：
- <AGENTS.md / README / CI / 架构文档 / design docs / API schema 等>

影响画像：
- Primary: <frontend/backend/fullstack/generic>
- Secondary: <如有>
- Why: <仓库事实如何支持该判断>

建议的计划边界：
- <finalize-plan 应写入 plan.md 的边界>

验证候选：
- <项目原生命令或 review-only 证据>

风险和未知：
- <仍需用户确认，且会影响计划的内容>
```

## `review-ready`

实现技能在完成当前任务实现并通过验证后使用。

```text
状态：review-ready

当前任务：
- <task id + summary>

改动摘要：
- <用户或系统可见变化>

验证结果：
- <运行过的命令、shared check、final validation 或 review-only 证据>

待用户 review：
- <需要用户检查的地方>

下一步：
- 通过后运行 `scripts/issue-workflow.sh complete <issue-id>` 完成当前任务。
```

## `complete`

完成当前任务后使用。

```text
状态：complete

已完成任务：
- <task id + summary>

证据：
- <runs/ 下的证据文件或本地状态路径>

下一任务：
- <next task；没有则说明 issue 任务全部完成>
```
