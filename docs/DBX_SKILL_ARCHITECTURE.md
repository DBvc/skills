# DBX Skill Repository Architecture

## 1. Goal

This repository should evolve from “a folder of good skills” into “a governed skill system”. The system should make it easy to answer four questions:

1. What skills exist?
2. When should each skill trigger?
3. How mature and reliable is each skill?
4. How do we safely improve a skill without making it worse?

## 2. Repository Layers

```text
.
├── README.md                       # user-facing overview and install commands
├── DBX_SKILL_STYLE_GUIDE.md        # writing and governance rules
├── DBX_SKILL_INDEX.md              # human-maintained skill map
├── docs/                           # deeper process docs and templates
├── scripts/                        # repo-level validators and inventory tools
└── skills/                         # runtime skills consumed by agents
```

Keep runtime skill files focused on execution. Put governance, maturity models, and release rituals at the repository root or under `docs/`.

## 3. Runtime Skill Package Shape

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/
├── assets/
├── evals/
└── README.md
```

Only `SKILL.md` is mandatory by the Agent Skills format, but production DBX skills should usually include evals and targeted references. Scripts are optional and should appear only when they reduce real execution risk.

## 4. Project-Level Files

### `README.md`

Audience: users installing or browsing the repository.

Must contain:

- short repository purpose;
- full stable skill list;
- install commands;
- local validation commands;
- links to governance docs.

### `DBX_SKILL_STYLE_GUIDE.md`

Audience: humans and agents modifying the repository.

Must contain:

- creation gates;
- skill shape and failure-mode model;
- directory rules;
- eval requirements;
- maturity model;
- patch hypothesis rule;
- output visibility policy.

### `DBX_SKILL_INDEX.md`

Audience: maintainers.

Must contain:

- every skill name;
- primary use;
- shape;
- maturity estimate;
- main risk;
- next best improvement.

### `docs/`

Audience: deeper maintenance.

Good candidates:

- eval guide;
- release checklist;
- templates;
- architecture notes;
- changelog or decision logs.

### `scripts/`

Audience: agents and maintainers.

Scripts should validate structure, generate inventory, and check eval schemas. They should not depend on private local paths.

## 5. Skill Lifecycle

```text
idea -> scenario card -> gates -> skeleton -> references/scripts/evals -> validation -> release -> regression
```

### Stage 1: Scenario card

Do this before writing a full skill.

```text
Scenario name:
Primary user:
Context of use:
Real job to be done:
Typical inputs:
Expected outputs:
Recurring failure modes:
Evidence sources:
Hard constraints:
Non-goals:
Success criteria:
```

### Stage 2: Gates

Create a full skill only if repeatability, stable job, evaluability, and safety pass. Domain/content skills must also have real domain substance.

### Stage 3: Skeleton

Minimum:

```text
skills/<name>/SKILL.md
evals/evals.json
```

Optional but often useful:

```text
references/rubric.md
references/examples.md
scripts/validate_*.py
assets/template.*
```

### Stage 4: Validation

Run:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

### Stage 5: Release

Use `docs/DBX_RELEASE_CHECKLIST.md`.

## 6. Three Kinds of Change

### Repo architecture changes

Examples:

- root docs;
- validation scripts;
- inventory structure;
- release checklist;
- CI workflow.

Rule: should not change runtime behavior of any skill unless explicitly intended.

### Architect skill changes

Examples:

- improving `dbx-skill-architect` routing;
- adding shape/failure-mode analysis;
- adding patch hypothesis;
- changing eval schema rules.

Rule: integrate lightly into `SKILL.md`, put deep material in references.

### Individual skill changes

Examples:

- adding git diff script to commit/PR skills;
- adding trigger evals;
- rewriting a review rubric;
- adding examples.

Rule: patch-first. Preserve the existing skill identity unless a rebuild is justified.

## 7. Dependency Policy

Repository-level scripts should default to Python standard library only.

A script may use external dependencies only when:

- the dependency is pinned or documented;
- the script is isolated;
- the value is clearly higher than maintenance cost;
- failure messages tell the agent what to install or run.

## 8. Replacement Package Policy

When producing a downloadable update package, prefer an overlay format:

```text
package-root/
├── APPLY.md
├── README.md
├── DBX_SKILL_STYLE_GUIDE.md
├── DBX_SKILL_INDEX.md
├── docs/
└── scripts/
```

The package can be copied over the repository root. If it changes a runtime skill, include the exact `skills/<name>/...` paths and document the affected files in `APPLY.md`.
