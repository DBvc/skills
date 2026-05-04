# Apply DBX Skills Architecture Update

This package is an overlay for the repository root. It does not modify any existing `skills/<name>/...` files.

## What this package changes

Adds or replaces:

```text
README.md
DBX_SKILL_STYLE_GUIDE.md
DBX_SKILL_INDEX.md
docs/DBX_SKILL_ARCHITECTURE.md
docs/DBX_EVAL_GUIDE.md
docs/DBX_RELEASE_CHECKLIST.md
docs/templates/triggers.example.json
docs/templates/evals.example.json
docs/templates/skill-maturity-card.md
docs/templates/patch-hypothesis.md
scripts/validate_skills.py
scripts/skill_inventory.py
scripts/run_trigger_evals.py
```

## Apply by copying

From your repository root:

```bash
# optional backup
git checkout -b dbx-skill-architecture-update

# copy the package contents over the repo root
cp -R /path/to/dbx-skills-architecture-update/. .

# inspect changes
git diff --stat
git diff
```

## Validate after applying

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/skill_inventory.py --root . --format markdown
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## Notes

- `validate_skills.py` may report frontmatter warnings or errors if existing `SKILL.md` files are not formatted with strict YAML delimiter lines. That is useful signal, not a runtime behavior change.
- Missing `evals/triggers.json` files are warnings. The next phase can add those skill by skill.
