# dbx-technical-plan

Lightweight DBX skill for technical implementation planning before code changes.

## Install

From the repository root, unzip the package so it creates:

```text
skills/dbx-technical-plan/
```

Then run the normal local checks from the DBX skills repository:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## What this skill adds

- A stateless planning controller between loose discussion and implementation.
- A bounded plan contract: goal, non-goals, evidence, source of truth, invariants, slices, validation, risks, and handoff.
- A dynamic-workflow-compatible thought pattern without requiring a specific host runtime.
- OpenAI product metadata in `agents/openai.yaml`.

## Suggested DBX index entry

Add something like this to the stable skill list when you promote it:

```markdown
- `dbx-technical-plan`: 证据边界内的软件技术实施规划：在写代码前收敛 goal、non-goals、source of truth、不变量、实施切片、验证模型、风险和 handoff。Evidence-bound technical implementation planning before code changes.
```

## Suggested routing note

```text
Use dbx-technical-plan after product/design/decision direction is clear and before implementation. Use dbx-linus-review for strict critique of an existing plan, dbx-diff-review for concrete diffs, dbx-code-ratchet for explicit bounded repair, and dbx-software-plan-first-* for stateful plan-first workflows.
```
