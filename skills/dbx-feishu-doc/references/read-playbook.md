# Feishu Doc read playbook

## Basic read

Use the official CLI or helper wrapper:

```bash
python3 skills/dbx-feishu-doc/scripts/lark_doc_call.py fetch --doc '<doc_url_or_token>'
```

For precise editing, request structure/block IDs when the CLI supports it:

```bash
python3 skills/dbx-feishu-doc/scripts/lark_doc_call.py fetch --doc '<doc_url_or_token>' --with-ids
```

If the wrapper shortcut does not match the current CLI syntax, use raw pass-through:

```bash
python3 skills/dbx-feishu-doc/scripts/lark_doc_call.py raw -- docs +fetch --api-version v2 --doc '<doc>' -o json
```

## Read scope

Choose scope deliberately:

| Need | Read scope |
| --- | --- |
| Summarize whole doc | Full document, with caveat on length/truncation |
| Update section | Headings + block IDs + target section content |
| Append under heading | Heading block + sibling/end position |
| Extract links/assets | Document structure + Drive/media references |
| Verify write | Target block or short read-back region |

## Output shape

```markdown
## 读取范围
- 文档：title / token / url
- 类型：docx / wiki / drive / unknown
- 范围：whole / heading / block / assets
- 完整性：complete / partial / unknown

## 关键内容
- ...

## 结构线索
- headings：...
- block ids：...
- embedded resources：...

## 限制
- 未读取：...
- 权限/分页/长度限制：...
```

## Long documents

For long documents:

- Do not claim full coverage if the tool truncated output.
- Fetch by sections or headings.
- Keep a map of headings and block IDs before summarizing.
- Tie conclusions to read sections.
