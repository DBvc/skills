# Content quality rubric

Use this for domain, taste, decision, and research skills where output quality cannot be fully validated by scripts.

## Content substance checks

A strong content skill names:

- target user and use context;
- artifact type and expected depth;
- required variables;
- hidden failure modes;
- data-source policy;
- uncertainty policy;
- expert quality rubric;
- examples or anti-examples;
- eval cases that catch plausible but wrong output.

## Signs of shallow output

- It uses correct section headings but could apply to any domain.
- It offers generic tips that ignore user constraints.
- It fails to ask for missing variables that materially change the answer.
- It does not separate current facts, assumptions, and judgments.
- It has no examples of what would look plausible but fail.
- It has no downstream handoff contract.

## Taste quality checks

For visual, writing, or presentation skills, check:

- Is there a clear aesthetic or rhetorical direction?
- Does the style serve the content goal?
- Are anti-patterns concrete enough to guide revision?
- Does the output avoid default AI symmetry and filler?
- Can a human reviewer compare two outputs using the rubric?

## Decision quality checks

For decision skills, check:

- Is the decision type explicit?
- Are facts, assumptions, values, and judgments separated?
- Are options compared against user-relevant criteria?
- Are irreversible risks named?
- Are validation actions concrete?
- Does the output avoid fake certainty?

## Research quality checks

For research skills, check:

- Is the research question explicit?
- Are primary and secondary sources separated?
- Are recency and update policy defined?
- Are contradictions preserved?
- Are unknowns named instead of filled with confident fog?

## Human scoring template

```yaml
human_rubric:
  domain_substance: 1-5
  trigger_fit: 1-5
  output_usefulness: 1-5
  evidence_quality: 1-5
  hidden_failure_handling: 1-5
  handoff_readiness: 1-5
  notes: ""
```

## Domain specificity test

A domain contract is weak when the important variables still make sense after replacing the domain name with another domain. For example, `audience, goals, constraints, examples, success criteria` can apply to travel, investing, visual design, and relationship advice, so those words alone do not pass the domain gate.

A stronger contract names variables that change the answer materially:

- travel: season, visa/passport, transport schedule, booking windows, opening hours, mobility, budget, local disruptions;
- relationship: observable facts, assumptions, motive inference, consent, privacy, safety escalation, power dynamics;
- investment: source date, jurisdiction, time horizon, liquidity need, tax treatment, risk tolerance, fact/assumption/judgment separation;
- visual/taste: message hierarchy, artifact medium, aspect ratio, typography, density, accessibility, anti-pattern examples.

## Eval quality checks

A runner eval is shallow when its required checks only test:

- section headings such as `## Summary`;
- file names such as `SKILL.md` or `evals/evals.json`;
- route markers such as `route: full_skill`;
- directory markers such as `scripts/` or `references/`.

Those checks are useful as structural checks, but each eval case should also include at least one required quality assertion that catches behavior, artifact validity, domain specificity, safety, or validation quality.
