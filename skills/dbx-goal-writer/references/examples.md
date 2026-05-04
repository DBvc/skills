# Examples

## Direct

```text
/goal 修复 checkout 优惠券输入框空字符串时错误触发校验的问题。Context: 关注 src/features/checkout 相关代码和现有优惠券测试。Scope: 只修改 checkout 相关实现、类型和测试。Non-goals: 不改公共表单库、不改优惠券 API。Constraints: 保持现有 UI 和 API 兼容，不新增依赖。Done when: 空字符串不触发错误校验，已有合法/非法优惠券行为保持不变。Validation: 运行 checkout 相关单测、typecheck 和 lint；如命令不存在，说明替代验证。Budget/stop rule: 如果 active goal budget 到达，停止启动新改动并总结进展、剩余工作和下一步。Pause if: 需要改公共校验库、API 契约或新增依赖。Report: 总结变更、测试结果和风险。
```

## File-based start

```text
/goal Execute account form zod migration according to .codex/goals/account-zod/GOAL.md. Read the goal contract before editing code. Respect Scope, Non-goals, Constraints, Acceptance Criteria, Validation, Budget and Stop Rules, and Pause Conditions. Use STATUS.md for progress if present. Completion requires all required validation to pass, or a clear explanation of why a check could not be run.
```

## Package trigger

Use package mode for:

- Framework migration
- Dependency upgrade across many packages
- Performance benchmark loop
- Test suite migration
- Security hardening
- Architecture refactor with multiple milestones
