# DBX Implementation-Bound Planning

## 结论

默认路径不再是：

```text
technical-plan -> plan-convergence -> Linus -> 继续改计划
```

现在分成四条互不暗中串联的路径：

| 用户意图 | 路径 |
| --- | --- |
| 直接实现 | 直接实现；普通实现请求不自动触发规划 workflow |
| 只要技术计划 | `dbx-technical-plan`；计划完成即返回，不自动进入 review loop |
| 审已有方案 | `dbx-linus-review` 做一次只读严格 review，或显式使用 `dbx-plan-convergence` 做 standalone gate/diagnose |
| 明确要求“计划、一次严格 review、然后开始首个代码切片” | 用户显式调用 `$dbx-implementation-bound-workflow` |

`dbx-implementation-bound-workflow` 目前是 manual-only 隔离实验，不进入默认路由，不接管 Plan-First。

本次变更必须按两个独立发布单元判断，不能把实验原型的未知收益混进默认路由：

1. **已知错误路径修复**：停止把普通 `dbx-technical-plan` 自动串到 convergence/review loop。它直接删除了用户已多次观察到的隐式重复门禁，并保留 plan-only、直接实现、显式 standalone review/convergence 和 Plan-First 兼容入口。该单元不依赖新 workflow。
2. **隔离实验**：新增 `$dbx-implementation-bound-workflow`，净收益仍为 `uncertain`。它只用于 old/new 对比，不是默认路径，也不是前一个修复的替代品。

## 为什么这样改

之前的问题不是单个 prompt 不够好，而是没有一个组件真正拥有整段任务：

- planner 可以继续补计划；
- reviewer 可以继续发现问题；
- convergence 可以继续分配下一步；
- implementer 又把“文档通过”当成“还要再确认一次”；
- run、预算、receipt 和权限散落在自然语言里，换一个 skill 就可能重置。

每个局部动作看起来都谨慎，但整体没有必须进入代码或明确停止的终点。

修复原则：

1. 普通 skill 保持单一职责和无状态。
2. 只有一个确定性脚本拥有 workflow 状态与 transition。
3. 默认不创建 workflow。
4. 一次 correction cycle 是“一次批量修订 + 一次最终 full review”，不是可嵌套的循环。
5. “文档 accepted”不是 terminal；实验 workflow 只能在 `needs_host_validation` 或 `blocked` 结束。
6. 只有真实 Git delta 能证明已产生首个代码切片；这个实验包不执行验证，也不声称实现完成。

## 默认技能边界

### `dbx-technical-plan`

负责：

- 仓库证据边界；
- goal / non-goals；
- source of truth 与适用 owner；
- 不变量；
- 首个可执行切片；
- 验证与 stop conditions。

不负责：

- 创建 run id；
- 保存 review budget；
- 签发 receipt；
- 决定 workflow completion；
- 默认调用 `dbx-plan-convergence`。

普通 plan-only 请求完成后直接返回计划。若原始请求已授权实现，首切片足够具体时可返回 `implementation_handoff.status: pending_preflight`；实现者只做当前仓库、工作区和权限检查，不重开通用 plan review。

实验 workflow 自己在 provider brief 中定义 path-backed `workflow_plan_result`；稳定的 `dbx-technical-plan` 不注册或路由这个实验协议。被该 brief 显式委托时，planner 把 `correlation_id` 当作不透明关联值，并且只支持：

- `draft`：生成一次计划；
- `bounded_revision`：一次性处理 workflow 接受的 findings。

Provider result 还必须声明 `provider_id`、`purpose`、计划文件 identity，以及结构化 `first_slice`（id、summary、authority 内的 target paths、非空 validation argv）。修订结果必须精确回显本轮关闭的 finding IDs。

### `dbx-linus-review`

负责只读技术判断：

- 核实 artifact identity；
- 判断真实问题、模型/ownership、兼容性、复杂度和首切片风险；
- 返回统一的 `delegated_review_result`。

不负责：

- run、grant、budget；
- receipt reuse 或 reopen；
- revision contract；
- `next_action` / `final_state`；
- 修改计划或代码。

单文件、bundle、有 findings、无 findings 都使用同一个结果结构，不再保留特殊的 machine-only 输出分支。

### `dbx-plan-convergence`

只用于用户明确要求的 standalone gate 或 stall diagnosis。它可以判断当前已有方案应当：

- 局部修订；
- 补证据；
- 请求 decision owner；
- 换方向；
- handoff；
- 因无进展或预算停止。

它不再是 `dbx-technical-plan` 到实现的默认必经路径，也不拥有跨 skill 的 feature trajectory。

## Manual-only workflow

`skills/dbx-implementation-bound-workflow/scripts/planning_workflow.py` 是唯一状态和 transition owner。

```text
draft
-> initial_review
-> implementation
-> host_validation
-> needs_host_validation

initial_review
-> correction_cycle                 # 初审持久化的 finding set，仅一次
-> final_review                     # 一次 full review，同时检查 closure
-> implementation
-> host_validation
-> needs_host_validation

任何不可安全继续的状态
-> blocked
```

禁止的边：

- `final_review -> correction_cycle`；
- `begin implementation -> general plan review`；
- `implementation -> document accepted`；
- 通过重新调用 skill 创建第二套 run/budget；
- reviewer 文本直接授予写权限。

### 状态约束

- 在同一个受信任 runtime registry 内，`origin_ref` 确定性映射到同一 `run_id`、state 和 plan 路径；重复 start 幂等，冲突输入失败。它不宣称跨任意 runtime 目录的全局唯一性。
- `start` 发生在计划生成前；第一个真实 operation 是 `draft`。
- state、provider result 和 artifact 必须位于 Git worktree 外的 owner-only runtime 目录；artifact 绑定 exact SHA-256。caller-written host result 不被接受。
- correction limit、used 都只能是 0 或 1；初审 blocking finding IDs 是唯一 correction contract，不另设自然语言 grant。
- 同一时刻最多一个 `active_operation`。
- 每个 mutating command 都要有稳定唯一 `event_id`。
- 相同 event 重试是幂等的；同一 event id 配不同 payload 必须报错。
- state 目录权限为 `0700`，state/lock 文件为 `0600`。
- 不允许模型手改 state JSON 或推断下一 phase。

### Review 规则

初次 full review 有三种合法结果：

- accepted：直接进入 `implementation`；它的 begin 操作执行窄 preflight；
- 有局部、明确、可一次修复的 findings：把 blocking finding IDs 持久化并进入唯一一次 correction；
- 方向错误、证据不足、需要 decision owner：`blocked`。

发生修订后：

- planner 一次性应用全部 accepted findings；
- artifact bytes 必须变化；
- 运行一次 final full review；
- final review 发现新 blocker 时直接 `blocked`，不再开始第二轮修订。

### Implementation preflight

`begin implementation` 同时执行窄 preflight，只检查进入首切片所需的当前事实：

- 当前 artifact 与 accepted review identity 一致；
- start 时已授权的明确 repo-relative paths；不允许 task-derived scope 在此扩权；
- 首切片目标在 authority scope 内；
- planning 期间除计划 artifact 外，workspace bytes 没有被偷偷改动；
- 当前 task 的验证命令和 stop condition 可执行。

它不能因为“再保险”重做通用方案 review。只有具体矛盾证据才能阻塞。

### Host validation handoff

进入 terminal `needs_host_validation` 前必须同时满足：

- 相对 implementation baseline 存在真实 Git delta；
- tracked / untracked 文件已分类；
- 所有 changed paths 都在 authority scope 内；
- 至少一个 changed path 命中计划声明的 first-slice target surface；
- helper 在 `begin host_validation` 时冻结首切片写入后的 Git 快照、cwd、argv/hash、300 秒 timeout、1 MiB 输出上限和外部副作用策略；helper 本身不执行 planner 提供的命令；
- file/symlink type 与 Git 可表示的 owner executable-bit 变化进入 delta；`0644 -> 0600` 和只改变 group/other execute 的变化不算实现；
- accepted review 仍绑定当前 plan hash。

terminal 输出固定声明 `first_slice_present: true`、`validation_status: not_run_by_controller`、`implementation_completion_claim: false`，并携带 frozen host request。受信 host 如何审批、执行、限制输出、检查外部副作用和捕获验证后快照，属于平台能力，不在本包的完成声明内。

`document accepted`、`ready-for-handoff`、`pending_preflight`、caller-written host JSON、非空 approval ref 或回复中声称“已修改”都不是验证/完成证据。

## Plan-First 边界

`dbx-software-plan-first-*` 继续保持 manual-only、phase-specific：

- 不由新 workflow 自动触发；
- 不接受跨 workflow 的隐式 delegated activation；
- selected profile 的既有 pre-seal convergence 兼容路径暂不迁移；
- strict finalize handoff 只有一次 initial full、一次 atomic correction 和一次 final full；不得再插入 scoped review；
- 显式调用 `implement-feature` 本身就是当前 sealed task 的代码授权，不重复向用户索权；
- `begin-implementation` 在首个代码写入前记录不可重置的 repo HEAD、task-start Git baseline，以及 sealed `allowed-path` / `required-path`；
- task-start 时已存在的 dirty / untracked 路径不得在实现期间从 Git status 消失；恢复既有 dirty 内容或删除既有 untracked 文件会失败关闭；
- 代码型 `step` / `loop-batch` 必须在验证前已有全部位于 allowed scope 且命中 required target 的实现 delta，并至少成功一次真实程序化验证；验证不得改变 HEAD、index 或 Git-visible workspace；
- 显式 `gate` / `promote` / `documentation-only` 只允许零 Git-visible implementation delta；一旦要写项目文件就必须使用代码型 task 的完整门禁。

等 manual-only workflow 的行为数据证明净收益后，再单独设计 Plan-First 持久状态适配。当前不建立第二个状态源。

兼容性：旧的 sealed 代码 task 如果没有 `allowed-path` / `required-path`，或仍持有 v1 implementation state，会失败关闭，必须重新 finalize/seal 后再开始实现。

## 发布门禁

发布检查先按 change unit 拆分路径。已知错误默认路径的独立删除，只有在 `net_value: positive`、有失败证据、保留明确回滚方式且不依赖 uncertain prototype 时才可发布。实验单元仍按下面的更严格规则隔离。

新 workflow 在进入默认路由前，至少要用相同任务集比较旧路径与实验路径：

| 指标 | 要求 |
| --- | --- |
| 到首个真实代码 delta 的比例 | 不低于旧路径 |
| 到首个代码 delta 的 review / revision 次数 | 明显下降 |
| 计划和状态 artifact 总体积 | 不增长或有明确收益 |
| 漏掉 S0/S1 的比例 | 不上升 |
| 越权 changed path | 0 |
| 假实现完成 | 0 |
| 卡在 document accepted / pending preflight | 0 |
| 默认误触发 | 0 |

在净收益仍不确定时，可以继续 isolated manual-only prototype，但不能：

- 改成 implicit/default routing；
- 删除旧兼容路径；
- 宣称问题已经普遍解决；
- 把实验状态合同复制到多个 provider skill。

目录登记必须把该 workflow 放在 `Experimental Skills`，不能列入 stable catalog。回滚方式是删除实验 package 和它在仓库外的 task-local runtime state；稳定技能不需要状态迁移。

## 验证入口

```bash
python3 -m unittest discover -s skills/dbx-implementation-bound-workflow/tests -v
python3 skills/dbx-skill-architect/scripts/run_skill_evals.py \
  skills/dbx-implementation-bound-workflow/evals/evals.json --validate-only
```

全仓还应运行严格 skill lint、eval schema、trigger schema、JSON/YAML parse 和 `git diff --check`。
