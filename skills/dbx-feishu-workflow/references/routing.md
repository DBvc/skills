# Routing between Feishu skills

## Single-domain routing

- Only project item read/write: use `dbx-feishu-project`.
- Only document read/write: use `dbx-feishu-doc`.
- Only generic planning/writing/review: use the relevant non-Feishu DBX skill.

## Cross-domain routing

Use `dbx-feishu-workflow` when both sides are involved:

```text
project item -> document
project query -> release document
document -> project comment
project acceptance criteria + document plan -> gap audit
repo/test evidence -> project comment + document update
```

## Delegate contracts

When invoking project behavior, inherit:

- metadata-first rule;
- dry-run/confirmation for writes;
- no-secret redaction;
- completion proof.

When invoking document behavior, inherit:

- block-aware updates;
- embedded resource routing;
- no whole-document overwrite for section edits;
- completion proof.

## Conflict policy

If project and document disagree:

1. Show both facts with source labels.
2. Identify impact.
3. Ask for resolution or propose a safe default.
4. Do not silently overwrite either source.

Common conflicts:

- Ticket acceptance criteria differ from document scope.
- Version/iteration differs between project and release note.
- Project says status is “待开发”, document says “已完成”.
- User asks to mark done but validation evidence is missing.
