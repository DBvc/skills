---
name: dbx-diff-review-control
description: High-signal code change review controller for PRs, patches, staged/index changes, working-tree diffs, commit ranges, and file-scoped review. Use when the user asks to review concrete code changes for functional/user-impact risks, data model correctness, state ownership, compatibility, or maintainability. Handles partial staged hunks and user-selected files/commits by selecting the exact review target before reading the diff. Do not use for implementation-only requests, generic code explanation, release publishing, issue triage, or plan-only Linus-style strict-pragmatic critique; for strict critique of a concrete diff, use this skill only to establish the target before dbx-linus-review.
---
# DBX Diff Review Control

Review concrete code changes as a scoped control loop, not as a generic checklist. The priority is high-signal findings that can affect users, break functionality, corrupt data/state, violate contracts, or make the code materially harder to reason about.

Default output language is Chinese unless the user requests otherwise. Be direct, technical, and evidence-first. Do not perform persona theater. Do not insult authors.

## Relationship to `dbx-linus-review`

These two skills share a strict engineering substrate: real problems, correct data structures, clear ownership, compatibility, and practical simplicity.

They are different controllers:

- `dbx-diff-review-control` is for concrete change-set review. It first selects the exact target: PR, branch diff, staged diff, working tree, commit range, selected files, or pasted patch.
- `dbx-linus-review` is for strict pragmatic judgment across diffs, architecture plans, and implementation proposals, especially when the user asks whether something is good enough, over-engineered, dangerously modeled, or worth doing.

If the user explicitly asks for Linus-style, harsh, strict-pragmatic, or architecture/方案 critique without a concrete diff target, prefer `dbx-linus-review`. If the user asks for strict critique of a concrete diff with target ambiguity, use this skill first to establish the target, then apply `dbx-linus-review`. If the user asks for ordinary PR/diff review, merge readiness, or selected-file/commit review, use this skill.

## Routing

Use this skill for:

- PR, patch, branch, commit-range, staged/index, unstaged, local working-tree, or pasted diff review.
- User-selected file review: “只看这几个文件”, “review these files”, “看 src/a.ts 和 src/b.ts”.
- User-selected commit review: “review commits A..B”, “看最近 3 个 commit”, “只看这个 commit”.
- Merge readiness checks focused on correctness, user impact, data model, state ownership, compatibility, regression risk, or maintainability.
- Frontend and full-stack changes where state ownership, async behavior, API contracts, persisted data, or UX flow correctness matter.
- Re-review after a previous review when the user asks whether findings were fixed.

Do not use this skill for:

- Direct implementation without review.
- Generic explanation of code behavior.
- Architecture or plan critique without a concrete code-change target, unless the user clearly wants diff-like risk review of a concrete proposal.
- Plan-only Linus-style, harsh, strict-pragmatic, or “is this good enough?” critique. Route to `dbx-linus-review`. For strict critique of a concrete diff, use this skill only for target selection when staged/unstaged/branch/file scope is ambiguous.
- Commit or PR writing. If review and PR writing are both requested, run this review first, then hand off to the appropriate commit/PR skill.
- Release, publish, push, issue closure, or GitHub triage workflows.

## Hard gates

Before producing findings, check these gates:

1. Artifact exists: diff, PR, patch, staged/index changes, working tree changes, commit range, selected files, or code snippet.
2. Target is selected: review exactly the change set the user intends, not “whatever git diff happens to show”.
3. Scope is bounded: review target and non-goals are clear enough to avoid reviewing the entire repository.
4. Evidence is possible: each finding can point to a changed file, function, line range, data path, public contract, user flow, or test/validation gap.
5. Review mode is selected: quick, standard, deep, focused, or re-review.

If artifact or target is missing, ask for the smallest missing input. If the likely target can be inferred from explicit wording, proceed and state the assumption. Do not invent findings from vibes.

## Target selection gate

Always select the review target before collecting or reading diffs. This is the main guard against reviewing the wrong files.

Priority order:

1. **Explicit pasted diff / patch**: use the supplied artifact. Do not inspect unrelated local changes unless the user asks.
2. **Explicit PR / branch / base**: review the PR or `base...head` branch diff.
3. **Explicit commit / commit range**: review only the named commit(s) or range.
4. **Explicit files**: review only the selected files within the selected source (`staged`, `local`, `branch`, or pasted artifact). Read neighboring files only as context and label them as context, not reviewed targets.
5. **Commit-ready / “要提交” / “只提交这些”**: prefer the staged/index diff (`git diff --cached`). This correctly handles partial staged hunks inside a file.
6. **Current changes / working tree**: review local changes. If both staged and unstaged exist, separate them and state whether both are in scope.
7. **No target evidence**: ask whether to review staged changes, working-tree changes, a branch diff, or specific files/commits.

When working in a repo, use `scripts/collect-review-context.py` with an explicit target when possible:

```bash
python3 skills/dbx-diff-review-control/scripts/collect-review-context.py --root . --target staged
python3 skills/dbx-diff-review-control/scripts/collect-review-context.py --root . --target branch --base origin/main
python3 skills/dbx-diff-review-control/scripts/collect-review-context.py --root . --target files --file-scope staged --files src/a.ts src/b.ts
python3 skills/dbx-diff-review-control/scripts/collect-review-context.py --root . --target commit-range --commit-range main..HEAD
```

The script is read-only. It does not run tests or modify files.

### Target contract

Build this internal target contract and print it when ambiguity or dirty state matters:

```yaml
review_target:
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

Rules:

- If reviewing staged/index changes, unstaged and untracked files are out of scope unless the user includes them.
- If the same file has staged target hunks and unstaged hunks, disclose the unstaged hunks as partial out-of-scope work.
- If reviewing selected files, other changed files are out of scope even if they are dirty. Mention them only if they affect interpretation or are dangerous to ignore.
- If reviewing commits, uncommitted local changes are out of scope unless the user asks to include them.
- If context files are inspected, do not turn pre-existing issues in those files into findings unless the diff materially worsens them.

See `references/target-selection-and-scope.md` for examples.

## Review modes

Choose the smallest mode that fits the request and risk.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `quick` | Small diff, user asks for obvious issues only | Find S0/S1 correctness, security, compatibility, and data-loss risks. Suppress low-value maintainability comments. |
| `standard` | Default PR/diff review | Review user impact, data model, invariants, maintainability, contracts, and validation. |
| `deep` | Large diff or high-risk area | Add specialist passes and adversarial verification. Use for auth, payments, migrations, persisted data, permissions, cross-service APIs, or core state models. |
| `focused` | User names a focus area | Keep findings inside the requested focus unless another issue is an S0/S1 blocker. |
| `re-review` | User asks whether prior findings were fixed | Check only prior findings and directly related regressions. Do not restart a nit hunt. |

Depth defaults:

- `quick`: under 100 changed lines and 1 to 5 files, no high-risk surfaces.
- `standard`: 100 to 500 changed lines, 6 to 10 files, or normal feature work.
- `deep`: over 500 changed lines, over 10 files, or any high-risk surface: auth, permissions, payments, data mutation, migrations, persisted schema, destructive operations, external integrations, cache/state model rewrites, public API changes.

## Evidence collection

Prefer direct evidence over conversational memory.

1. Select target with the target selection gate.
2. Read the supplied diff or collect local context using the explicit target.
3. Inspect changed files and surrounding code needed to understand changed behavior.
4. Read project rules only when relevant: `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, README, package manifests, schemas, test config, CI workflows, architecture notes, generated-code rules.
5. Do not read secrets, private local paths, raw chat transcripts, unrelated personal files, or credentials.
6. Never claim that tests, type checks, builds, or manual checks passed unless the command or observation happened in the current review session.

## Change model

Before listing findings, build this internal model. Print only the useful parts.

```yaml
change_model:
  stated_goal: ""
  actual_diff_goal: ""
  changed_user_paths: []
  core_entities: []
  state_owners: []
  new_artifacts: []
  module_owners: []
  path_fit_evidence: []
  important_invariants: []
  public_contracts_changed: []
  persisted_data_or_schema_changed: []
  async_or_concurrency_surfaces: []
  validation_surface: []
  highest_risk_surface: ""
```

A good review understands what the code is trying to protect before judging the syntax.

## Review passes

Run these passes in order. The files in `agents/` are optional specialist pass prompts, not a requirement to delegate. Use them with subagents only when the host supports delegation and the user has explicitly allowed multi-agent review; otherwise run the same passes sequentially in the current session.

1. **Intent and scope drift pass**
   - Does the selected change set implement the stated goal?
   - Are there unrelated abstractions, dependencies, state, or behavior changes inside the selected target?
   - Did it partially fix a class of bug while leaving equivalent selected-target instances unfixed?
   - If sibling instances outside the selected target look relevant, label them as out-of-scope follow-up unless they make the selected diff unsafe.

2. **User-impact correctness pass**
   - Which real user flows change?
   - What can break in production, not just in theory?
   - Consider empty states, retries, partial failure, logout/login, user switching, permission downgrade, stale data, double submit, navigation, refresh, hydration, offline/slow network, and rollback.

3. **Data model and invariant pass**
   - Identify core entities, identifiers, lifetimes, ownership boundaries, normalization/denormalization, derived state, cache keys, and schema mappings.
   - Ask whether new branches are real domain rules or patches over a bad representation.
   - Wrong data structure, wrong identity boundary, or wrong state owner should outrank style issues.

4. **New artifact ownership pass**
   - For new or moved source/config/test/doc files, check the intended owner, nearest existing module, and project-rule evidence for the chosen path.
   - Treat paths supplied by the prompt, plan, or handoff as target evidence, not as approval.
   - Flag placement only when it creates a wrong source of truth, unnecessary shared/public surface, hidden coupling, or real future change-cost risk.

5. **Contract and compatibility pass**
   - Check public APIs, exported types, props, configs, CLI behavior, persisted data, database migrations, route contracts, analytics events, feature flags, and backwards compatibility.
   - Never dismiss user breakage because the new design is cleaner.

6. **Maintainability pass**
   - Look for unnecessary concepts, leaky abstractions, hidden coupling, mixed responsibilities, duplicated sources of truth, and changes that make future fixes harder.
   - Flag only maintainability issues with a concrete future bug path or change-cost impact.

7. **Validation pass**
   - Check tests, type safety, lint/build coverage, regression tests, and manual verification gaps.
   - A missing test is a finding only when it leaves an important changed invariant unprotected.

8. **Verifier pass**
   - Try to disprove each candidate finding before reporting it.
   - Keep a finding only if it is introduced or materially worsened by the selected change set, has concrete evidence, has user or maintainability impact, and has a specific fix direction.

## Finding filter

Suppress findings that are:

- Pure style, naming, formatting, or taste unless they hide correctness or model risk.
- Already enforced by obvious lint/type checks and not useful to mention.
- Pre-existing and not worsened by the selected change set.
- Outside the selected review target, unless needed to explain why the selected target is unsafe.
- Low-confidence speculation without a code path, data path, or user path.
- Generic “add more tests” without naming the unprotected invariant.
- “Rewrite everything” without proving why a local fix cannot work.

Prefer 1 to 5 high-signal findings over a wall of minor comments.

## Severity

Use this severity scale. See `references/severity-and-evidence.md` for calibration.

- `[S0 blocker]`: likely data loss, security exposure, production outage, irreversible user harm, hard compatibility break, or unsafe migration/release path.
- `[S1 high]`: likely functional regression in an important user flow, wrong data ownership/model, broken invariant, auth/permission mistake, severe performance cliff, or unsafe integration behavior.
- `[S2 medium]`: real but bounded correctness or maintainability risk; unnecessary complexity likely to cause future bugs; incomplete validation of important behavior.
- `[S3 low]`: small cleanup, clarity, local simplification, or test clarity. Report sparingly.

Severity requires impact. Confidence requires evidence.

## Output contract

Use this shape by default. Omit sections that do not apply, but keep evidence inside each finding.

```markdown
## 核心判断
- 结论：可以合并 / 需要修改后合并 / 不建议合并 / 信息不足
- 主要风险：一句话说明最高风险
- Review 模式：quick / standard / deep / focused / re-review

## Review 目标
- 来源：staged / unstaged / local / branch / commit-range / selected-files / pasted patch / PR
- 范围：...
- 未纳入范围：...
- 假设：...

## 变更理解
- 目标：...
- 实际改动：...
- 关键数据/状态模型：...
- 用户影响面：...

## 主要发现
1. [S1 high] 标题
   - Evidence: 指向具体文件、函数、diff 行为、数据路径或用户路径
   - Impact: 会影响谁、在什么条件下出错、为什么重要
   - Fix: 最小可行修复方向
   - Confidence: high / medium / low
   - Verification: 已验证什么；未运行什么；还需要什么

## 数据结构和模型判断
- 哪些实体、状态 owner、生命周期或不变量是对的
- 哪些地方模型不稳，为什么会带来分支、缓存、同步或兼容性问题

## 可维护性判断
- 保留有明确后果的结构性评价
- 不写泛泛的“代码不够优雅”

## 验证建议
- Automated: 具体命令或测试建议
- Manual: 具体用户路径
- Not run: 当前没有运行或无法确认的验证

## 残余风险
- 合并后仍需要观察或补充的信息
```

If there are no major findings, say so directly:

```markdown
## 核心判断
未发现需要阻止合并的问题。

## Review 目标
...

## 残余风险
...

## 验证建议
...
```

Do not pad the answer with fake rigor. If the review is small, keep it small.

## Completion policy

You may say the review is complete when:

- The selected target was inspected.
- Any out-of-scope dirty files or excluded commits/files were disclosed when relevant.
- The change model was formed enough to judge user impact and data/model risks.
- Candidate findings were filtered through the verifier pass.
- Output includes evidence, impact, fix direction, confidence, and validation status for every finding.

You may not say the change is safe, verified, tested, ready, or green unless the relevant evidence exists in the current session. Use `Not run` or `未验证` for missing checks.

## References

- `references/target-selection-and-scope.md`: exact review target selection, staged subsets, selected files, commit ranges, and dirty-state disclosure.
- `references/severity-and-evidence.md`: severity calibration and evidence rules.
- `references/data-model-invariants.md`: data structure, ownership, and invariant review guide.
- `references/risk-surfaces.md`: frontend, backend, API, data, security, and integration risk surfaces.
- `references/reviewer-passes.md`: specialist pass protocol and verifier behavior.
- `references/examples.md`: example high-signal findings and anti-patterns.

## Scripts

- `scripts/collect-review-context.py`: safe local context collector with explicit target modes. It reads git/package metadata and suggests validation commands. It does not run project commands.
- `scripts/validate-review-report.py`: optional report sanity checker for saved Markdown review reports.

## Optional ratchet signals compatibility

When a meta workflow such as `dbx-code-ratchet` explicitly requests ratchet-compatible output, append a fenced `ratchet_signals` JSON block after the normal human-readable review.

This block is optional for ordinary review. Do not make normal PR review noisy.

The block provides signals, not decisions. `dbx-code-ratchet` still performs triage, direction gate, repair contract, progress gate, and final stop/pass decisions.

Use `references/ratchet-signals.md` for the schema. Prefer `unknown` or omission over fake certainty.

Important fields:

- `local_fixable_signal`: local bounded repair appears plausible.
- `direction_symptom_signal`: finding may indicate wrong model, state owner, identity boundary, source of truth, or cache lifetime.
- `scope_expansion_required_signal`: likely fix crosses API, schema, dependency, architecture, or module ownership boundaries.
- `human_decision_required_signal`: likely fix needs user, product, architecture, compatibility, or migration judgment.
