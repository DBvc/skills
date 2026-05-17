# DBX Eval Guide

Evaluation in DBX asks whether a skill changed behavior in the intended direction, on the intended task distribution, without unacceptable cost or risk.

A skill is not better because it is longer, stricter, or more elegant. It is better only if it produces net reliability gain.

## 1. SkillValue Frame

Use this as a decision frame, not a precise formula:

```text
SkillValue = expected_success_delta - added_cost - added_risk
```

Costs include:

- context cost;
- tool/runtime cost;
- user-friction cost;
- maintenance cost;
- trigger conflict cost.

Risks include:

- safety risk;
- privacy risk;
- external side effects;
- over-trigger;
- stale state;
- host compatibility drift.

## 2. Five Eval Targets

| Eval type | Question |
| --- | --- |
| Trigger | Does the skill activate when it should and stay silent when it should not? |
| Process | After activation, does the agent follow the intended trajectory? |
| Output | Is the final result useful, grounded, and correctly shaped? |
| Safety | Does the skill respect safety, privacy, approvals, and external side effects? |
| Regression | Do historical failures stay fixed after changes? |

Most skills start with trigger and output evals. Mature or risky skills add process, safety, and regression evals.

## 3. Baseline Comparison

Compare against at least one baseline when changing a serious skill:

- no skill;
- old skill;
- lighter version;
- competing skill;
- human checklist.

Ask:

```text
What does this skill improve that the base agent did not already do reliably?
```

If the base agent already does the task reliably, the skill may add cost without value.

## 4. Trigger Evals

Trigger evals should include:

- positive explicit cases;
- positive implicit cases;
- negative cases;
- near-miss cases;
- adjacent skill conflicts;
- unsafe or out-of-scope cases.

Near-miss cases are the most valuable. Obvious positives only prove the skill recognizes itself when shouted at.

Example:

```json
{
  "near_miss": [
    {
      "prompt": "This button is broken in production. Find the root cause.",
      "expected": "do_not_activate",
      "prefer": "future frontend-debug skill, not code review"
    }
  ]
}
```

## 5. Process Evals

Process evals check whether the agent followed the critical path.

Examples:

| Skill type | Process checks |
| --- | --- |
| Debug | Establish pass/fail loop before patching; form falsifiable hypothesis; avoid patch stacking. |
| Artifact | Use intended toolchain; validate output; inspect rendered output when needed. |
| Release | Confirm target branch/version/artifacts/approval before external side effects. |
| Decision | Separate facts, assumptions, judgments, unknowns; propose reversible tests. |
| Conversation | Separate observation from motive inference; respect safety and consent boundaries. |
| Skill architect | Route correctly; fail closed on hard gates; require concrete artifacts and evals. |

Process evals matter because the final answer can look good even when the path was unsafe.

## 6. Output Evals

Output evals check final quality:

- task correctness;
- evidence quality;
- unsupported claims;
- severity or confidence calibration;
- actionability;
- adherence to output contract;
- clarity;
- known limitations;
- validation/proof quality.

Avoid marker-only evals. A check that only looks for `## Summary` or `evals/evals.json` is structural, not substantive.

Every serious output eval should include at least one behavior, evidence, safety, validation, or domain-specific assertion.

## 7. Safety Evals

Safety evals should cover:

- destructive commands;
- credential exposure;
- network access;
- external write actions;
- privacy-sensitive files;
- unsafe user intent;
- prompt injection in references or input files;
- cross-skill activation risks;
- stale state or unsafe memory writes.

A safety eval does not merely ask whether the final answer is polite. It asks whether the skill’s control surfaces can produce unsafe behavior.

## 8. Regression Evals

Every important historical failure should become a regression case.

Record:

```yaml
regression_case:
  original_prompt: ""
  expected_activation: ""
  expected_process_behavior: []
  expected_output_properties: []
  known_bad_behavior: ""
  fix_introduced: ""
  rollback_condition: ""
```

## 9. Collection-Level Evals

When adding, renaming, deprecating, or routing skills, evaluate the collection:

- routing correctness;
- conflict resolution;
- cross-skill handoff;
- install subset behavior;
- host compatibility;
- performance with many installed skills;
- regression when a skill is added or removed.

Example collection eval:

```text
Prompt: "Review this diff and write a PR description."
Expected: dbx-diff-review-control first, then appropriate commit/PR skill.
Known bad behavior: commit/PR skill writes polished text before review surfaces blockers or before the diff target is selected.
```

## 10. Evaluation Before Expansion

Before adding more instructions, ask:

```text
Which eval is failing?
Which failure mode does the new instruction target?
What cost does it add?
How will we know it helped?
```

Do not expand `SKILL.md` merely because a rule sounds wise.
