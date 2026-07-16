---
name: dbx-plan-convergence
description: >-
  Manual-only, provider-agnostic controller for bounded convergence of an existing technical plan,
  architecture proposal, migration plan, ADR draft, or implementation proposal. Use only when the
  user explicitly asks for 方案收敛, plan convergence, 方案棘轮, or a controlled review-revision loop
  that must decide whether to revise locally, gather evidence, request a decision, explore another
  direction, finalize, or stop. It may coordinate any human, agent, skill, or tool through a small
  protocol, but has no required collaborator names. Do not use for first-draft planning, standalone
  review, generic brainstorming, code repair, implementation, or open-ended autonomous loops.
---

# DBX Plan Convergence

控制已有技术方案的有界收敛过程。

默认输出中文，除非用户要求其他语言。

## Position

这是一个 workflow controller，不是方案作者，也不是技术 reviewer。

内容能力属于可替换的 provider：

- planner / reviser 负责生成或修改方案；
- reviewer 负责发现技术、模型、兼容性、验证或复杂度问题；
- evidence provider 负责提供仓库、文档、测试、日志或约束事实；
- decision owner 负责产品、架构、兼容性、风险接受等决策；
- convergence control 属于本技能。

本技能只依赖输入输出协议，不依赖任何具体 skill、agent、模型或工具名称。可用 provider 可以是人、当前 agent、独立 agent、其他 skill 或外部工具。

第一产物是 **next-state decision**，不是新版方案。只有结论为 `revise-local` 时，才生成 revision contract，并在用户要求完整循环时把它交给可用 reviser。

## Activation

仅在用户显式要求以下意图时使用：

- “跑一轮方案收敛 / plan convergence”；
- “对这个方案跑方案棘轮”；
- “控制 plan -> review -> revise -> re-review loop”；
- “判断 review 后该修方案、补证据、找人决策还是换方向”；
- “继续上次的方案收敛状态”；
- “只跑 convergence gate，不要改方案”。

不要用于：

- 生成第一版技术方案；
- 只做一次严格 review；
- 普通方案讨论或开放式脑暴；
- 代码 diff 的 review-repair loop；
- 直接实现、提交、发布或修改生产系统；
- Ralph 风格持续完成全部任务；
- 用户明确说不要进入循环、只要直接判断。

这是 manual-only skill。不要因为看到“方案”“review”或“架构”就隐式激活。

## Modes

选择最小充分模式：

| Mode | Use when | Effect |
| --- | --- | --- |
| `gate_only` | 已有方案和 review，用户只想判断下一步 | 不修改方案，只输出 triage、phase、progress gate 和 next action |
| `bounded_loop` | 用户显式要求控制 review-revision-re-review | 可协调 provider，按预算运行有界循环 |
| `resume` | 用户提供之前的 convergence state | 校验状态后从下一门禁继续 |
| `diagnose_stall` | 用户怀疑方案在打转、膨胀或来回翻案 | 识别 flat、oscillation、bloat 或错误 phase |

若没有现成方案或具体 proposal，输出 `blocked-artifact`，并把任务交还给任意 planning provider。不要在本技能里偷偷生成第一版方案。

## Core definitions

### Review pass

对当前 artifact 的一次评审。初始 review 不计入 revision round。

### Revision round

必须同时包含：

1. 一个被接受的 revision contract；
2. 一次受约束的方案修订；
3. 对 accepted findings 和直接回归的 scoped re-evaluation。

只有改了文字但没有重新判断，不算有效 revision round。

### Direction epoch

围绕一组稳定 core anchors 的连续收敛阶段。

Core anchors 通常包括：

- problem / goal；
- success criteria；
- source of truth；
- state or data owner；
- public contract；
- migration / rollout / rollback boundary；
- critical invariants。

局部修订留在当前 epoch。方向性 pivot 开启新 epoch。新 epoch 获得新的 per-epoch 软预算，但 **总轮次、总 epoch 数和历史失败不会清零**。

这个模型允许谨慎探索，又避免把每次翻案伪装成“继续优化”。

## Hard gates

开始前建立：

```yaml
convergence_target:
  artifact_type: technical_plan | architecture_proposal | migration_plan | adr | implementation_proposal | other
  artifact_version: ""
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
  review_material_present: true | false
  requested_mode: gate_only | bounded_loop | resume | diagnose_stall
  may_revise_plan_text: true | false
  may_modify_code: false
```

必须满足：

1. 用户显式要求方案收敛或受控 review-revision loop。
2. 已有具体 artifact，或已有足够具体的 proposal 文本。
3. scope、goal 和 review target 足以避免评审整个宇宙。
4. 本技能不修改代码、不 commit、不 push、不发布、不执行迁移。
5. 方案文本只有在 `bounded_loop` 且用户允许时才可由 reviser 修改。
6. repo、版本、测试、约束或现有架构事实，未读取就不得当成已知。
7. 产品、架构、兼容性、风险接受和不可逆行为，不得由 controller 擅自替 decision owner 决定。
8. 同一 agent 同时担任 author 和 reviewer 时，必须标记 `provider_independence: none`，不得声称独立评审。
9. 任何 “safe / verified / validated / ready” 声明必须受 completion contract 约束。

## Phase gate

每个 epoch 先判断：

### `explore`

出现任一情况时进入 explore：

- core anchor 不稳定或互相矛盾；
- review finding 指向错误 source of truth、owner、identity、contract 或 migration model；
- 候选方向之间的关键 trade-off 尚未决定；
- 需要外部证据才能判断方向；
- 当前方案的局部修补不断增加 adapter、同步层、兼容层、flag 或例外分支。

Explore 阶段禁止把所有 finding 当作局部待办项。允许动作只有：

- `gather-evidence`
- `request-decision`
- `explore-alternatives`
- `pivot-required`
- `stop`

### `converge`

同时满足以下条件时进入 converge：

- goal、scope 和主要 success criteria 稳定；
- core anchors 足够稳定；
- 方向性 blocker 已关闭或被明确接受；
- 剩余 finding 可以被局部修订、验证增强或风险说明解决；
- 最小实施路径仍然清晰。

Converge 阶段只允许按 revision contract 修改，不得顺手换方向或扩大 scope。

## Finding normalization

把任何 reviewer 或人工意见归一化为以下类型：

| Type | Meaning | Default action |
| --- | --- | --- |
| `local_revision` | 当前方向成立，可局部修正文档、切片、边界或说明 | `revise-local` |
| `evidence_gap` | 缺仓库、文档、行为、测试、版本或约束事实 | `gather-evidence` |
| `decision_gap` | 缺产品、架构、兼容性、风险接受或 owner 决策 | `request-decision` |
| `direction_failure` | source of truth、owner、模型、contract 或路线错误 | `pivot-required` |
| `validation_gap` | 风险没有映射到验证、rollout、rollback 或观测 | 通常 `revise-local`，必要时 `gather-evidence` |
| `reviewer_conflict` | reviewer 对关键方向冲突，且不能由现有证据消解 | `gather-evidence` 或 `request-decision` |
| `bloat_signal` | 文档、层次或选项增加，但行动性和确定性没有增加 | `stop-bloat` |
| `advisory` | 有价值但不阻塞当前 handoff | defer 并记录 |

Finding 是信号，不是命令。Controller 负责最终 triage。

## Round budget

默认策略位于 `references/default-policy.yaml`。

核心原则：

- “两轮”是同一方向的 **soft checkpoint**，不是普遍质量上限。
- 方案重要性提高时，优先增加证据、独立 review 维度和 human checkpoint，而不是只增加相同循环次数。
- 超过 soft budget 必须有 progress credit。
- 达到 hard budget 必须停止，除非用户显式给出新的有界预算，并且上一轮通过 progress gate。
- 同一 finding 默认只允许一次失败的局部修订；再次失败通常说明分类错了。
- Pivot 开启新 epoch，但不重置 total budget。

高影响方案至少覆盖两个独立 review dimensions，例如：

- direction / model / ownership；
- compatibility / migration / rollout；
- validation / operability / failure containment；
- security / privacy / performance，仅在相关时。

“同一 reviewer 再读一遍”不自动算独立维度。

## Progress gate

一轮结束后，只有同时满足下面条件才可继续。

### 至少一个 progress credit

- 新外部证据解决了 material unknown；
- decision owner 关闭了关键分支；
- blocker 数量或最高严重度下降；
- source of truth、invariant、implementation slice、validation 或 rollback 的可行动性实质提高；
- review coverage 补上了之前未覆盖的高风险维度；
- pivot 明确淘汰了旧方向，并留下可追溯理由。

### 不得出现 disqualifier

- 新增同级或更高 blocker；
- core anchor 无新证据却发生未批准变化；
- finding 被关闭后又以同一根因重开；
- scope 或复杂度增长，但风险覆盖和行动性没有同步增长；
- 仅改写措辞、重排章节或加入防御性散文；
- 两个方向来回切换；
- provider 只在复述上一轮结论；
- validation / rollout / rollback 变得更弱。

若无 progress credit，结论为 `stopped-flat`。若方向或 anchor 来回切换，结论为 `stopped-oscillating`。若篇幅和机制膨胀，结论为 `stopped-bloat`。

## Provider protocol

Provider 必须按角色提供最小输出，详见 `references/provider-protocol.md`。

最低要求：

- reviewer finding 带 evidence、impact、confidence 和 suggested action signal；
- reviser 只接收 revision contract 和必要上下文；
- re-review 默认只检查 accepted findings、direct regressions 和 anchor drift；
- evidence provider 区分 observed fact、assumption、judgment 和 unknown；
- decision owner 的选择要记录 rationale 和 rejected alternatives。

不要在本技能中写死 provider 名称、模型版本或调用链。

若 host 无法隔离 provider，可在同一 session 顺序执行，但必须：

- 保持 author / reviewer / controller 角色边界；
- 标记非独立；
- 对高影响结论降低 confidence；
- 优先请求外部证据或人工 checkpoint。

## Workflow

### 0. Establish state

读取 artifact、现有 review、已知 evidence、open decisions 和历史 state。

选择 risk profile：

- `standard`
- `high_impact`
- `irreversible`

### 1. Enter or resume an epoch

识别 core anchors、phase、epoch id、revision round 和预算。

### 2. Obtain critique

使用任意可用 reviewer provider。首轮 review 可以较广；修订后的 re-review 必须 scoped。

### 3. Normalize and triage

归类 finding，合并同根因项，识别 direction failure、evidence gap、decision gap、bloat 和 reviewer conflict。

### 4. Choose one next action

每个 gate 只选择一个主动作：

- `revise-local`
- `gather-evidence`
- `request-decision`
- `explore-alternatives`
- `pivot-required`
- `finalize`
- `stop`

不要同时让 reviser 修文档、猜事实和做架构决策。

### 5. Issue a revision contract

仅当 action 为 `revise-local` 时生成合同：

```yaml
revision_contract:
  epoch_id: ""
  round: 1
  purpose: ""
  accepted_findings: []
  frozen_anchors: []
  allowed_changes: []
  forbidden_changes: []
  facts_to_preserve: []
  assumptions_to_keep_explicit: []
  required_validation_updates: []
  re_review_scope: []
  stop_if: []
```

使用 `assets/revision-contract-template.md`。

### 6. Revise through a provider

Reviser 不得：

- 解决 deferred finding；
- 引入新方向；
- 把 unknown 改写成 fact；
- 扩大 scope；
- 为了回答 review 而堆砌章节、抽象或兼容层；
- 删除关键风险、验证或 rollback。

### 7. Scoped re-evaluation

检查：

- accepted findings 是否关闭；
- 是否出现直接回归；
- core anchors 是否 drift；
- evidence boundary 是否被偷换；
- actionability 是否提高；
- scope 和 complexity 是否膨胀。

### 8. Apply progress gate

决定继续当前 epoch、开启新 epoch、finalize 或停止。

## Stop states

使用一个明确状态：

- `ready-for-handoff`
- `needs-evidence`
- `needs-decision`
- `pivot-required`
- `blocked-artifact`
- `stopped-flat`
- `stopped-oscillating`
- `stopped-bloat`
- `stopped-budget`
- `in-progress`

`ready-for-handoff` 只表示方案在当前 evidence boundary 下足以交给下一阶段。它不表示方案绝对正确，也不表示代码、测试或生产行为已验证。

## Completion contract

只有同时满足以下条件才可输出 `ready-for-handoff`：

1. 没有未解决的 `direction_failure`。
2. 会改变实施方向的 `decision_gap` 已关闭。
3. 会翻转计划的 `evidence_gap` 已关闭，或被显式列为实施前 stop condition。
4. core anchors 稳定。
5. implementation path、validation、rollout / rollback 与主要风险有映射。
6. 剩余 advisory、assumption、unknown 和 residual risk 已显式列出。
7. 没有 flat、oscillation 或 bloat 信号。
8. 高影响或不可逆方案满足 profile 的 review breadth 和 human checkpoint。
9. 没有把“文档更完整”误报为“方案已验证”。

## Output contract

默认输出：

```markdown
## 方案收敛结果

结论：<stop state>
模式：<mode>
风险档位：<profile>
阶段：<explore | converge>
方向 epoch：<current / max>
修订轮次：<current / soft / hard / total>

核心判断：
- ...

Finding triage：
- local_revision:
- evidence_gap:
- decision_gap:
- direction_failure:
- validation_gap:
- reviewer_conflict:
- bloat_signal:
- advisory:

Progress gate：
- credits:
- disqualifiers:
- decision: continue | pivot | finalize | stop

下一步合同：
- owner/provider:
- allowed:
- forbidden:
- required evidence or decision:
- stop_if:

剩余风险与证据边界：
- ...
```

`gate_only` 到这里停止。`bounded_loop` 只有在结论为 `revise-local` 且预算允许时继续。

## References

按需读取：

- `references/convergence-model.md`: epoch、round、两轮 checkpoint 和高影响方案策略；
- `references/default-policy.yaml`: 默认预算、profile 和 stop policy；
- `references/provider-protocol.md`: provider roles、finding schema 和适配规则；
- `references/progress-and-stop-gates.md`: progress、flat、oscillation、bloat 和 pivot 细则；
- `references/output-contract.md`: 输出示例；
- `references/examples.md`: 典型场景。
