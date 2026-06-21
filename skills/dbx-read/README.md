# dbx-read

Source-grounded reading skill for explicit URLs, PDFs, papers, docs, GitHub pages/files, local files, pasted text, and small source sets.

## Design decision

This is one skill with three internal stages:

```text
fetch -> think -> capture
```

It is not split into three production skills because the repeated user job is source-bound reading, and most prompts naturally combine grounding, analysis, and optional note capture. Mechanical ingestion or note-writing can still live in `scripts/`; long rubrics live in `references/`.

## Common invocations

```text
看下这个链接，告诉我值不值得读。
精读这篇技术文章，重点看机制、trade-off、对前端架构的启发。
把这篇论文读一下，判断实验和结论是否可靠。
把这个网页转成干净 Markdown，不要总结。
比较这两篇文章对同一个问题的判断差异。
把这次阅读沉淀成一篇 notes/read 下的 Markdown 笔记。
```

## Adjacent skills

- `dbx-attention-routing`: many mixed saved items before deciding what to read.
- `dbx-learn`: durable understanding, practice reps, quizzes, review, learning records.
- `dbx-write`: public article or viewpoint-driven writing from reading notes.
- DBX judgment/planning/review skills: when the source becomes evidence for a decision or implementation.

## Suggested repository index patch

Add to README stable skills table:

```markdown
| [`dbx-read`](skills/dbx-read/) | 来源约束阅读：对 URL、PDF、论文、文档、GitHub、本地文件或粘贴文本做抓取证据化、摘要、精读、比较、Markdown 提取和可选笔记沉淀。Source-grounded reading for explicit source material. |
```

Add to `DBX_SKILL_INDEX.md`:

```markdown
| `dbx-read` | Source-grounded reading, extraction, deep read, comparison, and optional capture for explicit sources. | research + procedure + evidence + light_tool | L5 | Source extraction can be partial or host-dependent; can over-trigger `dbx-learn`, `dbx-write`, and attention routing. | Use for explicit source reading; route noisy queues to `dbx-attention-routing`, durable learning to `dbx-learn`, article writing to `dbx-write`, and concrete code/product/design decisions to matching DBX skills. | Add baseline cases after real URL/PDF/GitHub reading sessions; add host-specific ingestion scripts only when failure evidence justifies them. |
```

Add to routing matrix primary intent table:

```markdown
| Read, summarize, extract, deep-read, compare, or capture explicit source material such as URL/PDF/paper/doc/GitHub/local file/pasted text | `dbx-read` | `dbx-learn` for durable learning, `dbx-attention-routing` for noisy queues, `dbx-write` for public prose, judgment/review/planning skills for decisions or implementation. |
```
