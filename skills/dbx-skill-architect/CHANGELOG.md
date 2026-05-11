# Changelog

## ASCT 0.3 runtime alignment

- Normalizes `SKILL.md`, README, scripts, and eval artifacts into readable multi-line files.
- Adds `placement_decision` to the architect contract so controls are placed in the right carrier before prose is written.
- Adds `state_contract` and `collection_impact` fields for stateful skills and skill-collection routing decisions.
- Keeps ASCT theory out of runtime prose; references point to focused application notes instead.
- Rewrites local validation scripts as executable, standard-library-only Python files.
- Adds placement and host-artifact eval coverage.
- Adds templates and references for ASCT 0.3 placement decisions.

## v7.2

- Strengthened `check_architect_output.py` from marker checks to artifact-body validation.
- Required `full_skill` outputs to provide fenced file blocks for `SKILL.md`, `evals/evals.json`, and `evals/triggers.json`.
- Parsed generated `SKILL.md` frontmatter and validated generated eval JSON artifacts.
- Added anti-placeholder validation for generated full-skill artifacts and generated skeletons.
- Added eval-quality lint: every eval case needs at least one required non-marker quality check.
- Added shape-specific done criteria for tool/fragile, coordination, review/procedure, and domain/content skills.
- Allowed `needs_clarification` to use `archetype: unknown` when blocking questions are present.
- Made patch hypotheses more concrete with `target_files` and `exact_edit_units`.

## v7.1

- Removed internal version wording from runtime `SKILL.md` and optional agent metadata.
- Strengthened hard gates, domain gates, skill shape, patch hypothesis, self-check, and full-package eval artifact validation.
- Treated minimum eval coverage as schema errors rather than warnings.
- Restored `create_skill_skeleton.py` output semantics: `--output` is the parent directory and the script creates `<output>/<name>/`.

## v7.0

- Added `skill_shape` to the opening decision contract.
- Added dominant failure-mode analysis.
- Added patch-hypothesis requirement for non-trivial improvements.
- Added trigger evals.
- Kept fail-closed hard gates, domain substance gates, mode/route/operation compatibility, and runner eval discipline.

## 2026-05-11 - ASCT 0.3 runtime fixup

- Fixed `run_skill_evals.py` so a single captured output can only be scored with an explicit `--case-id`.
- Added `--case-id` support for both `--outputs-dir` and `--captured-output` modes.
- Made package lint hermetic by replacing `py_compile` with `ast.parse`.
- Restored eval schema validation inside `lint_skill_package.py`.
- Removed the one-off birthday-writing prompt from output-eval semantics by turning it into an explicit skill-wrapper triage case.
- Fixed README skeleton command so its description satisfies the generator's minimum specificity requirement.
