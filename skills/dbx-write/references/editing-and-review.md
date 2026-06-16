# Editing and Review

Editing is meaning-preserving unless the user explicitly asks for rewriting the idea.

## Edit levels

### Light edit

Use when the text is mostly sound.

- fix wording;
- remove obvious filler;
- improve rhythm;
- preserve structure.

### Medium edit

Default for "润色 / 改一下 / 去 AI 味".

- clarify thesis;
- reorder local paragraphs if needed;
- cut repetition;
- rewrite weak openings/endings;
- preserve core meaning and voice.

### Structural rewrite

Use only when asked or when the current text cannot satisfy the goal without structure change.

- propose or apply new structure;
- preserve important material;
- mark major changes when useful.

### Review

Use when the user asks whether the text is good, deep, clear, convincing, publishable, or resonant.

- diagnose before rewriting;
- top issues first;
- give concrete repair moves.

## Meaning preservation

Do not change:

- factual claims;
- stance;
- uncertainty;
- identity and personal history;
- technical terms;
- examples;
- target audience;
- emotional temperature;

unless the user asks or the original is unsafe/unsupported.

## Edit workflow

1. Identify surface and audience.
2. Locate thesis.
3. Locate repeated or dead paragraphs.
4. Cut AI smell.
5. Repair section progression.
6. Repair sentence rhythm.
7. Check facts and personal truth.
8. Return the smallest useful artifact.

## When to comment instead of rewriting

Comment first when:

- the argument is self-contradictory;
- facts are suspicious and material;
- the author intent is unclear;
- the article has multiple possible theses;
- rewriting would erase a meaningful rough edge.

## Review rubric

```yaml
article_review:
  thesis:
    question: "Is this a real judgment or just a topic?"
  reader:
    question: "Who changes after reading this?"
  progression:
    question: "Does each section make a new move?"
  evidence:
    question: "Which claims need source, example, or uncertainty?"
  specificity:
    question: "Where is the scene, mechanism, cost, or boundary?"
  voice:
    question: "Does it sound like the author or generic AI?"
  ending:
    question: "Does it discover something or only summarize?"
```

## Output patterns

### Direct edit

Return revised text only unless asked for explanation.

### Edit with note

```markdown
## 改后版本

...

## 修改说明

- 保留：...
- 调整：...
- 建议补充：...
```

### Review

```markdown
## 核心判断

...

## 最大问题

1. ...
2. ...
3. ...

## 最小修法

...

## 可直接替换的片段

...
```

## Do not over-edit

A strong sentence may be uneven. Do not flatten it merely to satisfy a style rule.

Examples of roughness worth preserving:

- a sharp personal judgment;
- a short blunt sentence;
- an unusual metaphor that works;
- a hesitation that reveals honesty;
- a domain-specific phrase with precise meaning.
