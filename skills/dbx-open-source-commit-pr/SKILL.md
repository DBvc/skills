---
name: dbx-open-source-commit-pr
description: Generate or review concise English commit messages and PR descriptions for public or open-source repositories. Use when the user asks for commit text, PR body, release-style change summary, or validation wording based on a final diff, staged changes, working tree changes, or a specific commit. Do not use for internal M-xxx work PR contracts, generic code review, or explanations of what commits are.
---

# Open Source Commit/PR

Write public-facing English commit messages and PR descriptions from the final change set.

This skill is not a project diary. It should describe the shipped state, not the implementation journey.

## Trigger boundary

Use this skill when the user asks to:

- write, rewrite, or review an English commit message for public/open-source work;
- write, rewrite, or review a public PR description;
- turn a final diff, staged changes, working tree changes, or a specific commit into commit/PR text;
- improve validation wording in a public PR body.

Do not use this skill when:

- the user wants Chinese `M-xxx(type): title` work-contract PR format; use `dbx-work-commit-pr` instead;
- the user wants a code review, architectural review, bug fix, or implementation;
- the user only asks what a commit, PR, or conventional commit means;
- the output would expose private company context, Slack discussion, internal tickets, secrets, or user-specific process details.

## Source of truth

Use only the final change set as the factual boundary:

1. user-provided diff or patch;
2. staged changes;
3. working tree changes;
4. specific commit;
5. changed files opened only to clarify behavior or naming.

Conversation history can choose output format and scope, but it is not evidence of what shipped.

Ignore:

- planning discussions;
- failed attempts;
- temporary debugging;
- rejected alternatives;
- review back-and-forth;
- tool chatter;
- internal rollout/status details.

## Workflow

1. Determine the requested output: commit only, PR only, both, or review existing text.
2. Identify the final change set. Prefer `git diff --stat` plus the relevant `git diff` when available.
3. Extract public facts: changed behavior, affected area, compatibility impact, validation evidence, and known gaps.
4. Check for mixed scope. If unrelated themes are present, stop and recommend a split before drafting final text unless the user explicitly asks for a single combined commit.
5. Draft concise English text.
6. Check validation wording. Never invent tests or manual checks.
7. If the output is important or saved in a file, optionally run `scripts/check_commit_pr_output.py` against it.

## Commit rules

- Write in English.
- Do not add ticket IDs, private project names, company acronyms, or internal prefixes.
- Prefer the repository's existing style when obvious.
- Otherwise default to `type: subject` or `type(scope): subject`.
- Accept common public types: `feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf`, `inf` when the repository already uses it.
- Keep the subject short, specific, and centered on the final behavior or final code change.
- Avoid process verbs such as "adjust", "tweak", "address feedback", or "iterate" unless that is truly the shipped change.
- Omit the body for tiny self-explanatory commits.

When a commit body helps, use this compact shape:

```text
Background:
- why this final change exists

Main changes:
- the important final behavior or code changes
```

## PR rules

Use this default public PR shape unless the repository has a clear template:

```text
Summary:
- what changed

Why:
- why the change exists

Validation:
- Automated: exact commands that passed
- Manual: exact user-visible checks that were performed
- Not run: explicit gaps when nothing was verified

Risks:
- compatibility notes, migrations, known gaps, or follow-up risk
```

Keep PR text reviewable:

- Prefer concrete bullets over long prose.
- Name exact commands when they were run.
- Name manual actions and observations, not just intent.
- Use `Not run:` for missing validation instead of pretending confidence.
- Include risk only when it helps reviewers understand compatibility, migration, behavior, or follow-up exposure.

## Validation wording

Good:

```text
Validation:
- Automated: pnpm lint, pnpm typecheck, pnpm build
- Manual: opened Settings, changed the default model, restarted the app, and confirmed the setting persisted
- Not run: no end-to-end tests were run
```

Bad:

```text
Proof: tested locally
Proof: verified it works
Validation: should be fine
```

If no evidence exists, say so plainly.

## Mixed diff rule

If the diff contains unrelated themes, do not hide them behind a clean subject.

Return:

```text
This diff appears to contain multiple unrelated themes. I recommend splitting it before drafting a final commit message.

Suggested split:
- <type>: <scope 1>
- <type>: <scope 2>
```

Only draft a single merged message if the user explicitly asks for one.

## Output contract

For commit only:

```text
<type>(<optional-scope>): <subject>

<optional body>
```

For PR only:

```text
Summary:
- ...

Why:
- ...

Validation:
- Automated: ...
- Manual: ...
- Not run: ...

Risks:
- ...
```

For both, output commit first, then PR body.

For review existing text, return only the problems and a corrected version.

## Available helper script

`scripts/check_commit_pr_output.py` checks saved output for common public PR mistakes:

```bash
python3 scripts/check_commit_pr_output.py --artifact pr --file /path/to/output.md
```

It is a quality aid, not a replacement for reading the diff.

## References

See `references/examples.md` for concrete commit and PR examples, including how to replace weak proof claims with useful validation.
