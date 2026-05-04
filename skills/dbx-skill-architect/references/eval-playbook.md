# Eval playbook

Use evals to test behavior, not decorative compliance.

## Eval layers

### Trigger evals

Test whether the skill should activate:

```text
positive: should clearly trigger
negative: should clearly not trigger
near_miss: adjacent but should not trigger
failure_mode: should reveal a known failure
safety: unsafe or boundary-sensitive case
```

Store trigger evals in `evals/triggers.json` when using the DBX repo runner.

### Runner evals

Use `evals/evals.json` for output and process assertions. The v7 runner schema uses:

```json
{
  "skill_name": "example-skill",
  "pass_threshold": 0.85,
  "evals": [
    {
      "id": "positive-primary-1",
      "kind": "positive",
      "prompt": "...",
      "expected_behavior": "...",
      "checks": {
        "trigger": [{"type": "must_contain", "value": "structural marker", "required": true, "quality": "structural"}],
        "process": [{"type": "regex", "value": "behavior or artifact assertion", "required": true, "quality": "behavior"}],
        "output": [],
        "safety": []
      },
      "pass_criteria": {"all_required": true, "min_score": 0.85}
    }
  ]
}
```

Allowed check types in the bundled runner:

- `must_contain`
- `must_not_contain`
- `must_start_with`
- `regex`

Each check must include `required: true|false`. Newer DBX evals should also include `quality`:

- `structural`: headings, route markers, file names, directory markers;
- `behavior`: checks that the model made the right decision or followed the right process;
- `artifact`: checks generated files, scripts, fixtures, or runnable commands;
- `specificity`: checks concrete variables, target files, exact edit units, or non-generic decisions;
- `domain`: checks domain variables, stale-data rules, or expert failure modes;
- `safety`: checks refusal, escalation, consent, privacy, or authority boundaries;
- `validation`: checks proof, schema, runner compatibility, or regression behavior.

A case must have at least one required non-marker quality check. A suite that only checks `## Summary`, `SKILL.md`, `scripts/`, or `route: full_skill` should fail schema validation.

### Human rubrics

Use a human rubric when quality is real but not fully mechanical: taste, architecture judgment, relationship nuance, decision quality, research synthesis.

Do not call a human rubric `evals.json`. Name it `human-rubric.md` or put it in a reference file.

## Minimum coverage

A serious skill should include:

- 2 positive cases;
- 1 negative case;
- 1 near-miss case;
- 1 failure_mode or safety case.

Domain/content skills should also include at least 2 checks for domain variables, hidden failure modes, or data policy.

## Baseline comparison

When improving a skill, compare:

```text
old skill -> same prompt -> output A
new skill -> same prompt -> output B
```

When creating a new skill, compare:

```text
without skill -> output A
with skill -> output B
```

Track:

- output pass rate;
- human rubric score;
- token/context cost when available;
- tool/runtime cost when relevant;
- regression count.

## Assertion design

Good assertions are observable:

- output starts with the required YAML contract;
- output routes `domain_discovery` when domain gates are unknown;
- output does not include `SKILL.md` for one-off tasks;
- output includes `patch_hypothesis` for non-trivial improvements;
- eval JSON uses only canonical `kind` values;
- marker-only outputs fail unless they also satisfy behavior, artifact, specificity, domain, safety, or validation assertions;
- generated full-skill packages provide real file bodies, not filename lists.

Weak assertions are vague or brittle:

- output is good;
- output sounds expert;
- output contains exactly this long phrase;
- output has many sections.

## Running bundled checks

From the skill root:

```bash
python3 scripts/lint_skill_package.py .
python3 scripts/run_skill_evals.py evals/evals.json --validate-only
python3 scripts/run_skill_evals.py evals/evals.json --outputs-dir captured_outputs
python3 scripts/check_architect_output.py captured-output.md
```

The runner does not call an LLM. It validates schema and can score captured outputs if you save them as `captured_outputs/<eval-id>.md` or `.txt`.
