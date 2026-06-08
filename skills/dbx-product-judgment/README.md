# dbx-product-judgment

A DBX skill for evidence-bounded product correctness judgment across domains.

## Install

This zip is shaped for the `DBvc/skills` repository root:

```bash
unzip dbx-product-judgment.zip -d /path/to/skills-repo
python3 scripts/validate_skills.py --root /path/to/skills-repo
python3 scripts/run_trigger_evals.py --root /path/to/skills-repo --validate-only
```

The skill directory will land at:

```text
skills/dbx-product-judgment/
```

## Suggested `DBX_SKILL_INDEX.md` row

Add this row to the Current Stable Skills table when merging:

```markdown
| `dbx-product-judgment` | Evidence-bounded judgment of whether a product, feature, PRD, live UX, IA, interaction, content, implementation, roadmap, or competitor position is product-correct. | product audit + decision + research + implementation alignment | L5 | Unsupported certainty when target user, product artifact, or evidence is missing. | Use for product/feature correctness judgment; if the request becomes ordinary concrete diff review, hand off to `dbx-diff-review`; if it becomes skill creation, hand off to `dbx-skill-architect`. | Add baseline comparison cases after several real audits. |
```

## Shape

```yaml
skill_shape:
  primary: decision
  secondary:
    - product_audit
    - research
    - review
    - implementation_alignment
  dominant_failure_modes:
    - unsupported_product_certainty
    - context_bloat
    - domain_shallow
    - unverified_output
    - fragile_external_observation
  implementation_implication: "Keep SKILL.md as a control loop, move rubrics/playbooks/templates to references and assets, and use the report validator only for handoff structure."
```

## Local checker

```bash
python3 skills/dbx-product-judgment/scripts/validate-product-report.py path/to/report.md
```

The checker validates report shape and evidence markers. It does not validate product truth.
