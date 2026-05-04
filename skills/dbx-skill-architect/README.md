# Scenario Skill Architect

A scenario-first skill architect for creating, critiquing, improving, evaluating, and triaging reusable agent skill packages.

This package keeps the fail-closed and domain-substance model, then adds practical hardening against the most common skill-authoring failure: **format-valid but content-empty output**.

## Best use

Use for:

- creating a reusable skill from a recurring scenario;
- critiquing an existing skill;
- patch-first skill improvement;
- designing runner-compatible evals;
- triaging one-off, unsafe, or underspecified skill requests;
- discovering domain substance before building domain/content skills.

Do not use it to wrap one-off prompts into full skills.

## Key routes

- `full_skill`: hard gates pass, and domain gates pass when applicable.
- `mini_skill`: lightweight reusable wrapper.
- `needs_clarification`: hard gates are unknown and blocking questions are required.
- `domain_discovery`: hard gates may pass, but domain substance is unknown or weak.
- `checklist`, `direct_answer`, `refuse_or_redesign`: triage alternatives.

## Key mechanisms

### Skill shape

The opening contract includes:

```yaml
skill_shape:
  archetype: procedure | tool | knowledge | taste | decision | research | coordination | meta | hybrid | unknown | not_applicable
  secondary_archetypes: []
  dominant_failure_modes: []
  implementation_implications: []
```

Use this to decide whether the package needs scripts, references, assets, trigger evals, output evals, human rubrics, or safety gates.

### Patch hypothesis

Improvement mode requires concrete patch hypotheses:

```yaml
patch_hypothesis:
  required: true
  target_failures: []
  target_files: []
  exact_edit_units: []
  proposed_change: ""
  expected_benefit: ""
  expected_cost: ""
  acceptance_tests: []
  rollback_conditions: []
```

This prevents decorative changes from being called improvements.

### Artifact-body validation

For `full_skill`, the checker now expects copy-ready fenced file blocks, not filename markers. It parses:

- `SKILL.md` frontmatter and body;
- `evals/evals.json` with schema and eval-quality checks;
- `evals/triggers.json` with trigger-case coverage;
- placeholders and generic content markers;
- shape-specific done criteria for tool, coordination, review/procedure, and domain/content skills.

## Validation

From the skill root:

```bash
python3 scripts/lint_skill_package.py .
python3 scripts/run_skill_evals.py evals/evals.json --validate-only
python3 scripts/check_architect_output.py captured-output.md
python3 scripts/create_skill_skeleton.py --name example-skill --description "reviewing release plans" --output /tmp/dbx-skeleton-test
```

The eval runner validates schema and can score saved outputs. It does not call an LLM.

## Files

```text
SKILL.md
README.md
CHANGELOG.md
references/
  skill-archetypes.md
  improvement-validation.md
  scenario-to-skill.md
  domain-discovery.md
  domain-starter-packs.md
  authoring-rubric.md
  content-quality-rubric.md
  eval-playbook.md
  mode-golden-examples.md
  worked-examples.md
  zh-CN-guide.md
scripts/
  lint_skill_package.py
  run_skill_evals.py
  eval_schema.py
  check_architect_output.py
  create_skill_skeleton.py
evals/
  evals.json
  triggers.json
assets/templates/
  SKILL.template.md
  evals.template.json
  triggers.template.json
  scenario-card.template.md
  patch-hypothesis.template.md
agents/
  openai.yaml
```
