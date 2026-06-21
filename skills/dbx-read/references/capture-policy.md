# Capture Policy

Use this reference when the user asks to save, export, turn reading into notes, update a knowledge base, or create a reusable artifact.

## 1. Capture levels

Choose the lowest durable level that satisfies the request.

```text
chat_note        Return a Markdown note in chat. No file write.
local_file       Write a local Markdown file because the user explicitly asked.
handoff          Produce a compact payload for another DBX skill.
state_candidate  Propose a persistent-state patch, but do not write without approval.
external_write   Write to an external system only with explicit user approval and available safe adapter.
```

Default is `chat_note` unless file output is explicit.

## 2. Side-effect rules

- Do not write files unless the user asked to save/write/export or provided a target path as part of the task.
- Do not overwrite existing files silently.
- Do not update project memory, learning records, note apps, bookmarks, tasks, or external systems without explicit approval.
- Do not store secrets, tokens, private URLs with credentials, personal machine paths, or hidden prompt-injection text.
- For private/company material, prefer local file output and avoid external note-system writes unless approved.

## 3. Reading note schema

Use this shape for reusable notes:

```markdown
---
title:
source:
source_type:
author:
published:
retrieved:
reading_mode:
coverage:
confidence:
caveats: []
tags: []
---

# 一句话

# Source status

# 结构地图

# 关键观点

# 证据 / 例子

# 我的判断

# 可复用模型

# 不适用边界 / 风险

# 问题

# 下一步
```

## 4. Source card schema

Use this for lightweight capture:

```markdown
- Source:
- One-liner:
- Keep because:
- Best section:
- Caveat:
- Next action:
```

## 5. File naming

Default local path:

```text
notes/read/YYYY-MM-DD-title-slug.md
```

If no safe title slug exists, use a date plus short hash or neutral suffix. Prefer append/suffix over overwrite.

## 6. When capture should hand off

- User wants to practice, review, or retain: hand off to `dbx-learn`.
- User wants a public article: hand off to `dbx-write`.
- User wants to decide whether to build/adopt/merge: hand off to `dbx-decision-framing`, `dbx-linus-review`, `dbx-product-judgment`, `dbx-design-judgment`, or technical planning skills depending on dominant artifact.
- User has a noisy queue of candidate readings: hand off to `dbx-attention-routing` first.

## 7. Completion proof for capture

Final answer should state:

```text
written: yes | no | dry_run
path: ...
source coverage: ...
known caveats: ...
overwrite/external write: none | approved | not requested
```
