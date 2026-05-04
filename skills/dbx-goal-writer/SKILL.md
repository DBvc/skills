---
name: dbx-goal-writer
description: Use when the user wants to create, refine, start, or audit an OpenAI Codex goal contract for coding work, especially long-running or validation-heavy tasks. Produces copy-pasteable /goal commands, optional GOAL.md files, and only for large or strict tasks a goal package directory with plan, acceptance, validation, and status files. Do not implement the coding task unless explicitly asked.
---

# Goal Writer

Turn a rough coding request into a clear Codex `/goal` contract.

This skill is a goal foundry, not the implementation agent. While using it, do not edit the product code unless the user explicitly asks for implementation. Produce goal artifacts and the exact `/goal` command needed to start the run.

## Mental model

Treat `/goal` as a thread-level objective workflow, not a stable general-purpose CLI subcommand. In Codex CLI 0.128.0, OpenAI release notes describe persisted `/goal` workflows with app-server APIs, model tools, runtime continuation, and TUI controls for create, pause, resume, and clear. In current local builds, `goals` may still appear as an under-development feature flag, and official slash-command docs may lag behind the release surface.

Before making compatibility claims, use `references/codex-goal-compatibility.md`. When the user's environment is unknown, say that `/goal` is feature-gated or surface-dependent and should be verified with `codex --version`, `codex features list`, and the TUI slash popup.

A `/goal` can reference a file or directory path, but do not assume native `/goal --file` or `/goal --dir` flags. Do not invent pause/resume/clear slash syntax; point users to the local TUI controls or slash popup unless the current environment has been verified.

For file-based goals, always provide a copy-pasteable `/goal` command that tells Codex to read the referenced file or directory before editing code. Keep a short objective summary inside the command, not only the path.

## Activation examples

- `$dbx-goal-writer direct: 修复 checkout 优惠券空字符串校验问题`
- `$dbx-goal-writer file: 为 account 表单迁移到 zod 生成 GOAL.md`
- `$dbx-goal-writer package strict: 为 React 19 迁移生成完整 goal 目录`
- `$dbx-goal-writer start .codex/goals/account-zod/GOAL.md`
- `$dbx-goal-writer audit .codex/goals/account-zod/GOAL.md`

Preserve the user's language. If the user writes Chinese, write the goal and files in Chinese unless repository conventions clearly require English.

## Output modes

Choose the smallest mode that makes the task safe and reviewable.

### direct

Use for small or medium tasks where one command is enough.

Choose `direct` when the task is specific, scope is narrow, validation is simple, and no persistent plan/status file is needed.

Output:

1. `Mode: direct`
2. A copy-pasteable `/goal ...` command
3. A short readiness checklist
4. Blocking missing context only when necessary

### file

Use for medium tasks that need durable context but not a full directory.

Choose `file` when the task has several target files, meaningful constraints, important non-goals, or the user wants a reviewable contract before execution.

Default path for local/private goals:

```text
.codex/goals/<slug>/GOAL.md
```

Default path for team-reviewed/versioned goals:

```text
docs/codex-goals/<slug>/GOAL.md
```

Output:

1. `Mode: file`
2. Created or proposed `GOAL.md`
3. A copy-pasteable `/goal ...` command referencing the file
4. A short readiness checklist

### package

Use only for large, risky, long-running, strict, cross-cutting, migration, performance, security, benchmark, rollout, or multi-phase work.

Do not choose `package` merely because the request is a little ambiguous. When unsure between `file` and `package`, choose `file` and include open questions or pause conditions.

Recommended package tree:

```text
.codex/goals/<slug>/
  GOAL.md          # Goal contract and boundaries
  PLAN.md          # Milestones and sequencing
  ACCEPTANCE.md    # Completion and review contract
  VALIDATION.md    # Commands, manual checks, evidence
  STATUS.md        # Progress log for long runs
  scripts/validate.sh  # Optional; create only if commands are known and useful
```

Output:

1. `Mode: package`
2. Created or proposed package tree
3. A copy-pasteable `/goal ...` command referencing the directory or `GOAL.md`
4. How to run validation
5. A short readiness checklist

### start

Use when the user already has a `GOAL.md` or goal directory and wants the short command to activate it.

Input examples:

- `$dbx-goal-writer start .codex/goals/foo/GOAL.md`
- `$dbx-goal-writer start docs/codex-goals/react-19-migration/`

Output only the copy-pasteable `/goal ...` command plus one short note if the path looks suspicious.

Start command template:

```text
/goal Execute <short objective if known> according to <path>. Read the goal contract before editing code. Respect Scope, Non-goals, Constraints, Acceptance Criteria, Validation, Budget and Stop Rules, and Pause Conditions. Use STATUS.md for progress if present. Completion requires all required validation to pass, or a clear explanation of why a check could not be run.
```

### audit

Use when the user gives an existing `/goal`, `GOAL.md`, or goal package and asks whether it is clear enough.

Output:

1. `Verdict: ready | needs revision | unsafe | too broad`
2. Top issues by severity
3. Revised `/goal` or file patch
4. Blocking missing context only when necessary

## Mode selection defaults

- Use `direct` for one bug fix, one component change, one targeted test addition, or tasks under roughly 1 to 3 files.
- Use `file` for medium refactors, migrations limited to one feature area, or tasks where future review matters.
- Use `package` only for long-running, strict, multi-phase, cross-cutting, risky, or high-ambiguity work.
- If the user explicitly asks for a full package, create it. Otherwise avoid package sprawl.

## Goal contract schema

Every goal must contain these parts, inline or in files:

1. Objective: one sentence describing the outcome.
2. Context: current behavior, evidence, relevant files, examples, issue links, errors, or screenshots.
3. Target paths: likely directories or files to inspect or modify.
4. Scope: allowed changes.
5. Non-goals: explicitly out-of-scope changes.
6. Constraints: API compatibility, architecture, dependencies, style, security, performance, accessibility, release constraints.
7. Acceptance criteria: observable behavior and reviewable artifacts.
8. Validation: exact commands or manual checks.
9. Pause conditions: when Codex must stop and ask before continuing.
10. Budget and stop rules: token/time budget if known, and what Codex should do when the budget is reached or progress is blocked.
11. Reporting: final summary format.

## Quality rules

Reject or rewrite vague goals such as:

- 优化这个项目
- 重构所有代码
- 清理代码库
- Make it better
- Fix all bugs

A good goal answers:

- What changes?
- Where may Codex look or edit?
- What must not change?
- How will we know it is done?
- What commands prove it?
- What should happen when new risk appears?
- What should Codex do when the active goal budget is reached?

## Validation rules

Prefer commands already present in the repository:

- `package.json` scripts
- `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lockb`
- `Makefile`
- `pyproject.toml`
- `Cargo.toml`
- `go.mod`
- CI config

Do not invent project-specific commands confidently. If uncertain, mark commands as assumptions or TODOs.

For frontend repositories, common candidates are:

```text
pnpm test
pnpm typecheck
pnpm lint
pnpm build
```

Only include commands that likely exist, or explicitly label them as assumptions.

Create `scripts/validate.sh` only when:

- The task is package/strict, and
- The validation command sequence is known, and
- A script improves repeatability beyond listing commands in `VALIDATION.md`.

Do not place destructive commands in validation scripts unless explicitly authorized. Avoid deploy, production migration, database reset, lockfile deletion, secret rotation, or dependency installation commands unless the user requested them.

## Default pause conditions

Include these unless clearly irrelevant:

- Stop before changing public APIs or exported types beyond the agreed scope.
- Stop before adding new runtime dependencies.
- Stop before broad rewrites outside target paths.
- Stop before modifying lockfiles, generated files, migrations, or persisted data unless explicitly allowed.
- Stop if tests fail for reasons unrelated to the task and the cause is unclear.
- Stop if the implementation requires product, UX, security, or architecture decisions not specified in the goal.

## Budget and stop rules

For small direct goals, a budget can be omitted unless the user asks for one. For medium or large goals, include a clear stop rule:

- If a token or time budget is configured, stop starting new substantive work when the budget is reached.
- Summarize useful progress, remaining work, blockers, and the next concrete action.
- Do not claim completion merely because time, effort, or budget was spent.
- Mark the goal complete only when the current repository state satisfies every acceptance criterion and required validation is covered or honestly explained.

## Placement rules

For goal artifacts:

- Use `.codex/goals/<slug>/` for personal, local, temporary, or experiment-oriented goal contracts.
- Use `docs/codex-goals/<slug>/` for team-reviewed, versioned, PR-visible goal contracts.
- Use a feature-local path only when the goal is tightly scoped to a nested package or app, such as `apps/web/.codex/goals/<slug>/` in a monorepo.
- Avoid root-level `GOAL.md` unless the repository is dedicated to one task.
- Do not put one-off task goals in `AGENTS.md`. `AGENTS.md` is for durable repository instructions.

For skill installation:

- User scope: `$HOME/.agents/skills/dbx-goal-writer/`
- Repo scope: `<repo>/.agents/skills/dbx-goal-writer/`

## File creation behavior

If the user asks to create files, create them. Otherwise propose file contents in the response.

When creating files, prefer the smallest useful artifact:

- Direct command: no files.
- Single `GOAL.md`: one durable contract.
- Package: multiple files only for large or strict work.

If using the helper script, run it from the repository root or intended workspace root.

```bash
python <skill-path>/scripts/create_goal_artifact.py --title "<title>" --mode file
```

or:

```bash
python <skill-path>/scripts/create_goal_artifact.py --title "<title>" --mode package --validation-command "pnpm test"
```

Then edit generated placeholders before starting `/goal`.

## Direct goal template

```text
/goal <objective>. Context: <relevant files, symptoms, evidence, references>. Target paths: <paths or discovery boundaries>. Scope: <allowed changes>. Non-goals: <out of scope>. Constraints: <compatibility, architecture, dependencies, style>. Done when: <observable behavior and reviewable artifacts>. Validation: <exact commands or checks>. Budget/stop rule: <token/time budget if known, and summarize progress instead of starting new work when budget is reached>. Pause if: <stop conditions>. Report: <summary, risks, validation results>.
```

## File-based goal start template

```text
/goal Execute <short objective> according to <path>. Read the goal contract before editing code. Respect Scope, Non-goals, Constraints, Acceptance Criteria, Validation, Budget and Stop Rules, and Pause Conditions. Use STATUS.md for progress if present. Completion requires all required validation to pass, or a clear explanation of why a check could not be run.
```

## Final response format

When no files are created:

```text
Mode: <direct | file | package | start | audit>

<copy-pasteable /goal command or proposed files>

Why this is ready:
- <short checklist>
```

When files are created:

```text
Mode: <file | package>

Created:
- <paths>

Start with:
```text
/goal ...
```

Validate goal package:
```bash
python <skill-path>/scripts/check_goal_artifact.py <goal-path-or-dir>
```
```

Do not end by offering to implement the task unless the user explicitly asked for implementation.
