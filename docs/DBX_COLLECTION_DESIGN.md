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

The current DBX graph is maintained only in [`DBX_ROUTING_MATRIX.md`](./DBX_ROUTING_MATRIX.md). Keep relationship rules there so routing changes have one source of truth.

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
| “Review this completed diff and write a PR description.” | `dbx-diff-review` first, then appropriate commit/PR skill. |
| “Run L2 code ratchet on staged changes and auto-fix clear findings, but do not commit.” | `dbx-code-ratchet`. |
| “Audit this repo's architecture health and AI-coding decay risks, but do not change code.” | `dbx-architecture-health`. |
| “Use Linus-style review on this staged diff before the PR description.” | `dbx-diff-review` to lock target, then `dbx-linus-review`, then appropriate commit/PR skill. |
| “先给技术计划，并在开始实现前自动做一次 Linus 方案棘轮。” | `dbx-technical-plan` -> `dbx-plan-convergence`, with `dbx-linus-review` as the default read-only reviewer provider. |
| “Turn this fuzzy feature idea into scope, non-goals, and acceptance criteria before anyone codes.” | `dbx-crystallize`. |
| “Is this feature product-correct for the target user?” | `dbx-product-judgment`. |
| “Audit this screenshot/prototype design and give a handoff, but do not implement.” | `dbx-design-judgment`. |
| “Should I split this monorepo?” | `dbx-decision-framing`, not `dbx-linus-review` unless code/design evidence dominates. |
| “Make this message less harsh.” | `dbx-conversation-align` compact rewrite, not full decision analysis. |
| “Read this link and tell me the core argument and whether it is worth continuing.” | `dbx-read`. |
| “Convert this web page to clean Markdown without summarizing.” | `dbx-read`. |
| “Read this Feishu Project ticket and tell me its owner, status, and acceptance criteria.” | `dbx-feishu-project`. |
| “Append these release notes to this Feishu document.” | `dbx-feishu-doc`. |
| “Summarize today's Feishu group discussion about rollout blockers with message evidence.” | `dbx-feishu-im`. |
| “Use the trading domain pack to turn yesterday's feedback group messages into unresolved cases and FAQ candidates.” | `dbx-feishu-feedback-triage`. |
| “Create a technical-plan document from this Feishu ticket and comment the link back.” | `dbx-feishu-workflow`. |
| “I want to really understand React Server Components; build a mental model and one practice rep.” | `dbx-learn`. |
| “Explain closures in two sentences.” | Direct answer, not `dbx-learn`. |
| “Turn this reusable workflow into a skill.” | `dbx-skill-architect` triage, then create/improve if gates pass. |
| “Use $dbx-skill-portfolio-auditor to audit my installed skills.” | `dbx-skill-portfolio-auditor`. |
| “Write a Codex goal for this already-approved task.” | `dbx-goal-writer`. |
| “Make a restart packet so the next AI agent can continue.” | `dbx-agent-handoff`. |
| “Use $dbx-software-plan-first-finalize-plan to seal the agreed plan.” | `dbx-software-plan-first-finalize-plan`. |
| “先 plan-first 一下，不要写代码。” | Direct planning, not DBX Software Plan-First phase skills unless explicitly named. |

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
