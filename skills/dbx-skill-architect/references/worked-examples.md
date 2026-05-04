# Worked examples

## Example 1: Domain discovery instead of full package

User prompt:

```text
I want a skill for travel guides.
```

Correct shape:

```yaml
skill_shape:
  archetype: knowledge
  secondary_archetypes:
    - decision
  dominant_failure_modes:
    - domain_shallow
    - maintenance_drift
```

Correct route:

```yaml
mode: create
route: domain_discovery
operation: ask_domain_questions
```

Why: travel quality depends on traveler profile, location, season, budget, mobility, visa, safety, opening hours, booking policy, data freshness, and preference trade-offs.

Do not draft a full `SKILL.md` yet.

## Example 2: Tool skill should use scripts

User prompt:

```text
Create a reusable skill that validates JSON config files, normalizes them, and reports missing required fields.
```

Correct shape:

```yaml
skill_shape:
  archetype: tool
  dominant_failure_modes:
    - fragile_operation
    - unverified_output
```

Architecture:

```text
SKILL.md
scripts/validate_config.py
references/schema-notes.md
assets/example-config.json
evals/evals.json
```

Why: JSON parsing, schema checks, and normalization are mechanical and should not depend on model memory.

## Example 3: Improve existing skill with patch hypothesis

User prompt:

```text
Improve this PR-writing skill. It keeps writing vague validation like "tested locally".
```

Patch hypothesis:

```yaml
patch_hypothesis:
  target_failures:
    - "PR body accepts vague validation proof."
  proposed_change: "Add proof-quality rules plus an eval that rejects vague validation phrases unless paired with concrete commands or artifacts."
  expected_benefit: "Reviewers get actionable validation evidence."
  expected_cost: "Slightly stricter output may ask for missing proof more often."
  acceptance_tests:
    - "Prompt with only 'tested locally' must ask for concrete validation or mark proof as missing."
  rollback_conditions:
    - "Happy-path PRs with concrete commands become longer or less readable without quality gain."
```

## Example 4: Taste skill needs rubric, not rigid steps

User prompt:

```text
Create a skill for generating visual quote cards from essays.
```

Correct shape:

```yaml
skill_shape:
  archetype: taste
  secondary_archetypes:
    - tool
  dominant_failure_modes:
    - taste_collapse
    - fragile_operation
```

Architecture:

```text
SKILL.md
references/taste-rubric.md
references/anti-patterns.md
assets/templates/card.html
scripts/render_card.py
evals/evals.json
```

Why: design quality needs taste rubric and examples; rendering needs tooling.
