# dbx-skill-portfolio-auditor

Audit installed or repository skills and recommend installation scope changes: global, repo/project, explicit-only, disabled pending review, uninstall/archive, or merge/refactor.
It also flags likely trigger overlap between skills by comparing descriptions and `evals/triggers.json` positive, negative, and near-miss prompts.

This skill is intentionally configured as explicit-only for Codex through `agents/openai.yaml` because portfolio audits are infrequent, privacy-sensitive, and should not accidentally trigger during normal work.

## Install in DBX skills

Unzip this package at the repository root:

```bash
cd /path/to/DBvc/skills
unzip /path/to/dbx-skill-portfolio-auditor.zip
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

Then add the skill to repository-level docs.

Suggested `README.md` stable-skill row:

```markdown
[dbx-skill-portfolio-auditor](skills/dbx-skill-portfolio-auditor) Audit installed skills and decide global, project-scoped, explicit-only, disabled, or uninstall/archive placement.
```

Suggested `DBX_SKILL_INDEX.md` row:

```markdown
| `dbx-skill-portfolio-auditor` | Audit installed skills and recommend global/repo/explicit/disable cleanup. | meta + collection workflow + tool | L5 | Usage evidence and privacy boundaries can be weak if the user does not provide data. | Explicit/manual trigger; supports collection governance and may hand off single-skill creation to `dbx-skill-architect`. | Add baseline comparison with a real local portfolio audit after first use. |
```

Suggested routing note:

```markdown
- `dbx-skill-portfolio-auditor` is for installed-skill portfolio optimization. `dbx-skill-architect` remains the route for creating, critiquing, or improving one skill.
```

## Typical usage

```bash
# Inventory common local skill roots and repo skill roots.
python3 skills/dbx-skill-portfolio-auditor/scripts/inventory_installed_skills.py \
  --include-repo \
  --redact-paths \
  --format json \
  --output /tmp/skill-inventory.json

# Produce a conservative first-pass analysis.
python3 skills/dbx-skill-portfolio-auditor/scripts/analyze_skill_inventory.py \
  /tmp/skill-inventory.json \
  --format markdown \
  --output /tmp/skill-portfolio-analysis.md
```

Optional usage evidence file:

```json
{
  "skill_usage": {
    "dbx-work-commit-pr": {
      "explicit_invocations": 12,
      "notes": "Used for work PRs almost every week"
    },
    "some-rare-migration-skill": {
      "explicit_invocations": 1,
      "notes": "Rare but useful; should be explicit-only"
    }
  }
}
```

## Safety notes

- The inventory script does not access the network and does not modify files.
- The analysis script is heuristic. It cannot prove a skill is unused.
- Deleting, disabling, or moving skills should remain a reviewed, reversible change.
