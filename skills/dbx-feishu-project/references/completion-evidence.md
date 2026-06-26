# Completion evidence contract

Do not report external-system work as complete without evidence.

## Read completion

A read is complete when:

- The project/work item/query target is resolved or unresolved status is clearly stated.
- The tool output was inspected.
- Pagination and permission limits are stated.
- The answer separates observed fields from inference.

## Write completion

A write is complete when:

- The exact target object is known.
- The exact patch was approved or was explicitly requested in the same turn.
- The CLI/API returned success, or a follow-up read confirms the change.
- The response includes actual changed fields or created object IDs.

## Standard completion report

```markdown
## 完成结果
- 状态：completed | partially_completed | failed | blocked
- 操作：read | query | create | update | comment | transition | attach | relation
- 项目：...
- 对象：...
- 证据：redacted command envelope / response id / read-back values
- 变更：...
- 未完成：...
- 风险和限制：...
```

## Things not to say without proof

- “已经更新成功” without CLI/API success or read-back.
- “所有相关需求都查完了” without complete pagination.
- “权限没问题” without a successful operation.
- “字段就是 X” without metadata or an observed response.
- “版本/迭代模型是固定的” unless the specific project metadata proves it.
