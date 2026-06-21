# Mode Contracts

Use this reference when the user asks for a specific reading shape or when the default output would be ambiguous.

## 1. `skim`

Use for “看下”, “值不值得读”, “快速判断”, “给我一个 overview”.

Default output:

```markdown
## 一句话
...

## 关键点
1. ...
2. ...
3. ...

## 值不值得继续读
- 判断：值得 / 可跳过 / 只读某部分 / 需要更多上下文
- 理由：...

## Source status
- Source: ...
- Coverage: full | partial | selected | failed
- Caveats: ...
```

Stop when the user can decide whether to continue.

## 2. `summary`

Use for ordinary source-bound summaries.

Default output:

```markdown
## Source
- Title:
- Author / date:
- URL / file:
- Coverage:
- Caveats:

## TL;DR
...

## Main claims
1. ...
2. ...

## Evidence / examples
- ...

## What matters
- ...

## My reading judgment
- Strength:
- Weakness:
- Best use:
```

Avoid learning reps unless the user asks.

## 3. `extract_markdown`

Use when the requested artifact is clean Markdown, original structure, quotes, tables, or selected content.

Default output:

```markdown
# Title

> Source: ...
> Extraction status: ...
> Caveats: ...

[clean markdown body]
```

Rules:

- Preserve headings, lists, code blocks, links, table shape, and quote boundaries where possible.
- Mark omitted sections explicitly: `[image not extracted]`, `[table partially extracted]`, `[login-only section unavailable]`.
- Do not summarize when the user asked for source conversion, unless a separate summary is requested.

## 4. `technical_deep_read`

Use for engineering, architecture, programming languages, AI systems, frontend, infra, or software-process articles/docs.

Default output:

```markdown
## 核心判断
...

## Problem
作者真正处理的问题是什么？

## Context / assumptions
它依赖哪些组织、技术、规模、历史或约束？

## Mechanism
方案如何工作？关键状态、边界、数据流、控制流或反馈回路是什么？

## Trade-offs
它把复杂度从哪里转移到了哪里？换来了什么，牺牲了什么？

## Failure modes
在哪些情况下会失效、过度设计、误导或被滥用？

## Applicability to me
对前端架构、工程效率、AI 落地、软件工程或个人长期体系有什么可迁移点？

## Questions / verification
还需要验证什么？

## Source status
...
```

A good technical deep read should improve judgment, not just restate content.

## 5. `paper_read`

Use for papers, preprints, technical reports, benchmarks, formal specs, or empirical studies.

Default output:

```markdown
## 一句话贡献
...

## Research question
...

## Claim
...

## Method
...

## Evidence
- Data:
- Experiments:
- Metrics:
- Baselines:

## Validity threats
- Internal validity:
- External validity:
- Construct validity:
- Reproducibility:

## What changes if we believe it
...

## What not to generalize
...

## Reproduction / follow-up checks
...

## Source status
...
```

If the paper contains charts/tables and only text was inspected, mark visual evidence as unchecked.

## 6. `compare_sources`

Use for 2-5 sources. For larger sets, first triage or ask to scope.

Default output:

```markdown
## Comparison question
...

## Source table
| Source | Claim | Evidence | Caveat | My confidence |
| --- | --- | --- | --- | --- |

## Agreements
...

## Disagreements
...

## Evidence strength
...

## Provisional judgment
...

## What would change the judgment
...
```

Never merge sources before showing their individual claims.

## 7. `companion_read`

Use for “陪我读”, “逐段读”, “边读边问”, difficult English passages, philosophy, papers, dense essays, or source material the user wants to wrestle with.

Per section output:

```markdown
## Section N
### 这一段在做什么
...

### 译 / 释
...

### 概念和背景
...

### 这里最该想的问题
...

继续方式：继续 / 放慢 / 跳过 / 只问我问题
```

Do not process the whole source in one dump unless the user asks.

## 8. `capture_note`

Use when the user asks to save, turn into note, source card, Obsidian/Markdown/Org note, or reusable knowledge artifact.

Default output when not writing a file:

```markdown
## Note candidate
[Markdown note]

## Capture caveats
- Not written yet / written path
- Source coverage
- State/privacy caveats
```

Default output when writing a local Markdown file:

```markdown
已写入：`path/to/note.md`
Source coverage: ...
Caveats: ...
```

## 9. `handoff`

Use when reading is not the final job.

Default handoff:

```markdown
## Reading handoff
- Source:
- Coverage:
- Key claims:
- Useful evidence:
- Open questions:
- Recommended next DBX skill:
- Handoff payload:
```
