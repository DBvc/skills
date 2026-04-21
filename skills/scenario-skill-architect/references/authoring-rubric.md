# Authoring Rubric

Score each dimension from 0 to 2.

## Core skill quality

1. Scenario clarity: recurring user, context, stable job.
2. Trigger precision: clear use and non-use cases.
3. Hard gates: repeatability, stable job, evaluability, safety.
4. IR quality: objects, states, events, evidence, hypotheses, constraints, risky boundaries.
5. Workflow: ordered, bounded, no missing critical steps.
6. Evidence discipline: distinguishes observation, evidence, inference, and assumption.
7. Freedom control: scripts/templates/tools for fragile operations.
8. Output contract: schema-like, handles confidence, blockers, missing information.
9. Eval coverage: positive, negative, near-miss, failure_mode or safety.
10. Runner compatibility: eval JSON validates with `run_skill_evals.py`.
11. Maintainability: concise SKILL.md, shallow references, clear scripts.
12. Regression posture: has captured-output or ablation plan.

## Domain/content quality

Use these for domain/content skills. Score `not_applicable` only when the skill is not domain/content oriented.

13. Domain variables: concrete required variables are identified, not generic placeholders.
14. Failure knowledge: hidden pitfalls, anti-patterns, novice traps, or hidden costs are captured.
15. Data-source policy: separates real-time facts, user-provided facts, estimates, and unknowns.
16. Expert quality rubric: defines how an expert would judge the output.
17. Worked examples: includes good/bad or complete simulated examples.
18. Content-quality evals: evals catch shallow but well-formatted output.

## Interpretation

- 30-36: production candidate for domain/content skill
- 24-29: good draft, needs hardening
- 18-23: useful prompt, not yet a robust skill
- below 18: redesign from scenario and domain discovery cards

For non-domain skills, use dimensions 1-12:

- 20-24: production candidate
- 16-19: good draft, needs hardening
- 10-15: useful prompt, not yet a skill
- below 10: redesign from scenario card
