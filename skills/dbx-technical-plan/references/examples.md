# Examples and Anti-patterns

## Quick plan example

Prompt:

```text
先别写代码，帮我规划一下给这个 React hook 加 loading/error 状态怎么做。
```

Good output shape:

```markdown
## 快速技术计划
- 状态：ready
- 推荐路径：先确认 hook 当前返回值契约，再以兼容方式新增 loading/error，不改调用方语义。
- 关键假设：现有调用方可以接受新增字段，但不能接受字段含义变化。
- 最高风险：破坏调用方对 undefined/null 的判断。
- 实施步骤：
  1. 读 hook 和主要调用方，确认当前 contract。
  2. 新增状态字段，保持现有字段含义。
  3. 补一个成功、失败、加载中的测试或 Story/manual path。
- 验证：typecheck、相关 hook 测试、一个调用方路径。
- 需要停止并重新判断的情况：调用方依赖旧的 loading 推导逻辑或 hook contract 已经公开导出。
```

## Migration plan example

Prompt:

```text
给我一个把 legacy fetch wrapper 迁移到 typed HttpClient 的计划。
```

Good plan properties:

- starts with inventory, not edits;
- partitions call sites into mechanical, manual, and risky;
- states compatibility policy for errors, auth headers, retries, cancellation, and response parsing;
- uses batch order to reduce blast radius;
- defines typecheck, tests, and manual critical flows;
- leaves cleanup until after migration validation.

## Bug-fix strategy example

Prompt:

```text
这个缓存 bug 先不要修，帮我设计修复策略。用户切换账号后还能看到上一个账号的数据。
```

Good plan properties:

- names the invariant: cache entries must be scoped by user identity or cleared on identity switch;
- asks for repro path if missing;
- identifies owner: auth/session state, query cache, local store, persisted cache;
- proposes minimal patch only after source of truth is known;
- requires regression test or manual path for logout/login/user-switch;
- warns against sprinkling manual cache clears in random components.

## Anti-patterns

### Fake deep plan

Bad:

```text
Step 1: Analyze the codebase.
Step 2: Implement the change.
Step 3: Add tests.
Step 4: Deploy.
```

Why bad:

- no source of truth;
- no affected surface;
- no invariant;
- no slice boundaries;
- no validation mapping;
- no stop condition.

### Plan that is secretly implementation

Bad:

```text
I will edit these files now and create the new abstraction.
```

Why bad:

- this skill plans before code;
- it may hand off to implementation but should not silently mutate files.

### Over-planning a local task

Bad:

```text
For a one-line tooltip copy change, create a migration rollout matrix and architecture alternatives.
```

Why bad:

- ceremony adds noise;
- the plan should be smaller than the task.

### Treating handoff as approval

Bad:

```text
The previous handoff suggested putting config in src/shared, so that path is correct.
```

Why bad:

- prompts and handoffs are target evidence, not proof of ownership;
- path correctness must be grounded in project rules and source-of-truth boundaries.
