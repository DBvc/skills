# Technical Blog Playbook

Technical writing should make a reader's future judgment better. It is not a vocabulary parade.

## Required variables

Before drafting, infer or ask for:

```yaml
technical_article:
  target_reader: ""
  technical_object: ""
  problem_or_tension: ""
  current_source_of_truth: ""
  mechanism: ""
  tradeoff: ""
  failure_mode: ""
  example_or_case: ""
  boundary: ""
  reader_takeaway: ""
```

## Core questions

- What problem does the reader actually face?
- What false model causes bad decisions?
- What mechanism explains the behavior?
- Which boundary matters most?
- What breaks if the reader overgeneralizes?
- What should the reader do differently after reading?

## Mechanism over slogan

Weak:

```text
我们要提升研发效率。
```

Better:

```text
真正要缩短的是“写完代码到知道它错了”的时间。
```

Weak:

```text
架构要保持可扩展性。
```

Better:

```text
可扩展性不是多抽几层，而是下一次需求变化时，变动能不能被限制在预期边界内。
```

## Evidence in technical articles

Use:

- code snippets, diff, API behavior, docs, logs, screenshots, benchmark results, postmortems, design docs, or user-provided project facts;
- source hierarchy from `fact-and-evidence-policy.md`.

Do not invent production incidents or benchmark numbers.

## Architecture writing

When writing about architecture, name at least two:

- owner;
- boundary;
- source of truth;
- dependency direction;
- lifecycle;
- coupling point;
- validation path;
- migration cost;
- rollback path.

If none can be named, the paragraph is probably architecture perfume.

## AI adoption writing

When writing about AI in engineering, name:

- task type;
- context boundary;
- source material;
- verification loop;
- failure mode;
- human judgment boundary;
- adoption friction;
- quality signal.

Avoid:

```text
AI 将全面重塑研发范式。
```

Prefer:

```text
AI 最先改变的不是架构能力，而是把低价值样板代码的边际成本压低，让工程师更难用“我很忙”来掩盖判断缺席。
```

## Frontend writing

For frontend topics, useful lenses include:

- state ownership;
- rendering model;
- interaction latency;
- design system boundary;
- component API shape;
- data fetching lifecycle;
- observability;
- accessibility;
- dependency and build topology;
- local feedback speed;
- cross-team contracts.

## Output shape

A strong technical article often follows:

```markdown
# Title

Concrete technical tension.

## 表面问题

What people complain about.

## 真正机制

What creates the problem.

## 为什么这个机制以前不明显

Context or historical reason.

## 决策边界

How to decide.

## 代价和例外

Tradeoff.

## 可落地做法

Actionable heuristic or small plan.

## 结尾

One sentence that changes the reader's future judgment.
```

## Anti-patterns

- "最佳实践" without context;
- "银弹" framing;
- listing tools instead of decisions;
- migration plan without rollback;
- architecture philosophy without concrete boundary;
- performance advice without measurement;
- AI claims without evaluation loop;
- "工程效率" without feedback-path analysis.
