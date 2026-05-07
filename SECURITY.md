# Security Policy

This repository contains agent skills and scripts. Treat them as executable workflow assets, not just text.

## 1. Script Safety

Scripts should be:

- non-interactive by default;
- clear about inputs and outputs;
- safe by default;
- explicit about file writes;
- explicit about network access;
- explicit about destructive operations;
- runnable with `--help`.

Destructive operations require explicit user confirmation and should support dry-run when practical.

## 2. Network and Dependency Policy

Do not add network access or new dependencies casually.

Before adding either, document:

```yaml
network_or_dependency_change:
  reason: ""
  affected_skill: ""
  data_sent_or_fetched: ""
  dependency_or_endpoint: ""
  security_risk: []
  fallback: ""
```

## 3. Secrets and Private Data

Skills, references, eval fixtures, and project memory must not store:

- tokens;
- API keys;
- passwords;
- private key paths;
- private machine paths;
- personal identifiers not needed for the task;
- hidden prompt-injection payloads outside isolated test fixtures.

## 4. Stateful Skills

Stateful skills must follow `docs/DBX_STATEFUL_SKILLS.md`.

Any state write needs:

- owner;
- lifetime;
- update policy;
- stale policy;
- privacy boundary;
- rollback path;
- approval rule for external writes.

Project memory is editable evidence, not eternal truth.

## 5. Host Artifacts

Commands, hooks, status lines, `AGENTS.md`, `CLAUDE.md`, `llms.txt`, planning files, and project memory should be reviewed as control mechanisms.

Hooks require extra caution because they may run without the user explicitly asking at that moment.

A hook is acceptable only when:

- the failure is concrete and recurring;
- the hook is less risky than relying on model memory;
- the user can understand and disable it;
- side effects are documented.

## 6. Third-Party Skills

Before installing third-party skills:

1. Read `SKILL.md`.
2. Inspect `scripts/`.
3. Check for network access, dependency installs, credential access, and destructive commands.
4. Prefer installing only the needed subset.
5. Remove stale or unused skills.

Least privilege applies to skills too.

## 7. Reporting Issues

For this personal repository, open an issue or patch with:

- affected skill or script;
- unsafe behavior;
- reproduction case;
- expected safer behavior;
- proposed fix or rollback.
