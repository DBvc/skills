# Feishu Project read playbook

## URL to object

When given a URL:

1. Decode the URL with the official CLI if available.
2. Extract only decoded values returned by the tool.
3. Resolve the project space if not included.
4. Read the work item or project object by canonical identifiers.
5. If decode fails, ask for the object ID or project key instead of hand-parsing a brittle URL.

Suggested helper:

```bash
python3 skills/dbx-feishu-project/scripts/meegle_call.py decode-url --url '<feishu_project_url>'
```

## Project search

When given a project name, alias, or space label:

```bash
python3 skills/dbx-feishu-project/scripts/meegle_call.py project-search --query '<project name or key>'
```

If multiple spaces match, ask the user to choose unless the URL or surrounding context disambiguates.

## Metadata reads

Use metadata reads before interpreting local vocabulary:

```bash
python3 skills/dbx-feishu-project/scripts/meegle_call.py meta-types --project-key '<PROJECT_KEY>'
python3 skills/dbx-feishu-project/scripts/meegle_call.py meta-fields --project-key '<PROJECT_KEY>' --work-item-type '<TYPE_KEY>'
python3 skills/dbx-feishu-project/scripts/meegle_call.py raw -- workitem meta-roles --project-key '<PROJECT_KEY>' -o json
```

## Work item read

```bash
python3 skills/dbx-feishu-project/scripts/meegle_call.py workitem-get --project-key '<PROJECT_KEY>' --work-item-id '<ID>'
```

Read comments, relations, attachments, or workflow details separately when the user's question depends on them. Do not imply those surfaces were inspected if only the base item was read.

## Query reads

Before using MQL or filters:

1. Confirm field keys and enum values.
2. State intended page size and whether all pages are required.
3. Preserve the actual query in the answer.
4. Mark partial result if the tool returns a cursor, pagination limit, permission warning, or timeout.

## Read output shape

```markdown
## 范围
- 请求：...
- 项目：project_key / display name
- 对象：work_item_id / type / title / link
- 查询条件：...
- 完整性：complete / partial / unknown

## 结果
- 状态：...
- 负责人：...
- 版本 / 迭代：...
- 关键字段：...
- 评论 / 附件 / 关系：已读 / 未读 / 不适用

## 限制
- 未读取：...
- 权限或分页：...
```
