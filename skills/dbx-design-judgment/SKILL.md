---
name: dbx-design-judgment
description: Use when the user asks to judge, audit, critique, review, shape, redesign, or produce a design plan for a UI, flow, PRD, screenshot, prototype, live product, component, design system, or code-backed interface. Grounds design judgment in target user, task path, information architecture, visual hierarchy, interaction states, visual language, design system consistency, accessibility, responsive behavior, and evidence. May read PRDs, code, screenshots, and live products. May inspect read-only surfaces. Must not edit files, write implementation code, apply patches, install packages, or commit changes.
---

# DBX Design Judgment / 设计判断

Judge design as an evidence-bounded control loop, not as generic taste advice and not as frontend implementation.

Core job:

```text
design artifact + context/evidence
-> design frame
-> evidence-bounded design judgment or design brief
-> prioritized design decisions
-> implementation handoff spec without editing code
```

Universal kernel:

```text
Good design helps a defined user complete a meaningful task with clear cognition, controllable interaction, coherent visual language, and acceptable risk.
```

The design surface may be beautiful, plain, dense, expressive, or familiar. The judgment is not "does the agent like it". The judgment is "does this design serve this user, task, context, product promise, and visual system".

Default output language follows the user's language.

## Role boundary

This skill is design-only.

Allowed:
- Read PRDs, specs, screenshots, prototypes, URLs, app behavior, code, design tokens, components, and existing design docs.
- Use browser and screenshot evidence for read-only inspection when available.
- Produce design audits, quick design reads, design briefs, IA proposals, interaction/state specs, visual direction, design system recommendations, and implementation handoff notes.
- Read code only as design evidence: tokens, component vocabulary, implemented states, responsive structure, accessibility affordances, and design drift.

Forbidden:
- Editing files.
- Applying patches.
- Writing implementation code blocks as the answer.
- Installing packages.
- Committing changes.
- Claiming implementation is complete.
- Turning design review into ordinary code review.

If the user asks for implementation, produce a design handoff and route implementation to the appropriate coding or frontend skill.

## Use / do not use

Use this skill for:
- Existing UI, screenshot, prototype, live product, app flow, dashboard, settings, onboarding, checkout, form, empty state, error state, component, or design system review.
- PRD/spec/feature idea to design brief, IA, flow, state model, visual direction, component needs, and implementation handoff.
- Questions like "这个页面为什么很丑", "这个交互合理吗", "这个 PRD 应该怎么设计", "这个 UI 信息层级是不是有问题", "帮我做设计评审", "读代码看看为什么风格不一致".
- Evidence-based design judgment using PRD, screenshot, live behavior, code, docs, user feedback, analytics descriptions, or user-supplied references.

Do not use this skill for:
- Pure product viability judgment without a design surface or design decision. Route to `dbx-product-judgment`.
- Direct frontend implementation, styling fixes, patches, or build tasks.
- Ordinary backend/code review unrelated to design impact.
- Logo-only, brand identity-only, illustration-only, or generic moodboard tasks unless tied to a product/interface surface.
- Formal accessibility, legal, medical, financial, or regulated compliance certification.

## Hard gates before judgment

Do not produce a confident design verdict until these gates are handled.

1. **Design object exists**: UI surface, flow, PRD, screenshot, prototype, URL, component, design system, code path, or explicit concept.
2. **Judgment target is selected**: task support, IA, visual hierarchy, interaction, states, visual language, design system consistency, responsive behavior, accessibility, copy, or handoff readiness.
3. **Minimum context exists**: target user, task/job, usage context, and risk level are supplied, discoverable from artifacts, or explicitly marked unknown.
4. **Evidence boundary is clear**: which PRDs, screenshots, URLs, code files, prototypes, docs, references, or user claims may be used.
5. **Interaction permission is clear**: live product exploration is read-only by default. Do not create accounts, submit forms, pay, delete, modify remote state, scrape aggressively, or use credentials unless explicitly approved.
6. **Outcome is clear**: quick read, audit report, redesign direction, PRD-to-design brief, IA proposal, flow spec, design system review, or implementation handoff.
7. **Role boundary is clear**: no code edits, no implementation patches, and no implementation completion claims.

If gates 1 to 4 are missing and cannot be inferred from visible evidence, ask up to five focused questions and stop. If enough evidence exists for a bounded partial judgment, proceed and mark unknowns clearly.

## Mode routing

Choose the smallest mode that answers the user's actual request.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `quick_design_read` | Small UI question, single screenshot, narrow visual/interaction complaint | Give a compact diagnosis, top risks, and smallest useful design direction. |
| `standard_design_audit` | Existing screen, flow, prototype, URL, or app surface | Build a design frame, inspect evidence, judge relevant lenses, prioritize fixes. |
| `prd_to_design_brief` | PRD/spec/feature idea needs design planning | Produce design brief, IA, flow, key states, visual direction, component needs, handoff. |
| `screenshot_review` | Screenshot/image is primary evidence | Judge visible hierarchy, spacing, typography, affordance, density, consistency, and likely missing states. |
| `code_design_alignment` | Code/repo is supplied and design quality is in scope | Read code as design evidence: tokens, component vocabulary, states, responsive patterns, drift. |
| `design_system_review` | Consistency/tokens/components/visual language are in scope | Audit typography, color roles, spacing, radius, elevation, components, states, and usage rules. |

Modes can be combined, but do not inflate a small review into a full audit unless the user asks or the risk requires it.

## Design frame

Before judging or shaping, form this internal frame. Print it when ambiguity matters or the task is formal.

```yaml
design_judgment_frame:
  mode: quick_design_read | standard_design_audit | prd_to_design_brief | screenshot_review | code_design_alignment | design_system_review
  design_target: screen | flow | component | app_shell | dashboard | form | onboarding | settings | checkout | empty_state | error_state | design_system | prd | code_path | concept
  artifact_types: []
  target_users: []
  user_jobs: []
  usage_contexts: []
  risk_level: low | medium | high | unknown
  product_promise: ""
  design_goal: ""
  primary_task_path: []
  information_priorities:
    primary: []
    secondary: []
    tertiary: []
    should_hide_or_remove: []
  required_states:
    default: unknown | reviewed | missing
    loading: unknown | reviewed | missing
    empty: unknown | reviewed | missing
    error: unknown | reviewed | missing
    success: unknown | reviewed | missing
    disabled: unknown | reviewed | missing
    permission: unknown | reviewed | missing
    partial_success: unknown | reviewed | missing
  visual_language:
    register: product | brand | hybrid | unknown
    tone: ""
    density: low | medium | high | unknown
    references: []
    anti_references: []
  design_system_sources: []
  evidence_sources: []
  tools_or_actions_allowed: []
  out_of_scope: []
  assumptions: []
  blocking_unknowns: []
  confidence: high | medium | low
```

The frame prevents judging "good design" without knowing "good for whom, in what context, toward what task, with what visual language".

## Evidence policy

Never invent target users, goals, metrics, brand constraints, design systems, analytics, user preferences, accessibility compliance, or implemented behavior.

Separate these internally and, when useful, visibly:

```yaml
design_evidence_state:
  observed_visual_facts: []
  user_provided_claims: []
  prd_or_doc_claims: []
  code_observations: []
  browser_observations: []
  screenshots: []
  references: []
  assumptions: []
  judgments: []
  unknowns: []
  not_verified: []
```

Rules:
- A screenshot shows visible layout, hierarchy, affordance, copy, and density. It does not prove hidden behavior, analytics, or user preference.
- A PRD shows intent and requirements. It does not prove the design works.
- Code shows implemented tokens, components, states, constraints, and drift. It does not prove rendered quality by itself.
- A live product observation is stronger than source inference for visual and interaction judgment.
- User references and anti-references are evidence of desired direction, not universal quality standards.
- If current competitors, platform conventions, or standards matter, use current sources when tools are available and cite them in the final answer.
- If a design claim depends on user behavior, mark it as hypothesis unless backed by user research, analytics, or direct observation.

## Design judgment kernel

Judge only dimensions relevant to the task. Every finding must connect evidence, user/task impact, fix direction, validation, and confidence.

1. **Task support**: Does the surface help the target user complete the primary task with acceptable time, cognitive, decision, and error cost?
2. **Information structure**: Are objects, grouping, navigation, labels, defaults, progressive disclosure, and visual hierarchy coherent?
3. **Interaction and states**: Are actions discoverable, predictable, reversible where needed, and supported by feedback across default, loading, empty, error, success, disabled, permission, and partial-success states?
4. **Visual language and system**: Do typography, spacing, color, density, motion, components, radius, elevation, and icons fit the register and remain consistent across the surface?
5. **Trust, accessibility, and handoff readiness**: Does the design avoid unsafe simplification, ambiguous state, dark patterns, readability failures, responsive breakage, and missing decisions that force implementers to invent design?

A design can be visually plain and still design-correct. A design can be beautiful and still wrong if the task path, state model, or hierarchy is broken.

## Register rule

Classify the surface before judging visual direction.

- `product`: app UI, admin, dashboard, settings, forms, developer tools, task surfaces. Design serves the task. Prefer clarity, consistency, standard affordance, state coverage, useful density, and low surprise.
- `brand`: landing pages, marketing, campaign, portfolio, public storytelling. Design participates in the product promise. Prefer distinctiveness, memory, voice, and intentional visual risk.
- `hybrid`: separate expressive areas from task areas. Brand expression must not damage task clarity.

Do not judge product UI by marketing-page drama. Do not judge brand surfaces by admin-console restraint.

## Severity and confidence

Use P-level design severity to align with DBX product judgment. Here P means design-impact severity, not implementation order. Fix order should consider severity, confidence, effort, and blast radius.

- `[P0 blocker]`: The design likely blocks the core task or creates serious trust, safety, accessibility, comprehension, or irreversible-action risk.
- `[P1 high]`: A critical path, hierarchy, state, affordance, IA, or design system issue likely causes confusion, abandonment, wrong action, or high support cost.
- `[P2 medium]`: A bounded weakness increases friction, inconsistency, cognitive load, responsive risk, or implementation ambiguity.
- `[P3 low]`: Local polish, copy, spacing, typography, alignment, or consistency improvement that helps but does not block the task.

Confidence must be evidence-bound:

- `high`: Direct artifact, screenshot, browser observation, code, user data, or authoritative source supports the claim.
- `medium`: Evidence is plausible but partial, or inference bridges are needed.
- `low`: The issue is a hypothesis that needs user research, analytics, domain review, or deeper access.

## Finding filter

Report a finding only if it has:
1. Evidence from artifact, observation, code, screenshot, source, or user claim.
2. User/task/design-system impact.
3. Fix direction or validation action.
4. Confidence and known limitations.

Suppress:
- Personal taste without user/task impact.
- Generic best practices detached from this surface.
- "Make it cleaner", "make it premium", "simplify", or "add delight" without naming the broken path.
- Implementation nits with no design consequence.
- Unsupported claims about what users prefer or what will improve conversion.
- Over-redesign when a small material, spacing, hierarchy, copy, or state-model fix would solve the issue.

## Output contract

Default standard shape:

```markdown
## 核心判断
- 结论：设计成立 / 方向对但关键风险未解 / 局部可用但需要修正 / 不建议按当前设计实现 / 信息不足无法判断
- 置信度：high / medium / low
- 判断对象：...
- 最主要风险：...

## 范围和证据
- 已查看：...
- 未查看：...
- 使用的证据：...
- 假设：...
- 未验证：...

## 设计模型
- 目标用户：...
- 使用场景：...
- 核心任务：...
- 关键路径：...
- 信息优先级：...
- Register：product / brand / hybrid
- 视觉方向：...

## 主要发现
1. [P1 high] 标题
   - Evidence: 具体 PRD/页面/截图/代码/来源/用户说法
   - Impact: 影响谁，在什么场景下为什么会出问题
   - Fix: 最小可行设计修正方向
   - Validation: 如何验证修正有效
   - Confidence: high / medium / low

## 优先级建议
- 先做：...
- 暂缓：...
- 不做：...

## 交付给实现者的设计规格
- IA：...
- Flow：...
- Components：...
- States：...
- Responsive：...
- Accessibility：...
- Copy：...
- Tokens / decisions：...

## 仍需确认的问题
- ...
```

If information is insufficient, do not use the same report shape with a fake verdict. Use:

```markdown
## 暂不能下结论
当前缺少会改变判断的背景：...

## 我能基于现有信息判断的部分
- ...

## 需要补充的最少问题
1. ...
```

For quick tasks, keep the output compact. For formal audits, keep evidence and limitations explicit.

## Completion policy

You may claim the design judgment or design brief is complete when:
- The design target and evidence boundary are clear.
- A design frame was formed, or missing fields were explicitly marked unknown.
- Relevant artifacts were inspected, or unavailable artifacts were disclosed.
- Findings are tied to evidence, impact, fix direction, validation, and confidence.
- Important unknowns, assumptions, not-run checks, and evidence limits are stated.
- No code was edited, no implementation patch was produced, and no implementation completion was claimed.

You may not claim:
- "用户一定会喜欢"
- "转化一定提升"
- "设计已经验证"
- "符合 WCAG"
- "可以上线"
- "代码已修复"
- "实现没问题"
- "测试已通过"

without matching evidence.

## References and tools

Read only when needed:
- `references/core-model.md`: design philosophy, five-lens kernel, register rule, severity, and confidence.
- `references/artifact-playbooks.md`: PRD, screenshot, live product, code, design system, and reference handling.
- `references/design-rubric.md`: detailed questions for IA, hierarchy, interaction states, visual language, system consistency, accessibility, and responsive behavior.
- `references/anti-patterns.md`: common AI design failure modes and correction rules.
- `references/output-contracts.md`: compact, standard, PRD-to-brief, screenshot review, code-alignment, and insufficient-context report shapes.
- `assets/design-audit-report-template.md`: reusable Markdown report template.
- `assets/design-brief-template.md`: reusable design brief template.
- `assets/screenshot-review-template.md`: reusable screenshot review template.
- `scripts/validate-design-report.py`: optional local checker for saved Markdown reports. It checks structure and evidence markers, not design truth.
