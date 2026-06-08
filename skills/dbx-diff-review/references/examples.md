# Examples

## Staged subset review

User says: “帮我 review 要提交的 staged diff，另外两个文件是调试，不用管。”

Good response shape:

```markdown
## Review 目标
- 来源：staged/index diff
- 范围：`src/auth/cache.ts`, `src/auth/logout.ts`
- 未纳入范围：unstaged `src/debug.ts`, `src/dev-only.ts`
- 假设：本次结论只覆盖 staged hunks
```

Do not review the debug files. If they appear necessary for the staged diff to compile, say the staged target may be incomplete.

## Selected files review

User says: “只看 `src/store/user.ts` 和 `src/api/user.ts`。”

Good:

```text
我会把这两个文件作为 reviewed target；`src/types/user.ts` 只作为上下文读取。
```

Bad:

```text
我顺便 review 了整个 repo，发现 Profile 组件命名不好。
```

## High-signal data model finding

```text
[S1 high] Permission cache misses tenant boundary
Evidence: `permissionStore.ts` now caches by `userId`; `TenantSwitcher` keeps the same user id while changing tenant.
Impact: tenant switch can show actions from the previous tenant until reload.
Fix: key by session/tenant boundary or invalidate on tenant switch and permission refresh.
Confidence: high
Verification: not run; needs tenant-switch regression test.
```

## Weak finding to suppress

```text
[S2 medium] This code feels complex.
```

Suppress or rewrite with concrete evidence:

```text
The new `DraftBus` and `DraftStore` both mutate draft status. A failed save updates `DraftStore` but does not emit a rollback event, so the UI can keep showing “saved”.
```

## No major findings

```markdown
## 核心判断
未发现需要阻止合并的问题。最高风险是表单错误态没有自动化回归覆盖，但从 diff 读取看主路径合理。

## Review 目标
- 来源：selected files in staged diff
- 范围：...

## 残余风险
- 未运行 e2e，不能确认浏览器内交互。

## 验证建议
- `pnpm test form-draft`
- 手动验证：编辑、保存失败、刷新、重新打开草稿。
```
