# Scenario to Skill

Use this reference when the user gives a scenario rather than a ready skill spec.

## Contents

- Scenario card
- Domain discovery card
- IR card
- Lift and lower
- Skill-worthiness test
- Domain substance test

## 1. Scenario card

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

## 2. Domain discovery card

Use this for domain/content skills.

```text
Target user:
Artifact type:
Output depth:
Required variables:
Hidden failure modes:
Expert quality checks:
Data-source policy:
Uncertainty policy:
Must-not-omit fields:
Worked examples available:
Domain eval cases:
```

If this card is mostly unknown, use `route: domain_discovery`.

## 3. IR card

IR means Intermediate Representation.

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

## 4. Lift and lower

Use this pattern only for rules that change behavior:

```text
Domain rule -> meta rule -> root principle -> workflow step -> eval check
```

Example:

```text
Domain rule: Do not treat "Flow cancelled" as the root cause.
Meta rule: A terminal status label is not a causal explanation.
Root principle: Description is not explanation.
Workflow step: Backtrack to prior state, failing step, blocker, and evidence.
Eval check: Output must include "terminal status is not root cause" and a missing-evidence field.
```

Domain/content example:

```text
Domain rule: A travel itinerary without transfer time, budget, and verification items is not executable.
Meta rule: Domain artifacts require operational variables, not only narrative structure.
Root principle: Formatted output is not useful output.
Workflow step: Build a domain_content_contract before drafting the skill.
Eval check: Travel eval must fail if no time/distance/budget/verification appears.
```

## 5. Skill-worthiness test

Full skills need all hard gates:

- repeatability
- stable job
- evaluability
- safety/legitimacy

If these fail, do not create a full skill. Use direct answer, checklist, mini-skill, or safer redesign.

## 6. Domain substance test

Domain/content full skills also need:

- target user
- output depth
- domain variables
- data-source policy
- hidden failure modes
- expert quality rubric
- worked example

If these are unknown, do not draft full package. Run domain discovery first.
