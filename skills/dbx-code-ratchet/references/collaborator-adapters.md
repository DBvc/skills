# Collaborator Adapters

`dbx-code-ratchet` is a meta skill. It should compose existing skills instead of copying their review rubrics.

## Default role split

```text
parent controller
  - target contract
  - state
  - triage
  - direction gate
  - progress gate
  - final report

primary reviewer
  - skill: dbx-diff-review-control
  - read-only
  - independent context when Codex subagents are available

strict reviewer
  - skill: dbx-linus-review
  - read-only
  - only when direction, complexity, compatibility, state ownership, or over-engineering risk is present

repair worker
  - write access
  - one writer at a time
  - receives repair contract only

re-reviewer
  - skill: dbx-diff-review-control
  - read-only
  - mode: re-review
```

## Codex subagent policy

When using Codex subagents:

```yaml
context_mode: fork_context=false
model_policy: strongest_available_highest_reasoning
```

Do not hard-code a model version. Let Codex and the user's current configuration choose the concrete model. The skill should only require the strongest available model and highest practical reasoning level for critical roles.

Do not downgrade critical roles automatically:

- controller
- primary reviewer
- strict reviewer
- repair worker
- re-reviewer

Lightweight models may be considered only for non-critical file scanning or log grouping, and only when the user explicitly cares about cost or speed.

## Primary review prompt skeleton

Use this as an internal brief when delegating to a reviewer. Do not print this whole block unless the user asks to audit prompts.

```text
Use dbx-diff-review-control as an independent Codex reviewer.
Context mode: fork_context=false.
Scope: <target contract>.
Background summary: <3-8 lines: goal, known non-goals, target boundaries, main risk surfaces>.
Mode: standard | deep | quick.
Output: normal dbx-diff-review-control Markdown. If practical, append an optional fenced `ratchet_signals` JSON block using version 1. Do not modify files.
Stop condition: return findings with evidence, impact, fix direction, confidence, and validation status. Do not assume access to the parent thread.
```

## Strict review prompt skeleton

```text
Use dbx-linus-review as an independent Codex strict reviewer.
Context mode: fork_context=false.
Scope: <target contract and relevant review findings>.
Background summary: <3-8 lines, no parent-thread dump>.
Focus: direction health, data model, state ownership, compatibility, over-engineering, and whether local repairs are the wrong move.
Output: strict pragmatic Markdown. If practical, append optional `ratchet_signals` JSON with direction signals. Do not modify files.
```

## Repair worker prompt skeleton

```text
You are the repair worker for dbx-code-ratchet.
You may fix ONLY these accepted findings: <ids>.
Use this repair contract: <contract>.
Forbidden: deferred findings, rejected findings, unrelated cleanup, new dependencies, public API changes, schema/migration changes, broad refactors, deleting or weakening tests.
If the minimal fix is impossible under these constraints, stop and return escalation instead of editing around the boundary.
```

## Re-review prompt skeleton

```text
Use dbx-diff-review-control in re-review mode.
Scope: only accepted findings <ids> and direct regressions introduced by the repair diff.
Do not restart a full review. Do not report new S2/S3 issues unless they are direct regressions or reveal direction failure. Do not modify files.
```

## Manual override

User instructions win over this default policy. Common useful overrides:

- “只跑 gate，不改代码” -> gate-only mode.
- “Linus strict 必跑” -> run strict reviewer after primary review.
- “只自动修 S1，不修 S2” -> restrict auto-fix gate.
- “不要开 subagent” -> sequential roles in current context.
- “最多一轮 repair” -> lower `max_repair_rounds`.
