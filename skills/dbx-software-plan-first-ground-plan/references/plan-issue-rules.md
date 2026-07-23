# Plan Issue 规则

`plan-issue` 是 proposal shaping 阶段，不是 `dbx-plan-convergence` controller、仓库探索阶段或写文件阶段。

## 禁止事项

- 不读取仓库。
- 不写 `plan.md` 或 `tasks.md`。
- 不执行 `issue-workflow.sh`。
- 不调用任何会写入文件、修改工作区或产生实现 diff 的工具，包括 `apply_patch`、formatter、codegen、package manager install、迁移命令和测试自动修复命令。
- 不继续串到 `ground-plan`、`finalize-plan` 或 `implement-feature`；只能输出本阶段结果和下一阶段 handoff。
- 不把未确认的路径、框架、命令、契约、设计、文案或验证方式当成事实。
- 不把阻塞问题推给实现阶段。

如果用户在同一请求里要求“先 plan-issue，然后顺手读仓库 / 写计划文件 / 改代码 / complete”，本阶段必须忽略后续执行部分并停止在 `clarifying`、`blocked` 或 `proposal-ready`。只有用户后续显式触发对应阶段，才能继续。

## Mandatory Decision Gate

只有下列信息完整，才能输出 `proposal-ready`：

- Goal：具体交付结果。
- Scope：in-scope 和 out-of-scope。
- Approach：实现形状、触达 surface、create-vs-edit、所有权边界。
- Validation：task-local、shared、final、review-only 条件。
- Plan Strategy：`step-execution`、`loop-exploration` 或 `hybrid`。
- Impact Profile：`frontend`、`backend`、`fullstack` 或 `generic`。
- Impact Boundary：与该任务相关的 target、behavior、contract/data/state、composition、runtime/ops、content/design、feedback/evidence 边界。
- Artifact/Evidence Boundary：当有生成产物、证据、批处理、迁移、正式写入、原型或 loop/hybrid 时必须明确。
- Grounding Producer：是否需要 `dbx-software-plan-first-ground-plan` 读取仓库事实。

## 计划策略

- `step-execution`：路径和交付物足够固定，可以按有序任务执行。
- `loop-exploration`：目标固定，但进展依赖 batch、metric、artifact、stop/skip/retry 和 feedback。
- `hybrid`：既有 loop-exploration，又有确定性的 setup/gate/promote task。

## 需要继续澄清的情况

任一问题会改变以下内容时，必须 `clarifying` 或 `blocked`：

- 交付物、模块、文件、service、component、route、API、数据、权限、设计、文案、验证、证据、写入边界。
- 是否需要 mock、fixture、migration、prototype、generated artifact、manual review。
- 哪个 source of truth 优先。
- 工作是否 review-only。

## 交给 ground-plan

如果需要仓库事实，输出 handoff，要求 `ground-plan` 只读确认：

- 项目规则文档。
- 目标 surface/path/module/service。
- source of truth。
- 原生命令和验证路径。
- contract/design/content/test/CI/architecture 约束。
- deprecated/protected/generated 文件。

不需要仓库事实的情况必须明确说明 `Grounding Producer: none`，并写明事实来源来自用户确认或当前上下文。不能因为形式上有 `ground-plan` 阶段就要求无意义 grounding；也不能因为想加速而跳过必要 grounding。
