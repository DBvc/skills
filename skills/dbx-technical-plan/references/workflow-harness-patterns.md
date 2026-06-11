# Workflow Harness Patterns

This skill is portable. It should work as plain instructions in any skill host. When a host supports subagents, commands, workflow scripts, or external state, the same control loop can be lifted into a stronger harness.

## Plan holder axis

A technical plan becomes more reliable as the plan holder moves out of the model’s short-term context.

| Plan holder | Use when | Risk |
| --- | --- | --- |
| Model context | Small, fast, low-risk planning | Drift and forgotten constraints |
| Skill prose | Recurring planning pattern | Still depends on the model following steps |
| Plan file | Persistent implementation workflow | State can become stale |
| Script/runtime | Large, parallel, adversarial, or resumable work | Cost, permissions, and complexity |
| Human project system | High-stakes organization coordination | Slow and manual |

Use the lightest holder that preserves correctness.

## Sequential harness

Use when there is no subagent support.

```text
classify -> gather evidence -> frame problem -> choose shape -> draft plan -> adversarial check -> revise -> handoff
```

Keep intermediate notes short and do not dump scratchpad material into the final answer.

## Fan-out and synthesize

Use for large migrations, cross-package refactors, or architecture changes.

```text
planner
  -> source-of-truth scout
  -> risk mapper
  -> validation reviewer
  -> plan killer
  -> synthesizer
```

Rules:

- Workers are read-only.
- Each worker gets a narrow question.
- The synthesizer keeps only evidence-backed claims.
- The final plan is shorter than the worker notes.

## Classify and act

Use for codebase-wide planning.

```text
inventory candidates -> classify by risk/mechanical/manual -> choose batch order -> define validation per class
```

Good for:

- framework upgrades;
- API deprecation migration;
- design-system migration;
- request-client migration;
- test framework migration.

## Generate and filter

Use only when several real designs are plausible.

```text
generate alternatives -> filter by invariants/source-of-truth/compatibility -> select one -> record rejection reasons
```

Do not generate fake alternatives for a local fix.

## Adversarial verification

Use when failure cost is high.

```text
plan drafter -> independent plan killer -> revised plan -> final confidence and stop conditions
```

The plan killer should try to find:

- wrong owner;
- duplicate source of truth;
- missing compatibility policy;
- invalid rollout;
- no validation of key invariant;
- hidden scope expansion.

## Loop until grounded

Use when evidence gathering can remove uncertainty.

```text
unknown -> read source -> update assumptions -> revise plan -> stop when remaining unknowns are non-blocking
```

Stop when:

- the next unknown requires a human decision;
- reading more files will not change the plan;
- cost exceeds the value of more precision;
- the task should move to a stateful plan-first workflow.

## When to upgrade to a script or command

Move from prose skill to executable harness when any of these are true:

- many similar workers need to run;
- intermediate results must be cached;
- there are loops, branching, retries, or resumability needs;
- output must be schema-validated;
- workflow state should survive context resets;
- cost or permissions require explicit runtime controls.

Do not stuff runtime orchestration into `SKILL.md` just to look powerful. The skill should define policy. The harness should hold state and execute loops.
