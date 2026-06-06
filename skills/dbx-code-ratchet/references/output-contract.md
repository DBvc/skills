# Output Contract

## pass-ready example

```markdown
## 代码棘轮结果

结论：pass-ready

目标：
- 来源：staged
- 范围：src/auth/cache.ts, src/auth/logout.ts
- 未纳入范围：src/debug.ts unstaged，不在本次目标内

轮次：
- full review: 1 / 1
- repair rounds: 1 / 2
- re-review rounds: 1 / 2
- subagents: used, reviewers fork_context=false

风险变化：
- before: S0=0, S1=1, S2=1, S3=0, risk_score=30
- after: S0=0, S1=0, S2=0, S3=0, risk_score=0
- complexity: within budget

已自动修复：
1. F-001 [S1 state_ownership] logout 后权限缓存未失效。
2. F-002 [S2 validation_gap] 补了 user switch/logout 回归测试。

未自动修复：无。

方向判断：
- 当前方向：ok
- 证据：修复没有新增 owner、依赖、public API 或额外抽象。

验证：
- typecheck: passed
- tests: passed, focused auth tests
- lint: not_run，项目没有明确 lint 命令
```

## direction failure example

```markdown
## 代码棘轮结果

结论：stopped-direction-failure

原因：
多个 finding 指向同一根因：当前实现把 session-scoped state 放进 module singleton，导致 logout、user switch、permission downgrade 都需要补丁式清理。

我没有继续自动修，因为局部修复会继续增加分支和缓存同步逻辑。

建议：
1. 回滚当前 singleton cache 方案。
2. 先明确 session/user identity 是状态 owner。
3. 重新实现更小的局部缓存，再跑一次代码棘轮。
```

## diverging example

```markdown
## 代码棘轮结果

结论：stopped-diverging

原因：
第一轮自动修复关闭了 1 个 S2，但新增 1 个 S1 compatibility risk，并且 diff 从 2 个文件扩展到 7 个文件，超出复杂度预算。

建议：
- 回滚本轮 repair patch。
- 保留原始 review findings，重新判断修复方向。
```
