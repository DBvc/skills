# Learning Kernel

This reference expands the runtime learning model for `dbx-learn`. Load it when the user asks for a substantial learning session, practice design, review, or long-term plan.

## 1. Learning target hierarchy

A learning answer should optimize for usable capability, not coverage.

Capability levels:

1. **Name**: recognize the term.
2. **Explain**: describe the concept in plain language.
3. **Distinguish**: separate it from adjacent concepts and non-examples.
4. **Apply**: use it in a concrete task.
5. **Diagnose**: find failure modes and incorrect applications.
6. **Transfer**: apply it to a novel context.
7. **Teach**: explain it with examples, boundaries, and corrections.

For a short session, aim to move the user one level, not all seven.

## 2. Active recall

Fluent reading creates false confidence. Include a small retrieval move unless the user explicitly refuses.

Good recall prompts:

- “用自己的话解释 X，不要使用术语 Y。”
- “给出一个不是 X 的例子，并解释为什么不是。”
- “这个方案什么时候会失败？”
- “把这个概念应用到你正在做的项目里，会改变什么判断？”
- “我给你一个场景，你判断该不该用它。”

Bad recall prompts:

- “你明白了吗？”
- “总结一下上面内容。”
- “选择 A/B/C”，但答案只靠关键词匹配。

## 3. Practice reps

A practice rep is a small task that creates evidence of understanding.

A good rep has:

- one target capability;
- a concrete artifact or answer;
- a success signal;
- a stop condition;
- a feedback loop;
- a next rep trigger.

Examples:

```text
Concept: React Server Components
Rep: take a small client-heavy page and classify which state/data/UI parts can move server-side.
Artifact: a table with component, boundary, reason, risk.
Success signal: no client-only interaction is moved incorrectly.
Stop condition: 45 minutes or one page.
Feedback: compare against official constraints and runtime errors.
```

```text
Concept: Type variance
Rep: explain why assigning Array<Dog> to Array<Animal> is unsafe in mutable contexts, then write one TypeScript example.
Artifact: code snippet plus explanation.
Success signal: explanation identifies write position and mutation risk.
```

## 4. Spacing and interleaving

For durable knowledge, suggest lightweight revisit points:

```text
same day: one recall question
2 to 3 days: one counterexample
1 week: one application rep
2 to 4 weeks: one transfer problem
```

Do not force a calendar system unless the user asks. A simple `REVISIT.md` candidate is enough.

Interleave related topics when they are easily confused:

- cache vs memoization;
- type narrowing vs type assertion;
- concurrency vs parallelism;
- consistency vs availability;
- architecture principle vs implementation pattern.

## 5. Misconception handling

When a user answer is wrong or incomplete:

1. Quote or summarize the exact fragile part.
2. Name the misconception.
3. Give the minimal correction.
4. Ask one follow-up that tests the corrected boundary.

Avoid global judgment such as “you do not understand this”. Use local evidence:

```text
这里的问题不在结论，而在边界：你把 X 当成 Y 的充分条件了。
```

## 6. Cognitive load

Keep the first pass small:

- one core model;
- two or three distinctions;
- one example;
- one recall question;
- one next action.

Only expand after the user asks for depth or completes a rep.

## 7. Compression

End concept sessions with a compression sentence:

```text
X is useful when ..., but fails when ...; the main trap is ...
```

For technical concepts, prefer operational compression:

```text
Use X when you need to control ..., verify it by ..., avoid it when ...
```

## 8. Learning records

A learning record is not a session log. Record only facts that should change future teaching.

Worth recording:

- demonstrated understanding;
- corrected misconception;
- preferred example domain;
- completed rep and feedback;
- durable goal or constraint.

Not worth recording:

- the assistant explained something;
- a link was opened;
- the user seemed interested;
- a plan was generated but not attempted.
