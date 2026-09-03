# Product Conception Kernel

Load for opportunity synthesis, category reframing, open concept generation, or a formal product-thesis report.

## First principle

Product conception is not producing more ideas. It is discovering a better organizing logic for a human situation, making alternatives concrete, and committing to a direction without disguising uncertainty.

```text
Product judgment asks: Is this defined product right?
Product conception asks: What product should exist here at all?
```

## Three-loop model

```text
Generative loop:
  signals -> tensions -> structural insight -> distinct concepts -> specimens

Selective loop:
  experience -> comparison -> rejection/recombination -> commitment

Calibration loop:
  prediction -> real consequence -> review -> taste update
```

A single session can run the first two loops. Mature product taste requires the third loop across time.

## 1. Opportunity material

Collect only material capable of changing the product logic:

### Human material

- ambitions, frustrations, identity, expression, belonging, agency, trust, fear, and status;
- repeated workarounds or expertise bottlenecks;
- tasks users avoid, delegate, postpone, or perform through social coordination;
- hidden work performed by operators, assistants, reviewers, support, or family;
- moments where current products make people carry the system's internal model.

### Change material

- technical capability, cost collapse, reliability threshold, new interface, new distribution channel;
- regulation, platform policy, demographics, organization, or labor shift;
- behavior that has become habitual or newly unacceptable;
- a medium reaching sufficient scale for second-order creativity;
- a component becoming commodity while another layer becomes scarce.

### Maker material

- authentic conviction about what should be possible;
- unusual access, expertise, community, or distribution;
- experiences that reveal a problem others normalize;
- a quality or value the maker is willing to defend over time.

Maker material is part of the opportunity, not market evidence.

## 2. Structural insight operators

Use these as search operators, not mandatory checklist items.

### Remove a false trade-off

```text
People currently choose A or B because of constraint C.
Has C changed enough that a product can offer both?
```

Examples: power versus ease, expertise versus control, quality versus speed, personalization versus privacy.

### Democratize a capability

```text
Which outcome is currently reserved for experts, institutions, wealth, location, or privileged data?
What new mediation could make it available without pretending expertise is free?
```

### Change the core object

Existing categories often organize around the implementation artifact rather than the user's intention.

```text
email -> conversation or commitment
file -> living work object
task -> desired state change
dashboard -> decision
chat -> durable delegated work
```

Do not change vocabulary alone. The lifecycle, default actions, state ownership, and business model should follow the new object.

### Change the default ritual

Ask what users repeatedly do because the product assumes it:

- open an app;
- search for a command;
- fill a form;
- maintain a list;
- check a dashboard;
- repeat context;
- translate between systems.

Then ask whether a new medium makes a different default possible.

### Make the new medium native

New media first imitate old media. Find what becomes possible only when the medium's distinctive properties are used.

For AI this may include:

- adaptive rather than fixed flows;
- generated interfaces or artifacts;
- persistent delegated state;
- mixed initiative;
- tool execution;
- multimodal perception;
- simulation before action;
- explanation and uncertainty at the point of decision.

Do not add conversational UI merely because a model exists.

### Integrate or unbundle

Integration is justified when handoffs destroy the defining experience, state, trust, timing, or learning loop. Unbundling is justified when one product carries unrelated jobs, permissions, operating models, or risk.

For each boundary, ask:

```text
What coordination failure disappears if we own this layer?
What cost, lock-in, and organizational burden arrive with ownership?
Could a contract or integration preserve the experience instead?
```

### Shift who acts

Change the primary actor:

- user -> agent;
- expert -> non-expert with safeguards;
- individual -> team;
- organization -> network;
- creator -> audience;
- operator -> system;
- synchronous participant -> asynchronous delegate.

Then account for who inherits review, exceptions, and liability.

### Change time

Move value earlier, later, continuously, or at the moment of need:

- prevent rather than repair;
- rehearse before commit;
- ambiently maintain rather than periodically clean;
- preserve intent across sessions;
- make delayed consequences visible now.

### Reveal ignored human meaning

Functional products often ignore dignity, confidence, emotion, identity, authorship, or social meaning. These can be central product variables without turning the product into emotional manipulation.

## 3. Insight quality test

A strong insight usually has five parts:

1. a concrete human situation;
2. an underlying change or contradiction;
3. an inherited assumption;
4. a newly possible state transformation;
5. consequences for product object, interaction, or boundary.

Weak:

```text
AI makes planning faster.
```

Stronger:

```text
As agents can maintain and execute plans, the scarce resource shifts from writing tasks
to preserving intent and governing exceptions; products organized around task lists may
need to become living agreements between people and delegated systems.
```

The stronger statement is still a hypothesis. It merely has more explanatory and generative power.

## 4. Technology-to-product translation

For each enabling capability, fill this chain:

```yaml
enabling_change:
  capability: ""
  previous_constraint_removed_or_shifted: ""
  newly_possible_human_state: ""
  old_category_assumption: ""
  possible_new_core_object: ""
  new_default_interaction: ""
  hidden_system_work: []
  new_failure_modes: []
  trust_or_control_required: []
  initial_adoption_wedge: ""
```

Reject translations that stop at:

- “add AI”;
- “automate the workflow”;
- “personalize everything”;
- “one interface for all tools”;
- “proactive assistant”;
- “platform/ecosystem” without a first experience.

## 5. Concept distinctness test

Two concepts are structurally distinct when they differ in at least three high-leverage dimensions and those differences alter the user experience or operating model.

```yaml
concept_card:
  name: ""
  one_sentence_thesis: ""
  initial_user_and_situation: ""
  human_before_after: ""
  core_object: ""
  default_interaction_or_ritual: ""
  locus_of_intelligence_and_control: ""
  system_boundary:
    must_own: []
    borrow_or_integrate: []
    outside: []
  adoption_wedge: ""
  operating_or_business_shape: ""
  magic_moment: ""
  deliberate_non_goals: []
  strongest_failure_mode: ""
  decisive_unknown: ""
  first_specimen: ""
```

Feature variants are not distinct concepts:

```text
A: chat with summaries
B: chat with integrations
C: chat with proactive reminders
```

Possible structural divergence:

```text
A: a query tool the user invokes
B: a durable work object that governs delegated execution
C: an ambient environment that intervenes only at risk boundaries
```

## 6. Experience specimen design

The specimen should expose the defining experience and hardest assumption with the least construction.

Possible media:

- working software slice;
- clickable prototype;
- Wizard-of-Oz service;
- sample output or transformed artifact;
- acted workflow with real inputs;
- storyboard or narrated screen sequence;
- concierge delivery;
- API or command-line spike when technical behavior is the uncertainty.

The specimen is weak when it demonstrates breadth rather than the decisive moment.

Use this shape:

```yaml
experience_specimen:
  candidate: ""
  initial_user: ""
  concrete_situation: ""
  stakes_and_constraints: []
  before_state: ""
  trigger: ""
  first_30_to_90_seconds: []
  magic_moment: ""
  after_state: ""
  invisible_system_work: []
  remaining_user_work: []
  trust_and_control: []
  likely_break_point: ""
  observation_needed: ""
```

## 7. Whole-product coherence

A concept is coherent when these elements tell the same story:

```text
human transformation
core object
primary action
defaults and lifecycle
system boundary
trust and control
adoption wedge
business/operating model
product language
```

Examples of incoherence:

- a product promising calm but monetized by attention;
- an autonomous agent requiring constant manual confirmation;
- a beginner product exposing infrastructure concepts;
- an open platform whose critical value depends on uniform end-to-end behavior;
- a private tool whose business model requires extracting user data;
- a “simple” workflow that moves exceptions to an invisible operations team.

## 8. Creative selection without score theater

Weighted scoring is useful when criteria are stable, commensurable, and the task is optimization. Product conception often precedes that stability.

Prefer:

1. normalize candidates into concept cards;
2. experience each specimen;
3. compare pairs on the decisive difference;
4. state why one creates a stronger whole;
5. attack the leading concept;
6. eliminate, recombine, or remain explicitly unresolved;
7. choose the next proof.

Numbers may summarize known constraints, but do not let decimal scores disguise a value judgment.

## 9. Focus and the kill list

A selected thesis should produce explicit exclusions:

```yaml
focus_commitment:
  selected_thesis: ""
  what_must_be_true: []
  killed_concepts:
    - concept: ""
      reason: ""
      reusable_element: ""
  deliberate_non_goals: []
  deferred_but_not_rejected: []
  must_not_become: []
```

A kill list reduces future feature drift and preserves why alternatives lost. It may be revised when the decisive assumptions change.

## 10. Conception anti-patterns

- **Technology costume**: ordinary product plus fashionable capability.
- **Feature constellation**: many useful functions with no gravitational center.
- **Category thesaurus**: renaming old objects without changing behavior.
- **Idea confetti**: quantity without structural diversity or selection.
- **Pitch selection**: choosing the best story instead of the best experience.
- **Taste laundering**: calling preference a user fact.
- **Evidence veto**: refusing to explore because discontinuous ideas lack mature-market data.
- **Conviction laundering**: calling belief evidence.
- **Integration theology**: owning every layer because Apple did.
- **Minimalism theater**: hiding controls while transferring work and risk.
- **Genius cosplay**: role-playing a famous founder instead of improving the search process.
- **Consensus soup**: preserving every candidate until the product contains all of them.
- **Prototype pageant**: polished prototype that avoids the hardest assumption.
- **Premature PRD**: freezing requirements before a product thesis exists.

## 11. Completion state

Product conception ends in one of these states:

```text
concept_selected_unvalidated
prototype_required
needs_product_judgment
needs_crystallization
blocked_on_evidence
blocked_on_decision
```

It never ends with “the product is proven correct.” That belongs to later evidence and judgment.
