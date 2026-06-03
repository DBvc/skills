---
name: dbx-product-judgment-control
description: Use when the user asks to judge whether a product, feature, PRD, information architecture, content, interaction, UI flow, live product, implementation, roadmap, or competitor position is right, good, usable, valuable, coherent, worth building, or product-ready. Grounds judgment in target user, job/context, evidence, alternatives, critical path, trust, and implementation alignment. Ask blocking questions or collect evidence before judging when background is missing. Do not use for pure implementation, generic UI inspiration, ordinary code review without product judgment, generic market summaries, or unsupported guesses.
---

# DBX Product Judgment Control / 产品判断控制器

Judge product correctness as an evidence-bounded control loop, not as a taste checklist.

Core job:

```text
product artifact + context/evidence -> product contract -> evidence-bounded judgment -> prioritized fixes and validation plan
```

The universal kernel is stable across domains: a product is right when it helps a defined user in a real context achieve a valuable state change with acceptable cost, risk, trust, and implementation support. Domain facts, user groups, regulations, norms, competitors, and success metrics are not universal. Ground them in supplied artifacts, user answers, observed product behavior, code, PRD, or current external sources.

Default output language follows the user's language.

## Use / do not use

Use this skill for:

- Overall product, feature, PRD, MVP, roadmap, IA, content, interaction, UI, onboarding, settings, checkout, dashboard, internal tool, B2B workflow, AI product, developer tool, or mobile/web experience judgment.
- Questions like “这个产品做得对吗”, “这个功能好不好用”, “这个 PRD 是否成立”, “这个交互是否合理”, “这个实现是否支撑产品目标”, “和竞品比有没有优势”, “这个产品为什么感觉别扭”.
- Evidence-based audits of live URLs, screenshots, code, prototypes, docs, PRDs, analytics descriptions, user feedback, competitor pages, or market/domain materials.
- Product judgment that may include technical implementation review, but only when the product contract and user impact matter.

Do not use this skill for:

- Direct implementation with no product judgment.
- Ordinary code review focused only on diff correctness, style, or maintainability.
- Generic visual inspiration, logo/style exploration, or “make it pretty” requests with no product outcome.
- Generic market research that does not judge a specific product decision.
- One-off writing, summarization, translation, or explanation.
- Legal, medical, financial, safety-critical, or regulated compliance certification. You may flag product risks and recommend qualified review, but do not claim formal compliance.

## Hard gates before judgment

Do not produce a confident product verdict until these gates are handled.

1. **Product object exists**: product, feature, flow, PRD, code path, prototype, screenshot, URL, competitor set, or explicit concept.
2. **Judgment target is selected**: overall product, feature, flow, IA, content, interaction, UI, implementation alignment, roadmap, competitor position, or validation plan.
3. **Minimum context exists**: target user and job/context are supplied, discoverable from artifacts, or explicitly treated as unknown. If missing and material, ask blocking questions instead of guessing.
4. **Evidence boundary is clear**: which artifacts, URLs, code, PRDs, screenshots, sources, or user claims may be used.
5. **Interaction permission is clear**: for live products, know whether browsing, screenshots, login, form entry, test data, account creation, or external writes are allowed. Default is read-only exploration.
6. **Outcome criteria are possible**: define what “right” means for this task: adoption, task completion, trust, conversion, retention, learning, operational efficiency, revenue, safety, support reduction, implementation coherence, or another explicit criterion.
7. **Safety and legitimacy pass**: do not help with deception, non-consensual surveillance, dark patterns, credential collection, bypassing access controls, or harmful manipulation.

If gates 1 to 4 are missing and cannot be inferred from visible evidence, ask up to five blocking questions and stop. If enough evidence exists for a bounded partial judgment, proceed and mark unknowns clearly.

## No-guess policy

Never invent target users, business goals, metrics, domain rules, competitor facts, conversion rates, technical architecture, or user behavior.

Separate these categories internally and, when useful, visibly:

```yaml
product_evidence_state:
  observed_facts: []
  user_provided_claims: []
  document_claims: []
  code_observations: []
  external_sources: []
  assumptions: []
  judgments: []
  unknowns: []
  not_verified: []
```

Rules:

- A claim in a PRD is evidence of intent, not proof that users need it.
- A UI observation is evidence of what exists, not proof of user behavior.
- Code shows implemented behavior or constraints, not market value by itself.
- Competitor pages show positioning and capabilities, not necessarily adoption or quality.
- If current facts matter, use current external sources when tools are available and cite them in the final answer.
- If a high-stakes domain is involved, prefer authoritative sources and say when qualified expert review is required.

## Mode routing

Choose the smallest mode that can answer the user’s actual question.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `quick_product_read` | Small product/feature question, screenshot, single flow, early idea | Give a compact verdict, top risks, and next validation action. |
| `standard_product_audit` | Default for product, feature, PRD, flow, or implementation judgment | Build the product contract, inspect evidence, judge core dimensions, prioritize fixes. |
| `deep_product_audit` | High-stakes, ambiguous, large product, major roadmap, B2B workflow, regulated or revenue-critical flow | Add competitor/domain research, implementation alignment, risk model, validation design, and uncertainty map. |
| `prd_review` | PRD, requirements, roadmap, user stories, specs | Judge problem framing, users, success criteria, scope, edge cases, risks, metrics, implementation handoff. |
| `live_product_walkthrough` | URL, prototype, app, web product, or interactive surface | Explore representative flows, take screenshots when visual/interaction evidence matters, avoid external writes without approval. |
| `implementation_alignment` | Code/repo/API/data model is provided and product correctness is in scope | Map product promise to entities, state, APIs, errors, performance, telemetry, and validation. |
| `competitive_judgment` | User asks to compare competitors or market alternatives | Research current alternatives, compare on user job and switching cost, avoid stale or unsupported claims. |
| `validation_design` | User asks whether to build, ship, iterate, or test | Convert judgment into falsifiable assumptions, metrics, experiments, and decision gates. |

Modes can be combined, but do not inflate the audit if the user asked for a small judgment.

## Product contract

Before judging, form this internal contract. Print it when ambiguity matters or the task is formal.

```yaml
product_judgment_contract:
  mode: quick_product_read | standard_product_audit | deep_product_audit | prd_review | live_product_walkthrough | implementation_alignment | competitive_judgment | validation_design
  judgment_target: overall_product | feature | flow | ia | content | interaction | ui | implementation | roadmap | competitor_position | validation_plan
  artifact_types: []
  target_users: []
  jobs_to_be_done: []
  usage_contexts: []
  product_promise: ""
  desired_state_change: ""
  success_criteria: []
  evidence_sources: []
  tools_or_actions_allowed: []
  out_of_scope: []
  assumptions: []
  blocking_unknowns: []
  confidence: high | medium | low
```

The contract is not decoration. It prevents judging “good” without knowing “good for whom, in what situation, toward what outcome”.

## Evidence collection procedure

Use evidence in this order when available:

1. User-stated goal, constraints, target users, and non-goals.
2. Product artifact: PRD, screenshots, prototype, URL, app behavior, code, analytics description, user feedback, support tickets, research notes.
3. Direct observation: live walkthrough, screen inspection, code reading, flow reconstruction, state/error path review.
4. Current external facts: competitor pages, docs, standards, pricing, platform rules, public reviews, domain sources.
5. Inference, only after labeling it as inference and tying it to evidence.

Artifact-specific rules:

- **PRD/docs**: distinguish user evidence, business assumptions, solution decisions, acceptance criteria, metrics, edge cases, and open risks.
- **Live URL/product**: browse read-only by default; record the path taken; use screenshots when layout, interaction, or visual hierarchy matters; do not create accounts, submit forms, pay, scrape aggressively, or change external state without explicit approval.
- **Screenshots/prototypes**: judge visible hierarchy, affordances, labels, flow continuity, missing states, and likely mental model gaps. Do not infer analytics or hidden backend behavior from a screenshot.
- **Code/repo**: map product behavior to entities, state owners, APIs, persistence, permissions, error handling, performance, telemetry, and tests. Do not turn this into a generic code review unless product impact is clear.
- **Competitor research**: use current sources when tools are available; compare by user job, switching cost, time-to-value, risk, trust, distribution, and default path, not only feature count.
- **User feedback/analytics**: treat samples and anecdotes as evidence with limits. Ask about sample size, segment, collection bias, and time period when important.

## Universal product judgment kernel

Judge only dimensions relevant to the task. For each dimension, connect the judgment to user outcome, evidence, and trade-off.

1. **Problem and value**: Is the target problem real, frequent or intense enough, and worth solving compared with alternatives?
2. **User and context fit**: Is the product designed for a concrete user segment, moment, motivation, constraint, and risk level?
3. **State transformation**: Does the product clearly move the user from current state to desired state?
4. **Critical path**: Can the user reach the core value with low enough time, cognitive, decision, trust, and error cost?
5. **Concept model and IA**: Are objects, categories, navigation, permissions, lifecycle, defaults, and naming coherent?
6. **Information quality**: Is the right information shown at the right time, with useful priority, explanation, comparison, and feedback?
7. **Interaction quality**: Are actions discoverable, reversible where needed, predictable, accessible, and resilient to errors, empty states, slow networks, retries, and edge cases?
8. **Visual/UI support**: Does visual hierarchy, density, affordance, typography, spacing, contrast, and motion support the task rather than decorate it?
9. **Trust and safety**: Does the product avoid hidden costs, dark patterns, privacy surprises, ambiguous state, irreversible mistakes, and unsupported claims?
10. **Technical alignment**: Does implementation support the product promise through correct data models, state ownership, API contracts, reliability, performance, observability, security, and evolvability?
11. **Business and operating viability**: If in scope, can the product acquire, retain, monetize, support, and operate for the target users without undermining trust?
12. **Learning loop**: Are assumptions measurable? Are success metrics, guardrail metrics, experiments, feedback channels, and rollback gates defined?

A product can be visually simple but product-correct. A product can be beautiful and still wrong if the value path is broken.

## Severity and confidence

Use product severity, not aesthetic intensity.

- `[P0 blocker]`: The product likely fails the core job, creates serious user harm, violates trust/safety, or should not ship without redesign or expert review.
- `[P1 high]`: Important user flow, value proposition, data/state model, trust mechanism, or validation assumption is likely wrong or unprotected.
- `[P2 medium]`: Real but bounded weakness that increases friction, confusion, support cost, implementation risk, or learning uncertainty.
- `[P3 low]`: Local polish, clarity, hierarchy, copy, or simplification that helps but does not change product viability.

Confidence must be evidence-bound:

- `high`: Direct artifact, observation, code, user data, or authoritative source supports the claim.
- `medium`: Evidence is plausible but partial, or inference bridges are needed.
- `low`: The issue is a hypothesis that needs user research, analytics, domain review, or deeper product access.

## Finding filter

Report a finding only if it has:

1. Evidence from artifact, observation, code, user claim, or source.
2. Product impact tied to a user, job, flow, trust, risk, business outcome, or implementation constraint.
3. A fix direction or validation action.
4. Confidence and known limitations.

Suppress:

- Personal taste without user outcome impact.
- Generic “best practices” detached from this product.
- Feature-count comparisons with no user job or switching-cost analysis.
- Unsupported claims about users, metrics, competitors, or domain rules.
- Implementation nits with no product consequence.
- “Add AI”, “simplify UI”, “increase conversion”, or “improve onboarding” without naming the broken path.

## Implementation-alignment pass

Use this pass only when code, architecture, APIs, or technical implementation is in scope.

Build this internal model:

```yaml
implementation_alignment_model:
  product_promise: ""
  changed_or_relevant_user_paths: []
  core_entities: []
  state_owners: []
  lifecycles: []
  public_contracts: []
  persistence_or_schema: []
  permissions_or_privacy: []
  async_failure_surfaces: []
  performance_surfaces: []
  observability_and_metrics: []
  validation_coverage: []
```

Judge whether the implementation makes the intended product behavior natural, reliable, observable, and evolvable. Prefer findings about wrong entity boundaries, duplicated sources of truth, hidden state, missing error states, broken contracts, privacy gaps, missing metrics, and fragile flows over style comments.

## Output contract

Default shape:

```markdown
## 核心判断
- 结论：做对 / 方向对但未证明 / 局部成立但关键风险未解 / 不建议继续 / 信息不足无法判断
- 置信度：high / medium / low
- 判断对象：...
- 最主要风险：...

## 范围和证据
- 已查看：...
- 未查看：...
- 使用的证据：...
- 假设：...
- 未验证：...

## 产品模型
- 目标用户：...
- 核心场景：...
- 用户要完成的状态变化：...
- 当前关键路径：...
- 成功标准：...

## 主要发现
1. [P1 high] 标题
   - Evidence: 具体 PRD/页面/截图/代码/来源/用户说法
   - Impact: 影响谁，在什么场景下为什么会出问题
   - Fix: 最小可行修正方向
   - Validation: 如何验证修正有效
   - Confidence: high / medium / low

## 优先级建议
- 先做：...
- 暂缓：...
- 不做：...

## 验证计划
- 定性验证：...
- 定量验证：...
- 技术验证：...
- Guardrail：...

## 仍需确认的问题
- ...
```

If information is insufficient, do not use the same report shape with a fake verdict. Use:

```markdown
## 暂不能下结论
当前缺少会改变判断的背景：...

## 我能基于现有信息判断的部分
...

## 需要补充的最少问题
1. ...
```

For quick tasks, keep the output compact. For formal audits, keep evidence and limitations explicit.

## Completion policy

You may claim the product judgment is complete when:

- The judgment target and evidence boundary are clear.
- The product contract was formed, or missing fields were explicitly marked unknown.
- Relevant artifacts were inspected, or unavailable artifacts were disclosed.
- Findings are tied to evidence, impact, fix direction, validation, and confidence.
- Important unknowns, assumptions, not-run checks, and external-source limits are stated.

You may not claim:

- “用户一定会喜欢”, “一定能转化”, “竞品都不如它”, “技术上没问题”, “合规”, “验证通过”, “可上线”, or “测试已通过” without matching current evidence.

## References and tools

Read only when needed:

- `references/evidence-policy.md`: no-guess rules, question gates, live-product/tool safety, source hierarchy.
- `references/product-judgment-kernel.md`: detailed universal rubric, severity, confidence, and anti-patterns.
- `references/artifact-playbooks.md`: PRD, live URL, screenshot, code, competitor, analytics, and user-feedback playbooks.
- `references/output-contracts.md`: compact, standard, deep, PRD, live walkthrough, implementation alignment, and insufficient-context report shapes.
- `assets/product-audit-report-template.md`: reusable Markdown report template.
- `assets/product-context-question-bank.md`: optional question bank when context is missing.
- `scripts/validate-product-report.py`: optional local checker for saved Markdown reports. It checks structure and evidence markers, not product truth.
