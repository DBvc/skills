# dbx-product-judgment

A DBX skill for evidence-bounded product correctness judgment across domains.

## Repository Status

This skill is already integrated in this repository at:

```text
skills/dbx-product-judgment/
```

Run repository checks from the repo root after changing it:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## Routing

Use for evidence-bounded product correctness judgment. If the request becomes
ordinary concrete code diff review, route that part to `dbx-diff-review`. If it
becomes a high-impact non-product go/no-go decision, route to
`dbx-decision-framing`.

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
