# Embedded resource routing

Feishu documents can contain resources that are not plain text. Identify them before editing.

## Routing table

| Embedded item | Action |
| --- | --- |
| Sheet | Route to sheet-specific commands/tools. Do not edit as Markdown table unless user asks for text export only. |
| Base | Route to Base commands/tools. Treat records and fields as database rows, not paragraphs. |
| Wiki child page | Resolve child node/document before editing. |
| Image | Download/insert through media or Drive flow. Do not expose local temp paths in final answer. |
| Attachment | Use Drive/file operations. Preserve filename and permission boundary. |
| Whiteboard | Route to whiteboard-capable commands/tools. |
| Comment | Use Drive/comment APIs if the current CLI separates comments from document content. |

## Read behavior

When embedded resources are present:

- Mention that the main document was read but the embedded resource may require a separate read.
- Ask or route only if the user's answer depends on embedded content.
- Do not summarize unseen embedded resources based on title alone.

## Write behavior

When writing near embedded resources:

- Avoid replacing a parent range that contains embedded resources unless user approved it.
- Prefer inserting before/after known block IDs.
- Verify that attachments/images are accessible after upload.
