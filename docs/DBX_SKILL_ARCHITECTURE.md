# DBX Skill Architecture

This repository is organized as a governed skill collection, not a loose folder of prompts.

## 1. Layers

```text
DBvc/skills/
  README.md                    human overview and install entry
  DBX_SKILL_STYLE_GUIDE.md      applied authoring rules
  DBX_SKILL_INDEX.md            collection inventory and maturity map
  SECURITY.md                   safety policy
  docs/                         governance and design docs
  scripts/                      repo-level validators and inventories
  skills/                       runtime skill packages
  .github/workflows/            lightweight validation automation
```

## 2. Theory vs Applied Repository

`agent-skill-control-theory` explains the general ASCT model.

`DBvc/skills` applies that model to a concrete personal skill collection.

Runtime skills should not contain the whole theory. They should contain only task-relevant activation, workflow, evidence, validation, and boundary rules.

## 3. Control Surface Mapping

| Control surface | Repository layer |
| --- | --- |
| Activation | skill `description`, trigger evals, routing matrix, generated inventory. |
| Intent | runtime mode routing, hard gates, direct/clarification branches. |
| State | evidence policy, compatibility docs, state contracts, project memory if added. |
| Trajectory | workflow steps, stop conditions, approval gates, skill graph. |
| Execution | skill scripts, repo scripts, validators, CI. |
| Completion | proof fields, validation sections, output checkers, release checklist. |
| Evolution | patch hypotheses, evals, index, changelogs, compatibility updates, deprecation. |

## 4. Placement Architecture

Do not default to `SKILL.md`.

Use `docs/DBX_PLACEMENT_GUIDE.md` before adding a non-trivial control.

Typical placements:

- `SKILL.md`: runtime task controller;
- `references/`: long conditional knowledge;
- `scripts/`: deterministic or fragile operations;
- `assets/`: templates and reusable material;
- `evals/`: regression behavior;
- root docs: repository governance;
- commands/hooks: host-specific macro workflows or lifecycle guards;
- repo memory: persistent state;
- routing matrix: collection-level activation and conflict rules.

## 5. Collection Architecture

As the collection grows, DBX needs collection-level discipline:

- routing matrix;
- skill graph;
- install scope;
- script inventory;
- compatibility matrix;
- deprecation policy;
- collection-level evals.

See `docs/DBX_COLLECTION_DESIGN.md`.

## 6. Skill Lifecycle

1. Capture scenario.
2. Map base-agent failure modes.
3. Decide placement.
4. Pass creation gates.
5. Choose skill shape and dominant failure modes.
6. Create minimal `SKILL.md`.
7. Add references, scripts, assets only where they reduce failure.
8. Add trigger/output evals and, when needed, process/safety/regression evals.
9. Update `DBX_SKILL_INDEX.md` and routing docs.
10. Release with validation.
11. Evolve through patch hypotheses.

## 7. Current Architectural Bias

DBX intentionally favors:

- narrow, explicit runtime skills;
- strong trigger boundaries;
- proof and evidence contracts;
- deterministic checks for mechanical tasks;
- low ceremony for simple skills;
- repository-level governance outside runtime skills.

DBX intentionally avoids:

- turning every idea into a skill;
- automatically adding host commands or hooks;
- installing large catalogs without scope review;
- embedding ASCT theory into every `SKILL.md`;
- optimizing for public marketplace polish before personal reliability.
