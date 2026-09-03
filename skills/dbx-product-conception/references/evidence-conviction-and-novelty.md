# Evidence, Conviction, and Novelty

Load when current research, novelty, category claims, weak evidence, or strong maker conviction materially affects conception.

## Why this distinction matters

Early product creation contains facts, interpretations, values, and bets. Treating all of them as “evidence” kills originality or manufactures certainty.

Use this ledger:

```yaml
epistemic_ledger:
  observed_facts: []
  current_external_facts: []
  user_claims_or_experiences: []
  historical_lineage: []
  inferences: []
  analogies: []
  creator_convictions: []
  product_bets: []
  unknowns: []
  not_verified: []
```

## 1. Evidence by stage

### Opportunity stage

Useful evidence:

- repeated workarounds;
- resources already spent solving the problem;
- capability or cost curves;
- regulatory or distribution changes;
- behavior shifts;
- direct observation of constraints.

Do not demand mature retention or revenue data before a product exists.

### Concept stage

Useful evidence:

- whether a specimen is understandable;
- whether it creates the intended state change;
- technical feasibility of the defining behavior;
- whether users will grant required access, trust, or responsibility;
- comparative reactions to distinct product logics.

### Product-judgment stage

Useful evidence expands to:

- problem frequency/intensity;
- adoption and switching cost;
- repeated value;
- willingness to pay or organizational commitment;
- reliability, trust, safety, distribution, and operating viability.

Route to `dbx-product-judgment` when this becomes the primary question.

## 2. Conviction is allowed, but typed

Creator conviction can justify exploration when data cannot yet describe the new product. It may concern:

- what technology should do for people;
- which quality is non-negotiable;
- which category assumption feels obsolete;
- what future is worth building;
- what the maker is willing to sustain.

Conviction does not prove:

- market size;
- user adoption;
- timing;
- willingness to pay;
- technical feasibility;
- ethical legitimacy;
- superiority to alternatives.

Represent it explicitly:

```yaml
conviction:
  belief: ""
  origin: lived_experience | craft | values | domain_expertise | intuition | other
  consequence_for_product: ""
  confidence: low | medium | high
  evidence_that_would_change_it: []
  non_negotiable_or_revisable: ""
```

## 3. Inference must have a bridge

Weak:

```text
People use AI chat, therefore they want autonomous agents.
```

Stronger:

```text
Observed: users repeatedly paste context and ask for multi-step work.
Inference: some users value delegated completion, but current chat loses state and tool access.
Bet: a durable delegated-work object may produce more value than another conversation surface.
```

Each inference should identify:

- supporting observations;
- the causal or logical bridge;
- plausible alternatives;
- what observation would weaken it.

## 4. Analogy has a transfer contract

```yaml
analogy:
  source_domain: ""
  target_domain: ""
  transferred_structure: ""
  non_transferred_differences: []
  hypothesis_generated: ""
  evidence_needed: []
```

“iPhone for X” and “Uber for Y” are labels, not transfer contracts.

## 5. Novelty claims

Claims such as first, unique, no competitor, inevitable, category-creating, or nobody has tried this require current research.

Research should inspect:

- direct competitors;
- adjacent categories solving the same job;
- failed historical attempts;
- open-source and internal-tool patterns;
- substitute workflows and services;
- platform capabilities that may commoditize the concept;
- user reviews and reasons for abandonment when reliable.

Allowed conclusions:

```text
no close example found in searched sources
appears differentiated on X, not proved unique
historical attempts existed but enabling constraint Y changed
novelty is unverified; continue without using novelty as the thesis
```

Never infer “no competitor” from a weak search.

## 6. Inevitability test

Products often feel inevitable in retrospect. Before using that language, ask:

- Which enabling constraints recently changed?
- Which old attempts failed and why?
- What complementary behavior, distribution, or infrastructure is now present?
- What remains contingent on execution or trust?
- Which alternative future is equally plausible?

Replace “inevitable” with a falsifiable timing thesis.

## 7. Evidence can veto, constrain, or redirect

Evidence should not automatically average away an ambitious idea.

Possible effects:

- **veto**: violates safety, law, physics, or essential economics;
- **constrain**: narrows user, situation, autonomy, or boundary;
- **redirect**: reveals a different core object or wedge;
- **sequence**: ambitious future remains, but first product changes;
- **calibrate**: lowers confidence and raises proof burden;
- **support**: strengthens one mechanism or timing claim.

## 8. Prototype evidence limits

A compelling prototype can show:

- comprehension;
- immediate usefulness or emotional resonance;
- interaction quality;
- feasibility of a narrow behavior;
- preference between concrete alternatives.

It cannot by itself show:

- repeated use;
- total cost of operation;
- willingness to pay;
- ecosystem adoption;
- long-term trust;
- scale reliability;
- defensibility;
- broad market size.

State the evidence radius explicitly.

## 9. Product bet contract

```yaml
product_bet:
  thesis: ""
  evidence_supporting_exploration: []
  inference_chain: []
  creator_conviction: []
  decisive_assumptions: []
  known_constraints: []
  unknowns: []
  disconfirming_signals: []
  maximum_next_bet: time | money | scope | reputation
  next_evidence: ""
```

The size of the next bet should match evidence and reversibility, not the emotional power of the story.
