# Completion evidence contract

## Read completion

A read is complete when:

- The document identifier and type are known or clearly unresolved.
- The read scope is stated.
- Truncation, embedded resources, permission limits, and missing sections are disclosed.
- The answer separates document content from inference.

## Write completion

A write is complete when:

- The target document and write location are known.
- The exact change was requested or approved.
- The CLI/API returned success or read-back confirms the change.
- The final answer includes location and evidence.

## Standard report

```markdown
## 完成结果
- 状态：completed | partially_completed | failed | blocked
- 操作：read | create | append | update | extract
- 文档：title / url / token
- 位置：heading / block_id / end / new document
- 证据：redacted response / revision / read-back snippet
- 未完成：...
- 风险和限制：...
```

## Do not claim

- “全文已读完” if output was truncated.
- “文档已更新” without tool success or read-back.
- “表格内容是...” when only the parent document was read.
- “评论已添加” if only document body APIs were used.
