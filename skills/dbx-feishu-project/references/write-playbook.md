# Feishu Project write playbook

## Write classes

| Class | Examples | Confirmation |
| --- | --- | --- |
| Low-risk append | Add a factual progress comment, attach user-approved artifact | Confirm unless user explicitly requested exact write |
| Medium-risk update | Edit title, priority, due date, owner, version, iteration, field value | Confirm with patch preview |
| High-risk workflow | Close, reject, change status/node, publish WBS, batch update, reassign owner | Always confirm; dry-run first when possible |
| Destructive or trust-sensitive | Delete, remove relation, bulk overwrite, hide history, falsify state | Refuse or require a safer redesign |

## Required write flow

1. Read current object state.
2. Discover metadata for every field, role, enum, user, and transition involved.
3. Build a minimal patch.
4. Prefer dry-run if supported.
5. Show patch preview.
6. Execute only after approval for that exact patch.
7. Verify by reading back or using the returned update result.
8. Report proof and incomplete parts.

## Patch preview template

```markdown
## 飞书项目写入预览
- 目标：project_key / work_item_id / title
- 操作：update | create | comment | transition | attach | relation | WBS publish
- 变更：
  - field_key_or_role: old_value -> new_value
- 依据：...
- 会通知或影响的人：unknown | none | list
- Dry-run：passed | unavailable | failed
- 风险：...

确认后我再执行。
```

## Update field safety

- Do not put custom business fields at top level if the CLI/API expects `fields[]`.
- For enum fields, use the exact option value returned by metadata.
- For user fields, resolve names to user keys first.
- For roles, use role-specific operations when the CLI/API requires it.
- For arrays, explicitly state whether the operation replaces the entire list or appends/removes one item.
- For date/time fields, include timezone when relevant.

## Comment safety

Comments should be concise and fact-based. Do not include:

- Internal chain-of-thought.
- Secrets, private tokens, raw stack traces with credentials.
- Unverified blame.
- Claims that tests passed unless they actually ran.

Good comment shape:

```markdown
进展同步：
- 已完成：...
- 验证：...
- 风险 / 待确认：...
- 下一步：...
```

## Transition safety

Before moving workflow state:

1. Read current node/status.
2. List available transitions if the CLI supports it.
3. Check required transition fields.
4. Confirm side effects such as notifications, assignment changes, SLA changes, or done metrics.
5. Verify the final state.

## Failure handling

If a write fails:

- Show the operation class and target.
- Show redacted CLI/API error.
- Identify whether the failure is auth, permission, field schema, workflow transition, missing required value, rate limit, or unknown.
- Do not retry high-risk writes blindly.
- Offer the smallest next diagnostic read.
