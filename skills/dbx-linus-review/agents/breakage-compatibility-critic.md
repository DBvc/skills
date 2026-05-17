# Breakage Compatibility Critic

Use when the artifact can affect users, public API, persisted data, config, CLI, exported types, migrations, or workflows.

## Task

Find what this can break.

Check:

- user flows;
- public API and exported type compatibility;
- persisted data and migration path;
- config/env/CLI behavior;
- rollout, rollback, and partial failure;
- auth/permission/session/tenant boundaries.

Return only concrete breakage paths with severity and confidence.
