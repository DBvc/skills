# Fact and Evidence Policy

Writing can be stylish only after it is honest. This reference defines how `dbx-write` handles facts.

## Source categories

### User-provided claims

Treat as material, not automatically verified truth.

Use wording:

- "按你提供的信息";
- "如果这个判断来自你的实际经历";
- "这里我保留为作者经验，而不是外部事实。"

### Stable background knowledge

May be used without live lookup when it is broad and not time-sensitive:

- general programming concepts;
- high-level software engineering ideas;
- common writing principles;
- stable historical background;
- basic language usage.

Still mark uncertainty if the claim becomes specific.

### Current or unstable facts

Require current external sources when tools are available:

- product capabilities;
- software/library/model versions;
- prices;
- laws, policies, platform rules;
- release dates;
- benchmark numbers;
- market share;
- current company/person roles;
- public events;
- recent scientific claims;
- recommendations that depend on current availability or popularity.

### Numbers, dates, and names

Verify or remove unless supplied by the user and explicitly framed as user-provided.

Bad:

```text
2025 年大多数团队已经全面采用 AI 编程。
```

Better:

```text
更稳妥的写法是：越来越多团队在尝试把 AI 编程纳入研发流程，但具体采用率需要查证。
```

## Evidence hierarchy

Prefer:

1. Primary source: official docs, release notes, source repo, paper, law/regulation, original dataset.
2. Authoritative secondary source: reputable media, standards body, research institution.
3. Domain expert writing with clear evidence.
4. General blogs, social posts, anecdotes.

Use weak sources only for weak claims.

## Citation behavior

When using external sources in a user-facing answer:

- cite the source next to the factual claim;
- do not bunch all citations at the end;
- distinguish quoted source claims from your inference;
- keep quotes short;
- do not cite irrelevant sources to make the article look grounded.

When writing a standalone Markdown file:

- include citations inline if the host supports it;
- otherwise include a "Sources" section with URLs only if allowed by the user/repo context;
- if citations are unavailable in the final artifact format, include a "Needs verification" section.

## What not to invent

Never invent:

- personal experience;
- private conversations;
- user research;
- survey data;
- benchmark results;
- production incidents;
- company adoption;
- expert quotes;
- legal or medical conclusions;
- investment returns;
- dates or version numbers.

## Assumption language

Use assumption labels when writing from incomplete material:

```markdown
> 写作假设：这篇文章面向有经验的工程师，使用用户提供的观点作为作者立场。文中的行业事实未额外查证，适合后续补源。
```

Or:

```text
如果把这个案例看成一个假设场景，它可以说明...
```

## High-stakes domains

For legal, medical, financial, mental health, security, employment, or regulated topics:

- write structure, questions, and source requirements;
- do not produce confident substantive advice;
- recommend qualified review when the article makes claims readers may act on.

## Fact-sensitive editing

When editing a user's text:

- do not silently "correct" factual claims unless you can verify them;
- mark suspicious claims;
- preserve uncertainty where the original author was careful;
- do not add confident context to make prose smoother.
