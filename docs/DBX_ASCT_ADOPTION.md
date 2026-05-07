# DBX ASCT Adoption

This document explains how `DBvc/skills` applies [Agent Skill Control Theory](https://github.com/DBvc/agent-skill-control-theory) without duplicating the theory repository.

## 1. Relationship Between the Repositories

`agent-skill-control-theory` is the theory repository. It defines the general engineering theory:

- skill as a selectively loaded policy controller;
- five postulates;
- seven control surfaces;
- nine design laws;
- placement decisions;
- host-specific artifacts;
- collection-level design;
- SkillValue and safety constraints;
- templates and synthetic examples.

`DBvc/skills` is the applied repository. It contains runtime skills, governance docs, validation scripts, evals, release practices, and DBX-specific compatibility rules.

Rule:

```text
Theory repo: explain why skills work.
Skills repo: define how this skill collection is written, routed, checked, installed, and maintained.
Runtime skills: contain only instructions that change task behavior.
```

Do not copy the whole theory into runtime skills. Runtime skills need operational rules, not a philosophy buffet.

## 2. ASCT 0.3 Additions That Matter for DBX

ASCT 0.3 keeps the theory core stable and expands the applied framework around it:

| ASCT 0.3 area | DBX implication |
| --- | --- |
| Placement decisions | DBX must decide whether a control belongs in a skill, script, reference, hook, command, repo memory, or routing doc. |
| Host-specific artifacts | DBX should map commands, hooks, `AGENTS.md`, `CLAUDE.md`, `llms.txt`, planning files, and project memory back to control surfaces. |
| Collection design | DBX needs routing, conflict resolution, skill graph notes, installation scope, safety review, deprecation, and collection-level evals. |
| Expanded evaluation | DBX evals should distinguish trigger, process, output, safety, and regression behavior. |
| Frontend-debug example | Useful future candidate, but do not add a runtime skill until real bug cases justify it. |

## 3. ASCT to DBX Mapping

| ASCT concept | DBX applied form |
| --- | --- |
| Selectively loaded policy controller | `skills/<name>/SKILL.md` package with trigger description and runtime workflow. |
| Activation Control | `description`, `evals/triggers.json`, generated inventory, `docs/DBX_ROUTING_MATRIX.md`. |
| Intent Control | Mode routing, hard gates, direct-answer/clarification branches. |
| State Control | Current evidence policy, state contracts, `docs/DBX_STATEFUL_SKILLS.md`. |
| Trajectory Control | Workflow steps, stop conditions, approval gates, handoff protocol, skill graph. |
| Execution Control | `scripts/`, validators, deterministic checkers, dry-run commands, CI. |
| Completion Control | Proof fields, validation sections, explicit not-run/limitation statements. |
| Evolution Control | Patch hypotheses, evals, maturity index, release checklist, regression cases, deprecation. |
| Placement | `docs/DBX_PLACEMENT_GUIDE.md`. |
| Host artifacts | `docs/DBX_HOST_ARTIFACTS.md`. |
| Collection design | `docs/DBX_COLLECTION_DESIGN.md` and `docs/DBX_ROUTING_MATRIX.md`. |
| SkillValue | `docs/DBX_EVAL_GUIDE.md`, baseline comparison, cost/risk notes. |

## 4. Working Principles for DBX

DBX applies ASCT through six working principles:

1. **Reduce repeated task entropy.** Create or keep a skill only when it improves a recurring task distribution.
2. **Define boundaries before capability.** Every skill needs trigger, non-use, downgrade, and stop rules.
3. **Keep claims evidence-bounded.** The agent must not claim more than available evidence supports.
4. **Place controls correctly.** Put judgment in `SKILL.md`, long knowledge in `references/`, deterministic operations in `scripts/`, reusable materials in `assets/`, state in repo memory, and cross-skill priority in routing docs.
5. **Evolve through feedback.** Major changes need patch hypotheses, evals, and rollback conditions.
6. **Treat collections as systems.** Routing, conflicts, installation scope, security review, and deprecation are collection-level responsibilities.

## 5. When to Update Which Repository

Update `agent-skill-control-theory` when:

- a new concept changes the general theory;
- a public case study demonstrates a reusable ASCT pattern;
- terminology, postulates, laws, or value models need revision;
- a reusable template belongs across many skill repositories.

Update `DBvc/skills` when:

- a runtime skill changes;
- routing overlap changes;
- local eval or validation rules change;
- a DBX-specific maturity, compatibility, placement, or security policy changes;
- a practical docs page helps maintain this particular skill collection.

## 6. Anti-Patterns

Avoid these failure modes:

- turning every skill into an ASCT lecture;
- adding a runtime skill just because the theory has a new term;
- making `dbx-skill-architect` carry all repository governance in its `SKILL.md`;
- measuring skill quality by instruction length instead of net reliability gain;
- using ASCT labels in user-visible output when they do not help the user;
- treating host-specific artifacts as new theoretical primitives;
- creating collection routing only after skills already conflict in production.

## 7. Practical Rule

Before adding theory to a runtime skill, ask:

```text
Will this sentence change what the agent does during the task?
```

If yes, translate it into an operational rule.

If no, move it to `docs/`, `references/`, or the ASCT theory repository.
