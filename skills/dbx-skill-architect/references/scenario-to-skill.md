# Scenario to skill conversion

Use this file when turning a recurring scenario into a package.

## Scenario card

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

A scenario is weak if it says only “help with X”. It becomes skill-worthy when the input family, output target, failure modes, and success checks are stable.

## IR extraction

Create an intermediate representation before writing instructions:

```text
Objects:
States or results:
Events or actions:
Evidence:
Hypotheses:
Constraints:
Risky boundaries:
Output contract:
Reasoning mode:
Type errors to prevent:
```

IR prevents a common failure: turning a status label into a causal explanation. Example: “the PR is messy” is a state, not a root cause. The skill should ask which changes, files, or review constraints make it messy.

## Package architecture decision

Choose the smallest viable package:

```text
Single SKILL.md
  Good for short procedure skills with low domain depth and no fragile tooling.

SKILL.md + references/
  Good for domain knowledge, rubrics, examples, anti-patterns, and long templates.

SKILL.md + scripts/
  Good for parsing, validation, format conversion, scoring, command orchestration, or fragile operations.

SKILL.md + assets/
  Good for reusable templates, examples, visual resources, schemas, or static data.

SKILL.md + evals/
  Required for serious reusable skills in this repository.
```

## Principle extraction

Do not list principles as decoration. Convert each important rule into behavior:

```text
Domain rule -> meta rule -> root principle -> workflow step -> eval check
```

If a principle cannot change workflow, output, risk handling, domain substance, or evaluation, remove it.

## Done criteria

A full package is done only when it has:

- valid `SKILL.md` frontmatter;
- clear trigger and non-trigger boundaries;
- hard gates or required inputs;
- skill shape and dominant failure modes;
- domain contract when relevant;
- workflow and output contract;
- references/scripts/assets map when present;
- trigger evals or runner evals;
- validation status or manual checks.
