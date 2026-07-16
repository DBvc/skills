# Output Contract Examples

## 1. Local revision

```markdown
## 方案收敛结果

结论：in-progress
模式：bounded_loop
风险档位：standard
阶段：converge
方向 epoch：1 / 2
修订轮次：1 / soft 2 / hard 3 / total 5

核心判断：
- 当前 source of truth 和 owner 稳定。
- 两个 finding 都是局部实施切片和验证缺口，不需要换方向。

Finding triage：
- local_revision: F-001
- validation_gap: F-002
- 其他：无

Progress gate：
- credits: 上轮关闭一个 blocker，补齐 rollback 验证路径
- disqualifiers: 无
- decision: continue

下一步合同：
- owner/provider: 任意 revision provider
- allowed: 修改 T2 切片、补充失败路径验证和 rollback stop condition
- forbidden: 改 public API、换 state owner、扩大迁移范围
- stop_if: 最小局部修改不能关闭 F-001/F-002
```

## 2. Evidence gap

```markdown
## 方案收敛结果

结论：needs-evidence
阶段：explore

核心判断：
- 方案假设现有 token cache 由 request scope 管理，但当前没有仓库证据。
- 这个事实会决定是局部修复还是重做 owner 模型。

下一步合同：
- owner/provider: evidence provider
- required: 查明 cache 创建位置、生命周期、logout/user-switch 行为和相关测试
- forbidden: 在方案里把 request-scoped 当成既定事实
- stop_if: 无法访问所需仓库或运行时证据
```

## 3. Direction failure

```markdown
## 方案收敛结果

结论：pivot-required
阶段：explore
方向 epoch：1 已关闭

核心判断：
- logout、user switch 和 permission downgrade 三个 finding 共享根因。
- 当前方案把 session-scoped state 放在 process singleton。
- 继续增加 invalidation、flag 或同步分支只会放大模型复杂度。

下一步合同：
- 关闭旧方向，并记录 rejection reason。
- 先确认 session identity 和 owner boundary。
- 新候选方向进入 epoch 2。
- total revision budget 不清零。
```

## 4. Flat loop

```markdown
## 方案收敛结果

结论：stopped-flat
修订轮次：3

Progress gate：
- credits: 无
- disqualifiers:
  - blocker 和 material unknown 数量未下降
  - 新增 5 个章节，但 implementation slices 与 validation path 没变化
  - reviewer 只是重述上一轮意见

建议：
- 不再做第四轮文字修订。
- 转为补证据、让 decision owner 选分支，或缩小 scope。
```

## 5. Ready

```markdown
## 方案收敛结果

结论：ready-for-handoff
风险档位：high_impact
阶段：converge

完成证据：
- direction/model review 已覆盖
- migration/rollback review 已覆盖
- material decision gaps 已关闭
- repo-grounded evidence gaps 已关闭
- 关键风险已映射到验证和 rollout stop conditions
- residual risks 已列出

限制：
- ready 只针对当前 evidence boundary。
- 尚未实现代码，也没有声称测试或生产行为已验证。
```
