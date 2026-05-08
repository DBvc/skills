# DBX Skill Style Guide

This guide defines how to write, review, and evolve skills in `DBvc/skills`.

DBX uses [Agent Skill Control Theory](https://github.com/DBvc/agent-skill-control-theory), but this file is not a theory dump. It is the applied operational rulebook for this repository.

## 0. Core Positioning

A DBX skill is not a prompt snippet. It is a reusable agent work unit:

```text
trigger boundary + task model + workflow + evidence policy + tools/references + output contract + eval loop
```

In ASCT language, a skill is a selectively loaded policy controller. In DBX language, that means:

- it activates only for the right task distribution;
- it changes the agent's behavior in a bounded way;
- it uses external evidence and deterministic tools when model judgment is not enough;
- it defines when the agent may claim completion;
- it evolves through patch hypotheses and regression checks.

A skill is worth creating only when it lowers repeated task entropy more than it adds context, maintenance, trigger, safety, user-friction, or tooling cost.

## 1. Applied Control Surfaces

Use ASCT control surfaces as a review checklist, not as runtime ceremony.

| Control surface | DBX design question | Common DBX mechanism |
| --- | --- | --- |
| Activation | Should this skill be used? | `description`, trigger evals, routing matrix, generated index. |
| Intent | What task is the user actually asking for? | Mode routing, hard gates, direct-answer/clarification branches. |
| State | What is true right now? | Evidence source policy, current diff, tool output, state contract. |
| Trajectory | What path should the agent follow? | Workflow, stop conditions, handoff protocol, approval gates. |
| Execution | Which operations require tools? | Scripts, validators, dry-run, schema checks, render/open/reparse checks. |
| Completion | When may the agent claim done? | Validation section, proof fields, limitations, explicit not-run statements. |
| Evolution | How does the skill avoid drift? | Patch hypothesis, evals, index updates, compatibility notes, release checklist. |

Do not force these labels into user-visible output unless they improve the task result.

## 2. Placement Before Prose

Before adding a rule to `SKILL.md`, ask:

```text
Where should this control live?
```

| Control | Prefer placement |
| --- | --- |
| Always-on safety or repo convention | `AGENTS.md`, `CLAUDE.md`, root docs, or host-level instruction. |
| Explicit multi-skill workflow | command, routing matrix, or collection workflow. |
| Deterministic or repeatable check | `scripts/`, validator, hook, or CI. |
| Long or conditional knowledge | `references/`. |
| Template, schema, example artifact | `assets/`. |
| Project glossary, ADR, task brief, out-of-scope record | repo memory or stateful doc. |
| Task-specific recurring behavior | skill. |
| Skill conflict or priority | routing matrix or collection design doc. |

Wrong placement is a real defect. A sentence in a long `SKILL.md` is a weak substitute for a validator, hook, or routing rule when deterministic enforcement is possible.

## 3. Creation Gates

Before creating a full skill, pass these gates.

| Gate | Pass condition | Common fail |
| --- | --- | --- |
| Repeatability | The scenario repeats or the user explicitly wants a reusable routine. | One-off writing, one-time summary, one clever prompt. |
| Stable task distribution | There is a stable class of inputs, outputs, and failure modes. | “Make the model smarter” with no stable job. |
| Evaluability | Success can be checked by examples, assertions, artifact validation, rubric, or human review. | No one can tell whether it worked except by vague feeling. |
| Safety and legitimacy | The workflow is legal, consent-aware, non-deceptive, and non-coercive. | Surveillance, manipulation, privacy invasion, unsafe advice. |
| Domain substance | Domain/content skills include real variables, failure modes, data policy, expert rubric, and examples. | A clean structure with shallow content. |
| Net value | Expected success gain is larger than added context/tool/user/maintenance cost and risk. | Decorative rigor or theory cosplay. |
| Placement fit | The control really belongs in a skill rather than a script, hook, command, reference, or repo memory. | Everything becomes a skill. |

If a hard gate fails, do not create a full skill. Prefer a checklist, mini-skill, direct answer, safer redesign, script, hook, command, or captured note.

## 4. Skill Shape Is Implementation Strategy, Not Taxonomy

Do not argue about which box a skill belongs to. Use shape to decide where to put complexity.

| Shape | Primary risk | Best implementation weapons |
| --- | --- | --- |
| Procedure | Wrong sequence, missing gate, poor handoff. | Workflow, hard gates, output contract, examples. |
| Tool or format | Fragile file/CLI/API behavior. | Scripts, validators, schemas, rendering/open/reparse checks. |
| Knowledge | Stale or fabricated facts. | Source policy, references, citations, freshness rules. |
| Taste or craft | Generic output, weak aesthetics, style collapse. | Rubric, examples, anti-patterns, assets, human review. |
| Decision | Over-analysis, false certainty, hidden trade-off. | Fact/assumption/judgment split, options, reversible tests. |
| Research | Shallow summary, missing lineage, bad sources. | Source hierarchy, question map, evidence grading. |
| Coordination | Context leakage, duplicated work, weak synthesis. | Delegation protocol, context boundaries, parent synthesis. |
| Project memory or bootstrap | Stale project context, hidden state, privacy leakage. | State contract, owner/lifetime/update/stale policy. |
| Interaction mode | Session behavior persists after it should stop. | Activation/deactivation phrase, exception policy, lifetime. |
| Collection workflow | Skill conflict, wrong ordering, unsafe composition. | Routing matrix, skill graph, handoff contracts, collection evals. |
| Meta | Overbuilding, fake rigor, self-referential sprawl. | IR, patch hypothesis, evals, regression checks. |

Every serious skill should record its shape in design notes or references:

```yaml
skill_shape:
  primary: procedure | tool | knowledge | taste | decision | research | coordination | project_memory | interaction_mode | collection_workflow | meta | hybrid
  secondary: []
  dominant_failure_modes: []
  implementation_implication: ""
```

This block does not belong in normal user-visible output unless it changes the answer.

## 5. Dominant Failure Modes

Design from failure modes, not from favorite patterns.

| Failure mode | What it looks like | Preferred fix |
| --- | --- | --- |
| `wrong_trigger` | Skill fires too often or not often enough. | Better description, trigger evals, near-miss examples, routing matrix. |
| `context_bloat` | Main file is too long, agent loses the point. | Progressive disclosure, split references, compact runtime body. |
| `domain_shallow` | Output is formatted but not useful. | Domain variables, gotchas, expert rubric, worked examples. |
| `fragile_operation` | Commands, files, schemas, or formats break. | Scripts, validators, dry-run, structured output. |
| `unverified_output` | It sounds right but cannot be checked. | Assertions, proof fields, validation loop, explicit limitations. |
| `taste_collapse` | Generic AI slop, default layout, bland prose. | Taste rubric, anti-patterns, examples, constraints. |
| `safety_overreach` | Manipulation, privacy invasion, unsafe certainty. | Fail-closed gates, refusal, safe alternative. |
| `handoff_failure` | User or reviewer cannot act on the result. | Output contract, review focus, next actions. |
| `state_drift` | Project memory or workflow state becomes stale or unsafe. | State contract, stale policy, update/rollback path. |
| `collection_conflict` | Two skills fight, chain incorrectly, or bypass safety. | Routing matrix, skill graph, explicit precedence, collection eval. |
| `maintenance_drift` | Skill rots as tools/APIs/repos change. | Compatibility notes, versioned scripts, eval regression. |

## 6. Directory Contract

A production-oriented skill should follow the standard Agent Skills shape:

```text
skills/<skill-name>/
  SKILL.md       # required metadata + runtime instructions
  references/    # optional focused docs, rubrics, examples, gotchas
  scripts/       # optional reusable scripts, validators, parsers
  assets/        # optional templates, static resources, examples
  evals/         # recommended trigger and output evals
  README.md      # optional usage notes for humans
```

Repository-level governance lives outside individual skills:

```text
README.md
DBX_SKILL_STYLE_GUIDE.md
DBX_SKILL_INDEX.md
SECURITY.md
docs/
scripts/
```

Optional CI or host artifacts such as `.github/workflows/`, commands, hooks, and repo instructions also live at repository level when present.

Host-specific artifacts may exist when the host supports them:

```text
commands/
hooks/
AGENTS.md
CLAUDE.md
llms.txt
planning files
project memory
status line metadata
```

Treat those as implementations of the same control surfaces, not as new theory primitives.

## 7. `SKILL.md` Rules

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

The body should be operational.

Prefer:

- when to use and when not to use;
- required inputs and hard gates;
- workflow steps;
- evidence and uncertainty policy;
- output contract;
- completion proof;
- common failure modes;
- references/scripts map;
- eval plan.

Avoid:

- motivational prose;
- generic principles that do not change behavior;
- long theory dumps that should live in `docs/` or `references/`;
- repeated instructions with different words;
- making user-visible output overly ceremonial.

Main `SKILL.md` target: under 500 lines. If it grows beyond that, split references.

## 8. References, Assets, and Scripts

Use `references/` for material that is useful but not always needed:

- domain variables;
- expert rubrics;
- examples and counterexamples;
- templates;
- gotchas;
- longer explanation;
- source policy;
- captured failure analysis.

Use `assets/` for reusable materials:

- templates;
- schemas;
- examples;
- starter files;
- static resources.

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

## 9. Stateful Skill Rules

Most DBX skills should be stateless runtime protocols. A stateful skill is justified only when persistent state actually reduces repeated work.

Use `docs/DBX_STATEFUL_SKILLS.md` when a skill writes or changes:

- project glossary;
- ADR or decision record;
- task brief;
- out-of-scope record;
- progress file;
- issue labels or external workflow state;
- session interaction mode.

Stateful skills require a `state_contract`. Do not hide persistent behavior behind a normal writing or planning skill.

## 10. Eval Rules

Every serious skill needs two minimum eval surfaces, and mature skills should consider five.

Minimum:

- `evals/triggers.json`: activation correctness.
- `evals/evals.json`: output and boundary correctness after activation.

Mature eval target set:

| Eval type | Question |
| --- | --- |
| Trigger | Does the skill activate and stay silent correctly? |
| Process | Does it follow the intended trajectory? |
| Output | Is the result useful, grounded, and correctly shaped? |
| Safety | Does it respect approvals, privacy, destructive actions, and external side effects? |
| Regression | Do historical failures stay fixed? |

Mechanical checks should be scripted. Judgment checks should use a rubric and quote evidence.

Collection-level evals are needed when routing, skill graph, or install scope changes.

## 11. Maturity Model

| Level | Meaning | Exit criteria |
| --- | --- | --- |
| L0 | Idea | Scenario is named. |
| L1 | Checklist/prompt | Useful but not a valid skill package. |
| L2 | Valid SKILL.md | Frontmatter and basic workflow pass validation. |
| L3 | References/examples | Domain knowledge, examples, or rubrics are separated. |
| L4 | Scripts/tools | Fragile/mechanical steps are scripted. |
| L5 | Evals | Trigger and/or output evals exist. |
| L6 | Baseline comparison | New skill is compared with old/no skill. |
| L7 | Production regression | Regular validation, regression cases, compatibility, and release checklist. |

A skill can be stable at L2 if it is simple. Do not force all skills to L7. The point is explicit maturity, not decorative bureaucracy.

## 12. Change Management

Any non-trivial change should include a patch hypothesis:

```yaml
patch_hypothesis:
  target_skill: ""
  target_failure: []
  target_files: []
  exact_edit_units: []
  proposed_change: ""
  expected_benefit: []
  expected_cost: []
  evals_to_add_or_update: []
  regression_risk: []
  rollback_condition: []
```

Do not say “this is better” unless you can say what failure it reduces and how to notice regression.

## 13. User-Visible Output Policy

Internal structure is good. User-visible bureaucracy is not.

Use full contracts when:

- the user asks for an audit trail;
- the task is high-risk or highly ambiguous;
- the output is a formal decision memo, review report, or skill package;
- the skill is debugging its own route or gates.

Prefer compact natural language when:

- the user asks for a direct artifact;
- the task is low-risk;
- YAML would not help the user act.

A good skill should make the agent act more reliably, not make every answer look like a customs declaration for a tiny sandwich.
