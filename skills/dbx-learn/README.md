# DBX Learn

`dbx-learn` is a user-friendly learning skill for durable understanding, source-grounded research, practice reps, review, and optional learning records.

It is designed for this job:

```text
help me actually learn this -> choose the right learning mode -> create a compact capability-building artifact or interaction
```

## Best use

Use it for prompts like:

- “我想真正理解 React Server Components，帮我建立 mental model 和练习。”
- “系统研究一下 AI agent memory，给我学习 memo 和下一步实践。”
- “把这篇文章变成 3 个练习 rep。”
- “测测我对 TypeScript conditional types 的理解，先别给答案。”
- “我想持续学 Rust，不想每次从零开始，帮我设计学习记录。”

Do not use it for:

- short factual answers;
- ordinary summaries;
- generic recommendations;
- direct coding, debugging, code review, product judgment, design judgment, or skill creation;
- mixed inbox routing for courses, tools, saved articles, ideas, and tasks.

## User experience stance

No configuration is required before use.

The skill defaults to a stateless session. It only proposes persistent learning state when the user asks for it. It should not ask the user to hunt for setup files, and it should not silently create durable memory.

Default output is natural Chinese when the user writes Chinese. YAML is reserved for explicit state patches, machine-readable requests, or audits.

## Modes

| Mode | Use when |
| --- | --- |
| `concept` | Learn one concept, model, mechanism, or term. |
| `research` | Study a technical direction, current state, paper cluster, or controversy. |
| `source_digest` | Learn from user-provided materials. |
| `practice` | Turn knowledge into reps, demos, experiments, or artifacts. |
| `review` | Quiz, active recall, correction, and spaced review. |
| `quest_plan` | Create a 1 to 4 week learning path. |
| `state_update` | Propose or write learning records after explicit approval. |
| `direct_answer` | Escape hatch for ordinary answers when the skill was over-selected. |
| `safety_redirect` | Redirect unsafe learning goals to safe educational alternatives. |

## Package files

```text
SKILL.md
README.md
CHANGELOG.md
references/design-brief.md
references/learning-kernel.md
references/mode-contracts.md
references/source-and-state-policy.md
assets/concept-card.template.md
assets/research-memo.template.md
assets/practice-rep.template.md
assets/learning-record.template.md
assets/learning-state.example.md
evals/triggers.json
evals/evals.json
```

## Suggested repository index row

```md
| `dbx-learn` | Durable learning, source-grounded study, practice reps, review, and optional learning records. | learning + research + interaction + state-lite | L5 | Over-triggering ordinary explanations or summaries; state drift if learning records are written too eagerly. | Use when the user wants capability change, practice, review, or a learning workspace; route skill creation to `dbx-skill-architect`, mixed content routing to `dbx-attention-routing`, and direct implementation/review to coding skills. | Add baseline comparisons after real learning sessions. |
```

## Validation

At minimum, validate JSON syntax:

```bash
python3 -m json.tool evals/triggers.json >/tmp/dbx-learn-triggers.json
python3 -m json.tool evals/evals.json >/tmp/dbx-learn-evals.json
```

If the DBX repository eval runner is available, run the collection's normal trigger and output eval checks.
