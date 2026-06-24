# Repository Integration Snippets for dbx-crystallize

This file is not required for runtime. It gives copy-paste snippets for repository-level docs after adding `skills/dbx-crystallize/`.

## README Stable Skills row

```markdown
[`dbx-crystallize`](skills/dbx-crystallize) 模糊产品/软件想法、需求草稿、issue 或前置讨论的需求结晶：澄清用户/场景/状态变化、scope、non-goals、验收标准、边界状态、开放决策和 handoff。Requirement crystallization before product judgment, design, technical planning, or implementation.
```

## DBX_SKILL_INDEX.md row

```markdown
| `dbx-crystallize` | Pre-development requirement crystallization for fuzzy product/software ideas, feature requests, issue drafts, and stakeholder asks. | procedure + decision + coordination | L5 | Fake precision, over-questioning, and creep into product/design/technical judgment. | Use before product/design/technical planning when the primary task is clarifying requirements; route product-worth verdicts to `dbx-product-judgment`, UI/design correctness to `dbx-design-judgment`, technical implementation planning to `dbx-technical-plan`, and formal plan-first phases only when explicitly named. | Add baseline comparison after 10 real requirement discussions; tune blocking-question policy. |
```

## DBX_ROUTING_MATRIX.md primary intent row

```markdown
| Clarify a fuzzy product/software idea, feature request, issue draft, stakeholder ask, or pre-development discussion into precise requirements, scope, non-goals, acceptance criteria, and handoff | `dbx-crystallize` | `dbx-product-judgment` for product-worth verdicts, `dbx-design-judgment` for design correctness, `dbx-technical-plan` for implementation planning, and `dbx-software-plan-first-*` unless explicitly named. |
```

## DBX_ROUTING_MATRIX.md graph rule

```markdown
| `dbx-crystallize` precedes judgment/planning/implementation when requirements are fuzzy | Use it to produce a requirement contract before `dbx-product-judgment`, `dbx-design-judgment`, `dbx-technical-plan`, or implementation. Do not use it when the user already asks for a product verdict, design critique, concrete code review, or direct implementation. |
```

## DBX_ROUTING_MATRIX.md chaining rule

```markdown
### Requirement crystallization
Use `dbx-crystallize` when the user is still defining what should be built: fuzzy idea, issue draft, stakeholder ask, pre-development discussion, scope/non-goals, or acceptance criteria. It may hand off to `dbx-product-judgment` when product value/user/job is unresolved, to `dbx-design-judgment` when flow/IA/UI state is unresolved, and to `dbx-technical-plan` when requirements are clear but implementation strategy is not. Do not use it as a generic PRD writer or as a shortcut into code.
```

## Near-miss examples

```markdown
| "先别写代码，帮我把这个功能想清楚，写成可验收需求。" | `dbx-crystallize`. |
| "把老板这句话需求整理成 issue，重点写 scope、non-goals 和 AC。" | `dbx-crystallize`. |
| "这个功能到底值不值得做?" | `dbx-product-judgment`, not `dbx-crystallize` unless the user first asks to clarify the requirement. |
| "这个页面交互怎么设计?" | `dbx-design-judgment`, not `dbx-crystallize` unless the user asks for requirement contract first. |
| "需求已经定了，给我技术实施计划。" | `dbx-technical-plan`, not `dbx-crystallize`. |
```
