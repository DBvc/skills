# Goal artifact placement

## Recommended defaults

Use `.codex/goals/<slug>/` for personal, local, temporary, or experiment-oriented goals.

Use `docs/codex-goals/<slug>/` for team-reviewed, versioned, PR-visible goals.

Use feature-local paths in monorepos when the goal belongs to a single app or package, for example `apps/web/.codex/goals/<slug>/`.

## Avoid

- Root-level `GOAL.md` unless the repo is dedicated to one task.
- One-off task goals in `AGENTS.md`.
- Files outside the active workspace unless Codex has read access.
- Committing temporary status logs unless the team wants that trail in Git.

## Commit policy

Local/private goals can be gitignored.

Team goals should be committed only when they are useful for human review, PR context, auditability, or recurring migrations.
