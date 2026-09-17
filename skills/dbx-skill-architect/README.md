# Scenario Skill Architect

A scenario-first skill architect for creating, critiquing, improving, evaluating, and triaging reusable agent skill packages.

This package keeps the fail-closed and domain-substance model, then aligns the runtime controller with ASCT 0.3 placement, host-artifact, collection, and SkillValue discipline without turning `SKILL.md` into a theory document.

## Best use

Use for:

- creating a reusable skill from a recurring scenario;
- critiquing an existing skill;
- patch-first skill improvement;
- designing runner-compatible evals;
- triaging one-off, unsafe, misplaced, or underspecified skill requests;
- deciding whether a control belongs in a skill, script, reference, hook, command, repo memory, or routing matrix.

Do not use it to wrap one-off prompts into full skills.

## Key mechanisms

### Control surfaces and SkillValue

Create, critique, improve, and eval work should map the proposal to ASCT control surfaces and compare it against a baseline:

```yaml
control_surface_map:
  activation: strong
  intent: light
  state: light
  trajectory: strong
  execution: none
  completion: light
  evolution: strong
skill_value_check:
  baseline: base_agent | old_skill | lighter_version | competing_skill | human_checklist
  expected_success_delta: ""
  added_cost: []
  added_risk: []
  net_value: positive | uncertain | negative
```

If a lighter checklist, script, reference, direct answer, or host artifact has better net value, do not produce a full skill package.

### Placement before prose

The opening contract now includes a `placement_decision` block. This prevents ASCT 0.3 placement errors, especially writing scripts, hooks, global rules, or repo memory into `SKILL.md` prose.

### Artifact-body validation

For `full_skill`, the checker expects copy-ready fenced file blocks, not filename markers. It parses:

- `SKILL.md` frontmatter and body;
- `evals/evals.json` with schema and eval-quality checks;
- `evals/triggers.json` with trigger-case coverage;
- placeholders and generic content markers;
- shape-specific done criteria for tool, coordination, review/procedure, and domain/content skills.

### Positive-evidence evals

New suites use `schema_version: 8`. Every machine-scored case must positively observe required behavior, artifact, state, validation, or another non-structural result. Absence-only cases cannot pass on arbitrary non-empty text. Unversioned v7 suites remain compatible until they are deliberately migrated.

### Deterministic broad-change gate

Broad skill changes use a schema-v2 change manifest plus the actual Git delta. The validator counts affected skill roots and declared cross-skill/routing surfaces, then rejects uncertain or negative broad units that alter default routing, remove the old path, register stable, or claim improvement. Broad positive claims additionally require existing repo-relative baseline/outcome refs, executable before/after or operational checks, measured costs, and zero-exit rollback argv; a narrative evidence link or prose rollback alone fails. A known-bad default removal remains a separate positive unit and cannot name an uncertain prototype as its replacement.

## Validation

From the skill root:

```bash
python3 scripts/lint_skill_package.py .
python3 -m unittest discover -s tests -v
python3 scripts/run_skill_evals.py evals/evals.json --validate-only
python3 scripts/check_architect_output.py captured-output.md
python3 scripts/run_skill_evals.py evals/evals.json --outputs-dir /tmp/dbx-architect-outputs
python3 scripts/run_skill_evals.py evals/evals.json --captured-output /tmp/one-output.md --case-id positive-create-full-tool-skill-with-scripts
python3 scripts/create_skill_skeleton.py --name example-skill --description "Use when reviewing recurring release plans that need validation, handoff, and rollback criteria." --output /tmp/dbx-skeleton-test
python3 scripts/validate_change_manifest.py /path/to/change-manifest.json --repo-root /path/to/repo --scope staged
```

The eval runner validates schema and can score saved outputs. Use `--outputs-dir` for per-case files named `<eval-id>.md` or `--captured-output` with an explicit `--case-id`. It refuses to score one captured output against every eval case. It does not call an LLM.

## Package Files

```text
SKILL.md
README.md
CHANGELOG.md
references/asct-0.3-application.md
references/placement-and-host-artifacts.md
assets/templates/placement-decision.template.md
evals/evals.json
evals/triggers.json
scripts/eval_schema.py
scripts/run_skill_evals.py
scripts/check_architect_output.py
scripts/lint_skill_package.py
scripts/create_skill_skeleton.py
scripts/validate_change_manifest.py
tests/test_run_skill_evals.py
tests/test_eval_schema.py
tests/test_validate_change_manifest.py
assets/change-manifest.schema.json
assets/templates/change-manifest.example.json
```
