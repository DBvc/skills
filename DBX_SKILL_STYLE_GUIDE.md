# DBX Skill Style Guide

## 0. Core Positioning

A DBX skill is not a prompt snippet. It is a reusable agent work unit:

```text
trigger boundary + task model + workflow + evidence policy + tools/references + output contract + eval loop
```

A skill is worth creating only when it lowers repeated task entropy. It should make the agent more reliable, not merely more verbose.

## 1. Creation Gates

Before creating a full skill, pass these gates.

| Gate | Pass condition | Common fail |
|---|---|---|
| Repeatability | The scenario repeats or the user explicitly wants a reusable routine. | One-off writing, one-time summary, one clever prompt. |
| Stable job | There is a stable job-to-be-done, transformation, diagnosis, decision, or artifact. | “Make the model smarter” or “answer better” with no stable input/output. |
| Evaluability | Success can be checked by examples, assertions, artifact validation, rubric, or human review. | No one can tell whether it worked except by vague feeling. |
| Safety and legitimacy | The workflow is legal, consent-aware, non-deceptive, and non-coercive. | Surveillance, manipulation, privacy invasion, unsafe advice. |
| Domain substance | Domain/content skills include real variables, failure modes, data policy, expert rubric, and examples. | A clean structure with shallow content. |

If any hard gate fails, do not create a full skill. Prefer a checklist, mini-skill, direct answer, or safer redesign.

## 2. Skill Shape Is Implementation Strategy, Not Taxonomy

Do not argue about “which category” a skill belongs to. Use shape to decide where to put complexity.

| Shape | Primary risk | Best implementation weapons |
|---|---|---|
| Procedure | Wrong sequence, missing gate, poor handoff. | Workflow, hard gates, output contract, examples. |
| Tool or format | Fragile file/CLI/API behavior. | Scripts, validators, schemas, rendering checks. |
| Knowledge | Stale or fabricated facts. | Source policy, references, citations, freshness rules. |
| Taste or craft | Generic output, weak aesthetics, style collapse. | Rubric, examples, anti-patterns, assets, human review. |
| Decision | Over-analysis, false certainty, hidden trade-off. | Fact/assumption/judgment split, options, reversible tests. |
| Research | Shallow summary, missing lineage, bad sources. | Source hierarchy, question map, evidence grading. |
| Coordination | Context leakage, duplicated work, weak synthesis. | Delegation protocol, context boundaries, parent synthesis. |
| Meta | Overbuilding, fake rigor, self-referential sprawl. | IR, patch hypothesis, evals, regression checks. |

Every skill should record:

```yaml
skill_shape:
  primary: procedure | tool | knowledge | taste | decision | research | coordination | meta | hybrid
  secondary: []
  dominant_failure_modes: []
  implementation_implication: ""
```

This block may live in `references/` or internal design notes. Do not force it into user-visible output unless it changes the answer.

## 3. Dominant Failure Modes

Design from failure modes, not from favorite patterns.

| Failure mode | What it looks like | Preferred fix |
|---|---|---|
| `wrong_trigger` | Skill fires too often or not often enough. | Better description, trigger evals, near-miss examples. |
| `context_bloat` | Main file is too long, agent loses the point. | Progressive disclosure, split references. |
| `domain_shallow` | Output is formatted but not useful. | Domain variables, gotchas, expert rubric, worked examples. |
| `fragile_operation` | Commands, files, schemas, or formats break. | Scripts, validators, dry-run, structured output. |
| `unverified_output` | It sounds right but cannot be checked. | Assertions, proof fields, validation loop. |
| `taste_collapse` | Generic AI slop, default layout, bland prose. | Taste rubric, anti-patterns, examples, constraints. |
| `safety_overreach` | Manipulation, privacy invasion, unsafe certainty. | Fail-closed gates, refusal, safe alternative. |
| `handoff_failure` | User or reviewer cannot act on the result. | Output contract, review focus, next actions. |
| `maintenance_drift` | Skill rots as tools/APIs/repos change. | Compatibility notes, versioned scripts, eval regression. |

## 4. Directory Contract

A production-oriented skill should follow the standard Agent Skills shape:

```text
skills/<skill-name>/
  SKILL.md              # required metadata + runtime instructions
  references/           # optional focused docs, rubrics, examples, gotchas
  scripts/              # optional reusable scripts, validators, parsers
  assets/               # optional templates, static resources, examples
  evals/                # recommended trigger and output evals
```

Repository-level governance lives outside individual skills:

```text
DBX_SKILL_STYLE_GUIDE.md
DBX_SKILL_INDEX.md
docs/
scripts/
.github/workflows/
```

Do not put repo governance inside a runtime skill unless the agent needs it during execution.

## 5. SKILL.md Rules

### Frontmatter

`SKILL.md` must start with YAML frontmatter:

```yaml
---
name: dbx-example-skill
description: What it does and when to use it. Include trigger keywords and boundaries.
---
```

Required rules:

- `name` equals the parent directory name.
- `name` uses lowercase ASCII letters, numbers, and hyphens.
- `description` explains both capability and trigger context.
- Avoid generic descriptions such as “helps with writing”.

### Body

The body should be operational. Prefer:

- when to use and when not to use;
- required inputs and hard gates;
- workflow steps;
- evidence and uncertainty policy;
- output contract;
- common failure modes;
- references/scripts map;
- eval plan.

Avoid:

- motivational prose;
- generic principles that do not change behavior;
- long theory dumps that should be references;
- repeated instructions with different words;
- making user-visible output overly ceremonial.

Main `SKILL.md` target: under 500 lines. If it grows beyond that, split references.

## 6. References Rules

Use `references/` for material that is useful but not always needed:

- domain variables;
- expert rubrics;
- examples and counterexamples;
- templates;
- gotchas;
- longer explanation;
- source policy;
- captured failure analysis.

Keep each reference file focused. One reference should answer one class of question. Avoid long reference chains where one reference tells the agent to open another reference that opens another cave door.

## 7. Scripts Rules

Add scripts when a step is:

- repetitive;
- fragile;
- mechanical;
- parse-heavy;
- format-sensitive;
- easy to validate deterministically;
- dangerous enough to need dry-run or confirmation.

Script interface requirements:

- non-interactive by default;
- `--help` documented;
- clear errors;
- structured stdout when possible;
- diagnostics to stderr;
- idempotent where practical;
- safe defaults;
- explicit `--confirm` or `--force` for destructive operations.

Do not script human judgment just to look rigorous. A rubber stamp with Python on it is still a rubber stamp.

## 8. Eval Rules

Every serious skill needs two kinds of evals.

### Trigger evals

File: `evals/triggers.json`

Purpose: test whether the skill should activate.

Minimum coverage:

- 2 positive explicit cases;
- 2 positive implicit cases;
- 2 negative cases;
- 2 near-miss cases;
- safety cases when relevant.

### Output evals

File: `evals/evals.json`

Purpose: test whether the skill produces better outputs after activation.

Minimum coverage:

- 2 happy path cases;
- 1 edge case;
- 1 near-miss or failure-mode case;
- 1 safety/boundary case when relevant.

Mechanical checks should be scripted. Judgment checks should use a rubric and quote evidence.

## 9. Maturity Model

| Level | Meaning | Exit criteria |
|---|---|---|
| L0 | Idea | Scenario is named. |
| L1 | Checklist/prompt | Useful but not a valid skill package. |
| L2 | Valid SKILL.md | Frontmatter and basic workflow pass validation. |
| L3 | References/examples | Domain knowledge, examples, or rubrics are separated. |
| L4 | Scripts/tools | Fragile/mechanical steps are scripted. |
| L5 | Evals | Trigger and/or output evals exist. |
| L6 | Baseline comparison | New skill is compared with old/no skill. |
| L7 | Production regression | Regular validation, regression cases, and release checklist. |

A skill can be stable at L2 if it is simple. Do not force all skills to L7. The point is explicit maturity, not decorative bureaucracy.

## 10. Change Management

Any non-trivial change should include a patch hypothesis:

```yaml
patch_hypothesis:
  target_skill: ""
  target_failure: []
  proposed_change: ""
  expected_benefit: []
  expected_cost: []
  evals_to_add_or_update: []
  regression_risk: []
  rollback_condition: []
```

Do not say “this is better” unless you can say what failure it reduces and how to notice regression.

## 11. User-Visible Output Policy

Internal structure can be strict. User-visible structure should fit the task.

| Situation | Output visibility |
|---|---|
| High-risk, high-ambiguity, or meta work | Show gates and contract. |
| Normal complex work | Show conclusion, assumptions, and key reasoning. |
| User asks for direct result | Keep self-check internal and output the artifact. |
| Safety boundary | Show enough boundary reasoning to be transparent. |

A good skill should make the agent think better. It should not force the user to watch every gear spin.
