# dbx-skill-portfolio-auditor

Manual-only skill for auditing installed or repository skills and recommending installation scope changes: global, repo/project, explicit-only, disabled pending review, uninstall/archive, or merge/refactor.
It also flags likely trigger overlap between skills by comparing descriptions and `evals/triggers.json` positive, negative, and near-miss prompts.

This skill is intentionally configured as explicit-only for Codex through `agents/openai.yaml` because portfolio audits are infrequent, privacy-sensitive, and should not accidentally trigger during normal work.

## Repository Status

This skill is already integrated in this repository at:

```text
skills/dbx-skill-portfolio-auditor/
```

Run repository checks from the repo root after changing it:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## Routing

This skill is explicit/manual-only. Use it when the user names
`$dbx-skill-portfolio-auditor` or launches it from the skill UI. For generic
skill cleanup questions, ask whether to run it. Use `dbx-skill-architect` for
creating, critiquing, improving, or evaluating one skill.

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
