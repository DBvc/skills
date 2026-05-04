# Skill archetypes and failure-mode recipes

Use this file when a scenario can be implemented in several ways. The archetype is not a label for the user. It is an implementation decision.

## Core rule

Choose architecture by dominant failure mode:

```text
failure mode -> control surface -> artifact to add
```

A good skill reduces the right kind of freedom. A poor skill reduces freedom everywhere and becomes a tiny bureaucracy with a markdown hat.

## Archetypes

### Procedure skill

Use for repeatable workflows such as reviews, releases, commit/PR drafting, incident triage, decision memos, or debugging loops.

Common failures:

- Step order is skipped.
- The agent overfits to chat history instead of source evidence.
- Output is not handoff-ready.
- Risky actions happen without approval.

Implementation:

- Put workflow, gates, and output contract in `SKILL.md`.
- Put examples and rubrics in `references/`.
- Add scripts only for mechanical checks.
- Add evals for positive, negative, near-miss, failure, and safety cases.

Eval focus:

- Correct route.
- Evidence used.
- Required sections present.
- Failure modes caught.
- No unsafe escalation.

### Tool skill

Use for file formats, CLI workflows, APIs, schemas, rendering, transformation, or validation.

Common failures:

- Invalid generated files.
- Broken command sequence.
- Missing dependencies.
- The agent guesses format details.
- Output is not re-opened, tested, or validated.

Implementation:

- Keep `SKILL.md` short.
- Put fragile operations in `scripts/`.
- Give scripts `--help`, non-interactive arguments, clear errors, and structured output.
- Put format notes and gotchas in `references/`.
- Add artifact validation evals.

Eval focus:

- Generated artifact opens.
- Schema passes.
- Expected files exist.
- Edge cases fail clearly.

### Knowledge skill

Use when quality depends on correct sources, current facts, policies, APIs, or domain documentation.

Common failures:

- Fabricated facts.
- Stale assumptions.
- Missing citations or source-of-truth checks.
- Overconfident answers when evidence is weak.

Implementation:

- Define source hierarchy.
- Require citation or provenance policy.
- Mark current, user-provided, estimated, and unknown facts separately.
- Add maintenance policy for changing domains.

Eval focus:

- Uses correct source type.
- Does not invent missing facts.
- Flags stale or unstable facts.
- Separates fact, assumption, and judgment.

### Taste skill

Use for visual design, writing, storytelling, cards, presentations, UI polish, tone, or personal style.

Common failures:

- Generic default output.
- Template-like symmetry.
- Style overpowers purpose.
- Rubric is vague and cannot guide revision.

Implementation:

- Put taste principles, examples, anti-patterns, and critique rubric in `references/`.
- Put reusable templates or visual assets in `assets/`.
- Keep `SKILL.md` focused on when to use the taste layer and how to choose output mode.
- Use human rubric evals when deterministic checks are insufficient.

Eval focus:

- Output serves the content goal.
- Avoids listed anti-patterns.
- Has a clear design or writing direction.
- Human reviewer can compare before/after.

### Decision skill

Use for high-impact choices with trade-offs, uncertainty, irreversible steps, or user-specific constraints.

Common failures:

- The agent gives a recommendation before framing the decision.
- Trade-offs are flattened.
- Uncertainty is hidden.
- Validation actions are missing.

Implementation:

- Use gates for decision worthiness.
- Separate facts, assumptions, preferences, constraints, and judgments.
- Add option comparison and reversible next steps.
- Avoid pretending to optimize what is actually preference-sensitive.

Eval focus:

- Identifies decision type.
- Separates facts from assumptions.
- Names blocking information.
- Gives validation actions instead of false certainty.

### Research skill

Use for paper reading, market maps, topic histories, evidence synthesis, or domain evolution.

Common failures:

- Summary without research question.
- Missing lineage or contradictory evidence.
- Citation laundering.
- No update or recency policy.

Implementation:

- Define source strategy.
- Require question framing and evidence map.
- Separate primary sources, secondary commentary, and speculation.
- Add contradiction and freshness handling.

Eval focus:

- Research question is explicit.
- Sources are appropriate.
- Claims map to evidence.
- Unknowns and conflicts are preserved.

### Coordination skill

Use for subagents, independent review, context isolation, delegation, synthesis, or handoff.

Common failures:

- Reviewer contamination.
- Duplicated work.
- Parent agent leaks conclusions into child tasks.
- Synthesis hides disagreement.

Implementation:

- Define parent, child, reviewer, and synthesizer roles.
- Specify context inheritance rules.
- Make handoff artifacts explicit.
- Preserve dissent and confidence.

Eval focus:

- Context boundaries are respected.
- Independent reviewers stay independent.
- Synthesis cites which worker found what.
- Disagreement is not flattened.

### Meta skill

Use for creating, critiquing, improving, or evaluating other skills.

Common failures:

- One-off prompt becomes an overbuilt full package.
- Structure is clean but domain substance is empty.
- Eval only checks headings.
- Improvement is asserted but not tested.

Implementation:

- Fail closed on full creation.
- Add skill shape and failure-mode classification.
- Use patch hypotheses for improvement.
- Require trigger and output evals.

Eval focus:

- Correctly refuses overbuilt requests.
- Routes domain-discovery cases.
- Produces compatible eval artifacts.
- Patches rather than rebuilds by default.

## Failure-mode control table

| Failure mode | Primary control | Secondary control |
|---|---|---|
| `wrong_trigger` | description, trigger evals | near-miss examples |
| `context_bloat` | references, progressive loading | short main file |
| `domain_shallow` | domain contract | examples, content evals |
| `fragile_operation` | scripts | schema, dry run, validation |
| `unverified_output` | output contract | proof, regression cases |
| `taste_collapse` | taste rubric | examples, anti-patterns |
| `safety_overreach` | hard gates | approval, safer redesign |
| `handoff_failure` | recipient contract | next-action checklist |
| `maintenance_drift` | source/version policy | update evals |

## Hybrid rule

A hybrid skill should still name one dominant failure mode. If all failure modes are equally important, the scenario is probably too broad. Split it or create a root router plus smaller specialized skills.
