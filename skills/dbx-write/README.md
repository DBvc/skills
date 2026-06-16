# dbx-write

A DBX skill for Chinese-first viewpoint writing: technical blogs, personal essays, opinion pieces, Markdown drafts, structural review, editing, and occasional English versions.

## Repository Status

This package is designed to be integrated at:

```text
skills/dbx-write/
```

Run repository checks from the repo root after adding it:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

Also update root `README.md` and `DBX_SKILL_INDEX.md`; see `INTEGRATION.md` in this zip package for suggested snippets.

## Routing

Use when the dominant artifact is a viewpoint-driven written piece.

Route away when the dominant artifact is:

- commit/PR writing;
- code comments or changelog/release notes;
- product/design correctness judgment;
- interpersonal message strategy;
- direct implementation, diff review, or technical plan.

## Shape

```yaml
skill_shape:
  primary: taste
  secondary:
    - writing
    - procedure
    - knowledge
    - evidence
    - light_tool
  dominant_failure_modes:
    - taste_collapse
    - generic_ai_prose
    - unsupported_factual_claims
    - fabricated_personal_experience
    - context_bloat
    - wrong_trigger
    - overediting_author_voice
  implementation_implication: "Keep SKILL.md as the runtime control loop; move style, structure, fact policy, and language-specific rubrics to references; use a small script only for deterministic draft-file creation."
```

## File writer

```bash
python3 skills/dbx-write/scripts/create_draft_file.py \
  --title "AI 改变的不是前端交付，而是判断边界" \
  --output-dir drafts \
  --content-file article.md
```

The script validates safe overwrite behavior and returns JSON.
