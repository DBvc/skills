---
name: dbx-plan-convergence
description: Explicit-only, provider-agnostic controller for bounded convergence of an existing technical plan, architecture proposal, migration plan, ADR draft, or implementation proposal. Use when the user explicitly asks for 方案收敛, plan convergence, 方案棘轮, or a controlled review-revision loop, or when an already user-authorized parent workflow explicitly delegates that convergence step with artifact, scope, provider bindings, budget, and modification authority. It decides whether to obtain review, revise locally, gather evidence, request a decision, explore alternatives, pivot, finalize, or stop. Do not use for first-draft planning, standalone review, generic brainstorming, code repair, implementation, or open-ended autonomous loops.
---

# DBX Plan Convergence

控制已有技术方案的有界收敛过程。

默认输出中文，除非用户要求其他语言。

## Position

这是 workflow controller，不是方案作者，也不是技术 reviewer。

内容能力属于可替换 provider：

- artifact provider 提供已有方案；
- reviewer provider 发现技术、模型、兼容性、验证或复杂度问题；
- revision provider 按合同局部修改方案；
- evidence provider 提供仓库、文档、测试、日志或约束事实；
- decision owner 负责产品、架构、兼容性和风险接受决策；
- convergence control 属于本技能。

本技能只依赖协议，不依赖任何具体 skill、agent、模型或工具名称。它可以调用已绑定 provider，但不复制 provider 的专业知识。

第一产物是 **transition decision**，不是新版方案：

```yaml
transition:
  next_action: ""
  final_state: null
```

只有 `next_action: revise-local` 时才生成 revision contract。只有 `bounded_loop`、修改权限允许、provider 可用且预算通过时，controller 才协调执行该局部修订。

## Activation

### Direct explicit activation

仅在用户明确要求以下意图时直接使用：

- “跑一轮方案收敛 / plan convergence”；
- “对这个方案跑方案棘轮”；
- “控制 plan -> review -> revise -> re-review loop”；
- “判断 review 后该修方案、补证据、找人决策还是换方向”；
- “继续上次的方案收敛状态”；
- “只跑 convergence gate，不要改方案”。

### Delegated explicit activation

可以被一个已经由用户显式授权的父 workflow 委托调用。父 workflow 必须传递核心 handoff；`completion_profile` 可省略，省略时默认为 `handoff_ready`：

```yaml
delegation:
  originating_intent: ""
  artifact: {}
  scope: []
  provider_bindings: {}
  budget: {}
  completion_profile: handoff_ready | strict_acceptance
  modification_authority: none | plan_text_only
```

### Current invocation classification

输出形态只由**当前调用**决定。只把当前输入中可消费的顶层结构根视为 delegated 候选，识别 `delegation`、`plan_convergence_handoff` 和 `plan_bundle_handoff`。

恰好出现一个根时，按该 wrapper 自身合同校验，并把其内容归一化为 controller 的 artifact、scope、provider bindings、budget、completion profile 和 modification authority；未知扩展字段原样保留。识别到 wrapper 但字段无效时，走现有 input gate 和失败状态，不得退回 direct。出现多个识别根时 fail closed，报告委托输入歧义，不得签发成功 receipt。没有识别根且用户直接显式激活时，才归类为 direct。

Resume state、history、artifact 正文、引用示例或旧 `activation.kind` 只用于审计，不能改变当前调用的输出形态。不得根据 completion profile、artifact 类型、父 workflow 名称或历史来源猜测 direct/delegated。

委托不等于隐式激活。普通“帮我做方案”“自动完成任务”请求，若父 workflow 没有显式选择本 controller，不得自行加载。

不要用于：

- 生成第一版技术方案；
- 只做一次严格 review；
- 普通方案讨论或开放式脑暴；
- 代码 diff 的 review-repair loop；
- 直接实现、提交、发布或修改生产系统；
- 持续完成全部任务的开放式 autonomous loop；
- 用户明确说只要直接判断、不进入流程控制。

## Modes and input gates

选择最小充分模式：

| Mode | Required input | Effect |
| --- | --- | --- |
| `gate_only` | artifact + applicable review material | 不调用 provider，不修改方案，只输出 gate decision |
| `bounded_loop` | artifact + existing review 或 available reviewer binding | 可协调初始 review、局部 revision、scoped re-review 和 progress gate |
| `resume` | convergence state + current artifact | 校验 schema、artifact identity 和 pending transition 后继续 |
| `diagnose_stall` | artifact + comparable history | 诊断 flat、oscillation、bloat 或错误 phase，不继续修改 |

具体门禁：

- `gate_only` 没有 review material 时，返回 `next_action: obtain-review`、`final_state: needs-review`。
- `bounded_loop` 没有现成 review 时，只有已绑定 reviewer 才能获得初始 critique。
- `resume` 必须先归一化旧 v2 state：缺失 `completion_profile` 时按 `handoff_ready`，缺失 fingerprint scheme 或 structured content ref 时按 `null`，缺失 acceptance 状态时按 `not_requested`，缺失 final-acceptance budget 时按 max `2` / used `0`；绝不从旧 state 推断 `strict_acceptance`。归一化后再确认当前 artifact 与 state 中记录的 type/scheme/version/fingerprint 一致；bundle 还必须匹配同一 `file_bundle` plan/tasks refs。不一致时返回 `blocked-state-mismatch`。旧 state 的空 scheme/ref 不影响普通 `handoff_ready`，但不能满足 strict bundle acceptance。
- `diagnose_stall` 检查 flat/bloat 至少需要一个 before/after transition；检查 oscillation 至少需要两个 anchor flips 或三个可比较 snapshot。历史不足时返回 `blocked-insufficient-history`。
- 没有现成 artifact 或足够具体 proposal 时，返回 `next_action: obtain-artifact`、`final_state: needs-artifact`。不要偷偷生成第一版方案。

## Completion profiles

`completion_profile` 只改变完成门，不改变 mode、transition 集合或 provider 分工：

- `handoff_ready`：默认通用路径。关闭已知 material findings 并满足 completion contract 后即可交接；不得表述为严格 reviewer 已接受。
- `strict_acceptance`：用于准备进入实现、并要求严格 reviewer 最终验收的组合路径。DBX implementation-bound technical-plan handoff 只有在单 artifact 已物化为可读取 path 时才选择此 profile；chat-only artifact 使用 `handoff_ready`。

`strict_acceptance` 不新增 final state；通过时仍输出 `finalize + ready-for-handoff`，但必须附带 identity-bound `strict_acceptance_receipt`。

如果初始 full review 已绑定当前 artifact，且之后没有发生 artifact revision，它可以作为最终验收 review。只要 artifact 被修改过，旧 full review 和旧 receipt 立即失效；scoped re-review 只能证明 accepted findings 已关闭，不能单独签发 strict acceptance。

## Core definitions

### Review pass

对一个明确 artifact 版本的一次评审。每个 review pass 必须绑定：

- review id；
- artifact version；
- optional artifact fingerprint；
- provider id/type/capability；
- per-review independence；
- review dimensions；
- full 或 scoped review 范围；
- findings。

Finding 必须记录 `source_review_id`。Scoped re-review 还必须绑定产生该修订的 revision contract id；full review 不需要 contract id，序列化模板使用 `null`。详见 `references/provider-protocol.md`。

如果 review 明确针对旧版本，且无法证明相关内容未变，不得把 finding 自动应用到新版本。应返回 `needs-review`。

同一轮中同时提供 artifact 和明确针对该 artifact 的自然语言 review 时，controller 可以分配 session-local version/id，不要求用户手写 schema。持久化、resume、多版本或多 reviewer 场景必须使用显式版本绑定。

### Revision round

必须同时包含：

1. 一个被接受的 revision contract；
2. 一次受约束的 artifact revision；
3. 对新版 artifact 的 scoped re-review；
4. 一次 progress gate。

初始 review 不计入 revision round。只有改了文字但没有重新判断，不算有效 round。

### Direction epoch

围绕一组稳定 core anchors 的连续收敛阶段。

Core anchors 按任务适用性选择，常见包括：

- problem / goal；
- success criteria；
- source of truth；
- state or data owner；
- public contract；
- migration / rollout / rollback boundary；
- critical invariants。

Anchor status：

- `unknown`
- `stable`
- `conflicted`
- `not_applicable`

不要为了填表让普通小方案虚构 public contract、migration 或 rollout 散文。

局部修订留在当前 epoch。方向性 failure 关闭旧 epoch；只有外部提供新候选方向后，才能开启新 epoch。新 epoch 获得新的 per-epoch 软预算，但总轮次、总 epoch 数和历史失败不清零。

## Transition model

`next_action` 表示接下来应该做什么。`final_state` 表示当前 convergence invocation 是否结束或需要外部 handoff。

| next_action | final_state | Meaning |
| --- | --- | --- |
| `obtain-artifact` | `needs-artifact` | 缺已有方案，交给 artifact provider |
| `obtain-review` | `needs-review` | 缺 review 或 review 已 stale |
| `revise-local` | `null` | 当前方向可局部修，workflow 仍可继续 |
| `gather-evidence` | `needs-evidence` | 必须外部补事实后 resume |
| `request-decision` | `needs-decision` | 必须由 decision owner 选择后 resume |
| `explore-alternatives` | `needs-alternatives` | 方向尚未选定，但当前方向不一定已失败 |
| `initiate-pivot` | `pivot-required` | 当前方向已被否决，关闭 epoch 并等待新方向 |
| `finalize` | `ready-for-handoff` | 当前证据边界内可交给下一阶段 |
| `stop` | `stopped-*` 或 `blocked-*` | 循环停止或输入不一致 |

每个 gate 只能选择一个主动作。后续可能动作使用：

```yaml
follow_up_if:
  condition: ""
  action: ""
```

不要把动作数组写成“先 gather evidence，再 request decision”。先选当前最小可执行动作。

## Hard gates

开始前建立：

```yaml
convergence_target:
  artifact_type: technical_plan | implementation_plan_bundle | architecture_proposal | migration_plan | adr | implementation_proposal | other
  artifact_version: ""
  artifact_fingerprint_scheme: null | exact-bytes-sha256 | plan-first-bundle-sha256-v1
  artifact_fingerprint: ""
  artifact_content_ref:
    kind: inline | path | current_context | file_bundle | null
    value: null
    plan: null
    tasks: null
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
  requested_mode: gate_only | bounded_loop | resume | diagnose_stall
  completion_profile: handoff_ready | strict_acceptance
  review_material_present: true | false
  reviewer_binding_available: true | false
  may_revise_plan_text: true | false
  may_modify_code: false
```

必须满足：

1. 用户直接显式授权，或已授权父 workflow 显式委托。
2. artifact、scope 和 goal 足以避免评审整个宇宙。
3. review 必须绑定到当前 artifact；stale review 不得继续应用。
4. 本技能不修改代码、不 commit、不 push、不发布、不执行迁移。
5. 只有 `bounded_loop` 且 `may_revise_plan_text: true` 时，revision provider 才能修改方案。
6. repo、版本、测试、约束或现有架构事实，未读取就不得当成已知。
7. 产品、架构、兼容性、风险接受和不可逆行为，不得由 controller 替 decision owner 决定。
8. independence 记录在每个 review pass 上；同一上下文承担 author 和 reviewer 时必须标记 `none`。
9. 任何 safe、verified、validated、ready 声明必须受 completion contract 约束。
10. `strict_acceptance` 没有可用 reviewer 时返回 `obtain-review + needs-review`；不得降级为 `handoff_ready`。
11. 没有有效 `strict_acceptance_receipt` 时，不得输出“严格 reviewer 已接受”“strict PASS”或同义声明。
12. `strict_acceptance` 必须在 review 前由 controller 或 artifact provider 用已声明、可识别的确定性 scheme 计算 `sha256:<64 lowercase hex>`：单文件必须使用可读取的 `content_ref.kind: path` 并直接 hash 该文件的 exact bytes；`implementation_plan_bundle` 必须使用带完整 plan/tasks refs 的 `file_bundle` 和 `plan-first-bundle-sha256-v1`。`inline`、`current_context`、placeholder、未知 scheme、格式错误、不可读取或无法重算均返回 `obtain-artifact + needs-artifact`，不得调用 final review 或签发 receipt。普通 `handoff_ready` 仍可使用 inline/current-context artifact。

## Phase gate

### `explore`

出现任一情况时进入 explore：

- applicable core anchor 不稳定或互相矛盾；
- finding 指向错误 source of truth、owner、identity、contract 或 migration model；
- 候选方向之间的关键 trade-off 尚未决定；
- 需要外部证据才能判断方向；
- 局部修补持续增加 adapter、同步层、兼容层、flag 或例外分支。

Explore 阶段禁止把所有 finding 当作局部待办。允许动作：

- `gather-evidence`
- `request-decision`
- `explore-alternatives`
- `initiate-pivot`
- `stop`

### `converge`

同时满足以下条件时进入 converge：

- goal、scope 和主要 success criteria 稳定；
- applicable core anchors 足够稳定；
- 方向性 blocker 已关闭或被明确接受；
- 剩余 finding 可通过局部修订、验证增强或风险说明解决；
- 最小实施路径仍然清晰。

Converge 阶段只允许按 revision contract 修改，不得顺手换方向或扩大 scope。

## Finding normalization

| Type | Meaning | Default transition |
| --- | --- | --- |
| `local_revision` | 当前方向成立，可局部修正文档、切片、边界或说明 | `revise-local` + `null` |
| `evidence_gap` | 缺仓库、行为、测试、版本或约束事实 | `gather-evidence` + `needs-evidence` |
| `decision_gap` | 缺产品、架构、兼容性或风险决策 | `request-decision` + `needs-decision` |
| `direction_failure` | source of truth、owner、模型、contract 或路线错误 | `initiate-pivot` + `pivot-required` |
| `validation_gap` | 风险没有映射到 validation、rollout、rollback 或 observability | 通常 `revise-local`，缺事实时 `gather-evidence` |
| `reviewer_conflict` | reviewer 对关键方向冲突且证据不足 | 先 `gather-evidence`，必要时 follow-up `request-decision` |
| `bloat_signal` | 文档、层次或机制增加，但行动性和确定性没有增加 | `stop` + `stopped-bloat` |
| `advisory` | 有价值但不阻塞当前 handoff | defer 并记录 |

Finding 是信号，不是命令。Controller 负责合并同根因 finding 并选择一个主 transition。

## Round budget

默认策略位于 `references/default-policy.yaml`。

核心原则：

- “两轮”是同一方向的 soft checkpoint，不是普遍质量上限。
- `strict_acceptance` 的 final full review 使用独立预算；预算耗尽仍未通过时必须 `stop + stopped-budget`。
- 方案重要性提高时，优先增加证据、review dimensions、independence 和 human checkpoint，而不是只增加相同循环次数。
- 超过 soft budget 必须有 progress credit。
- 达到 hard budget 必须停止；用户只能显式增加一个新的有界预算。
- 同一 finding 默认只允许一次失败的局部修订；再次失败通常说明分类错了。
- Pivot 不重置 total budget。

高影响方案至少覆盖两个相关的 review dimensions。多个 reviewer 重复同一 lens 仍只算一个维度；多个模型也不自动等于独立信息。

## Execution boundary

Controller 可以协调已绑定 provider 完成：

- obtain initial review；
- normalize findings；
- issue revision contract；
- bounded local revision；
- scoped re-review；
- strict profile 的 final full acceptance review；
- progress gate。

Controller 必须暂停或 handoff：

- `gather-evidence`
- `request-decision`
- `explore-alternatives`
- `initiate-pivot`

它可以在 evidence、decision 或新方向被外部提供后通过 `resume` 继续，但不得自己查事实、替 owner 决策或生成新方向来绕过边界。

`gate_only` 永远不调用 provider、不修改 artifact。

`bounded_loop` 只有同时满足以下条件才继续：

```text
next_action == revise-local
and final_state == null
and budget_allows
and modification_authority_allows
and revision_provider_available
```

## Progress gate

一轮结束后，只有同时满足下面条件才可继续。

### 至少一个 progress credit

- 新外部证据解决 material unknown；
- decision owner 关闭关键分支；
- blocker 数量或最高严重度下降；
- source of truth、invariant、implementation slice 或 validation 的行动性实质提高；
- review coverage 补上未覆盖的高风险维度；
- 被否决方向留下可追溯理由，并且不再作为模糊 fallback。

### 不得出现 disqualifier

- 新增同级或更高 blocker；
- core anchor 无新证据却发生未批准变化；
- finding 被关闭后又以同一根因重开；
- scope 或复杂度增长，但风险覆盖和行动性没有同步增长；
- 仅改写措辞、重排章节或加入防御性散文；
- 两个方向来回切换；
- provider 只复述上一轮结论；
- validation 或适用的 rollout/rollback/containment 变弱；
- scoped re-review 针对的不是 revision 后 artifact。

若无 progress credit，使用 `stop + stopped-flat`。若方向来回切换，使用 `stop + stopped-oscillating`。若机制膨胀，使用 `stop + stopped-bloat`。

## Workflow

1. **Validate activation and mode inputs**：检查 direct/delegated authority、artifact、review、history 和 modification authority。
2. **Bind artifact identity**：记录 type/scheme/version/fingerprint 和 structured content ref；bundle 必须保留两个 exact file refs。拒绝 stale review 或 stale resume state。
3. **Establish state**：选择 risk profile，识别 epoch、phase、applicable anchors 和预算。
4. **Obtain or consume critique**：`gate_only` 只消费；`bounded_loop` 可调用已绑定 reviewer。
5. **Normalize and triage**：归类 finding、合并根因、记录 review provenance。
6. **Choose one transition**：输出 `next_action`、`final_state` 和 optional `follow_up_if`。
7. **Issue revision contract**：仅在 `revise-local` 时生成，冻结 anchors、artifact type/scheme/content refs 和禁止项；bundle 必须同时绑定 `plan.md` 与 `tasks.md`。
8. **Revise through provider**：只在 bounded execution gates 全部通过时执行。
9. **Scoped re-review**：绑定到新版 artifact，只检查 accepted findings、direct regressions、anchor drift、evidence drift、scope 和 bloat。
10. **Apply progress gate**：继续当前 epoch、等待外部输入、关闭旧 epoch、进入候选完成态或停止。
11. **Apply completion profile**：`handoff_ready` 使用通用完成门；`strict_acceptance` 先检查当前 artifact 是否已有 qualifying independent full review，发生过 revision 时必须运行 fresh full review。新 finding 回到 triage；通过后签发 receipt。
12. **Render output**：先按当前 invocation 分类，再按 mode 使用 compact 或 diagnostic 输出；完整 state 只在 resume、诊断或用户要求时展示。

## Final states

允许的非空 `final_state`：

- `needs-artifact`
- `needs-review`
- `needs-evidence`
- `needs-decision`
- `needs-alternatives`
- `pivot-required`
- `ready-for-handoff`
- `blocked-state-mismatch`
- `blocked-insufficient-history`
- `stopped-flat`
- `stopped-oscillating`
- `stopped-bloat`
- `stopped-budget`

`needs-*` 和 `pivot-required` 是当前 invocation 的 handoff state，可在外部输入到达后 resume。`ready-for-handoff` 只表示方案在当前 evidence boundary 下足以交给下一阶段，不表示代码、测试或生产行为已验证。

## Completion contract

只有同时满足以下条件才可输出 `ready-for-handoff`：

1. 没有未解决的 `direction_failure`。
2. 会改变实施方向的 `decision_gap` 已关闭。
3. 会翻转方案的 `evidence_gap` 已关闭；仅非方向性实施未知可以作为明确 stop condition 留下。
4. 所有 applicable core anchors 为 `stable`；非适用项明确为 `not_applicable`。
5. implementation path 和 validation 与主要风险有映射。
6. 仅当任务涉及兼容性、迁移、发布或不可逆风险时，要求 rollout、rollback 或 containment 达到 profile 要求。
7. review pass 与当前 artifact identity 一致，review breadth 满足 profile。
8. 剩余 advisory、assumption、unknown 和 residual risk 已显式列出。
9. 没有 flat、oscillation 或 bloat 信号。
10. 高影响或不可逆方案满足 human checkpoint policy。
11. 没有把“文档更完整”误报为“方案已验证”。

`strict_acceptance` 还必须同时满足：

12. qualifying review 是绑定当前 artifact type、recognized fingerprint scheme、version、structured content ref 和经重算确认的 `sha256:<64 lowercase hex>` fingerprint 的 `full` review，并发生在最后一次 revision 之后。单 artifact content ref 必须是可读取的 `path`；bundle content ref 必须是带非空 plan/tasks 的 `file_bundle`。`inline` 与 `current_context` 只能用于普通 `handoff_ready`，不能产生 strict receipt。
13. qualifying reviewer 的 independence 为 `independent`；review pass 的 provider id 必须唯一匹配 `provider_bindings.reviewers`，并原样携带该 binding 的非空 capability，不能根据 provider/skill 名称推断；它只接收当前 artifact、scope、evidence boundary、non-goals 和 requested dimensions，不接收作者隐藏推理或旧 reviewer 结论。
14. 未解决的 `blocker` 和 `high` finding 数量为 0，review judgment 为 `accept` 或 `accept_with_advisories`。
15. `medium` finding 已修复，或被 reviewer 明确判为非阻塞并作为 residual risk 记录；涉及产品、架构、兼容性或风险接受时还必须由 decision owner 解决。Controller 不得自行降级或接受风险。
16. 输出 `strict_acceptance_receipt`，绑定 artifact identity、structured content ref、final full review id、由匹配 provider binding 证明的 reviewer capability、independence、judgment 和 residual findings。

任一内容修改都会使 receipt 失效。Final full review 发现新 finding 时，按正常 triage 选择 `revise-local`、`gather-evidence`、`request-decision`、`initiate-pivot` 或 `stop`；不得保留旧 PASS。

## Output contract

默认输出模式：

```yaml
output_mode:
  gate_only: diagnostic
  bounded_loop: compact
  resume: compact
  diagnose_stall: diagnostic
```

`strict_acceptance` 成功使用同一个 canonical YAML proof，但 presentation 取决于当前 invocation：

- **delegated**：只输出 raw YAML，从 `qualification` 开始，以 `strict_acceptance_receipt` 结束；不得添加 Markdown fence、标题或周边说明。
- **direct**：先输出有实际判断的中文 compact summary，再输出唯一的 `## 机器回执` 标题和唯一一个 `yaml` fenced canonical proof；closing fence 必须是响应结尾，不得添加尾注。Summary 至少说明 transition、核心判断、final review、artifact identity、证据边界和 residual risks。

Canonical proof 的字段、顺序和内容不因 presentation 改变。Direct 输出不得把内部 state dump 当作 summary，也不得在 fence 外复制 `strict_acceptance_receipt`。

其他 Compact 输出必须包含：

```markdown
## 方案收敛结果

Transition:
- next_action: <required action>
- final_state: <state or null>
- phase: <current phase>

核心判断：
- <current judgment>

下一步合同：
- owner/provider role: <role>
- allowed: <allowed work>
- forbidden: <forbidden work>
- stop_if: <stop condition>

证据边界与剩余风险：
- <evidence limits and residual risks>
```

`strict_acceptance` 通过时还必须包含 `strict_acceptance_receipt`。未请求该 profile 时，普通 `ready-for-handoff` 不得伪装成严格验收结果。Receipt schema 和示例见 `references/provider-protocol.md` 与 `references/output-contract.md`。

存在 blocker 或 gap 时增加：

```markdown
Blocker / gap：
- <material blocker or gap>
```

Diagnostic 输出额外包含：review provenance、完整 triage、epoch/budget、progress credits/disqualifiers、anchor status 和 history evidence。

不要输出空分类。异常停止、人类决策、stale review 或 direction failure 即使在 compact mode 下也必须显示原因。

`gate_only` 输出 transition 后停止。`bounded_loop` 只按 execution boundary 继续。

## References

按需读取：

- `references/convergence-model.md`: epoch、round、transition 和高影响策略；
- `references/default-policy.yaml`: mode gates、预算、execution 和 output policy；
- `references/provider-protocol.md`: review pass、provider roles 和 adapter rules；
- `references/progress-and-stop-gates.md`: progress、stale review、flat、oscillation、bloat 和 ready gate；
- `references/output-contract.md`: compact / diagnostic 示例；
- `references/examples.md`: 典型场景；
- `references/state-migration-v1-to-v2.md`: state schema 迁移。

Assets:

- `assets/convergence-state-template.json`: v2 resumable state skeleton；
- `assets/review-pass-template.json`: review provenance envelope；
- `assets/revision-contract-template.md`: bounded local revision contract。
