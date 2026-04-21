# Domain Discovery / 领域发现

Use this reference when the user wants a domain/content skill, such as travel planning, news releases, repair diagnosis, relationship analysis, social content, sports prediction, investment framework, hiring rubrics, technical architecture, teaching material, or incident analysis.

A domain skill is not production-ready merely because it has triggers, workflow, output contract, and evals. It must know what makes output **useful in that domain**.

## Contents

- Domain substance gates
- Domain discovery questions
- Failure knowledge extraction
- Domain content contract
- Examples across domains
- Anti-surface checks

## Domain substance gates

```yaml
domain_substance_gates:
  target_user_defined: pass | fail | unknown | not_applicable
  output_depth_defined: pass | fail | unknown | not_applicable
  domain_variables_identified: pass | fail | unknown | not_applicable
  data_source_policy_defined: pass | fail | unknown | not_applicable
  failure_knowledge_identified: pass | fail | unknown | not_applicable
  expert_quality_rubric_defined: pass | fail | unknown | not_applicable
  worked_example_available: pass | fail | unknown | not_applicable
```

If these are mostly `unknown`, route to `domain_discovery`, not `full_skill`.

## Core domain discovery questions

Ask only the most relevant 5-10 questions. Do not dump all of them.

1. Who will actually use the output, and in what situation?
2. What artifact should the skill produce: checklist, memo, itinerary, diagnosis, script, report, plan, rubric, or decision table?
3. What output depth is required: quick, standard, deep, or operational?
4. What concrete variables must be present for the output to be useful?
5. Which variables, if omitted, make the result look complete but fail in real use?
6. What are the common novice mistakes, hidden costs, anti-patterns, or traps?
7. What would a domain expert check first to judge quality?
8. Which facts must be real-time, user-provided, cited, estimated with label, or marked unknown?
9. Do you have one good sample and one bad sample?
10. What 5 eval cases would expose surface-level answers?

## Failure knowledge extraction

Failure knowledge is the domain's negative expertise: things that look plausible but fail in reality.

Ask:

```text
- What do beginners usually miss?
- What looks efficient but creates hidden cost?
- What sounds impressive but is not actionable?
- What assumptions often break in real environments?
- Which output fields are non-negotiable?
- What must be verified before execution?
- What mistakes create safety, privacy, money, legal, or reputation risk?
```

## Domain content contract

For domain/content skills, produce this before drafting the final package:

```yaml
domain_content_contract:
  target_user: ""
  artifact_type: ""
  output_depth: "quick | standard | deep | operational"
  required_variables: []
  hidden_failure_modes: []
  expert_quality_checks: []
  data_source_policy:
    realtime_required: []
    user_provided_required: []
    can_estimate_with_label: []
    must_not_fabricate: []
  uncertainty_policy: []
  must_not_omit: []
  worked_examples_needed: []
  domain_eval_cases: []
```

Weak contract smells:

- `required_variables` contains only generic terms like "context" or "quality".
- `hidden_failure_modes` is empty or only repeats safety policy.
- No distinction between real-time facts, estimates, assumptions, and unknowns.
- No expert-quality checks.
- Evals only check section headings, not usefulness.

## Examples across domains

### Travel itinerary planner

Required variables might include dates, origin, destinations, budget, traveler type, mobility, transport preferences, hotel zone, time windows, distance/transfer time, weather sensitivity, reservations, ticketing, and backup options.

Hidden failure modes might include holiday crowds, impossible transfer times, missing ticket reservations, underestimating walking/climbing, wrong hotel district, unverified opening hours, no rainy-day alternative, hidden transport costs, and vague budget handling.

Expert checks might include: day-by-day timing, transfer table, budget split, accommodation-zone logic, energy level, backup plans, real-time verification checklist.

### News release writer

Required variables might include announcement type, audience, facts, quotes, metrics, embargo, legal review, brand voice, boilerplate, and media target.

Hidden failure modes might include fabricated quotes, unverified metrics, vague headline, missing news hook, unsupported superlatives, legal/PR risk, and mixing ad copy with news release.

### Repair diagnosis

Required variables might include device/model, symptoms, recent changes, tools available, safety boundary, observation steps, and stop conditions.

Hidden failure modes might include replacing parts before diagnosis, unsafe disassembly, treating symptom as root cause, ignoring power/fuel/sensor basics, and lacking escalation criteria.

### Relationship interpretation

Required variables might include exact words, context, recent events, relationship pattern, user's goal, consent boundary, and desired communication style.

Hidden failure modes might include mind-reading, manipulation, overfitting one message, ignoring context, and turning uncertainty into accusation.

### Sports prediction

Required variables might include objective, teams, date, injuries, lineup rotation, fixture congestion, home/away, odds baseline, style matchups, and uncertainty metric.

Hidden failure modes might include overvaluing recent streaks, ignoring injuries/rotation, treating probability as certainty, and cherry-picking stats.

### Technical architecture

Required variables might include current pain, scale, constraints, migration path, rollback, ownership, interface boundaries, tests, and adoption plan.

Hidden failure modes might include big-bang rewrite, premature abstraction, moving complexity to the wrong layer, missing migration cost, and optimizing local metrics.

## Anti-surface checks

A domain skill is surface-level if it:

- produces generic advice that could fit any domain;
- lacks concrete required variables;
- lacks hidden failure modes;
- has no data-source policy;
- has no expert-quality rubric;
- has no worked example;
- evals only test headings and not domain usefulness;
- avoids specifics entirely instead of separating confirmed / estimated / unknown.
