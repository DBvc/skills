# dbx-crystallize Core Model

## Skill shape

```yaml
skill_shape:
  primary: procedure
  secondary:
    - decision
    - coordination
    - writing
  dominant_failure_modes:
    - premature_implementation
    - fake_precision
    - missing_non_goals
    - vague_acceptance
    - product_judgment_creep
    - design_or_technical_plan_creep
    - questionnaire_sprawl
    - handoff_failure
  implementation_implication: "Keep SKILL.md operational, split examples/templates into references/assets, and use evals to protect trigger and output boundaries."
```

## What this skill optimizes

The core effect is **ambiguity reduction before downstream work**.

A fuzzy request usually contains a mix of:

- real user need;
- stakeholder preference;
- solution guess;
- hidden constraint;
- missing decision;
- unvalidated product bet;
- unchosen design direction;
- premature implementation detail.

`dbx-crystallize` separates those layers and preserves only what can safely become a requirement contract.

## Requirement definition

A useful requirement has this shape:

```text
actor + context + current state + desired state + constraints + acceptance checks + non-goals
```

A weak requirement usually has this shape:

```text
solution noun + vague adjective + assumed user + no edge cases
```

Example:

```text
Weak: 增加一个更智能的导出按钮。
Better: 运营管理员在筛选订单列表后，可以导出当前筛选结果；导出过程有进度和失败重试；普通成员不可导出；本次不支持定时导出和跨租户汇总。
```

## Readiness states

Use exactly one primary status.

- `crystallized`: Requirements are clear enough for implementation planning or issue execution.
- `assumption-bound`: Usable as a draft, but important assumptions must be confirmed before build.
- `needs-product-judgment`: User/job/value/priority/product correctness is unresolved.
- `needs-design-judgment`: Flow, IA, state presentation, visual hierarchy, or interaction contract dominates.
- `needs-technical-plan`: Requirements are clear but architecture/source-of-truth/implementation strategy is unresolved.
- `blocked`: Missing or unsafe decisions would materially change the requirement.

## Dominant failure modes and controls

| Failure mode | What it looks like | Control |
| --- | --- | --- |
| `premature_implementation` | Agent starts writing code or technical plan | Role boundary, readiness handoff, no code edits. |
| `fake_precision` | Invented users, metrics, thresholds, or policies | Fact/assumption/unknown split and `TBD` markers. |
| `solution_lock_in` | User says "add button" and agent never asks state change | Translate solution to desired state and job. |
| `missing_non_goals` | Scope quietly balloons | Mandatory scope, non-goals, and must-not-change fields. |
| `vague_acceptance` | "works well", "easy to use", "fast enough" | Observable ACs and thresholds marked TBD when unknown. |
| `questionnaire_sprawl` | Agent asks 20 generic PM questions | Max five blocking questions; only ask decision-changing questions. |
| `judgment_creep` | Agent decides whether feature is worth doing | Handoff to product judgment; no confident product verdict. |
| `design_creep` | Agent turns requirement into UI redesign | Handoff to design judgment when design surface dominates. |
| `technical_creep` | Agent freezes architecture before requirements settle | Handoff to technical plan after requirement readiness. |
| `handoff_failure` | Output is pretty but not usable by engineer/tester | IDs, ACs, edge cases, readiness, next target. |

## What not to optimize

Do not optimize for a complete-looking PRD. Optimize for downstream correctness.

Do not optimize for zero unknowns. Optimize for visible unknowns.

Do not optimize for answering every question now. Optimize for finding the questions that actually change the contract.

Do not optimize for novelty. Most requirement work benefits from boring clarity.
