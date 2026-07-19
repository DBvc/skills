# Output Contract Examples

Compact output always includes transition, core judgment, next-step contract, evidence boundary, and residual risks. Include a blocker/gap section only when it is non-empty.

## 1. Compact local revision

```markdown
## 方案收敛结果

Transition:
- next_action: revise-local
- final_state: null
- phase: converge

核心判断：
- 当前 source of truth 和 owner 稳定。
- 两个 finding 都属于局部实施切片与验证缺口。

下一步合同：
- owner/provider role: revision provider
- allowed: 修改 T2 切片，补充失败路径验证与 rollback stop condition
- forbidden: 改 public API、换 state owner、扩大迁移范围
- stop_if: 最小局部修改不能关闭 F-001/F-002

证据边界与剩余风险：
- 尚未运行实现或测试。
```

内部 transition：

```yaml
transition:
  next_action: revise-local
  final_state: null
  reason: local findings only
  owner_role: revision_provider
  follow_up_if: null
```

## 2. Evidence gap

```markdown
## 方案收敛结果

Transition:
- next_action: gather-evidence
- final_state: needs-evidence
- phase: explore

核心判断：
- 方案假设现有 token cache 由 request scope 管理，但当前没有仓库证据。
- 该事实会决定是局部修复还是重做 owner 模型。

Blocker / gap：
- evidence_gap: 查明 cache 创建位置、生命周期、logout/user-switch 行为和相关测试。

下一步合同：
- owner/provider role: evidence provider
- forbidden: 把 request-scoped 改写成既定事实
- stop_if: 无法访问所需仓库或运行时证据
```

## 3. Alternatives are not a pivot

```markdown
## 方案收敛结果

Transition:
- next_action: explore-alternatives
- final_state: needs-alternatives
- phase: explore

核心判断：
- local cache 与 shared owner 两个方向都还可行。
- 当前证据不足以否决任一方向，缺的是明确比较标准。

下一步合同：
- owner/provider role: planner / alternative assessor
- allowed: 比较 ownership、failure isolation、migration cost 和 reversibility
- forbidden: 把当前方向写成已失败
```

## 4. Direction failure

```markdown
## 方案收敛结果

Transition:
- next_action: initiate-pivot
- final_state: pivot-required
- phase: explore

核心判断：
- logout、user switch 和 permission downgrade 三个 finding 共享根因。
- 当前方案把 session-scoped state 放在 process singleton。
- 继续增加 invalidation、flag 或同步分支只会放大复杂度。

下一步合同：
- 关闭 epoch E1，并记录 rejection reason。
- 先确认 session identity 和 owner boundary。
- 等外部提供新候选方向后再开启 E2。
- total revision budget 不清零。
```

## 5. Stale review

```markdown
## 方案收敛结果

Transition:
- next_action: obtain-review
- final_state: needs-review

核心判断：
- R1 评审的是 plan v1，当前 artifact 是 v2。
- 无法证明 v2 未改变 R1 涉及的 ownership 和 migration 部分。

下一步合同：
- owner/provider role: reviewer provider
- required: 对 v2 重新评审，或提供 R1 仍适用的明确证明
- forbidden: 直接把 R1 findings 当成 v2 的有效 finding
```

## 6. Reviewer conflict with one primary action

```yaml
transition:
  next_action: gather-evidence
  final_state: needs-evidence
  reason: expected implementation count can resolve abstraction need
  owner_role: evidence_provider
  follow_up_if:
    condition: support_horizon_remains_a_policy_choice
    action: request-decision
```

Do not output:

```yaml
next_action:
  - gather-evidence
  - then request-decision
```

## 7. Flat loop diagnostic

```markdown
## 方案收敛诊断

Transition:
- next_action: stop
- final_state: stopped-flat
- phase: converge

Review provenance：
- R1 reviewed v1
- R2 reviewed v2
- R3 reviewed v3

Progress gate：
- credits: 无
- disqualifiers:
  - blocker 和 material unknown 未下降
  - 新增 5 个章节，但 implementation slices 与 validation path 没变化
  - reviewer 只是重述上一轮意见

建议：
- 不再做第四轮文字修订。
- 转为补证据、让 decision owner 选分支，或缩小 scope。
```

## 8. Compact ready output

```markdown
## 方案收敛结果

Transition:
- next_action: finalize
- final_state: ready-for-handoff
- phase: converge

主要收敛：
- 删除了未被需求证明的通用 adapter 层。
- 将三阶段迁移缩减为一次局部替换和兼容性验证。

本次循环：
- full review: 1
- local revision: 1
- scoped re-review: 1

证据边界与剩余风险：
- 当前调用方清单来自仓库扫描。
- 尚未实现代码，也未运行测试。
- residual risk: 边缘调用方可能在实施期暴露，T1 有 stop condition。

下一步：
- 可以进入实现。
```

## 9. Resume mismatch

```markdown
## 方案收敛结果

Transition:
- next_action: stop
- final_state: blocked-state-mismatch

核心判断：
- state 记录 artifact v2 / fingerprint abc。
- 当前输入 artifact v3 / fingerprint def。
- 不能从旧 pending revision contract 继续。

下一步合同：
- 提供与 state 一致的 artifact，或为 v3 建立新的 review pass 与 convergence state。
```

## 10. Diagnostic output fields

Diagnostic mode may include:

```yaml
result:
  mode: gate_only
  risk_profile: high_impact
  phase: explore
  artifact:
    version: v2
    fingerprint: ""
  review_provenance:
    - id: R1
      artifact_version: v2
      provider:
        independence: partially_independent
      dimensions:
        - direction_model_ownership
  triage:
    direction_failure:
      - F-003
  progress:
    credits: []
    disqualifiers:
      - wrong_owner_model
  transition:
    next_action: initiate-pivot
    final_state: pivot-required
  evidence_boundary: []
  residual_risks: []
```

Omit empty categories in user-visible output unless the user requests the serialized state.
