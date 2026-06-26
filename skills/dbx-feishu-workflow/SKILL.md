---
name: dbx-feishu-workflow
description: Use when the user asks to coordinate a development workflow across Feishu Project/Meegle work items and Feishu documents, such as reading a ticket, updating a technical plan, syncing implementation progress, writing release notes, or commenting back with validation evidence. This is an orchestration skill; delegate project operations to dbx-feishu-project and document operations to dbx-feishu-doc. Do not use for single-domain Feishu operations or generic planning without external Feishu read/write.
---
# DBX Feishu Workflow / 飞书研发流程编排

Coordinate Feishu Project and Feishu documents without mixing their source-of-truth boundaries.

Core job:

```text
project item + document target + development evidence -> synchronized workflow plan -> safe external reads/writes -> completion report
```

## Activation boundary

Use this skill when the request spans both domains:

- Read a Feishu Project ticket/story/bug and update a linked Feishu technical document.
- Read a Feishu document and sync conclusions, validation, blockers, or next steps back to a project item comment.
- Create a technical plan from a project item, then link or comment it back to the item.
- Produce release notes from version/ticket data and write them to a Feishu document.
- Compare project acceptance criteria with document implementation plan and report gaps.
- Update both project status and documentation after user-approved implementation evidence.

Do not use this skill for:

- Only reading or writing a Feishu Project item. Use `dbx-feishu-project`.
- Only reading or writing a Feishu document. Use `dbx-feishu-doc`.
- Generic workflow advice with no Feishu external operation.
- Code implementation itself. This skill may consume implementation evidence, but it does not replace coding/review skills.

## Orchestration contract

Build this internal contract. Print it before any cross-system write.

```yaml
feishu_workflow_contract:
  mode: ticket_to_doc | doc_to_ticket | release_sync | acceptance_audit | progress_sync | diagnose
  project_sources: []
  document_sources: []
  source_of_truth:
    requirement: "project | document | user | unknown"
    technical_plan: "document | repo | user | unknown"
    validation: "tool_output | user_claim | unknown"
  intended_project_writes: []
  intended_doc_writes: []
  required_delegates: []
  write_requires_confirmation: true
  unresolved_conflicts: []
```

## Hard gates

1. **Source-of-truth gate**: project facts, document facts, repo facts, and user claims must be labeled separately.
2. **No silent double-write**: never update both a project item and a document without a combined preview.
3. **Delegation gate**: project operations follow `dbx-feishu-project`; document operations follow `dbx-feishu-doc`.
4. **Conflict gate**: when the ticket and document disagree, stop and present the conflict unless the user gave a resolution rule.
5. **Evidence gate**: do not write “verified”, “done”, or “accepted” unless evidence supports it.
6. **Approval gate**: any external write needs exact target and user approval unless the current request explicitly asked for that exact write.
7. **State gate**: do not store secrets or copied external content in persistent repo memory. If a durable mapping is needed, store only stable IDs/links with user approval.

## Runtime workflow

### 1. Plan routing

Classify the request:

| Mode | Project read | Doc read | Project write | Doc write |
| --- | --- | --- | --- | --- |
| `ticket_to_doc` | required | optional | optional link/comment | required |
| `doc_to_ticket` | optional | required | required comment/update | optional |
| `release_sync` | required query | optional | optional | required |
| `acceptance_audit` | required | required | optional comment | optional fix doc |
| `progress_sync` | optional | optional | required comment/status | optional |
| `diagnose` | as needed | as needed | none by default | none by default |

### 2. Gather evidence by domain

Keep separate buckets:

```yaml
workflow_evidence:
  project_observed_facts: []
  document_observed_facts: []
  repo_or_test_observed_facts: []
  user_claims: []
  assumptions: []
  conflicts: []
  unknowns: []
```

### 3. Build a combined preview

For any write across one or both systems:

```markdown
## 飞书研发流程写入预览
### 项目侧
- 目标：...
- 操作：comment / update field / transition / link
- 内容摘要：...

### 文档侧
- 目标：...
- 位置：...
- 操作：create / append / section update
- 内容摘要：...

### 依据
- 项目事实：...
- 文档事实：...
- 验证事实：...
- 用户声明：...

### 风险
- 冲突：...
- 权限：...
- 会通知的人：unknown / none / list
```

Ask for confirmation if not already authorized.

### 4. Execute in safe order

Default order:

1. Read project and document.
2. Resolve conflicts.
3. Write document draft/update first when creating a durable plan.
4. Write project comment/link after the document target exists.
5. Transition project status only after validation and explicit approval.
6. Verify writes by tool response or read-back.

### 5. Report completion

```markdown
## 同步结果
- 状态：completed | partially_completed | failed | blocked
- 项目侧：read/write result, IDs, link, evidence
- 文档侧：read/write result, title, link/location, evidence
- 冲突处理：...
- 未完成：...
- 下一步：...
```

## References

Read only when needed:

- `references/dev-workflow-playbooks.md`: common ticket/doc/release workflows.
- `references/routing.md`: when to delegate to project/doc skills.
- `references/state-contract.md`: durable IDs, links, and secret boundaries.
