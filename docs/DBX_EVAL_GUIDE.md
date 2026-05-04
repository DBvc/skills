# DBX Skill Evaluation Guide

## 1. Evaluation Philosophy

A skill is not better because it is longer, stricter, or more elegant. It is better if it improves real task outcomes under realistic prompts without unacceptable trigger, token, time, safety, or maintenance cost.

Evaluate three things separately:

1. Trigger behavior: should the skill activate?
2. Process behavior: did the agent follow the right workflow after activation?
3. Output behavior: is the result useful, grounded, safe, and handoff-ready?

## 2. Trigger Evals

File:

```text
skills/<skill-name>/evals/triggers.json
```

Recommended schema:

```json
{
  "skill_name": "dbx-example",
  "version": "0.1",
  "cases": [
    {
      "id": "positive-explicit-1",
      "kind": "positive",
      "prompt": "帮我根据这个 diff 写 PR 描述",
      "expected_trigger": true,
      "rationale": "Explicit request for the skill's core task."
    }
  ]
}
```

Allowed `kind` values:

```text
positive
negative
near_miss
failure_mode
safety
```

Minimum coverage:

| Kind | Minimum | Purpose |
|---|---:|---|
| positive | 4 | explicit and implicit true triggers |
| negative | 2 | unrelated tasks |
| near_miss | 2 | adjacent tasks that should not trigger |
| failure_mode | 1 | known ambiguity or tricky wording |
| safety | 1 when relevant | unsafe or boundary-sensitive requests |

## 3. Output Evals

File:

```text
skills/<skill-name>/evals/evals.json
```

Recommended schema:

```json
{
  "skill_name": "dbx-example",
  "pass_threshold": 0.85,
  "evals": [
    {
      "id": "positive-primary-1",
      "kind": "positive",
      "prompt": "Realistic user task here.",
      "expected_behavior": "What a successful run should do.",
      "checks": {
        "trigger": [],
        "process": [],
        "output": [],
        "safety": []
      },
      "pass_criteria": {
        "all_required": true,
        "min_score": 0.85
      }
    }
  ]
}
```

Good checks are specific:

- detects mixed diff and stops before drafting;
- separates fact, assumption, and judgment;
- includes exact validation evidence or says not run;
- refuses unsafe surveillance request;
- produces a handoff-ready review finding with evidence.

Weak checks are vague or brittle:

- “output is good”;
- “uses exactly this phrase” when wording is not essential;
- only checks headings but not usefulness.

## 4. Baseline Comparison

When improving a skill, compare:

```text
old skill -> new skill
```

When creating a new skill, compare:

```text
no skill -> with skill
```

Record:

```json
{
  "case_id": "positive-primary-1",
  "old_score": 0.62,
  "new_score": 0.84,
  "token_delta": "+18%",
  "time_delta": "+7%",
  "regression": false,
  "notes": "New version caught mixed scope and refused to fabricate validation."
}
```

A skill can spend more tokens if it buys real reliability. It should not spend more tokens just to sound more structured.

## 5. Human Rubric

Use human rubric for quality that cannot be fully scripted:

- code review usefulness;
- decision quality;
- relationship communication safety;
- visual taste;
- domain expertise;
- writing voice.

Rubric template:

```text
Score 5: Excellent. Specific criteria.
Score 4: Good, minor gaps.
Score 3: Acceptable but shallow or incomplete.
Score 2: Misleading, brittle, or low value.
Score 1: Unsafe, wrong, or unusable.
```

Require evidence for every score. A review without evidence is just a weather report from inside a cave.

## 6. Regression Set

Every skill should preserve a small regression set:

- one primary success case;
- one common edge case;
- one near-miss case;
- one safety or boundary case when relevant;
- one historical failure that motivated an improvement.

## 7. Commands

```bash
# Validate trigger eval schema
python3 scripts/run_trigger_evals.py --root . --validate-only

# Emit a Markdown pack for manual or agent-based trigger testing
python3 scripts/run_trigger_evals.py --root . --emit-agent-pack trigger-eval-pack.md

# Validate skill structure and output eval JSON shape
python3 scripts/validate_skills.py --root .
```
