---
name: open-source-commit-pr
description: Generate English commit messages and PR descriptions for public or open-source repositories. Use when the user asks to write, rewrite, or review a commit message or PR body for staged changes, working tree diffs, a specific patch, or a recent commit. Base the output on the final diff and changed files, not on conversational history, abandoned approaches, or internal company process details.
---

# Open Source Commit/PR

Write concise, English commit messages and PR descriptions for open-source work.

Treat the final diff as the source of truth. Ignore intermediate discussion, failed attempts, and process chatter unless the user explicitly asks to include them.

## Workflow

1. Determine the scope first.
   - Use the exact diff or files the user provided.
   - Otherwise inspect the relevant final change set: staged changes, working tree changes, or a specific commit.
2. Gather facts from code, not conversation.
   - Prefer `git diff --stat` plus the relevant `git diff`.
   - Open changed files only when needed to clarify behavior or naming.
   - Use recent commit history only to match repository style, not to infer change content.
3. Ignore implementation journey.
   - Do not mention planning discussions, debugging steps, rejected ideas, or temporary failures unless they are visible in the final code or the user explicitly wants them captured.
4. Decide the output target.
   - Commit only
   - PR only
   - Both
5. Write from the final state.
   - Describe what changed and why it matters now.
   - Keep speculation out. If motivation is not visible in the diff, say less.
6. Flag scope problems.
   - If the diff contains multiple unrelated themes, stop and recommend splitting the commit before drafting the final message.
   - Only draft a merged commit when the user explicitly asks for one.
   - Do not hide a mixed diff behind an artificially clean subject line.

## Commit Rules

- Write in English.
- Do not add ticket IDs or company-specific prefixes.
- Prefer the repository's existing style if it is obvious from recent history.
- Otherwise default to `type: subject` or `type(scope): subject`.
- Use standard open-source-friendly types such as `feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf`, or `inf` when the repo already uses it.
- Keep the subject short, specific, and centered on the final change.
- Do not stuff the subject with process words like "adjust", "tweak", or "address feedback" unless that is truly the shipped change.
- Omit the body for tiny, self-explanatory commits.
- When a body helps, default to:

```text
Background:
- why this final change exists

Main changes:
- the most important final code or behavior changes
```

## PR Rules

- Write for public review, not for internal status tracking.
- Avoid internal ticket IDs, org jargon, rollout plans, Slack context, or team-specific acronyms unless the user explicitly wants them.
- Prefer concrete sections over long prose.
- Use this default structure unless the repository clearly wants something else:

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

## Validation Guidance

Prefer `Validation` over `Proof`.

For PR descriptions, prefer explicit `Automated`, `Manual`, and `Not run` lines over a generic validation paragraph.

Good validation is factual and specific:

- `Automated: pnpm lint, pnpm typecheck, pnpm build`
- `Manual: created a new conversation, reloaded the app, and confirmed history persisted`
- `Not run: no end-to-end tests were run`

Bad validation is vague:

- `Proof: tested locally`
- `Proof: verified it works`
- `Proof: should be fine`

If no validation evidence exists, say so plainly instead of inventing confidence.

## Content Boundaries

- Use the final diff as the content boundary.
- Use user instructions to choose format and scope, not to invent facts.
- Do not echo conversational phrases just because they appeared in chat.
- Discard rejected approaches and discussion history even if they were prominent in the conversation.
- Do not mention tools, debugging sessions, or review comments unless they materially changed the final code and belong in the public record.
- Prefer final behavior over implementation journey.

## Examples

See [references/examples.md](references/examples.md) for concrete commit and PR examples, including how to turn weak "proof" claims into useful validation.
