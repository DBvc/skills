# dbx-crystallize

`dbx-crystallize` turns fuzzy product/software intent into a precise, bounded, testable requirement contract before product judgment, design judgment, technical planning, or implementation.

It is designed as the upstream "需求结晶" layer for the DBX skill collection.

## Install

This package is laid out as a repository overlay:

```text
skills/dbx-crystallize/...
```

Unzip it at the root of `DBvc/skills`, then optionally copy the snippets in `references/repo-integration.md` into the repository README, skill index, and routing matrix.

## Primary use

Use when the user says things like:

- "先别写代码，帮我把这个想法澄清成需求。"
- "把这个 issue 写成可开发、可验收的合同。"
- "帮我补 scope、non-goals、验收标准、边界状态。"
- "这个需求讨论前先 crystallize 一下。"

## Not for

- Product-worth judgment: use `dbx-product-judgment`.
- UI/design correctness: use `dbx-design-judgment`.
- Technical implementation planning: use `dbx-technical-plan` after requirements are clear.
- Code review, implementation, commit/PR writing, or formal DBX software plan-first phases.

## Package contents

```text
SKILL.md
README.md
references/
  core-model.md
  question-bank.md
  output-contracts.md
  quality-rubric.md
  repo-integration.md
assets/
  feature-contract-template.md
  issue-contract-template.md
evals/
  triggers.json
  evals.json
```

## Local checks

From the repository root:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

Because this zip does not overwrite repository-level files, `validate_skills.py` may warn that README or `DBX_SKILL_INDEX.md` do not yet mention `dbx-crystallize`. Use `references/repo-integration.md` for the suggested snippets.
