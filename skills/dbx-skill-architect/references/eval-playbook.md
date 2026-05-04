# Eval Playbook

## Eval types

- `positive`: should trigger/use the skill.
- `negative`: should not trigger; direct answer or unrelated workflow.
- `near_miss`: similar surface form but should route smaller or differently.
- `failure_mode`: expected common failure.
- `safety`: unsafe or privacy-invasive case requiring refusal/redesign.

## Runner-compatible JSON

Top-level must be:

```json
{
  "skill_name": "example-skill",
  "pass_threshold": 0.85,
  "evals": []
}
```

Each eval must be:

```json
{
  "id": "positive-primary-1",
  "kind": "positive",
  "prompt": "A realistic request that should use the skill.",
  "expected_behavior": "Use the skill workflow and output contract.",
  "checks": {
    "trigger": [{"type": "must_contain", "value": "expected marker", "required": true}],
    "process": [],
    "output": [],
    "safety": []
  },
  "pass_criteria": {"all_required": true, "min_score": 0.85}
}
```

Supported check types:

- `must_contain`
- `must_not_contain`
- `regex`
- `must_start_with`

Do not use string checks. Do not use `cases` as the top-level key. Do not set `all_required` to an array. If you are giving a human rubric, label it `human_rubric`, not `evals.json`.

## Captured-output protocol

Save outputs as:

```text
outputs/<case_id>.md
outputs/<case_id>.txt
outputs/<case_id>/output.md
outputs/<case_id>/output.txt
```

Score:

```bash
python scripts/run_skill_evals.py evals/evals.json --outputs-dir outputs
```

## Ablation

For each major principle, create one test where removing that principle should cause a distinct failure.
