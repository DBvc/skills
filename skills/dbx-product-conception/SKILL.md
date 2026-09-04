---
name: dbx-product-conception
description: Use when the user wants to discover, invent, reframe, or converge what a not-yet-defined product should be from weak signals, enabling technology, changing behavior, latent human capability, or competing concepts. Produces distinct product logics, concrete experience specimens, a selected product thesis, deliberate non-goals, and a prototype/validation handoff through evidence-labeled creative selection. Prefer dbx-product-judgment when a defined product, feature, PRD, roadmap, or live experience already exists and the question is whether it is valuable, coherent, usable, viable, or worth building. Prefer dbx-crystallize when direction is chosen and requirements or scope need precision. Do not use for generic idea lists, Steve Jobs impersonation, pure design critique, implementation, or unsupported novelty claims.
---

# DBX Product Conception / 产品构想

Create and select product directions before product correctness can be judged.

Core job:

```text
weak signals + enabling changes + human tensions + creator conviction
  -> opportunity frame
  -> distinct product logics
  -> concrete experience specimens
  -> creative selection
  -> selected thesis + kill list + proof handoff
```

This is a search-and-selection controller, not a product oracle. It aims to improve the probability of non-obvious, coherent insight. It does not promise genius, impersonate Steve Jobs, or claim that a selected concept is product-correct.

Default output language follows the user's language. Normal outputs do not mention Jobs unless the user asks for the research basis or explicitly requests Jobs-derived analysis.

## Use / do not use

Use this skill when the primary task is to:

- turn a technology, platform, behavior, cultural, regulatory, cost, or distribution shift into possible native products;
- discover what a product should fundamentally be before a stable concept or PRD exists;
- reframe a conventional feature bundle into a stronger product thesis or category logic;
- generate genuinely different product concepts rather than variants of one feature list;
- compare competing concepts, demos, prototypes, or product logics through creative selection;
- identify the human capability, core object, default interaction, system boundary, magic moment, adoption wedge, and deliberate non-goals of a direction;
- train product taste explicitly through comparative exercises and a judgment ledger.

Do not use this skill for:

- judging whether an already-defined product, feature, PRD, roadmap, implementation, or competitor position is correct or worth building; use `dbx-product-judgment`;
- clarifying a chosen direction into requirements, scope, acceptance criteria, and handoff; use `dbx-crystallize`;
- deciding among high-impact real actions where product conception is not the primary artifact; use `dbx-decision-framing`;
- reviewing fixed-intent UI, flows, screenshots, interaction states, or design systems; use `dbx-design-judgment`;
- generic “give me 20 startup ideas” lists with no request for thesis, structural insight, or selection;
- market summaries, competitor lists, historical explanation, or source reading without a conception task;
- direct implementation, code generation, design production, or external writes;
- pretending to be Steve Jobs, copying his rhetoric, or using aggression as a creativity method.

## Hard gates before conception

Do not generate a confident product thesis until these gates are handled.

1. **Conception seed exists**: at least one arena, enabling change, human situation, structural tension, existing concept to reframe, or candidate set exists.
2. **Conception target is selected**: opportunity synthesis, category reframe, concept generation, creative selection, product thesis, or taste training.
3. **Freedom map is clear**: distinguish fixed constraints from assumptions that may be redesigned. Never treat laws, safety boundaries, contractual facts, or explicit non-goals as mere conventions.
4. **Evidence boundary is clear**: know which user claims, artifacts, prototypes, current sources, historical analogies, and personal convictions may be used.
5. **Proof medium is possible**: define the next experience specimen, prototype, storyboard, role-play, sample artifact, or demo that can expose the concept to reality.
6. **Safety and legitimacy pass**: do not create deceptive, coercive, addictive, non-consensual, discriminatory, privacy-invasive, or access-bypassing products.

If gates 1 to 4 are missing and cannot be inferred, ask up to five blocking questions and stop. If a bounded seed exists, proceed with explicit unknowns rather than turning every uncertainty into an interview.

## Evidence and conviction policy

Keep these categories separate internally and expose them when the distinction matters:

```yaml
conception_evidence_state:
  observed_facts: []
  external_facts: []
  user_experiences_or_claims: []
  historical_lineage: []
  inferences: []
  creator_convictions: []
  product_bets: []
  unknowns: []
  not_verified: []
```

Rules:

- A technology capability is an affordance, not a product and not evidence of demand.
- A user request is evidence of a stated solution or desire, not proof of the underlying problem or best product form.
- A historical analogy generates hypotheses; it does not prove timing, adoption, or market size.
- A compelling story or magic moment is a design hypothesis until a specimen produces observable reactions or behavior.
- A prototype reaction is evidence about comprehension, usability, or immediate desire only within its sample. It does not prove retention, willingness to pay, distribution, or viability.
- Maker conviction is legitimate input for discontinuous creation, but label it as conviction rather than laundering it into user evidence.
- Claims that an idea is first, unique, inevitable, or category-defining require current external research. Otherwise mark them unverified.
- External facts that may have changed require current sources and citations when tools are available.

Load `references/evidence-conviction-and-novelty.md` for formal or research-heavy work.

## Mode routing

Choose the smallest mode that can change the quality of the product direction.

| Mode | Use when | Primary output |
| --- | --- | --- |
| `opportunity_synthesis` | Inputs are weak signals, new capabilities, changing behavior, or a broad arena. | Opportunity frame and candidate human transformations. |
| `category_reframe` | An existing concept is derivative, feature-heavy, or trapped in an old category. | Hidden assumptions, alternative category logics, and a reframed thesis. |
| `concept_generation` | Direction is not selected and distinct alternatives are needed. | Three to five structurally different concepts with experience specimens. |
| `creative_selection` | Several concepts, demos, or prototypes already exist. | Pairwise judgment, eliminations, selected direction, and kill list. |
| `product_thesis` | One direction is emerging but lacks a coherent product model. | Thesis, core object/default, boundary, non-goals, and proof plan. |
| `taste_calibration` | The user explicitly wants to improve product taste through practice. | Comparative exercise, prediction, critique, and ledger entry. |

Modes may be combined, but do not perform an elaborate opportunity survey when the user only needs selection among concrete prototypes.

## Product conception contract

Build this internally before substantial work. Print it only when ambiguity or handoff value justifies it.

```yaml
product_conception_contract:
  mode: opportunity_synthesis | category_reframe | concept_generation | creative_selection | product_thesis | taste_calibration
  conception_target: new_product | category | product_reframe | competing_concepts | product_thesis | taste_training
  arena: ""
  triggering_changes: []
  human_situations: []
  latent_capabilities_or_desires: []
  fixed_constraints: []
  reimaginable_assumptions: []
  creator_convictions: []
  current_alternatives_or_candidates: []
  evidence_sources: []
  proof_medium: ""
  desired_ambition: incremental | substantial | category_shaping
  allowed_actions: []
  out_of_scope: []
  blocking_unknowns: []
  confidence: high | medium | low
```

Target users may be unknown at the beginning of opportunity synthesis, but a selected concept must identify an initial user, situation, motivation, and adoption wedge.

## Conception workflow

### 1. Reconstruct the arena

Map the raw material before inventing a solution:

- what people are trying to accomplish, express, avoid, become, or coordinate;
- painful workarounds, tolerated compromises, broken handoffs, hidden operators, and expertise bottlenecks;
- enabling changes in technology, cost, distribution, regulation, culture, or behavior;
- what is newly possible, newly necessary, newly desirable, or newly distributable;
- existing products and inherited category assumptions;
- the maker's authentic conviction and why the work is worth caring about.

Do not reduce the arena to a list of feature requests.

### 2. Find structural insights

Search for one to three high-leverage tensions:

- an accepted trade-off that may no longer be necessary;
- a valuable capability trapped behind expertise, organization, location, cost, or timing;
- a workflow whose current core object is wrong;
- a product that exposes its implementation model instead of the user's world;
- a new medium still imitating the old medium;
- a fragmented journey that needs justified integration;
- an over-integrated product that should be unbundled;
- an emotional, identity, trust, or agency need ignored by functional tools;
- a change near the origin of a behavior or platform that could redirect later outcomes.

Express each candidate insight as:

```text
Because <underlying change or contradiction>,
people can or need to move from <current human state>
to <new human state>,
but current products remain organized around <obsolete assumption>.
```

An insight is not “AI can automate X.” It explains why a different product logic has become possible or necessary.

### 3. Generate distinct product logics

For open-ended conception, produce at least three genuinely different concepts. They must differ in several of these dimensions:

- core product object;
- primary actor or beneficiary;
- default interaction or ritual;
- locus of intelligence and control;
- system boundary and integration strategy;
- time horizon or usage cadence;
- adoption wedge;
- business or operating shape.

Useful concept families, applied only when relevant:

- remove a category of work rather than accelerating every step;
- give non-experts a capability previously reserved for experts;
- turn a passive artifact into an active collaborator or environment;
- redesign the core object or default action of an existing category;
- make a new medium native instead of copying the previous medium;
- integrate a fragmented journey when control is necessary for the experience;
- unbundle an overgrown product into a sharper tool;
- create a platform that lets users or third parties generate value;
- design a new ritual around expression, trust, identity, or coordination.

Do not pad the set with cosmetic variations. Two concepts with the same object, workflow, boundary, and value path are one concept wearing different hats.

### 4. Make each serious concept experiential

Before selection, create an experience specimen for each serious candidate. It can be a working demo, click prototype, storyboard, role-play, sample artifact, or precise text simulation.

```yaml
experience_specimen:
  initial_user: ""
  concrete_situation: ""
  before_state: ""
  trigger: ""
  first_30_to_90_seconds: []
  core_object_or_surface: ""
  magic_moment: ""
  after_state: ""
  invisible_system_work: []
  remaining_user_work: []
  likely_break_point: ""
```

Narrative polish is not a substitute for a specimen. Prefer something that can surprise the team, reveal awkwardness, or die cheaply.

### 5. Run creative selection

Judge candidates comparatively, not as isolated pitch decks. Prefer pairwise comparison and direct use over a fake weighted score.

Ask:

1. **Human significance**: Does it create a meaningful capability or state change?
2. **Directness**: Does the experience reach value without making users understand the machinery?
3. **Whole-product coherence**: Do object, interaction, boundary, defaults, operating model, and story reinforce one thesis?
4. **Technology leverage**: Does the enabling change create a discontinuity, or merely decorate an ordinary product?
5. **Timing and wedge**: Why can this begin now, and who is motivated enough to cross the adoption gap?
6. **Experiential force**: When made concrete, does the better future become legible without a long explanation?
7. **Generative potential**: Can users, creators, developers, or later products build new value on top?
8. **Proofability**: Can the decisive uncertainty be exposed by the next affordable specimen?
9. **Maker conviction**: Is there enough authentic care to endure the work, without treating conviction as market proof?

Eliminate or weaken concepts that are mainly:

- a feature bundle with no product thesis;
- a polished story whose core experience cannot be made concrete;
- novelty in labels, visuals, or AI presence rather than behavior;
- integration by ideology, creating cost and control without improving experience;
- simplification that merely transfers work to an operator, reviewer, user, or support team;
- dependent on implausible behavior change, unavailable data, or an unowned ecosystem shift;
- exciting only because evidence and constraints were ignored;
- impossible to distinguish from alternatives through a near-term specimen.

The agent may recommend a winner, but the final value-laden taste decision remains visibly human-owned.

Load `references/creative-selection.md` for deep selection work.

### 6. Commit the concept

For the selected direction, state:

- one-sentence product thesis;
- initial user and situation;
- human before-state -> after-state;
- core product object;
- default interaction or ritual;
- magic moment;
- what the product must own and what it should borrow, integrate, or leave outside;
- why now;
- deliberate non-goals;
- killed alternatives and why they lost;
- evidence, inference, conviction, bet, and unknowns;
- what would cause abandonment or substantial reframing.

Focus is the result of selection, not a shortcut that prevents divergence.

### 7. Define the first proof and handoff

End with the smallest artifact or experiment that can change the decision:

- next experience specimen or prototype;
- one or two decisive assumptions;
- predicted observable reactions or behavior;
- disconfirming signals;
- constraints and guardrails;
- decision after the test.

Use these handoff states:

```text
concept_selected_unvalidated
prototype_required
needs_product_judgment
needs_crystallization
blocked_on_evidence
blocked_on_decision
```

Route to `dbx-product-judgment` when the next question is whether the selected direction is valuable, coherent, adoptable, viable, trustworthy, or worth building. Route to `dbx-crystallize` only after direction is sufficiently chosen and the task becomes requirements clarification.

## Jobs-derived transfer rules

This skill incorporates mechanisms supported by Jobs's own words and first-hand accounts, not a personality simulation.

- Treat the world and current category rules as designed, therefore potentially redesignable.
- Start from human capability and experience, while also scanning enabling technologies and historical trajectories.
- Connect distant domains at the level of structure, not surface aesthetics.
- Train taste through exposure, making, comparison, mistakes, and consequence.
- Join thinking with doing; make ideas concrete early.
- Generate alternatives before focus, then select and say no.
- Use user observation and testing to reveal blindness; do not ask users to invent the discontinuous solution for the team.
- Treat integration, minimalism, secrecy, and perfection as contingent choices, not dogma.
- Prefer strong contributors, explicit ownership, rigorous disagreement, and clear final responsibility over lone-genius mythology.
- Balance quality ambition with shipping and learning.

Never infer that intimidation, humiliation, arbitrary certainty, or copying Jobs's language improves creativity. Load `references/jobs-research-and-transfer.md` when the research basis matters.

## Output contract

Default compact shape:

```markdown
## 核心洞察
- 触发变化：...
- 人的状态变化：...
- 被旧类别遮住的机会：...

## 候选产品逻辑
### 概念 A：...
- Thesis / Core object / Default / Experience specimen / Why now / Non-goals / Proof burden

### 概念 B：...
...

### 概念 C：...
...

## 创意选择
- 最强比较：...
- 淘汰：...
- 推荐：...
- 选择依据与不确定性：...

## 选中构想
- 产品 thesis：...
- 初始用户与场景：...
- Before -> After：...
- Magic moment：...
- Must own / Borrow / Outside：...
- Deliberate non-goals：...
- Kill list：...

## 第一份体验样本
- 要做出的 specimen：...
- 要观察的反应或行为：...
- 证伪信号：...

## 证据、押注与未知
- Evidence：...
- Inference：...
- Conviction：...
- Bet：...
- Unknowns：...

## Handoff
- State：concept_selected_unvalidated | prototype_required | needs_product_judgment | needs_crystallization | blocked_on_evidence | blocked_on_decision
- Next：...
```

Use the matching contract in `references/output-contracts.md`, including for shorter modes and blocked states. Only a saved Markdown file using the **Standard conception report** contract may be checked with:

```bash
python3 skills/dbx-product-conception/scripts/validate-conception-report.py path/to/report.md
```

The script checks the standard report's handoff shape and epistemic labels only. It cannot prove originality, taste, or product quality. Do not use it to validate the smaller mode contracts.

## Conditional references

Load only what the task needs:

- `references/product-conception-kernel.md`: deeper insight, concept, specimen, and selection rubrics.
- `references/jobs-research-and-transfer.md`: source-grounded Jobs mechanisms, corrections, and non-transferable myths.
- `references/creative-selection.md`: prototype-driven selection procedure.
- `references/evidence-conviction-and-novelty.md`: research, novelty, evidence, and conviction boundaries.
- `references/taste-calibration.md`: explicit long-term taste-building practice.
- `references/output-contracts.md`: report schemas and handoffs.
- `references/worked-example.md`: synthetic end-to-end example.
- `references/repo-integration.md`: DBX collection routing snippets.

## Stop conditions

Stop or narrow when:

- no conception seed exists and the user declines to provide an arena, change, tension, or candidate;
- candidates still differ only by features; return to structural divergence rather than selecting;
- no concept can be made concrete enough to compare;
- the decisive question is current market fact but research is unavailable;
- the user asks for certainty that a concept will succeed;
- the task has become product correctness judgment, requirement crystallization, design review, technical planning, or implementation;
- safety or legitimacy fails.

## Completion proof

Completion is mode-relative. A response is complete when it satisfies the selected mode's contract in `references/output-contracts.md`. For narrower modes, claim only that the requested mode is complete, not that the full product-conception cycle is complete.

Do not claim the full product-conception cycle is complete unless a **Standard conception report** includes:

1. an explicit opportunity or structural insight;
2. distinct concepts or a justified reason not to generate alternatives;
3. concrete experience specimens for serious candidates;
4. comparative selection or an explicit unresolved decision;
5. a selected thesis or blocked state;
6. deliberate non-goals or kill decisions;
7. separated evidence, inference, conviction, bets, and unknowns;
8. a prototype or validation handoff without claiming product correctness.
