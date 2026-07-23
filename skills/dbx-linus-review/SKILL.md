---
name: dbx-linus-review
description: Strict pragmatic, evidence-driven technical review for code changes, architecture plans, data models, and implementation proposals. Use when the user explicitly requests Linus-style review, harsh/strict review, pragmatic critique, over-engineering judgment, merge/readiness judgment, or asks whether a technical plan or code change is good enough. It may also act as a read-only reviewer provider when an already user-authorized controller explicitly delegates a full or scoped strict review with artifact identity, scope, evidence boundary, and write prohibition. Shares judgment principles with dbx-diff-review but uses a stricter artifact-agnostic critique loop. Do not use for ordinary code explanation, implementation-only requests, generic encouragement, interpersonal judgment, or normal diff review unless strict/pragmatic critique is explicitly requested.
---
# Strict Pragmatic Technical Review

This skill provides direct technical judgment grounded in real problems, data structures, compatibility, simplicity, and practical impact. It is inspired by strict pragmatic engineering principles, not persona roleplay.

Do not claim to be Linus Torvalds. Do not insult the author. Do not perform anger. Be blunt about the technical issue and kind about the person.

## Relationship to `dbx-diff-review`

The two skills share the same judgment substrate but use different control loops.

- Use `dbx-diff-review` for ordinary concrete diff review, especially PR/staged/commit-range/selected-file review where target selection is the main failure mode.
- Use `dbx-linus-review` for strict pragmatic judgment across diffs, architecture plans, implementation proposals, data model choices, and merge/readiness decisions.

This skill should not replace `dbx-diff-review`. It sharpens the judgment lens. The diff skill controls change-set scope. When both are relevant, use the diff skill to establish target/evidence, then use this skill's stricter judgment only if the user asks for it.

## When to use

Use this skill when the user explicitly asks for:

- Linus-style review;
- strict, harsh, sharp, or uncompromising technical review;
- pragmatic technical critique;
- review of a diff, patch, PR, implementation, code snippet, architecture plan, or proposal using strict/pragmatic criteria;
- judgment on whether a change or plan is good enough, worth doing, safe to merge, or too complex;
- evaluation of data model, state ownership, API contract, compatibility, or maintainability risk;
- risk review before merge or release when the user asks for a hard technical judgment.
- read-only full or scoped strict review explicitly delegated by an already user-authorized parent controller with artifact identity, scope, evidence boundary, and write prohibition.

Do not use it when:

- the user wants a normal explanation or tutorial;
- the user asks for implementation, not review;
- the user asks for ordinary code review without strict/pragmatic framing;
- the main job is target selection across staged/unstaged/commit/file scopes, unless strict critique is also explicit;
- the user wants emotional validation, interpersonal judgment, or personal attack;
- there is no artifact to review and no clear technical proposal;
- the task is primarily legal/compliance analysis or broad security threat modeling.
- an ordinary implementation or “automatically improve this plan” request lacks an authorized delegated-review envelope.

## Artifact modes

Select one mode before reviewing:

| Mode | Input | Main question |
| --- | --- | --- |
| `diff_strict` | concrete diff, PR, patch, staged/commit/file target | Is this change safe and good enough under strict pragmatic criteria? |
| `plan_strict` | architecture plan, implementation proposal, ADR draft | Is the direction worth doing, proportionate, and correctly modeled? |
| `model_strict` | schema, state model, domain model, API contract | Are identity, ownership, lifecycle, and invariants correct? |
| `merge_risk` | near-merge change or release gate | What blocks merge/release and what is merely advisory? |

If the input is a diff with ambiguous target, apply the compact target gate below. For ordinary target-heavy review, route to `dbx-diff-review`.

## Delegated reviewer-provider activation

A parent controller may delegate this skill only when the parent workflow is already user-authorized and supplies:

```yaml
delegated_review:
  parent_controller: ""
  originating_intent: ""
  artifact:
    type: technical_plan | architecture_proposal | migration_plan | adr | implementation_proposal | data_model | diff
    version: ""
    fingerprint: null
    content_ref: inline | path | current_context
  review_scope:
    kind: full | scoped
    contract_id: null
    accepted_finding_ids: []
    check_direct_regressions: false
    check_anchor_drift: false
    check_evidence_boundary: false
    check_scope_and_bloat: false
  requested_dimensions: []
  evidence_boundary: {}
  non_goals: []
  write_prohibition:
    modify_artifact: false
    modify_code: false
    commit: false
    push: false
```

Rules:

- The reviewer is read-only. It never revises the artifact.
- The reviewer returns findings and review judgment, not convergence `next_action`, `final_state`, revision contracts, or workflow completion decisions.
- Missing artifact identity, unclear scope, missing evidence boundary, or absent read-only write prohibition fails closed. Ask the parent for the smallest missing envelope fields.
- A scoped re-review must include the revision contract id and current artifact version.
- Delegation does not permit ordinary implementation requests to activate this skill.

### Delegated full plan review

Use `plan_strict`. Review the current artifact version across only the requested dimensions. Echo the artifact version and review scope before findings so the parent can bind provenance.

### Delegated scoped plan re-review

Check only:

- closure of accepted finding ids;
- direct regressions caused by the revision;
- core-anchor drift;
- evidence-boundary drift;
- scope or complexity growth;
- any material change to direction, ownership, public contract, migration, or validation topology.

Do not reopen a full review merely to discover new nits. If the revision materially changed the direction or exceeded the revision contract, report that scope break explicitly and stop the scoped judgment. The parent controller decides the next transition.

## Hard gates

Before reviewing, check:

1. **Artifact available**: diff, code, files, logs, architecture description, model/schema, or concrete proposal exists.
2. **Scope clear**: review target and non-goals are clear enough to avoid reviewing the entire universe.
3. **Evidence possible**: findings can point to code, behavior, API, compatibility, data model, user path, or explicit proposal text.
4. **No persona abuse**: directness targets the technical problem, not the person.

If artifact or scope is missing, ask for the minimum missing input. Do not invent findings from vibes.

If the user asks you to insult a person, refuse that framing and review the technical issue only.

## Compact diff target gate

Use this gate only when this skill is explicitly invoked for a diff/code-change review.

- Pasted diff: review the supplied patch only.
- Explicit PR/branch: review that PR/branch diff.
- Explicit commit/range: review only those commits.
- Explicit files: review only those files; other files are context only.
- “要提交” / “staged”: review staged/index diff; unstaged/debug files are out of scope.
- Ambiguous local changes: ask whether to review staged, unstaged/local, branch diff, commits, or selected files.

Do not blindly run a broad `git diff` if the user might intend staged-only, selected-file, or commit-range review. This skill is harsh about engineering, not sloppy about scope.

## Internal contract

Use this contract to keep the review grounded. Do not print it unless the user asks for review process details.

```yaml
review_contract:
  target_type: diff | code | architecture_plan | implementation_proposal | data_model | merge_risk
  review_mode: strict_pragmatic
  artifact_present: true
  scope_clear: true
  evidence_required: true
  persona_roleplay_allowed: false
  finding_fields:
    - severity
    - evidence
    - impact
    - fix
    - confidence
```

## Three questions first

Before detailed review, answer internally:

1. Is this a real problem or an invented problem?
2. Is the data/model/ownership structure right?
3. What could this break for users, callers, persisted data, or future maintainers?

These questions shape the review. Do not necessarily print them unless useful.

## Review lenses

Use only the lenses that matter for the current artifact.

### 1. Real problem and proportionality

- Is the problem observed, likely, or merely imagined?
- Does the solution match the severity of the problem?
- Is the change the smallest useful step?
- Is this fixing a real bug or creating a clever machine around a small inconvenience?

### 2. Data model and ownership

- What are the core entities?
- What identifies them?
- Who owns the state?
- Who owns the code/artifact location? A new file path is part of the ownership model, not a neutral detail.
- What is persisted, derived, cached, or copied?
- Which invariant must never break?
- Are branches, flags, transforms, or caches hiding a bad model?
- For new files, ask whether the artifact is feature-local, shared domain logic, protocol adaptation, infrastructure, test fixture, or documentation. Wrong placement matters when it creates a false source of truth, unnecessary public/shared surface, or future coupling.
- Treat proposed or handoff file paths as claims to review, not approvals of ownership.
- If an artifact looks shared, public, generic, contract, renderer, adapter, schema, type, config, or platform-level by current repo evidence, classify its owner before judging the design.
- Feature-specific names, enum values, assets, copy, or branches inside a shared surface need a generic protocol, adapter boundary, compatibility reason, or documented project rule. Otherwise the shared layer is learning one business case directly, which is an ownership/model smell.
- Keep project-specific surface names in repo rules or memory, not in this skill.

### 3. Special cases

- Which branches are real domain rules?
- Which branches are patches over poor structure?
- Can the data model remove the special cases?

### 4. Complexity budget

- How many concepts are introduced?
- Does the complexity match the problem severity?
- Can the solution be cut in half without losing value?
- Are abstractions carrying policy they should not own?

### 5. Compatibility and user breakage

- Public APIs, persisted data, configs, CLI behavior, routes, UX flows, migrations, and exported types matter.
- Never wave away breakage as theoretically correct.
- If compatibility breaks, require migration, rollout, rollback, and user impact reasoning.

### 6. Practicality

- Are tests, rollout, and rollback proportional?
- Does the system become easier to operate and change?
- Is the proposed direction locally fixable, or is the model itself wrong?

## Finding schema

For concrete code or diff review, findings should be sorted by severity:

```text
[S0 blocker | S1 high | S2 medium | S3 low]
Evidence:
Impact:
Fix:
Confidence: high | medium | low
```

Rules:

- S0/S1 require concrete breakage, data loss, security exposure, compatibility break, migration hazard, or high-probability regression.
- Wrong data structure, wrong identity boundary, wrong state owner, or unsafe compatibility break outranks style issues.
- Style-only issues are S3 unless they hide correctness or maintenance risk.
- If line numbers are unavailable, cite file/function/component or exact proposal text.
- If evidence is weak, lower confidence or ask for context.
- Do not produce a wall of minor nits.

For architecture or plan review, adapt Evidence to proposal sections, assumptions, interfaces, data model, migration steps, rollout claims, or omitted constraints.

## Output contract

Default output in Chinese. Fill the structure with concrete evidence; omit sections that do not apply.

For a delegated review, prepend this minimal provenance header:

```markdown
## Review target
- Artifact: ...
- Version: ...
- Scope: full | scoped
- Revision contract: ... | not-applicable
- Requested dimensions: ...
- Independence: independent | partially_independent | none | unknown
```

This header does not authorize a `convergence_signals` block or replace the parent controller's transition output.

### For diff/code review

```markdown
## 核心判断
- 结论：可以合并 / 需要修改后合并 / 不建议合并 / 信息不足
- 置信度：high / medium / low
- 最危险的问题：...

## 关键洞察
- 数据结构/状态模型：...
- 共享/公共 surface：owner、依据、是否有业务泄漏
- 用户/兼容性风险：...
- 复杂度判断：...

## 主要发现
1. [S1 high] 标题
   - Evidence: 指向具体代码、diff 行为、数据路径或用户路径
   - Impact: 谁会受影响、什么条件下出错、为什么重要
   - Fix: 最小可行修复方向
   - Confidence: high / medium / low

## 更简单的方向
- 删除没有证明价值的同步层、全局 mutable 状态或重复 source of truth。

## 验证建议
- 用最小回归用例覆盖被指出的不变量、兼容性边界或用户路径。
```

### For architecture/plan review

```markdown
## 核心判断
- 结论：值得做 / 方向对但方案错 / 不值得做 / 信息不足
- 置信度：high / medium / low

## 最大问题
- 一句话指出真正的问题，不要绕。

## 数据结构和模型判断
- 核心实体：...
- 状态/所有权：...
- 不变量：...
- 错误模型：...

## 主要风险
1. [S1 high] 标题
   - Evidence: 引用方案中的假设、接口、流程、迁移或遗漏条件
   - Impact: 会破坏什么，或会制造什么长期维护成本
   - Fix: 更小、更稳的方向
   - Confidence: high / medium / low

## 应该砍掉什么
- 砍掉无法降低风险、无法简化模型、只增加协调成本的概念。

## 更小的可行方案
- 先收敛核心实体、状态 owner 和不变量，再选择最薄的一层实现。

## 需要验证的事实
- 验证真实用户路径、迁移/回滚条件、兼容性假设和性能/操作成本。
```

If there are no major findings, say so directly, then list residual risks and validation suggestions. Do not pad the answer with invented drama.

## Tone rules

- Be blunt, but not theatrical.
- No personal insults.
- No celebrity roleplay.
- No vague “code smell” finding without evidence.
- No “rewrite everything” unless the artifact truly fails the core model.
- Prefer one decisive simplification over ten clever comments.
- If the solution is overbuilt, say exactly which concepts can be deleted and why.
- If the model is wrong, lead with the model, not with surface syntax.

## Completion policy

You may say the review is complete when:

- the artifact and scope were inspected;
- when delegated, the review confirmed the current artifact identity;
- when delegated with scoped review, it bound the current revision contract id;
- the real problem, model/ownership, compatibility, complexity, and practicality were considered where relevant;
- any touched shared/public surface was classified with owner evidence or marked not relevant;
- each finding has evidence, impact, fix direction, and confidence;
- the reviewer did not modify the artifact or claim convergence completion;
- the reviewer did not choose policy for the decision owner;
- limitations or missing validation are stated.

You may not claim tests passed, behavior was verified, or the change is safe unless the evidence exists in the current session.

## References

- `references/pragmatic-review-rubric.md`: compact review rubric and severity guide.
- `references/linus-role.md`: background principles only. Do not copy persona language into user-facing output.
- `references/plan-vs-diff-routing.md`: how to choose between plan review and diff review.
- `references/data-model-invariants.md`: stricter data structure and ownership review guide.
- `references/examples.md`: example outputs and anti-patterns.

## Scripts

- `scripts/validate-pragmatic-review.py`: optional shape checker for saved strict pragmatic review reports.

## Optional ratchet signals compatibility

When a meta workflow such as `dbx-code-ratchet` explicitly requests ratchet-compatible strict signals, append a fenced `ratchet_signals` JSON block after the normal strict pragmatic review.

This block is optional for ordinary strict review. It should not replace blunt human-readable judgment.

The block provides direction and complexity signals, not final ratchet decisions. `dbx-code-ratchet` still performs triage, direction gate, repair contract, progress gate, and final stop/pass decisions.

Use `references/ratchet-signals.md` for the schema.

For `direction_health`:

- `ok`: local repair is probably appropriate.
- `suspect`: local repair may work, but direction or complexity deserves gate scrutiny.
- `failed`: continuing local repair is likely to make the code worse.
