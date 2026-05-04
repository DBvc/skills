# dbx-goal-writer skill

`dbx-goal-writer` turns rough coding requests into durable OpenAI Codex `/goal` contracts.

It supports five outputs:

1. `direct`: copy-pasteable `/goal` command
2. `file`: single `GOAL.md`
3. `package`: goal directory for large or strict work
4. `start`: copy-pasteable `/goal` command for an existing goal file/directory
5. `audit`: review and rewrite an existing goal

## Install

In this repository:

```text
skills/dbx-goal-writer/SKILL.md
```

Personal use from this checkout:

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/skills/dbx-goal-writer" "$HOME/.agents/skills/dbx-goal-writer"
```

Repo-scoped use:

```bash
mkdir -p .agents/skills
ln -s "$(pwd)/skills/dbx-goal-writer" .agents/skills/dbx-goal-writer
```

Expected path:

```text
<skills-root>/dbx-goal-writer/SKILL.md
```

Restart Codex if the skill does not appear immediately.

## Usage

```text
$dbx-goal-writer direct: 修复 checkout 优惠券空字符串校验问题
```

```text
$dbx-goal-writer file: 为 account 表单迁移到 zod 生成 GOAL.md
```

```text
$dbx-goal-writer package strict: 为 React 19 迁移生成完整 goal 目录
```

```text
$dbx-goal-writer start .codex/goals/account-zod/GOAL.md
```

```text
$dbx-goal-writer audit .codex/goals/account-zod/GOAL.md
```

## Important behavior

Codex CLI 0.128.0 added persisted `/goal` workflows, but this surface may still be feature-gated or absent from public slash-command docs. Verify with `codex --version`, `codex features list`, and the local TUI slash popup when the user's environment matters.

A goal file or directory is a userland convention. The active Codex `/goal` should still be created with a slash command that references that path and tells Codex to read it before editing.

Recommended file-based start command:

```text
/goal Execute <short objective> according to .codex/goals/<slug>/GOAL.md. Read the goal contract before editing code. Respect Scope, Non-goals, Constraints, Acceptance Criteria, Validation, Budget and Stop Rules, and Pause Conditions. Use STATUS.md for progress if present. Completion requires all required validation to pass, or a clear explanation of why a check could not be run.
```

## Helper scripts

Create a single-file goal:

```bash
python skills/dbx-goal-writer/scripts/create_goal_artifact.py --title "Account zod migration" --mode file
```

Create a package scaffold:

```bash
python skills/dbx-goal-writer/scripts/create_goal_artifact.py --title "React 19 migration" --mode package --validation-command "pnpm test" --validation-command "pnpm typecheck"
```

Check a goal:

```bash
python skills/dbx-goal-writer/scripts/check_goal_artifact.py .codex/goals/react-19-migration
```
