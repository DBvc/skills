# Changelog

## v7.2

- Strengthens `check_architect_output.py` from marker checks to artifact-body validation.
- Requires `full_skill` outputs to provide fenced file blocks for `SKILL.md`, `evals/evals.json`, and `evals/triggers.json`.
- Parses generated `SKILL.md` frontmatter and validates generated eval JSON artifacts.
- Adds anti-placeholder validation for generated full-skill artifacts and generated skeletons.
- Adds eval-quality lint: every eval case needs at least one required non-marker quality check.
- Adds shape-specific done criteria for tool/fragile, coordination, review/procedure, and domain/content skills.
- Allows `needs_clarification` to use `archetype: unknown` when blocking questions are present.
- Makes patch hypotheses more concrete with `target_files` and `exact_edit_units`.
- Adds `references/domain-starter-packs.md` for travel, relationship, investment, and visual/taste starter variables and failure modes.

## v7.1

- Removes internal version wording from runtime `SKILL.md` and optional agent metadata.
- Strengthens `check_architect_output.py` so hard gates, domain gates, skill shape, patch hypothesis, self-check, and full-package eval artifacts are validated as errors where required.
- Treats minimum eval coverage as schema errors rather than warnings.
- Requires runner eval cases to include at least one required check.
- Restores `create_skill_skeleton.py` output semantics: `--output` is the parent directory and the script creates `<output>/<name>/`.
- Expands bundled eval templates so newly generated skeletons pass the stricter validator.

## v7.0

- Adds `skill_shape` to the opening decision contract.
- Adds dominant failure-mode analysis.
- Adds patch-hypothesis requirement for non-trivial improvements.
- Adds `references/skill-archetypes.md` and `references/improvement-validation.md`.
- Adds `evals/triggers.json` for DBX repo-level trigger eval validation.
- Rewrites bundled scripts with standard-library-only validation and clearer CLI behavior.
- Keeps fail-closed hard gates, domain substance gates, mode/route/operation compatibility, and runner eval discipline.
