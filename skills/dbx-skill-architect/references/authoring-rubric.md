# Skill authoring rubric

Score each dimension from 1 to 5.

## 1. Reuse worthiness

1: One-off prompt wrapped as a skill.
3: Reusable but broad or loosely bounded.
5: Clear recurring scenario with stable input family, output, and failures.

## 2. Trigger accuracy

1: Description is generic or misleading.
3: Core use is described, but near-miss cases are unclear.
5: Should-trigger, should-not-trigger, and near-miss boundaries are obvious.

## 3. Boundary and safety

1: Unsafe or irreversible behavior is not controlled.
3: Boundaries are named but not operational.
5: Fail-closed gates, approval points, and safer alternatives are explicit.

## 4. Skill shape fit

1: Structure does not match the dominant failure mode.
3: Shape is plausible but not used to guide architecture.
5: Archetype and failure modes clearly determine instructions, references, scripts, assets, and evals.

## 5. Domain substance

1: Generic best practices and polished structure only.
3: Some domain variables or examples are present.
5: Required variables, hidden failure modes, data-source policy, expert rubric, examples, and domain evals are all concrete.

## 6. Freedom calibration

1: Everything is vague or everything is over-constrained.
3: Some fragile steps are controlled.
5: Fragile operations are tightened while judgment and creativity retain useful freedom.

## 7. Tooling and validation

1: Mechanical checks are left to the model.
3: Some scripts or validation steps exist.
5: Fragile, repeatable, or machine-checkable steps are scripted and documented.

## 8. Output contract

1: Output is unspecified or decorative.
3: Required sections exist but evidence and handoff are weak.
5: Output is directly usable by the next human, agent, or tool, with evidence and uncertainty policy.

## 9. Eval quality

1: No evals, or evals only check headings.
3: Basic positive/negative cases.
5: Trigger evals, near-miss cases, failure/safety cases, output checks, and baseline comparison plan.

## 10. Context economy

1: Main file is bloated and mixes everything.
3: Some references exist but main file is still heavy.
5: Main file guides runtime decisions; details are split into focused references, scripts, assets, and evals.

## Production-ready threshold

A production-ready skill should generally score:

```text
Reuse worthiness >= 4
Trigger accuracy >= 4
Boundary and safety >= 4
Skill shape fit >= 4
Eval quality >= 3
Context economy >= 4
```

Tooling is required only when the dominant failure mode includes `fragile_operation`, `unverified_output`, or machine-checkable artifact quality.
