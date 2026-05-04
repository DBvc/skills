# Codex Goal Compatibility Notes

Last checked: 2026-05-05 in a local Codex CLI 0.128.0 environment.

## Current evidence

- OpenAI Codex release `rust-v0.128.0` was published on 2026-04-30 and says it added persisted `/goal` workflows with app-server APIs, model tools, runtime continuation, and TUI controls for create, pause, resume, and clear.
- Local `codex --version` returned `codex-cli 0.128.0`.
- Local `codex features list` showed `goals` as `under development` and enabled in this environment.
- OpenAI's public CLI slash-command docs may not list `/goal` yet, so absence from docs does not prove absence from the local TUI.
- OpenAI's feature maturity docs describe `under development` as not ready for use. Treat `/goal` as changing, feature-gated, and surface-dependent.

## Runtime behavior to preserve in goals

The checked-in Codex goal continuation template tells the agent to continue toward the active thread goal, avoid repeating completed work, and perform a completion audit before marking the goal complete. That audit should map every explicit requirement, file, command, test, gate, and deliverable to concrete evidence.

The budget-limit template tells the agent not to start new substantive work after the goal reaches its token budget. It should summarize useful progress, identify remaining work or blockers, and leave the user with a clear next step.

## Skill policy

- Prefer `/goal <objective>` as the generated start command unless the current TUI proves a more specific syntax.
- Do not invent `/goal --file`, `/goal --dir`, or pause/resume/clear command syntax.
- For file or package goals, make the `/goal` text explicitly say to read the referenced path before editing code.
- Include completion evidence and budget stop rules in generated `GOAL.md` files.
- When a user wants to rely on `/goal` in an unknown environment, tell them to verify `codex --version`, `codex features list`, and the TUI slash popup first.

## Sources

- OpenAI Codex release 0.128.0: https://github.com/openai/codex/releases/tag/rust-v0.128.0
- Codex CLI slash commands: https://developers.openai.com/codex/cli/slash-commands
- Codex feature maturity: https://developers.openai.com/codex/feature-maturity
- Goal continuation template: https://raw.githubusercontent.com/openai/codex/6014b6679ffbd92eeddffa3ad7b4402be6a7fefe/codex-rs/core/templates/goals/continuation.md
- Goal budget-limit template: https://raw.githubusercontent.com/openai/codex/6014b6679ffbd92eeddffa3ad7b4402be6a7fefe/codex-rs/core/templates/goals/budget_limit.md
