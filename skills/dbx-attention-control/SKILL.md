---
name: dbx-attention-control
description: Use when the user wants a reusable attention-allocation controller for mixed inbox items, saved content, tasks, ideas, signals, courses, tools, notes, or external-system metadata. Routes each item by stable attention states, grounded in visible evidence and a user-approved profile. Use high-risk prompts only to guard or safety-stop direct action requests. Do not use for ordinary summarization, one-off recommendations, product-specific automation by default, or silent external writes.
---

# DBX Attention Control / 注意力控制

This skill is a stable kernel for deciding what incoming material should become in the user's attention system. It is not a product adapter, tag pack, productivity method, or collector-specific workflow.

Core job:

```text
mixed input -> evidence-bounded attention route -> optional profile patch -> optional dry-run adapter mutation
```

## 0. Use / do not use

Use this skill when the user asks to:

- classify, route, prune, prioritize, or review a noisy collection of inputs;
- decide what deserves action, study, experiment, tracking, reference storage, incubation, or deletion within a provided mixed batch;
- build or refine a reusable personal attention profile;
- map route decisions into tags, task fields, note metadata, queues, or another external system through a dry-run adapter plan;
- learn from corrections so future triage matches the user better.

Do not use this skill when:

- the user only asks for a normal summary, explanation, rewrite, translation, or single factual answer;
- the task is mainly product-specific API usage, import/export plumbing, or deterministic parsing;
- the user asks you to provide direct stock picks, guaranteed predictions, medical/legal/tax decisions, surveillance, manipulation, or silent destructive changes;
- there is no stable repeated attention-allocation problem.

High-risk classification requests may still trigger this skill, but only to route items to `guard` or `safety_stop`. Never satisfy requested action labels such as buy/sell/add-position, diagnosis, legal conclusion, or destructive write.

## 1. Layer separation is mandatory

Never bake the user's examples into the kernel.

Separate every run into four layers:

```text
kernel         Stable attention model: routes, evidence, cost, risk, completion proof.
profile        User-specific horizons, non-goals, thresholds, source map, tag vocabulary.
adapter        Optional mapping from kernel routes to a specific external system.
mechanics      Scripts, schemas, import/export, validation, and write execution.
```

If a rule depends on a tool, app, collector, tag vocabulary, or personal preference, it belongs in `profile`, `adapter`, or `mechanics`, not in the kernel.

## 2. Mode selection

Choose exactly one primary mode before processing:

```text
profile_bootstrap       Create or revise the user's attention profile.
item_routing            Route one or more mixed information/action items.
adapter_dry_run         Map route decisions into proposed external-system mutations.
review_and_calibrate    Use user corrections to propose profile/rubric patches.
direct_answer           Answer normally; do not run the full kernel.
safety_stop             Refuse or bound unsafe/deceptive/silent-side-effect requests.
```

`direct_answer` and `safety_stop` are escape modes. In those modes, answer plainly and do not emit the full route table, adapter plan, completion proof, or validated JSON envelope unless the user explicitly asks for a machine-readable audit artifact.

Adjacent optional views, such as urgency/importance, review queues, or tag maps, are projections of the route result. They are not the kernel.

## 3. Evidence gate

Classify only from visible evidence or explicitly available tool output.

Allowed evidence:

- item title, text, excerpt, URL, source, author, timestamp, existing tags, folder/project, due date, note, user comment, or stable id;
- user-approved attention profile;
- explicit corrections from previous runs;
- connector/tool output that is visible in the current run.

Do not infer hidden article quality, financial truth, urgency, motive, or source credibility from vibes. When evidence is thin, use `clarify` or low-confidence `track`/`store`, not a confident route.

## 4. Attention kernel

Treat every item as a claim on attention.

For each item, identify:

```text
attention_claim     What is this item asking for? act, learn, decide, monitor, store, buy, worry, reply, etc.
horizon_fit         Does it fit now, current cycle, long-term themes, or no known horizon?
evidence_strength   Is there enough evidence for the proposed route?
transformability    Can it become an action, artifact, rule, experiment, reference, or decision?
compound_value      Will it improve future judgment, capability, systems, or leverage?
attention_cost      Time, context switching, maintenance, queue pollution, unfinished-thread cost.
risk_reversibility  Financial, privacy, health, legal, relationship, career, or destructive risk.
```

Use qualitative scoring: `high | medium | low | unknown`. Do not use fake precision unless the user asks for an explicit scoring experiment.

## 5. Stable route taxonomy

Use these canonical routes:

```text
act_now       Convert into immediate bounded action because it supports a current commitment or decision.
build         Schedule focused learning/building because it has durable compounding value.
test          Run a small reversible experiment before deeper commitment.
track         Keep as a weak signal; revisit only if repeated or triggered.
store         Keep as searchable reference; no active attention.
incubate      Keep out of the active inbox until a named trigger, date, or project state.
drop          Remove or ignore because expected value is low, duplicated, stale, or mostly stimulus.
guard         Do not act directly because the item carries significant risk or safety uncertainty.
clarify       Evidence is insufficient; ask for or fetch the smallest missing context that would change the route.
```

Route names are intentionally generic. External tags, app states, queues, and methods should map onto these routes instead of replacing them.

## 6. Decision rules

### act_now

Use only when the item is both relevant to a current commitment and actionable with a bounded next step.

Reject false urgency. A vivid item is not urgent unless there is evidence of deadline, consequence, dependency, or explicit user commitment.

### build

Use when the item is not necessarily urgent but has durable compounding value and deserves focused time.

The route should include a suggested focus block, artifact, or learning outcome. Do not mark too many items as `build`; it is expensive.

Default cap: without a user-approved profile, route at most three items per batch to `build`. If more than three items look build-worthy, keep the strongest three as `build` and route the rest to `track`, `store`, or `incubate` with an upgrade trigger. Break ties by current horizon fit, concrete artifact/outcome, evidence strength, and low regret; do not break ties by novelty or excitement.

### test

Use when promise is high but uncertainty is also high.

A valid test needs a small scope, success signal, stop condition, and review trigger.

### track

Use for repeated-signal detection without active investment.

Good for trends, weak market/news/product signals, early tools, ideas, or claims that may matter later.

### store

Use when retrieval value is real but active attention value is low.

Store by retrieval intent, not only topic.

### incubate

Use when an item may matter, but timing is wrong.

Every `incubate` route needs a trigger such as date, project milestone, repeated signal count, or dependency becoming active.

### drop

Use when keeping the item would mostly preserve guilt, FOMO, duplication, stale context, or stimulus.

Dropping is a successful output, not a failure.

### guard

Use for high-risk items. Typical cases include trading tips, health/legal/tax claims, privacy-sensitive material, irreversible operations, or content with strong incentive misalignment.

`guard` means "do not convert into direct action yet." It may still become education, research, or a bounded review.

### clarify

Use when the missing context would materially change the route. Ask for the smallest missing field, or state the best low-confidence tentative route.

## 7. Profile policy

The skill may read a user-approved attention profile. It must not invent hidden memory.

A profile can include:

```yaml
attention_profile:
  active_horizons:
    now: []
    cycle: []
    long_term: []
  non_goals: []
  route_thresholds: {}
  source_map:
    trusted: []
    weak: []
    blocked: []
  domain_weights: {}
  risk_policy: {}
  tag_vocabulary: []
  adapter_preferences: {}
  review_cadence: {}
```

When no profile exists, use broad defaults and current-user evidence only. If classification would be arbitrary, ask up to five high-leverage bootstrap questions.

When the user corrects a result, output `profile_update_candidates`; do not silently change long-lived memory.

## 8. Adapter policy

External systems are adapters, not the skill's identity.

For any external-system change:

1. route items through the kernel first;
2. map routes to external fields only through an adapter manifest or user-approved mapping;
3. produce a dry-run mutation plan;
4. require explicit approval for the exact batch before writing;
5. report what changed, what did not, and how to roll back.

Never silently tag, delete, archive, schedule, prioritize, move, rewrite, or publish anything.

## 9. Output contract

Use Chinese when the user writes Chinese unless a system field requires English identifiers.

Choose one output surface:

```text
human_default     Use concise user-visible sections or a table. This is the default.
json_validated    Use only when the user asks for machine-readable output, validation, automation, adapter batch review, or an auditable artifact.
```

For `json_validated`, produce JSON that matches `assets/attention-output.schema.json`. This schema is only for `profile_bootstrap`, `item_routing`, `adapter_dry_run`, and `review_and_calibrate`; `direct_answer` and `safety_stop` should stay as plain natural-language responses.

For normal user-visible output, prefer:

```text
结论
核心分类 / 路由结果
建议动作
可选外部系统映射
可能更新到个人规则的内容
边界和不确定性
```

For each item, include at least:

```text
id_or_locator | title | route | confidence | evidence_used | reason | next_step_or_no_action | risk_notes
```

For adapter dry-runs, include:

```text
target_system | item_id_or_locator | operation | field | old_value_if_known | new_value | reason | rollback_note | confidence
```

## 10. Completion proof

Before claiming completion, state:

- how many items were processed;
- what evidence was available;
- whether a profile was used;
- whether any external write happened;
- what remains uncertain;
- which profile or adapter changes need approval;
- whether validation was run, when applicable.

Do not imply full-corpus reading, connector access, mutation, sync, validation, or durable memory updates when they did not happen.

## 11. References and tools

Read only when needed:

- `references/attention-kernel.md`: full mental model, anti-patterns, route examples.
- `references/profile-and-state.md`: profile schema, memory, feedback, staleness, privacy.
- `references/connector-adapter-protocol.md`: generic external-system adapter contract.
- `assets/attention-profile.example.yaml`: starter profile template without user-specific domains.
- `assets/attention-output.schema.json`: machine-readable output schema.
- `assets/connector-adapter.schema.json`: adapter manifest schema.
- `scripts/validate_attention_output.py`: deterministic validation for JSON output.
