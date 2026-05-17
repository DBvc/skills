# DBX Skill Collection Design

A skill collection is not just a folder of skills. At collection scale, new problems appear: routing, composition, conflicts, installation scope, security review, versioning, and deprecation.

This document applies ASCT collection-level design to `DBvc/skills`.

## 1. Collection-Level Control Surfaces

| Control surface | DBX expression |
| --- | --- |
| Activation | README, skill index, generated inventory, routing matrix, trigger evals. |
| Intent | Routing questions, task categories, mode decisions, near-miss examples. |
| State | Shared docs, compatibility notes, project memory policies, state contracts. |
| Trajectory | Skill graph, required order, handoff contracts. |
| Execution | Shared scripts, script policy, local validation, CI. |
| Completion | Cross-skill proof requirements and output contracts. |
| Evolution | Release checklist, eval suites, compatibility notes, deprecation. |

## 2. Human Discovery vs Agent Activation

Human-facing metadata says what the collection is for.

Agent activation metadata says when one skill should fire.

Do not confuse these:

```text
Human discovery:
A personal skill collection for engineering, review, decision, communication, and Codex workflows.

Agent activation:
Use dbx-work-commit-pr when the user asks for a Chinese work-context commit message or PR description based on final diff.
Do not use it for open-source public PRs or code review findings.
```

README and marketplace metadata can be broad. `description` must be precise.

## 3. DBX Skill Graph

Useful relationship types:

```text
precedes: A should run before B.
requires: B depends on output from A.
competes: A and B are alternatives.
fallback: use B if A cannot proceed.
handoff: A produces a contract for B.
```

Current DBX graph:

| Relationship | Meaning |
| --- | --- |
| `dbx-diff-review-control` precedes commit/PR skills | If user asks to review concrete code changes and then write PR text, review the selected change set first. |
| `dbx-diff-review-control` precedes `dbx-linus-review` for concrete diffs | If strict pragmatic judgment is requested on a diff with staged/branch/file ambiguity, establish the target first. |
| `dbx-linus-review` handles explicit strict critique | Use for Linus-style, harsh, over-engineering, model, plan, or merge/readiness judgment. |
| `dbx-decision-framing` precedes `dbx-goal-writer` | If user has not decided whether to do the work, decide before writing a Codex goal. |
| `dbx-skill-architect` precedes new skill creation | If request is one-off, triage before full skill creation. |
| `dbx-subagent-context-control` supports `dbx-goal-writer` | Goal contracts may include subagent context strategy when Codex subagents are involved. |
| `dbx-conversation-align` competes with `dbx-decision-framing` | Use conversation-align for wording/boundaries; decision-framing for real action trade-offs. |
| `dbx-open-source-commit-pr` competes with `dbx-work-commit-pr` | Choose based on public/open-source vs work/internal context. |

## 4. Conflict Resolution

When two skills might trigger:

1. Prefer the skill that matches the user's primary requested artifact.
2. Prefer review/decision before writing downstream artifacts when risk is unresolved.
3. Prefer narrow host-specific skills only when the host context is explicit.
4. Prefer direct answer when the task is one-off and does not need a full skill.
5. Prefer safety boundary before rewrite, persuasion, or action planning.

Examples:

| User request | Preferred routing |
| --- | --- |
| “Review this completed diff and write a PR description.” | `dbx-diff-review-control` first, then appropriate commit/PR skill. |
| “Use Linus-style review on this staged diff before the PR description.” | `dbx-diff-review-control` to lock target, then `dbx-linus-review`, then appropriate commit/PR skill. |
| “Should I split this monorepo?” | `dbx-decision-framing`, not `dbx-linus-review` unless code/design evidence dominates. |
| “Make this message less harsh.” | `dbx-conversation-align` compact rewrite, not full decision analysis. |
| “Turn this reusable workflow into a skill.” | `dbx-skill-architect` triage, then create/improve if gates pass. |
| “Write a Codex goal for this already-approved task.” | `dbx-goal-writer`. |

## 5. Installation Scope

Large catalogs should not be installed wholesale by default. DBX is still small, but the rule matters as it grows.

Consider:

- user scope vs repo scope vs organization scope;
- trusted vs untrusted skills;
- script permissions;
- network access;
- dependency installation;
- environment variable access;
- sensitive domain risk;
- host compatibility;
- deprecation status.

Least privilege applies to skills too.

## 6. Collection Safety

Collection-level risks include:

- cross-skill activation promotion;
- hidden scripts across many skills;
- unpinned dependencies;
- network access through unexpected paths;
- credential leakage;
- stale skills that retain high permissions;
- malicious or unreviewed community contributions;
- deprecated skills remaining discoverable.

Recommended controls:

- script inventory;
- network policy;
- credential policy;
- dependency pinning policy;
- installation subsets;
- security review before release;
- compatibility matrix;
- deprecation process.

## 7. Collection Evaluation

Evaluate at two levels.

### Skill-level eval

- trigger correctness;
- process adherence;
- output quality;
- safety behavior;
- regression.

### Collection-level eval

- routing correctness;
- conflict resolution;
- command behavior if commands exist;
- cross-skill handoff;
- install subset behavior;
- performance under many installed skills;
- regression when a skill is added, removed, renamed, or deprecated.

## 8. Deprecation Policy

If a skill becomes obsolete:

1. Mark it deprecated in `DBX_SKILL_INDEX.md`.
2. Explain replacement or fallback.
3. Add trigger evals to prevent accidental activation if still installed.
4. Keep compatibility notes for at least one release cycle.
5. Remove only when users have a migration path.

Do not let stale skills linger as haunted cutlery in the drawer.
