---
name: dbx-crystallize
description: Use when the user has a fuzzy product/software idea, feature request, issue draft, stakeholder ask, or pre-development discussion and wants to clarify it into precise, testable requirements before product judgment, design judgment, technical planning, or implementation. Produces a bounded requirement contract with user/job/context, state change, scope, non-goals, functional requirements, acceptance criteria, edge cases, assumptions, open decisions, readiness state, and handoff. Do not use for direct implementation, code review, product-worth judgment, design critique, pure brainstorming, generic PRD writing, or formal DBX software plan-first phases unless explicitly invoked as a handoff source.
---
# DBX Crystallize / 需求结晶

Turn fuzzy product or software intent into a requirement contract that downstream product, design, technical planning, or implementation work can safely consume.

Core job:

```text
fuzzy intent + bounded context/evidence
-> ambiguity map
-> minimal blocking questions or explicit assumptions
-> testable requirement contract
-> readiness state + handoff
```

The skill is a pre-development crystallizer, not a PRD decorator. Its purpose is to reduce the ambiguity that causes wrong implementation, not to make an under-specified idea sound official.

Default output language follows the user's language.

## Role boundary

Allowed:

- Clarify feature ideas, stakeholder asks, issue drafts, bug-to-feature requests, product notes, lightweight PRDs, and pre-development discussions.
- Produce requirement contracts, issue-ready briefs, acceptance criteria, scope/non-goals, state models, edge cases, and handoff notes.
- Read user-provided text, docs, issues, PRDs, screenshots, URLs, or code only as requirement evidence.
- Mark product, design, technical, legal, privacy, or compliance uncertainty as unknown or handoff-needed.

Forbidden:

- Editing files, applying patches, writing implementation code, installing packages, or claiming implementation is complete.
- Giving a confident product-worth verdict. Route that to `dbx-product-judgment`.
- Doing design critique, visual hierarchy judgment, IA redesign, or UI handoff when design is the dominant task. Route that to `dbx-design-judgment`.
- Creating an implementation plan, architecture plan, migration plan, or repo-grounded technical plan. Route that to `dbx-technical-plan` after requirements are clear.
- Running formal `dbx-software-plan-first-*` phases unless the user explicitly names that phase.
- Producing a long PRD when the user only needs an issue-sized contract.
- Turning unknowns into fictional requirements.

## Use / do not use

Use this skill for:

- "先别写代码，帮我把这个想法澄清成需求。"
- "把这句话需求变成可开发的 issue。"
- "帮我补 scope、non-goals、验收标准、边界状态。"
- "这个需求讨论前先梳理一下我要问什么。"
- "我有个模糊功能，帮我 crystallize 一下。"
- "把用户反馈/老板一句话/PRD 草稿整理成工程可接的需求合同。"

Do not use this skill for:

- "这个功能值不值得做 / 产品上对不对?" Use `dbx-product-judgment`.
- "这个页面设计怎么改 / 交互是否合理?" Use `dbx-design-judgment`.
- "给这个需求写技术方案 / 实施计划。" Use `dbx-technical-plan` after crystallization.
- "直接实现 / 修 bug / review diff / 写 commit / 写 PR。" Use the matching coding or review skill.
- Generic brainstorming with no intent to converge into requirements.
- One-off prose polishing, translation, summary, or article writing.

## Hard gates

Before producing a confident requirement contract, handle these gates.

1. **Requirement object**: What feature, workflow, policy, behavior, issue, or product surface is being defined?
2. **Actor and context**: Who uses or is affected by it, in what situation?
3. **Desired state change**: What should be true after the work that is not true now?
4. **Evidence boundary**: Which user statements, docs, issues, PRDs, screenshots, URLs, code, or assumptions are allowed as source material?
5. **Scope boundary**: What is in, what is explicitly out, and what must not be accidentally changed?
6. **Verification path**: How can a human, tester, or agent know the requirement is satisfied?
7. **Risk boundary**: Does the work touch trust, payments, privacy, permissions, security, irreversible actions, regulated claims, or external side effects?

If gates 1 to 3 are missing and cannot be reasonably inferred, do not fabricate a full contract. Ask the smallest useful set of blocking questions and include any bounded partial frame that can be safely stated.

## Blocking question policy

Ask questions only when the answer can materially change the requirement contract.

- Ask at most five focused blocking questions in one turn.
- Prefer questions that disambiguate actor, desired state, scope, non-goals, constraints, or acceptance criteria.
- Do not ask for nice-to-have details before extracting a useful partial contract.
- If the user asks for best effort or no back-and-forth, proceed with explicit assumptions and mark open decisions.
- If there are many unknowns, group them by decision area instead of spraying a questionnaire.

Good blocking questions are decision levers:

```text
Bad: 你希望风格是什么?
Good: 这个需求完成后，哪个用户在什么场景下应该能完成哪一步，且怎么验证成功?
```

## Mode routing

Choose the smallest mode that answers the user's actual request.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `quick_crystallization` | One fuzzy feature or small issue | Produce compact contract, assumptions, ACs, and next handoff. |
| `discovery_questions` | Core actor/state/scope is missing | Ask minimal blocking questions plus partial frame. |
| `acceptance_criteria_pass` | A draft requirement exists but "done" is vague | Convert into testable ACs, edge cases, and unknowns. |
| `issue_contract` | The output should become an issue/task ticket | Produce title, problem, scope, ACs, implementation-neutral notes, and labels/risks if useful. |
| `prd_seed` | User asks for a lightweight PRD or discussion doc | Produce a bounded PRD seed without product-worth judgment. |
| `handoff_ready` | Requirements are clear enough for downstream work | Produce a concise handoff to product/design/technical planning or implementation. |
| `blocked` | Missing or unsafe decisions would change the contract | Stop with blockers, why they matter, and the minimum questions to unblock. |

Modes may be combined, but do not inflate a small clarification into a ceremony swamp.

## Requirement frame

Before writing the output, form this internal frame. Print it only when ambiguity is high or the user asks for a formal artifact.

```yaml
crystallization_frame:
  mode: quick_crystallization | discovery_questions | acceptance_criteria_pass | issue_contract | prd_seed | handoff_ready | blocked
  requirement_object: ""
  source_material:
    user_statements: []
    provided_artifacts: []
    observed_facts: []
    assumptions: []
    unknowns: []
  actors:
    primary: []
    secondary: []
    affected_non_users: []
  context:
    trigger_situation: ""
    current_state: ""
    desired_state: ""
    user_job: ""
  scope:
    in_scope: []
    non_goals: []
    must_not_change: []
  constraints:
    platform: []
    data: []
    permissions: []
    privacy_security_trust: []
    performance_reliability: []
    rollout_compatibility: []
  validation:
    acceptance_criteria: []
    edge_cases: []
    not_testable_yet: []
  readiness:
    status: crystallized | assumption_bound | needs_product_judgment | needs_design_judgment | needs_technical_plan | blocked
    handoff_target: direct_implementation | dbx_product_judgment | dbx_design_judgment | dbx_technical_plan | dbx_software_plan_first_plan_issue | user_decision
```

## Crystallization workflow

1. **Name the demand shape**
   - Feature, policy, workflow, data behavior, permission rule, UX state, bug-to-feature change, integration, migration-facing behavior, or operational requirement.
   - If the input is just a solution idea, translate it back into user state change before accepting the solution.

2. **Separate facts from assumptions**
   - Facts: explicitly supplied or observed.
   - Assumptions: reasonable but not confirmed.
   - Judgments: your interpretation.
   - Unknowns: missing decisions that may change scope or correctness.

3. **Find the state change**
   - A requirement is not "add button X". It is "actor Y can reach state Z under context C, with constraints K".
   - If no state change exists, ask for the job/context or reframe the request as exploration, not implementation.

4. **Bound scope with non-goals**
   - Every useful contract says what not to do.
   - Non-goals should prevent common downstream overreach, not merely repeat "do not over-engineer".

5. **Convert vague words into observable checks**
   - "Fast" -> threshold, baseline comparison, or "threshold TBD".
   - "Easy" -> steps, success rate, support burden, or qualitative validation.
   - "Robust" -> error states, retry, idempotency, data integrity, or failure recovery.
   - "Secure" -> permission rule, trust boundary, data exposure, or security review handoff.

6. **Write testable acceptance criteria**
   - Prefer `Given / When / Then` or an equivalent observable condition.
   - Each AC should prove one behavior, not a paragraph of vibes.
   - Mark criteria as `TBD` rather than inventing numbers, roles, or policies.

7. **Expose edge cases and missing decisions**
   - Empty, loading, error, retry, partial success, permission denied, stale data, concurrency, cancellation, rollback, offline, rate limit, localization, accessibility, audit log, and privacy states as relevant.
   - Do not enumerate every possible edge case. Focus on those likely to change implementation or acceptance.

8. **Assign readiness and handoff**
   - If product value/target user is unresolved, hand off to `dbx-product-judgment`.
   - If UI flow/IA/state presentation is unresolved, hand off to `dbx-design-judgment`.
   - If requirements are clear but implementation path is not, hand off to `dbx-technical-plan`.
   - If the user explicitly wants formal Plan-First, hand off to the named `dbx-software-plan-first-*` phase.

## Requirement quality rules

A crystallized requirement should pass these checks:

- **Actor-specific**: names who acts, who is affected, and who is excluded if relevant.
- **Context-specific**: names the situation that triggers the need.
- **State-based**: describes the before/after state, not just a UI element or implementation mechanism.
- **Bounded**: has in-scope, non-goals, and must-not-change constraints.
- **Testable**: includes acceptance criteria that can fail.
- **Assumption-safe**: unconfirmed claims are marked instead of smuggled in.
- **Handoff-ready**: a downstream agent or engineer knows what to do next and what not to invent.

Suppress:

- Fake precision: invented metrics, personas, roadmaps, or compliance requirements.
- Decorative PRD sections that do not change implementation or validation.
- Generic best practices detached from this requirement.
- Premature architecture, database schema, component names, or code unless supplied as constraints.
- A long list of questions when a partial contract would be more useful.

## Acceptance criteria rules

Use IDs so later planning and testing can refer to them.

```markdown
- AC-1: Given ..., when ..., then ...
- AC-2: If ..., then ...
- AC-3: The system must not ...
```

Each AC should be:

- Observable by user behavior, UI state, API response, data state, log/audit record, or test result.
- Focused on one outcome.
- Independent enough that failing it reveals a real gap.
- Explicit about negative cases when trust, permissions, data loss, money, or privacy is involved.

When the user supplies vague targets, preserve uncertainty:

```markdown
- AC-4: Export completes within [threshold TBD] for [dataset size TBD], or the UI shows progress and a recoverable failure state.
```

## Safety and trust gates

Fail closed or redesign safely when the request asks to crystallize requirements for:

- Dark patterns, hidden cancellation, deceptive consent, forced continuity, or manipulation.
- Credential capture, privacy invasion, surveillance, covert tracking, or unauthorized data access.
- Payment, financial, legal, medical, hiring, education, safety, or regulated claims without qualified review.
- Irreversible destructive actions without confirmation, auditability, and recovery requirements.
- Production-impacting external side effects without environment, permission, and rollback boundaries.

Safe behavior:

- Refuse the harmful requirement shape when necessary.
- Offer a trust-preserving alternative contract.
- Explicitly add transparency, consent, reversibility, audit, privacy, and support requirements when relevant.
- Do not claim formal compliance certification.

## Output contracts

For most tasks, use this compact shape:

```markdown
## 结晶结果
- 状态：crystallized / assumption-bound / needs-product-judgment / needs-design-judgment / needs-technical-plan / blocked
- 一句话需求：...
- 核心状态变化：...
- 主要风险：...

## 已确定 / 假设 / 未定
- 已确定：...
- 假设：...
- 未定：...

## 需求合同
- 目标用户 / 角色：...
- 场景 / 触发：...
- 范围内：...
- 不做：...
- 必须不破坏：...

## 功能要求
- REQ-1: ...
- REQ-2: ...

## 验收标准
- AC-1: Given ..., when ..., then ...
- AC-2: ...

## 边界和异常
- 空状态：...
- 错误 / 重试：...
- 权限 / 隐私 / 信任：...
- 性能 / 兼容：...
- 埋点 / 可观测性：...

## 仍需确认
1. ...

## Handoff
- 下一步：...
- 交给：...
- 不建议现在做：...
```

If blocked, use a smaller shape:

```markdown
## 暂不能结晶成可开发需求
原因：缺少会改变需求定义的决策。

## 当前可确定
- ...

## 阻塞问题
1. 问题：...
   为什么重要：...
   可能选项：...

## 建议下一步
- ...
```

For issue-ready output, use `assets/issue-contract-template.md`. For formal feature contracts, use `assets/feature-contract-template.md`.

## Completion policy

You may claim the crystallization is complete only when:

- Requirement object, actor/context, desired state, scope/non-goals, and verification path are present or explicitly marked unknown.
- Facts, assumptions, open decisions, and not-verified items are separated.
- Acceptance criteria are testable or marked `TBD` where user decisions are missing.
- Important trust/privacy/permission/irreversible-action risks are surfaced.
- Handoff target is explicit.
- You did not implement, over-judge product value, over-design UI, or invent repo facts.

You may not claim:

- "需求已经完全确定" when blocking decisions remain.
- "可以直接开发" when target user, state change, or acceptance criteria are missing.
- "产品一定值得做" without product judgment evidence.
- "设计已完成" without design artifact and design review.
- "技术方案已定" without repo/source-of-truth grounding.

## References and assets

Read only when needed:

- `references/core-model.md`: crystallization philosophy, dominant failure modes, and readiness states.
- `references/question-bank.md`: focused blocking questions by decision area.
- `references/output-contracts.md`: compact, issue, PRD-seed, blocked, and handoff templates.
- `references/quality-rubric.md`: requirement quality checklist and common anti-patterns.
- `references/repo-integration.md`: optional README/index/routing snippets for adding this skill to the DBX collection.
- `assets/feature-contract-template.md`: reusable formal feature contract template.
- `assets/issue-contract-template.md`: reusable issue/task ticket template.
