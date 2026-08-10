---
name: dbx-software-plan-first-finalize-plan
description: Manual trigger only. Use only when the user explicitly names `dbx-software-plan-first-finalize-plan`, `$dbx-software-plan-first-finalize-plan`, or asks to manually trigger this exact DBX Software Plan-First plan finalization phase. Do not auto-trigger for ordinary plan writing, finalize, seal, or implementation requests.
---

# DBX Software Plan-First Finalize Plan

## DBX repository notes

- This repository uses the `dbx-` prefix for stable skills; use the prefixed skill names in handoffs and cross-skill routing.
- Keep this phase self-contained: load only the required references for the active phase, and do not pull sibling skill files unless the workflow explicitly hands off to that phase.

## Manual Trigger

- Manual trigger only.
- Use only when the user explicitly names `dbx-software-plan-first-finalize-plan`, `$dbx-software-plan-first-finalize-plan`, or says to use/trigger this exact skill.
- Do not auto-trigger for ordinary plan writing, `plan.md/tasks.md`, finalize, seal, or plan-first requests.

用于把已经收敛的计划写入过程产物，并建立 workflow seal。

## 语义

- 只能在 Goal、Scope、Approach、Validation、Plan Strategy、Impact Profile、Impact Boundary 已完整时使用。
- 如果需要仓库事实但尚未 grounding，先交给 `dbx-software-plan-first-ground-plan`。
- 如果当前调用来自已选择 DBX implementation-bound planning profile 的父 workflow，`plan.md` 与 `tasks.md` 的精确文件 bundle 是最终 acceptance artifact：现有决策与 grounding 门满足后可以先物化文件，但只有 current `ready-for-handoff` 与 qualifying `strict_acceptance_receipt` 都绑定该 bundle identity 时才可 seal。
- 如果用户直接显式调用本 skill，且明确确认当前计划已经收敛，现有 Mandatory Decision Gate、grounding、ownership、validation 和 artifact boundary 全部满足，则不强制制造新的 convergence run。
- 如果计划会新增、移动或固定 source/config/test/doc 产物，产物归属必须已经由项目事实或用户确认支持；归属未定时不要 seal，先返回 grounding 或澄清。
- 写入中文 `plan.md` 和 `tasks.md`。
- 运行 `scripts/issue-workflow.sh seal <issue-id>` 建立 seal。
- 计划过程产物固定写入 `.plan-first/issues/<issue-id>/`，不作为提交产物；若 `.plan-first/config.toml` 显式配置 `plan_docs.mode = "tracked"`，只提交同步到项目文档路径的 `plan.md` 和 `tasks.md` 副本。
- 是否自动提交以及提交格式由 `.plan-first/config.toml` 控制。

## 必须读取

- `references/workflow-rules.md`
- `references/plan-template.md`
- `references/tasks-template.md`
- `references/config.md`
- `references/impact-profiles.md`
- `references/artifact-evidence-boundary.md`

## 工作流

1. 先区分首次物化与 selected-profile resume。Selected profile 只要已有未 seal 的 `plan.md/tasks.md`，无论 receipt 缺失、stale、属于 proposal 还是有效，都禁止运行 `init`、禁止重填或改写文件，直接进入第 5 步做只读 identity 校验；只读路径也不得创建或改写 `.git/info/exclude`。只有 bundle 尚不存在时才走首次物化路径。
2. 首次物化或 direct/manual 路径运行：

```sh
scripts/issue-workflow.sh init <issue-id>
```

3. 用中文填写 `plan.md` 和 `tasks.md`。
4. 确认 `tasks.md` 每个任务包含：`验收:`、`验证:`，以及必要的 `使用检查:`、`依赖:`、`约束:`。会新增或迁移产物的任务，必须在 `约束:` 中写明产物归属、依据和禁止误放的边界。
5. 运行 `scripts/issue-workflow.sh bundle-fingerprint <issue-id>`，以只读方式取得 `scheme: plan-first-bundle-sha256-v1`、两个 exact file hash 和 bundle fingerprint。Bundle version 固定为 `plan-first-<issue-id>-bundle-<fingerprint 前 12 位 hex>`。
6. 对 selected profile 校验 `completion_profile: strict_acceptance`、`ready-for-handoff` 和 receipt 是否绑定第 5 步的同一 bundle type/scheme/version/fingerprint 及同一 plan/tasks refs，且 receipt 为 `passed`、`reviewer_capability` 与 handoff 的 provider binding 相同、`scope: full`、`independence: independent`、`reviewed_after_last_revision: true`、`open_blocker_high: 0`、judgment 为 `accept` 或 `accept_with_advisories`。没有 qualifying receipt 时保持文件未 seal，输出下列**完整 delegated activation envelope**给 external `dbx-plan-convergence`；parent 必须转发该 envelope，不能把旧 proposal artifact identity 合并回来。

```yaml
plan_bundle_handoff:
  originating_intent: ""
  requested_mode: bounded_loop
  status: needs_plan_convergence
  completion_profile: strict_acceptance
  artifact:
    type: implementation_plan_bundle
    version: ""
    fingerprint_scheme: plan-first-bundle-sha256-v1
    fingerprint: ""
    content_ref:
      kind: file_bundle
      value: null
      plan: .plan-first/issues/<issue-id>/plan.md
      tasks: .plan-first/issues/<issue-id>/tasks.md
  scope: []
  goal: ""
  non_goals: []
  success_criteria: []
  evidence_boundary:
    repo_facts_read: []
    user_supplied_facts: []
    assumptions: []
    unknowns: []
    not_read_or_not_run: []
  risk_profile: standard | high_impact | irreversible
  provider_bindings:
    reviewers:
      - id: dbx-linus-review
        capability: strict_pragmatic_plan_review
    revision_provider:
      id: original_plan_author
    parent_workflow:
      id: ""
  budget:
    initial_full_review_passes: 1
    local_revision_rounds: 2
    scoped_re_review_passes: 2
    final_acceptance_full_review_passes: 2
  modification_authority: plan_text_only
  may_modify_code: false
```

输出前必须把 originating intent、version、fingerprint、file_bundle plan/tasks refs、scope、goal、evidence boundary 和 parent id 填成当前真实值；空值不是可消费 handoff。

7. Receipt 有效时，不再修改 `plan.md` 或 `tasks.md`。把 receipt 绑定的 scheme 和 fingerprint 交给同一次 `seal` 调用，由脚本在写 seal 前复算并原子拒绝 identity drift：

```sh
scripts/issue-workflow.sh \
  --expected-bundle-scheme plan-first-bundle-sha256-v1 \
  --expected-bundle-fingerprint <receipt-fingerprint> \
  seal <issue-id>
```

8. 报告 workspace root、计划文件位置、配置模式、任务数量、bundle fingerprint 和下一步执行命令。

## 禁止事项

- 不在决策不完整时写计划。
- 不在 selected profile 的 bundle receipt 缺失、stale、identity mismatch、fingerprint 无法重算或 qualification 不满足时 seal；缺 receipt 时只允许物化未 seal 的 plan bundle 并交给 external convergence。
- 不用 proposal receipt 为新生成的 `plan.md` / `tasks.md` bundle 签 seal。
- 不把项目特定规则写进通用 skill；只把本仓库 grounding 到的规则写进本 issue 计划。
- 不跳过 seal。
- 不在 finalize 阶段实现代码。

## 输出

用中文说明：workspace root、计划文件位置、任务数量、影响画像、验证模型、配置模式、bundle fingerprint、是否已 seal、下一步执行命令；等待严格验收时还要输出 `plan_bundle_handoff`。
