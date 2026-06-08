---
name: dbx-code-ratchet
description: >
  Manual-only bounded code ratchet for concrete code changes. Use when the user explicitly asks to run code ratchet, 棘轮自修, 棘轮实现, review-repair-revalidation, or L2 ratchet on staged changes, working-tree diffs, selected files, commit ranges, or pasted patches. This skill may modify code. It orchestrates existing review and repair skills, triages findings, blocks direction failures, applies only bounded local repairs, validates, and stops with a pass or escalation report. Do not use for read-only review, open-ended implementation, product planning, background automation, or Ralph-style PRD completion loops.
---
# DBX Code Ratchet

代码棘轮是一个可修改代码的 meta skill。它不替代 `dbx-diff-review` 或 `dbx-linus-review`，而是调度它们，然后控制一个有界的 review -> triage -> repair -> validation -> re-review 循环。

核心目标不是清空所有 finding，而是在明确边界内让当前改动的风险单调下降。风险不下降、复杂度膨胀、方向可疑时，棘轮必须停下来。

默认输出语言是中文，除非用户要求其他语言。

## Position

Use this skill as a workflow controller:

- Review knowledge belongs to reviewer skills.
- Repair knowledge belongs to implementer or repair workers.
- Convergence knowledge belongs to this skill.

This skill decides whether to continue, stop, defer, escalate, or recommend rollback. It should not duplicate the full rubric of existing review skills.

## Activation

Use this skill only when the user explicitly asks for one of these:

- “跑代码棘轮”, “跑 code ratchet”, “棘轮自修”, “棘轮实现”。
- “对 staged changes 跑 L2 棘轮”。
- “review 出问题后自动修，再 re-review”。
- “对这个 diff 做有界 review-repair-revalidation”。
- “用现有 diff review / Linus review 做自动修复闭环”。

Do not use this skill for:

- Ordinary read-only review. Use `dbx-diff-review`.
- Explicit strict/pragmatic review without repair. Use `dbx-linus-review`.
- Open-ended feature implementation from requirements. Use the relevant implementation workflow.
- Ralph-style autonomous PRD/story completion loops.
- Commit, push, release, issue closing, or background work.
- Any request where the user says “只 review”, “不要改代码”, “你自己看不要搞复杂”, or “不要开 subagent”。

If the user asks for code ratchet but also says no code modification, run gate-only mode and do not edit files.

## Host and model policy

This first version is Codex-first.

When Codex subagents are available and the user has not disabled them:

- Use independent reviewer subagents with `fork_context=false`.
- Give each reviewer a compact task brief, not the parent thread.
- Do not leak one reviewer’s conclusion into another independent reviewer.
- Use the strongest available model and highest practical reasoning level for controller, reviewers, repair worker, and re-review.
- Do not hard-code a model version in this skill. Let Codex and the user’s current configuration select the concrete model.
- Do not downgrade critical review, direction gate, triage, repair, or re-review unless the user explicitly asks for lower cost or lower reasoning.

If subagents are unavailable, run the roles sequentially in the current session, but preserve role boundaries and state that subagent isolation was not used if that matters to the result.

## Default L2 profile

The default profile is L2 safe automation:

```yaml
profile: l2_safe_default
max_full_review_rounds: 1
max_repair_rounds: 2
max_re_review_rounds: 2
max_same_finding_attempts: 1
commit_changes: false
push_changes: false
complete_software_task: false
full_review_after_repair: false
```

A “round” means an automatic repair attempt. The initial full review is not a repair round. Re-review after repair must check only accepted findings and directly related regressions.

Do not switch to more rounds unless the user explicitly requests it and the progress gate says risk is decreasing.

## Hard gates before starting

Before reading deeply or editing code, establish:

```yaml
ratchet_target:
  source: pasted_patch | pr | branch | staged | unstaged | local | commit | commit_range | selected_files
  base: ""
  head: ""
  included_files: []
  selected_files: []
  context_files_read: []
  out_of_scope_dirty_files: []
  partial_out_of_scope_files: []
  target_assumption: ""
```

Required gates:

1. A concrete target exists or can be safely inferred from explicit user wording.
2. The user explicitly requested code ratchet or automatic review-repair. This skill may modify code.
3. The selected target is bounded enough to avoid reviewing the whole repository by accident.
4. Staged, unstaged, untracked, selected-file, and commit-range boundaries are disclosed when relevant.
5. Existing dirty files outside the target are not touched.
6. No commit, push, release, destructive migration, or issue closure is performed.
7. Tests, builds, type checks, or manual checks are never claimed as passed unless actually run or observed in this session.

If a target is missing, ask for the smallest missing input. If the user clearly says “staged”, prefer staged/index diff.

## Collaborator skills

Default collaborators:

- `dbx-diff-review`: primary concrete diff reviewer and re-reviewer.
- `dbx-linus-review`: optional strict direction, data-model, state-owner, compatibility, and over-engineering reviewer.
- `dbx-subagent-context`: Codex subagent context isolation helper when delegation is used.

Selection rules:

```yaml
collaborator_priority:
  1: explicit_user_instruction
  2: project_or_repo_ratchet_config
  3: references/default-policy.yaml
  4: this_skill_default
```

Use `dbx-diff-review` for the initial full review by default. Trigger `dbx-linus-review` when any of these are true:

- Multiple findings point to the same root cause.
- A finding mentions wrong state owner, wrong identity boundary, wrong data model, duplicated source of truth, compatibility break, or patching over a bad representation.
- The diff adds a shared abstraction, cache, global mutable state, public API, schema, migration, dependency, new config flag, or broad module move.
- Complexity budget is exceeded or unclear.
- The user explicitly asks for strict, Linus-style, pragmatic, over-engineering, merge-risk, or direction review.

Ask reviewer skills for normal human-readable output. When invoked by this skill, also request an optional ratchet-compatible `ratchet_signals` block if practical. Do not require strict JSON when it would make a small review noisy.

## Workflow

### 1. Snapshot

Collect a safe snapshot before modifying anything:

- `git status --short` when available.
- selected diff target and diff stat.
- staged versus unstaged separation when relevant.
- current validation hints from package manifests, project docs, CI, or existing scripts.

Do not run expensive or destructive commands without clear project evidence.

### 2. Deterministic pre-checks

Run only safe, relevant commands when project evidence supports them, such as typecheck, unit tests for touched area, lint, build, or focused test commands. Record `passed`, `failed`, `not_run`, or `unavailable`. Never invent green status.

### 3. Primary review

Invoke `dbx-diff-review` on the exact target. Use `standard` unless the diff is tiny, high-risk, or the user requests another mode.

The review should produce evidence-rich findings. If asked for ratchet compatibility, include signals, not final auto-fix decisions.

### 4. Normalize findings

Normalize findings into this shape:

```yaml
finding:
  id: F-001
  source_skill: dbx-diff-review | dbx-linus-review | third_party | manual
  severity: S0 | S1 | S2 | S3
  category: correctness | state_ownership | data_model | compatibility | maintainability | validation_gap | complexity | scope_drift | security | performance | other
  title: ""
  evidence: ""
  impact: ""
  fix_direction: ""
  confidence: high | medium | low
  introduced_by_current_diff: true | false | unknown
  local_fixable_signal: true | false | unknown
  direction_symptom_signal: true | false | unknown
  scope_expansion_required_signal: true | false | unknown
  human_decision_required_signal: true | false | unknown
  verification_hint: ""
```

Use `scripts/normalize-findings.py` for saved review reports when useful. If parsing from Markdown is lossy, lower parse confidence and do not over-trust inferred fields.

### 5. Finding gate

Classify every finding:

```yaml
triage_status:
  - auto_fix
  - defer_not_worth
  - reject_false_positive
  - escalate_human_decision
  - direction_failure
  - rollback_recommended
```

Default `auto_fix` only when all are true:

- S0/S1, or high-value S2 correctness, compatibility, state ownership, invariant, or validation gap.
- Evidence and impact are concrete.
- It is introduced or materially worsened by the current target.
- The smallest fix is local.
- No new dependency, public API change, persisted schema change, migration, architecture layer, broad module move, or product decision is required.

Default `defer_not_worth` for S3, low-confidence speculation, taste-only comments, generic “add tests” without an invariant, or improvements that are real but not worth this ratchet.

Default `reject_false_positive` for unsupported, pre-existing, out-of-target, or contradicted findings.

Default `escalate_human_decision` for product semantics, architecture direction, compatibility policy, migration strategy, public API, dependency, or cross-module ownership decisions.

### 6. Direction gate

Before any repair, decide whether the current implementation direction is still worth local repair.

Stop with `stopped-direction-failure` when any are true:

- Multiple findings are symptoms of the same wrong data model, state owner, identity boundary, source of truth, cache lifetime, or compatibility boundary.
- Fix directions require growing branches, adapters, caches, flags, synchronization, or special cases instead of removing the root cause.
- `dbx-linus-review` says the model is wrong, the solution is overbuilt, or local repair is not recommended.
- The smallest local repair no longer looks small.
- Repair would require crossing a hard gate.

Do not treat a direction finding as a todo list. It is a stop sign.

### 7. Repair contract

Generate a closed-world repair contract for exactly the accepted findings:

```yaml
repair_contract:
  accepted_findings: []
  forbidden_findings: []
  allowed_files: []
  forbidden_files: []
  allowed_change_types: []
  forbidden_change_types:
    - new_dependency_without_user_approval
    - public_api_change_without_user_approval
    - schema_or_migration_without_user_approval
    - unrelated_cleanup
    - deferred_finding_fix
    - test_deletion_or_weakening
    - broad_refactor
  stop_if_minimal_fix_not_possible: true
```

Give the repair worker only the accepted findings, constraints, target summary, and validation hints. Do not give it deferred findings as inspiration fuel.

### 8. Repair

Use exactly one writer at a time. Repair may run in a Codex subagent or in the current session, but it must be sequential.

The worker may modify code only to satisfy the repair contract. If it needs to expand scope, it must stop and return an escalation instead of editing around the boundary.

### 9. Validation after repair

Run relevant deterministic checks again when possible. Record what was run and what was not run. If a check fails, decide whether the failure is a direct accepted finding, direct repair regression, or unrelated existing failure.

### 10. Scoped re-review

Use `dbx-diff-review` in `re-review` mode.

Re-review scope:

- Are accepted findings fixed?
- Did the repair introduce directly related regressions?
- Did a new S0/S1 blocker appear?
- Did a direction failure appear?

Do not restart a full review. Do not open a nit hunt. New S2/S3 findings that are not direct regressions should be deferred unless they reveal a direction failure.

### 11. Progress gate

After every repair round, compute whether the ratchet moved forward:

```yaml
progress_gate:
  risk_score_decreased: true | false
  accepted_open_findings_decreased: true | false
  new_s0_or_s1: true | false
  complexity_budget_exceeded: true | false
  validation_worse: true | false
  scope_expanded: true | false
  direction_health: ok | suspect | failed
```

Risk score weights:

```yaml
S0: 100
S1: 25
S2: 5
S3: 1
```

Stop unless all are true:

- Risk score decreased or all accepted findings are closed.
- No new S0/S1 appeared.
- Complexity did not materially increase.
- Scope did not expand beyond the repair contract.
- Validation did not get worse.
- Direction health is not failed.

Use `scripts/score-ratchet-progress.py` when saved findings are available.

## Complexity budget

Use this budget as a gate, not a pseudo-precise metric:

```yaml
complexity_budget:
  allow_new_dependency: false
  allow_public_api_change: false
  allow_schema_or_migration: false
  allow_unrelated_cleanup: false
  max_new_files: 2
  max_loc_growth_ratio: 0.25
  watch_signals:
    - new exported symbols
    - new shared abstractions
    - new cache or state owner
    - new config or feature flag
    - new adapter layer
    - broad module move
    - one-implementation interface
    - performance optimization without evidence
```

Local simplification can be auto-fixed. New architecture direction must escalate.

## Stop states

Use these final states:

- `pass-ready`: validation and scoped re-review support that accepted findings are fixed and residual risk is disclosed.
- `needs-human-decision`: continuing requires product, architecture, compatibility, dependency, schema, migration, or scope judgment.
- `stopped-direction-failure`: findings indicate the current implementation direction is likely wrong.
- `stopped-diverging`: repair made risk, complexity, or validation worse.
- `stopped-validation-failed`: checks failed and safe local repair is not allowed or not enough.
- `stopped-scope-unsafe`: target, dirty state, or repair boundary is unsafe.

`pass-ready` is not the same as “safe to deploy” unless the relevant evidence exists.

## Output contract

Use this shape:

```markdown
## 代码棘轮结果

结论：pass-ready / needs-human-decision / stopped-direction-failure / stopped-diverging / stopped-validation-failed / stopped-scope-unsafe

目标：
- 来源：staged / unstaged / local / branch / commit-range / selected-files / pasted patch
- 范围：...
- 未纳入范围：...

轮次：
- full review: 1 / 1
- repair rounds: 0-2 / 2
- re-review rounds: 0-2 / 2
- subagents: used / not used, fork_context=false where used

风险变化：
- before: S0=?, S1=?, S2=?, S3=?, risk_score=?
- after: S0=?, S1=?, S2=?, S3=?, risk_score=?
- complexity: within budget / exceeded / not measured

已自动修复：
1. F-001 [S1 correctness] ...

未自动修复：
1. F-004 [direction_failure] ...
2. F-005 [defer_not_worth] ...

方向判断：
- 当前方向：ok / suspect / failed
- 证据：...

验证：
- typecheck: passed / failed / not_run / unavailable
- tests: passed / failed / not_run / unavailable
- lint/build/manual: ...

需要你判断：
- ...
```

Keep the final report compact. The user should read the gate result, not a dump truck of internal logs.

## Completion policy

You may say the ratchet run is complete only when:

- The target contract was established.
- Existing reviewer skills or explicit review roles inspected the selected target.
- Findings were triaged through finding, direction, and progress gates.
- Any repair was bounded by a repair contract.
- Re-review was scoped to accepted findings and direct regressions.
- Validation status is explicit, including not-run checks.
- The final state is one of the defined stop states.

You may not say all issues are fixed unless accepted findings are closed and deferred or rejected findings are disclosed.

## References

- `references/default-policy.yaml`: default L2 profile, collaborators, gates, and budgets.
- `references/collaborator-adapters.md`: how to compose existing DBX review skills and Codex subagents.
- `references/ratchet-signals-schema.md`: optional reviewer output block for machine-readable signals.
- `references/direction-gate.md`: direction-failure and diverging-loop rules.
- `references/output-contract.md`: final report and state examples.
- `references/examples.md`: example pass, direction failure, and diverging outputs.

## Scripts

- `scripts/normalize-findings.py`: extract optional `ratchet_signals` JSON or fallback severity findings from review Markdown.
- `scripts/score-ratchet-progress.py`: compute before/after risk score and gate hints from normalized findings.
- `scripts/validate-ratchet-state.py`: validate saved ratchet state JSON.
