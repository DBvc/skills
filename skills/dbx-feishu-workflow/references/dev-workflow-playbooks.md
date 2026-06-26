# Feishu development workflow playbooks

## Ticket to technical document

Use when the user says: “根据这个 ticket 写/更新技术方案”.

Steps:

1. Read the project item with `dbx-feishu-project`.
2. Extract requirement, acceptance criteria, constraints, version/iteration, owner, due date, links, and open questions.
3. Read existing linked document if provided.
4. Build or update the technical plan with sections:
   - Background and goal.
   - Scope and non-goals.
   - Current facts from ticket.
   - Proposed implementation.
   - Acceptance matrix.
   - Risks and open questions.
   - Validation plan.
5. Preview document write.
6. After document write, optionally comment back to the project item with the doc link and summary.

## Document to ticket comment

Use when the user says: “把文档结论同步回 ticket”.

Steps:

1. Read document target and relevant section.
2. Read project item if status/context matters.
3. Separate document conclusions from project facts.
4. Draft a concise comment:
   - 已确认：...
   - 方案变化：...
   - 验证：...
   - 风险 / 待确认：...
   - 文档链接：...
5. Preview comment before writing.

## Release sync

Use when the user says: “根据版本里的 ticket 生成发布说明/上线记录”.

Steps:

1. Resolve version/iteration field or work item type with `dbx-feishu-project`.
2. Query included work items.
3. Group by feature/fix/risk/breaking change when metadata supports it.
4. Mark partial result if pagination is incomplete.
5. Write release note to document only after preview.
6. Do not mark all tickets done unless explicitly requested and verified.

## Acceptance audit

Use when the user says: “对齐 ticket 验收标准和技术方案”.

Steps:

1. Read project acceptance criteria.
2. Read document implementation plan and validation plan.
3. Build an acceptance matrix:
   - Requirement.
   - Project source.
   - Document coverage.
   - Validation evidence.
   - Gap.
   - Proposed fix.
4. Ask whether to update the doc, comment on project, or both.

## Progress sync

Use when implementation evidence exists and the user wants Feishu updated.

Evidence levels:

| Claim | Acceptable wording |
| --- | --- |
| Tool output shows pass | “验证通过：command ...” |
| User says tested | “用户声明已验证：...” |
| No validation | “验证：未运行/未提供” |
| Partial validation | “部分验证：...” |

Never inflate evidence level during sync.
