# MQL and query safety

MQL or filter queries are useful but brittle because project fields and enum values are local.

## Before building a query

- Resolve project key.
- Confirm work item types.
- Confirm field keys and enum values.
- Confirm user keys for people filters.
- Decide whether the user needs all pages or a sample.
- Decide sort order if freshness or priority matters.

## Query contract

```yaml
query_contract:
  project_key: ""
  target_type: ""
  business_question: ""
  field_keys_used: []
  enum_values_used: []
  users_used: []
  page_size: 50
  all_pages_required: false
  sort: ""
  expected_columns: []
```

## Avoid

- Free-text search when a structured field exists and has been confirmed.
- Field display names inside MQL when the API expects field keys.
- Mixing version, iteration, release, and tag unless metadata shows how the project models them.
- Returning a count without saying whether pagination is complete.

## Output for queries

```markdown
## 查询
- 业务问题：...
- MQL / filter：...
- 字段映射：display name -> field_key
- 页数：read pages / total known pages / unknown

## 结果摘要
- 总数：known / lower bound / unknown
- 分组：...
- 最高风险项：...

## 结果明细
| ID | Type | Title | Status | Owner | Version | Updated | Link |
| --- | --- | --- | --- | --- | --- | --- | --- |
```
