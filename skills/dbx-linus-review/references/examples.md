# Examples

## Strict plan review

Input:

```text
为了解决表单草稿状态，我们引入 DraftManager、DraftBus、DraftStore、DraftReconciler 四个概念。
```

Good output direction:

```markdown
## 核心判断
方向对，但方案过度设计。你不是缺四个抽象，你是没有定义草稿状态的 owner 和生命周期。

## 数据结构和模型判断
- 核心实体：draft
- 状态 owner：应该是 form session 或 server draft record 二选一，不应该同时散在 Bus/Store/Reconciler
- 不变量：同一个 draft 在保存失败、刷新、重新打开时只能有一个真实状态

## 主要风险
1. [S1 high] 四个概念分裂了草稿状态 owner
   - Evidence: DraftStore 保存状态，DraftBus 传播状态，DraftReconciler 又能改状态。
   - Impact: 保存失败或重试时 UI 很容易显示已保存但实际未保存。
   - Fix: 先定义一个 draft state machine，再决定是否需要 store。
   - Confidence: medium

## 应该砍掉什么
先砍 DraftBus 和 DraftReconciler。
```

## Strict diff review

Input:

```text
Diff adds global mutable permission cache keyed by userId. Logout clears token but not cache.
```

Good output direction:

```markdown
## 核心判断
不能这样合并。权限缓存的生命周期错了。

## 关键洞察
- 数据结构/状态模型：permissions 被建模成 userId 级别，但真实边界是 session/tenant/permission version。
- 用户/兼容性风险：logout/login 或 tenant switch 后可能读到旧权限。

## 主要发现
1. [S1 high] logout 后权限缓存仍然有效
   - Evidence: cache is global and logout only clears token.
   - Impact: user may see actions from a previous permission set.
   - Fix: scope cache to session/tenant boundary or clear on logout and permission refresh.
   - Confidence: high
```

## Anti-pattern

Bad:

```text
这代码太烂了，重写吧。
```

Better:

```text
The current representation forces three special cases because it stores derived state as mutable source state. Collapse it back to X and delete Y/Z.
```
