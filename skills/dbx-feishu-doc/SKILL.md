---
name: dbx-feishu-doc
description: Use when the user needs to read, summarize, create, append to, or safely update Feishu/Lark Docx, Wiki, or document-like resources in a development workflow. Prefer official lark-cli document operations and block-aware updates. Do not use for Feishu Project/Meegle work items, generic writing without a Feishu document target, or editing external documents without clear permission.
---
# DBX Feishu Doc / 飞书文档操作

Operate Feishu documents as structured external artifacts. Prefer block-aware reads and minimal writes over whole-document overwrite.

Core job:

```text
Feishu doc identifier + user intent -> document read/write plan -> CLI/MCP/API execution -> redacted evidence report
```

## Activation boundary

Use this skill for:

- Reading or summarizing Feishu Docx, Wiki pages, document URLs, or document tokens.
- Creating a Feishu document from a development artifact such as PRD, technical plan, release note, design doc, test report, or review result.
- Appending implementation progress, validation notes, decision records, release notes, or meeting summaries to a Feishu document.
- Updating a specific document section, heading, block, table of contents region, or structured document fragment.
- Extracting document structure, block IDs, headings, embedded resources, images, attachments, or linked Wiki/Drive resources.

Do not use this skill for:

- Feishu Project / Meegle work item read/write. Use `dbx-feishu-project`.
- Generic Markdown writing when no Feishu document read/write target exists.
- Comment-only operations if the document comment API belongs to Drive rather than Docx in the current toolchain.
- Editing spreadsheets, Base records, or whiteboards as if they were plain text. Route to the correct Feishu capability or stop with a boundary note.
- External writes without user permission.

## Execution contract

For every document operation, build this internal contract. Print it before writes or ambiguous updates.

```yaml
feishu_doc_contract:
  mode: read | summarize | create | append | section_update | block_update | extract_assets | diagnose
  doc_identifier: "url | token | wiki_node | unknown"
  document_type: "docx | wiki | drive_file | unknown"
  target_location: "whole_doc | heading | block_id | end_of_doc | unknown"
  input_format: "markdown | xml | plaintext | file | unknown"
  write_intent: "none | create | append | replace_section | patch_blocks"
  read_only: true
  write_requires_confirmation: true
  auth_state: "unknown | cli_ready | missing_cli | missing_auth | permission_blocked"
  embedded_resources: []
  unresolved_risks: []
```

## Hard gates

1. **Permission gate**: do not edit a document unless the user provided the URL/token or explicitly authorized the target.
2. **Structure gate**: for precise edits, fetch structure/block IDs before patching. Do not overwrite the whole document to change one section.
3. **Location gate**: if the target section or block is ambiguous, ask for the heading/block or present candidate locations.
4. **External write gate**: show update preview and ask for confirmation unless the user has explicitly requested this exact write.
5. **Secret gate**: never write secrets, tokens, private logs, auth headers, cookies, or hidden chain-of-thought into a document.
6. **Embedded-resource gate**: do not treat Sheets, Base, Wiki children, attachments, or whiteboards as plain text. Identify and route.
7. **Completion gate**: only claim a document changed when the tool response or follow-up read supports it.

## Preferred tool path

Prefer official tools in this order:

1. `lark` or `lark-cli` document commands for Docx/Wiki/Drive operations.
2. `scripts/lark_doc_call.py` for safer subprocess execution, v2 defaults, redaction, JSON envelopes, and common document shortcuts.
3. Official Lark OpenAPI MCP when it is configured and exposes the needed document/block tool.
4. A thin SDK/API wrapper only for a tool gap, still following the same gates.

If no document tool is available, report setup failure and do not pretend to have read or updated the document.

## Runtime workflow

### 1. Resolve the document

- Accept document URL, token, Wiki node, or a clearly named document only if a search tool is available.
- Prefer user identity for documents in a user's Drive/Wiki. Do not assume a bot can see user-owned docs.
- Determine whether the target is Docx, Wiki, Drive attachment, Sheet, Base, or another resource.

Read `references/document-model.md` when the resource type is unclear.

### 2. Read before editing

For any update:

- Fetch the current document or target block.
- For section/block edits, fetch with block IDs or structure when supported.
- Identify headings, target range, existing content, and embedded resources.
- Preserve content that is outside the requested target range.

### 3. Choose the smallest safe write

Write strategy:

| User intent | Preferred action |
| --- | --- |
| New document | Create doc with title and content |
| Add progress/release notes | Append to end or specified heading |
| Replace one section | Fetch section/block, preview replacement, patch only that region |
| Update checklist/table-like content | Confirm whether it is Docx blocks, Sheet, or Base |
| Add images/attachments | Use document/Drive attachment flow, not raw local paths in final text |

### 4. Preview writes

Before writing, show:

```markdown
## 飞书文档写入预览
- 文档：title / token / url
- 位置：end / heading / block_id / new document
- 操作：create / append / replace section / patch blocks
- 内容摘要：...
- 可能影响：links, comments, embedded resources, formatting
- 未确认：...
```

### 5. Complete with proof

After execution:

```markdown
## 已完成
- 操作：read | create | append | update | extract
- 文档：title / url / token
- 位置：heading / block_id / end / new doc
- 证据：redacted command envelope / document revision / read-back snippet
- 未完成：...
- 需要人工确认：...
```

## Command helpers

- `scripts/lark_doc_call.py`: safe wrapper around `lark` or `lark-cli`; defaults document operations to `--api-version v2` where applicable.
- `scripts/redact_output.py`: standalone output redaction.

Read references only when needed:

- `references/auth.md`: auth and secret boundaries.
- `references/document-model.md`: Docx/Wiki/Drive/block model and near-miss resources.
- `references/read-playbook.md`: document fetch and structure extraction.
- `references/write-playbook.md`: safe create/append/update strategy.
- `references/embedded-resources.md`: Sheets/Base/Wiki/attachment/whiteboard routing.
- `references/completion-evidence.md`: proof and final report contract.
