---
name: dbx-feishu-project
description: Use when the user needs to read, query, create, update, comment on, attach files to, or transition Feishu Project / Lark Project / Meegle work items such as story, ticket, bug, requirement, version, iteration, task, defect, or release work. Default to read-only until a concrete write target, exact change, and user approval are clear. Do not use for Feishu documents, generic project-management advice, or code implementation without an external Feishu Project operation.
---
# DBX Feishu Project / 飞书项目操作

Operate Feishu Project / Lark Project / Meegle as an external-system control loop, not as free-form guessing.

Core job:

```text
user request + Feishu Project identifiers + metadata discovery -> bounded read/write plan -> CLI/API execution -> redacted evidence report
```

## Activation boundary

Use this skill for:

- Reading or summarizing a Feishu Project / Lark Project / Meegle URL, story, ticket, task, bug, requirement, version, iteration, defect, or work item.
- Querying work items by project, type, owner, version, iteration, status, priority, due date, tag, relation, or MQL.
- Creating or updating work items, fields, roles, comments, workflow nodes, status, relations, attachments, deliverables, WBS plan rows, or work hours.
- Syncing development progress back to a Feishu Project item.
- Diagnosing why a project operation failed due to permission, missing metadata, field type, invalid role, invalid transition, pagination, or stale CLI/API assumptions.

Do not use this skill for:

- Feishu document editing. Use `dbx-feishu-doc`.
- Requests that only ask how project management works with no Feishu operation.
- Code review, implementation, architecture judgment, commit/PR writing, or product judgment unless the user explicitly asks to use Feishu Project as an evidence source or write target.
- Circumventing permissions, scraping private spaces without consent, hiding or falsifying project state, or silently mutating external records.

## Execution contract

For every operation, build this internal contract. Print it before any write, destructive action, or ambiguous batch action.

```yaml
feishu_project_contract:
  mode: read | query | create | update | comment | transition | attach | workflow_sync | diagnose
  requested_object: ""
  source_identifiers: []
  project_key: "known | discovered | unknown"
  work_item_type: "known | discovered | unknown | not_applicable"
  target_work_item_ids: []
  metadata_needed: []
  intended_changes: []
  read_only: true
  write_requires_confirmation: true
  auth_state: "unknown | cli_ready | missing_cli | missing_auth | permission_blocked"
  evidence_expected: []
  unresolved_risks: []
```

## Hard gates

1. **Authority gate**: never write until the user has provided or approved the target project/work item and exact intended change.
2. **Metadata gate**: never guess `project_key`, work item type key, field key, role key, user key, workflow transition, or enum value when the CLI can discover it.
3. **Dry-run gate**: for create, update, transition, relation, attachment, WBS publish, and batch operations, use dry-run when the CLI supports it; otherwise show the patch summary and ask for explicit confirmation.
4. **No-secret gate**: never print access tokens, app secrets, auth headers, cookies, device codes, credential cache paths, or private machine paths.
5. **Read-only default**: URL decoding, project search, metadata reads, and work item reads are safe defaults. External writes are opt-in.
6. **Partial-result gate**: if pagination, permission, rate limit, or query scope is uncertain, mark the result incomplete instead of pretending the project state is exhaustive.
7. **Human workflow gate**: do not silently move ownership, change priority, close work, or publish plans in ways that affect teammates unless the user specifically requested that operation.

## Preferred tool path

Prefer official CLI execution in this order:

1. `meegle` or `meegle-cli` for Feishu Project / Meegle.
2. `scripts/meegle_call.py` when you need safer subprocess execution, redaction, JSON envelopes, or stable pass-through.
3. A project-specific MCP server only when it is already configured in the host and exposes the needed Meegle operations.
4. A thin SDK/API wrapper only for a CLI gap, with the same gates and redaction policy.

If no executable/project tool is available, stop with a setup failure. Do not simulate successful external writes.

## Runtime workflow

### 1. Resolve identity and scope

- If the user provides a Feishu Project URL, decode it first. Do not hand-slice URL paths.
- If the user provides a project name, search and resolve the authoritative `project_key`.
- If the user says story/ticket/version/bug/需求/缺陷/迭代, discover the configured work item type or field in that project.
- If the user names a person, resolve to the system user key before a write.

Read `references/project-concepts.md` and `references/read-playbook.md` when the object model is unclear.

### 2. Discover metadata before interpreting business words

Use metadata reads before writing or forming a strong query:

- Work item types.
- Field definitions, field keys, required fields, value types, enum options, relation fields.
- Roles and role operations.
- Workflow nodes, transitions, required transition fields.
- User keys and team membership.

Treat story, ticket, version, iteration, release, bug, and defect as local project vocabulary until confirmed.

### 3. Execute reads and queries with evidence boundaries

For reads, return:

```markdown
## 飞书项目读取结果
- 范围：project / work item / query / view / relation
- 已解析对象：project_key, work_item_type, work_item_id, title, status, owner, link
- 关键字段：...
- 评论 / 附件 / 关系：...
- 未读取或不完整：pagination, permission, rate limit, unsupported object
```

For queries, state the query/filter, page limit, sort order, and whether the result is complete.

### 4. Plan writes before executing

For writes, produce a patch preview:

```markdown
## 待写入飞书项目
- 目标：project_key / work_item_id / title
- 操作：create / update / comment / transition / attach / relation / WBS publish
- 字段变更：old -> new when old value is known
- 依据：用户请求 / 文档 / 代码 / 讨论记录
- 风险：required fields, permission, workflow side effect, notifying teammates
- 执行方式：dry-run available / confirmation required / unsupported
```

Then ask for confirmation unless the user already gave explicit permission for this exact write in the current request.

### 5. Complete with proof, not vibes

After execution, return:

```markdown
## 已完成
- 操作：...
- 对象：project_key / work_item_id / title / link
- 实际变更：...
- 工具证据：command kind, return code, redacted response id or updated field list
- 未完成：...
- 需要人工确认：...
```

Never claim a field, comment, status, or workflow node changed unless the tool response or follow-up read confirms it.

## Command helpers

Use these helper scripts when useful:

- `scripts/meegle_call.py`: safe pass-through wrapper around `meegle` or `meegle-cli`; returns redacted JSON envelopes.
- `scripts/redact_output.py`: standalone redaction filter for CLI stdout/stderr.

Read these references only when needed:

- `references/auth.md`: credential and secret policy.
- `references/project-concepts.md`: Feishu Project object model and local vocabulary traps.
- `references/read-playbook.md`: URL decode, metadata, query, pagination, result contract.
- `references/write-playbook.md`: write gates, dry-run, confirmation, patch preview, rollback notes.
- `references/mql.md`: MQL and query safety.
- `references/completion-evidence.md`: completion proof format.
