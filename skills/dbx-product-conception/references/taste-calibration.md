# Taste Calibration

Load only when the user explicitly wants to improve personal product taste, review past judgments, or establish a durable judgment ledger.

## Definition

Product taste is a trained ability to discriminate among concrete possibilities when rules are incomplete and several choices are locally defensible.

It combines:

- perception of details that change the whole experience;
- recognition of coherence and unnecessary concepts;
- sensitivity to human meaning, timing, and category assumptions;
- memory of prior products and consequences;
- willingness to choose and reject;
- calibration about where intuition is reliable.

Taste is not merely visual style, confidence, minimalism, popularity, or personal preference.

## What a skill can do

A skill can:

- select useful comparison sets;
- force predictions before hindsight;
- make criteria and values explicit;
- require concrete artifacts rather than slogans;
- preserve decisions, confidence, and alternatives;
- compare predictions with later evidence;
- identify repeated calibration errors;
- expose the user to stronger exemplars and makers' reasoning.

A skill cannot instantly install:

- decades of embodied experience;
- domain-specific tacit knowledge;
- emotional sensitivity to a medium;
- courage, authority, or consequence;
- a guaranteed ability to identify category-defining products.

## Calibration loop

```text
observe without outcome knowledge
-> predict and choose
-> state rationale and confidence
-> inspect/use the artifact
-> reveal outcome and context
-> identify misses and luck
-> update the personal discriminator
-> choose the next exercise
```

Do not let the outcome overwrite the original prediction.

## Judgment ledger

Use `assets/insight-ledger-entry.yaml` or this compact record:

```yaml
judgment_entry:
  date: ""
  artifact_or_decision: ""
  question: ""
  prediction: ""
  selected_option: ""
  rejected_options: []
  rationale: []
  confidence: 0.0
  values_or_tradeoffs: []
  evidence_available_then: []
  unknowns_then: []
  outcome_observed_later: []
  what_was_right: []
  what_was_wrong: []
  luck_or_external_change: []
  missed_variable: ""
  taste_update: ""
  next_exercise: ""
```

Use confidence bands rather than fake precision when appropriate:

```text
low: a weak preference or unfamiliar domain
medium: informed judgment with material uncertainty
high: repeated experience and clear product consequences
```

## Exercise families

### 1. Blind pairwise product comparison

Choose two products or prototypes solving a similar human job. Hide adoption or brand outcomes when possible.

Predict:

- which product communicates its model faster;
- which default better expresses the thesis;
- where the first user error occurs;
- which product is more likely to earn repeated use;
- what each product deliberately refuses to do.

Then inspect evidence and update the ledger.

### 2. Historical fork

Reconstruct a product decision using only information available at the time. Choose before revealing the actual result.

Avoid survivor bias:

- a failed product may contain excellent conception;
- a successful product may benefit from distribution, timing, or luck;
- later imitation does not prove the original business was viable.

### 3. Concept-to-specimen translation

Take a persuasive concept statement and create the first 60 seconds of use. Record which claims disappear when made concrete.

This trains sensitivity to pitch-selection errors.

### 4. Deletion drill

Given a product with many locally useful features:

- state the whole-product thesis;
- remove one concept, workflow, or object;
- name who inherits the removed work;
- predict whether coherence or value improves;
- test against representative tasks.

This trains real focus rather than minimalist aesthetics.

### 5. Core-object reframe

Describe the same opportunity using three different core objects. For each, derive lifecycle, default action, permissions, business model, and failure modes.

This trains recognition that naming and architecture can encode product assumptions.

### 6. Medium-native redesign

Take a product imported from an older medium and ask what the newer medium uniquely permits. Build one specimen that cannot be expressed naturally in the old medium.

### 7. Boundary drill

For one concept, produce three versions:

- tightly integrated;
- contract-and-integration based;
- sharply unbundled.

Predict which boundary is required by the experience and which is ideology.

### 8. Failure autopsy

Analyze a failed product without starting from “it was a bad idea.” Separate:

- product conception;
- implementation quality;
- timing;
- distribution;
- operating model;
- business model;
- external change;
- luck.

Then ask whether the original thesis should be killed, sequenced differently, or tried under changed constraints.

## Exemplar corpus

Store exemplars as mechanisms, not mood boards:

```yaml
exemplar:
  product_or_artifact: ""
  user_and_situation: ""
  defining_thesis: ""
  core_object: ""
  decisive_detail: ""
  why_it_changes_the_whole: ""
  rejected_or_absent_elements: []
  enabling_conditions: []
  weaknesses_or_costs: []
  transfer_hypothesis: ""
  transfer_limits: []
```

A good corpus contains:

- successful and failed products;
- different industries and media;
- products loved by the user and products the user dislikes;
- original versions and later imitations;
- products with strong conception but weak economics;
- products with ordinary conception but exceptional execution or distribution.

## Calibration metrics

Do not reduce taste to one score. Track patterns such as:

- prediction accuracy by domain;
- overconfidence and underconfidence;
- frequency of changing judgment after direct use;
- repeated missed variables;
- tendency to overvalue novelty, polish, technical elegance, simplicity, or breadth;
- ability to identify what should be killed;
- quality of disconfirming predictions;
- whether later product work shows less rework or stronger coherence.

## Common calibration failures

- **Hindsight polish**: rewriting the original reason after seeing the result.
- **Outcome worship**: equating commercial success with product quality.
- **Aesthetic capture**: overvaluing visual refinement.
- **Engineer capture**: preferring elegant mechanisms users must understand.
- **Novelty bias**: treating difference as value.
- **Simplicity bias**: removing visible complexity while hiding work.
- **Founder mythology**: attributing collective systems to one person.
- **Domain leakage**: assuming taste trained in one product class transfers fully to another.
- **No consequence**: making judgments without later observing outcomes.

## Twelve-session starter sequence

1. Two products, same job, blind comparison.
2. One product's 60-second experience reconstruction.
3. Feature deletion and cost-transfer audit.
4. Three core-object reframes.
5. Historical fork with outcome hidden.
6. Failed-product autopsy.
7. Medium-native redesign.
8. Integration versus unbundling boundary drill.
9. Three concepts from one enabling change.
10. Prototype-driven creative selection.
11. Review the first ten ledger entries for calibration patterns.
12. Design the next six exercises around the largest repeated error.

The sequence is only scaffolding. Real product decisions with recorded outcomes produce stronger learning.
