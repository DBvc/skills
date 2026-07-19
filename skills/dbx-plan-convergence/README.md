# dbx-plan-convergence

Explicit-only、provider-agnostic 的技术方案收敛控制器。

它不负责“把方案写好”，而负责判断：

- 当前是在 explore 还是 converge；
- review finding 应推动局部修订、补证据、请求决策、探索替代方向、pivot 还是停止；
- review 是否针对当前 artifact 版本；
- 当前循环是否有真实信息增益；
- 何时可以 handoff，何时只是文档变胖；
- 高影响方案如何提高严谨度，而不是盲目增加相同轮数。

## v3 status

v3 冻结 v2 的 controller kernel，不增加新状态或新执行能力，只修复接口一致性：

- compact 输出只在 blocker / gap 实际存在时展示该部分；
- scoped re-review envelope 显式携带 revision `contract_id`；
- 未绑定 reviewer 的空白模板使用 `provider.type: unknown`，不再默认声称来自人类；
- `convergence_state_version` 仍为 `2`，现有 v2 state 无需迁移。

## v2 foundation

- 分离 `next_action` 与 `final_state`，移除把 `in-progress` 当终态的歧义。
- 所有 review pass 绑定 artifact version/fingerprint，并记录 per-review independence。
- 增加 mode-specific input gates、stale review gate 和 resume identity gate。
- 明确 controller 只协调 review/local revision loop；evidence、decision、alternative 和 pivot 必须 handoff。
- `explore-alternatives` 使用 `needs-alternatives`，不再误报为当前方向已经失败。
- Core anchor 支持 `not_applicable`，避免小方案被 rollout/migration 模板灌成水泥柱。
- `bounded_loop` 与 `resume` 默认 compact 输出；完整状态仅在 gate、诊断、恢复或用户要求时展示。
- 增加 state v1 -> v2 迁移说明和 trajectory eval cases。

## Install

从 `DBvc/skills` 仓库根目录解压，使目录成为：

```text
skills/dbx-plan-convergence/
```

然后运行：

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

这个 ZIP 只包含 skill 目录，不修改根 README、index、routing matrix 或其他 skills。

## No hard dependency

运行时不引用任何固定 planner、reviewer、evidence skill 或模型名称。

Provider 可以是：

- 人工作者或 reviewer；
- 当前 agent 的隔离角色；
- 独立 agent；
- 任意 planning / review / repository-grounding capability；
- 文档、代码库、测试、日志或外部工具。

组合依赖协议和 provider binding，不依赖具体名称。DBX collection 可以在外部 workflow 中绑定默认 provider，但 binding 不进入 controller 内核。

## Activation

### Direct

```text
对下面的方案和 review report 跑 dbx-plan-convergence gate_only。
只判断下一步，不要修改方案。
```

### Delegated

一个已由用户授权的父 workflow 可以显式委托：

```yaml
delegation:
  originating_intent: "对当前技术方案执行有界收敛"
  artifact: "plan-v2"
  scope: ["auth-cache"]
  provider_bindings:
    reviewer: "configured-reviewer"
    reviser: "configured-reviser"
  budget:
    revision_rounds: 1
  modification_authority: plan_text_only
```

这不允许普通 planning 请求隐式触发本技能。

## Core model

```text
artifact identity
  -> review pass bound to artifact
  -> finding normalization
  -> one transition decision
  -> optional revision contract
  -> bounded revision
  -> scoped review bound to new artifact
  -> progress gate
  -> continue / handoff / pivot / finalize / stop
```

Transition 分离动作和结果：

```yaml
transition:
  next_action: revise-local
  final_state: null
```

“同一方向两轮”是默认 soft checkpoint，不是质量上限。Pivot 关闭旧 epoch，但总预算不会清零。

## Typical use

### Gate only

```text
对下面的方案和 review report 跑 gate_only。
输出 next_action、final_state、finding triage 和理由，不要调用 reviewer 或修改方案。
```

### Bounded loop

```text
对这个现有技术方案跑 bounded_loop。
只允许局部 revision；遇到 evidence、decision、alternative 或 pivot 时暂停 handoff。
```

### Diagnose a stuck loop

```text
这个方案已经经历多个 review/revision 版本。
诊断 flat、oscillation 或 bloat，不要继续修改。
```

### Resume

```text
使用这个 convergence state 和当前 artifact 继续。
先校验 version/fingerprint；不一致就停止。
```

## Package layout

```text
skills/dbx-plan-convergence/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── assets/
│   ├── convergence-state-template.json
│   ├── review-pass-template.json
│   └── revision-contract-template.md
├── evals/
│   ├── evals.json
│   ├── trajectories.json
│   └── triggers.json
└── references/
    ├── convergence-model.md
    ├── default-policy.yaml
    ├── examples.md
    ├── output-contract.md
    ├── progress-and-stop-gates.md
    ├── provider-protocol.md
    └── state-migration-v1-to-v2.md
```

## Collection integration boundary

以下内容应放在 collection workflow、command 或 routing matrix，不放进本 skill：

- 默认使用哪个 planner 或 reviewer；
- 技术计划是否默认进入 convergence；
- evidence state 应路由给谁；
- convergence 在持久化计划流程中的前后顺序；
- 跨模型 reviewer 的执行与资源预算；
- 自动实现、验证和代码 ratchet 的跨 controller 调度。

本 skill 只暴露稳定的 transition、provider 和 state 协议。

## Suggested repository entries

### README stable skills

```markdown
| `dbx-plan-convergence` | 显式触发、provider-agnostic 的技术方案收敛控制器：绑定 review 与 artifact 版本，区分探索与收敛，triage findings，用 evidence / decision / direction / progress gates 控制局部 revision loop，并在 stale、打转、膨胀或方向错误时 handoff 或停止。 |
```

### DBX skill index

```markdown
### `dbx-plan-convergence`

- Position: explicit-only, provider-agnostic plan convergence controller.
- Trigger: explicit 方案收敛 / plan convergence / 方案棘轮，或已授权父 workflow 的显式委托。
- Near miss: first-draft planning, standalone review, brainstorming, code repair, implementation.
- Main risk controlled: stale review, action/state ambiguity, false convergence, evidence invention, decision substitution, oscillation, and document bloat.
```
