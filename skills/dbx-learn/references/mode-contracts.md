# Mode Contracts

Use this reference when the runtime `SKILL.md` mode contracts are too compact for the user's task.

## 1. `concept`

Inputs that help:

- concept name;
- user's current level;
- intended use case;
- adjacent concepts that confuse the user;
- preferred example domain.

Default output:

```text
结论
核心模型
为什么重要
边界和反例
相邻概念区分
常见误解
工程或真实例子
压缩句
主动回忆问题
下一步练习
证据和不确定性
```

Stop when:

- the concept is defined, bounded, exemplified, and one recall move exists;
- deeper history or formalism would add load without changing immediate capability.

## 2. `research`

Use when the user asks for a field, direction, paper cluster, technical trend, or current state.

Inputs that help:

- research question;
- output purpose: learn, decide, write, build, teach;
- freshness requirement;
- source list or allowed search scope;
- depth target.

Workflow:

1. Turn the request into 2 to 5 research questions.
2. Establish source hierarchy and freshness need.
3. Prefer primary sources for claims that matter.
4. Digest sources into findings, not a link pile.
5. Record conflicts and weak evidence.
6. Build a mental model and next learning actions.

Default output:

```text
研究问题
来源策略
核心发现
概念地图
时间线或演化脉络
争议和冲突
可用判断模型
实践或学习 reps
未核验内容
```

Stop when:

- the question map is answered enough for the requested depth;
- unresolved conflicts are explicit;
- next learning action is clear.

## 3. `source_digest`

Use when the user provides documents, links, transcripts, papers, notes, code, or mixed materials and wants to learn from them.

Workflow:

1. Identify source boundaries.
2. Extract claims, examples, definitions, procedures, and open questions.
3. Remove duplicated or low-value material.
4. Convert the source into concept cards, practice reps, or a research memo.
5. Preserve source attribution where available.

Output can include:

```text
材料地图
核心概念
值得保留的例子
容易误读的点
练习或复习题
下一步阅读顺序
```

## 4. `practice`

Use when the user wants to improve by doing.

A rep must include:

```text
target_capability
artifact
constraints
steps
success_signal
feedback_method
stop_condition
reflection_questions
next_rep_trigger
```

Prefer shippable reps over abstract homework:

- demo;
- small code spike;
- architecture comparison table;
- concept card;
- bug diagnosis diary;
- annotated source reading;
- one-page teaching note.

## 5. `review`

Use when the user wants testing, retention, or correction.

Interaction policy:

- Ask 1 to 3 questions first.
- Do not provide answers before the user answers unless requested.
- After the answer, give precise feedback and one correction rep.
- If the user performs well, increase transfer difficulty.
- If the user struggles, reduce scope and test one boundary.

Question types:

```text
recall          explain from memory
boundary        classify example/non-example
application     apply to a concrete scenario
diagnosis       find the flawed reasoning
transfer        use the idea in a new domain
teach_back      explain to another person
```

## 6. `quest_plan`

Use for 1 to 4 week learning plans.

Plan structure:

```text
north_star_goal
current_assumptions
scope_and_non_scope
phase_slices
weekly_reps
resources_by_need
review_cadence
success_signals
adjustment_rules
first_action_today
```

A good plan limits resources. It should not become a museum of links with no reps.

## 7. `state_update`

Use only when persistent learning state is requested or clearly useful and approved.

State update candidate:

```yaml
learning_state_patch:
  target_path: "learning/learning-records/0001-example.md"
  reason: "The user demonstrated understanding by applying the concept to a new case."
  write_status: "candidate_only | user_approved_written | not_written"
  summary:
    learned: []
    corrected_misconceptions: []
    reps_completed: []
    next_review: []
  rollback_or_delete: "Remove this record if later evidence shows the understanding was not demonstrated."
```

Do not claim durable memory changed unless a real write happened or the host has approved memory behavior.
