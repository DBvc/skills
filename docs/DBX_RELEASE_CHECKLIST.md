# DBX Skill Release Checklist

Use this before merging or publishing skill changes.

## 1. Scope

- [ ] Change type is clear: repo architecture, architect skill, or individual skill.
- [ ] Affected files are listed.
- [ ] Existing skill identity is preserved unless a rebuild is explicitly justified.
- [ ] Non-trivial changes have a patch hypothesis.

## 2. Skill Validity

- [ ] Every skill directory has `SKILL.md`.
- [ ] `name` matches the directory name.
- [ ] `description` states what the skill does and when to use it.
- [ ] `SKILL.md` is not overloaded with long reference material.
- [ ] File references use relative paths.

Command:

```bash
python3 scripts/validate_skills.py --root .
```

## 3. Trigger Quality

- [ ] Description covers explicit and implicit triggers.
- [ ] Near-miss cases are documented.
- [ ] Non-use boundaries are clear.
- [ ] `evals/triggers.json` exists for serious skills.

Command:

```bash
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## 4. Output Quality

- [ ] Output contract is handoff-ready.
- [ ] Evidence and uncertainty policies are explicit where needed.
- [ ] The skill does not invent validation, facts, motives, source data, or user intent.
- [ ] Domain/content skills include domain variables, hidden failure modes, data-source policy, expert rubric, and examples.

## 5. Scripts and Tools

- [ ] Scripts are non-interactive.
- [ ] Scripts have `--help`.
- [ ] Errors say what went wrong and what to try.
- [ ] Structured output goes to stdout.
- [ ] Diagnostics go to stderr.
- [ ] Destructive actions require explicit confirmation or dry-run first.

## 6. Evals and Regression

- [ ] Positive cases exist.
- [ ] Negative cases exist.
- [ ] Near-miss cases exist.
- [ ] Failure-mode or safety cases exist where relevant.
- [ ] Old behavior was compared with new behavior for meaningful changes.
- [ ] Regression risks are documented.

## 7. Repository Consistency

- [ ] README skill list matches `skills/`.
- [ ] `DBX_SKILL_INDEX.md` is updated.
- [ ] Inventory script output has been reviewed.
- [ ] No private local paths or machine-specific assumptions were added.

Command:

```bash
python3 scripts/skill_inventory.py --root . --format markdown
```

## 8. Release Note

Use this mini template:

```text
Change:
Why:
Targeted failure:
Validation:
Regression risk:
Rollback:
```
