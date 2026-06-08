# Attention Kernel

## 1. Core thesis

The skill is not optimizing saved knowledge. It is optimizing attention allocation.

Every incoming item is treated as a claim on a scarce resource:

```text
attention, context, time, future retrieval surface, emotional load, and decision bandwidth
```

A good output says what the item should become:

```text
action | focused capability building | reversible experiment | weak signal | searchable reference | incubated option | deletion | guarded review | clarification request
```

## 2. Stable variables

Use these variables for every item, regardless of source system.

### attention_claim

What is the item trying to make the user do?

Typical claims:

```text
act | learn | decide | monitor | store | buy | trade | worry | reply | share | compare | research | unknown
```

Do not equate an item's surface format with its claim. A note may hide an action. A task may actually be a someday idea. A course may really be a capability bet. A market message may be stimulus rather than research.

### horizon_fit

Where does this item fit?

```text
now          current commitment, deadline, active project, live decision
cycle        current month/quarter/theme
long_term    durable compounding domain
outside      interesting but outside known goals
unknown      insufficient profile or item context
```

### evidence_strength

How much confidence is justified?

```text
high     enough source/content/context to route confidently
medium   enough for a provisional route
low      title/excerpt-only or missing key context
unknown  cannot judge without more information
```

### transformability

Can the item become something useful?

```text
action        concrete next step
artifact      note, checklist, design doc, code, decision memo
rule          reusable principle or heuristic
experiment    small test with success signal and stop condition
reference     searchable retrieval object
signal        trend/claim to monitor for recurrence
none          cannot be usefully transformed
```

### compound_value

Will processing this item make future work or judgment better?

High compound value often appears in:

- durable principles;
- decision frameworks;
- technical architecture patterns;
- systems that improve repeated work;
- examples that sharpen judgment;
- experiments that generate feedback.

### attention_cost

Cost includes:

- focused time;
- context switching;
- new unfinished thread;
- maintenance of tags/queues;
- repeated reviews;
- emotional noise;
- opportunity cost against current commitments.

### risk_reversibility

Risk includes:

- financial loss;
- privacy exposure;
- health/legal/tax/employment harm;
- relationship damage;
- irreversible destructive operations;
- manipulative or non-consensual use;
- acting on low-credibility claims.

High risk does not mean discard. It means route through `guard` unless the user explicitly asks for bounded research or professional-quality review.

## 3. Route table

| Route | Meaning | Use when | Bad use |
| --- | --- | --- | --- |
| `act_now` | Current bounded action | Now-fit and concrete action are both high | Using it for interesting items with no commitment |
| `build` | Focused capability/system building | Compound value high and worth a scheduled block | Marking every good article/course as study |
| `test` | Reversible experiment | Promise high, uncertainty high, cheap test available | Open-ended tinkering without stop condition |
| `track` | Weak signal monitoring | May matter if repeated or confirmed | Secretly following everything forever |
| `store` | Searchable reference | Retrieval value high, active value low | Making the reference bucket a guilt archive |
| `incubate` | Park until trigger | Timing wrong but potential value real | Deferring without trigger |
| `drop` | Remove from attention system | Low value, duplicate, stale, mostly stimulus | Dropping due to thin evidence when clarify is needed |
| `guard` | Risk-bounded review | Action could harm or evidence bar is high | Turning guard into paralysis for harmless items |
| `clarify` | Need smallest missing context | Missing context would change route | Asking broad questions when tentative route is enough |

## 4. Default route heuristics

Use `act_now` only if:

```text
horizon_fit is now
AND transformability includes action
AND evidence_strength is not low/unknown
AND risk is not high
```

Use `build` only if:

```text
compound_value is high
AND it supports cycle or long_term horizon
AND attention_cost is justified
```

Without a user-approved profile, keep at most three `build` items per batch. If more than three items satisfy the `build` heuristic, choose the strongest three by current horizon fit, concrete artifact/outcome, evidence strength, and low regret. Route the overflow to `track`, `store`, or `incubate` with an explicit upgrade trigger.

Use `test` when:

```text
promise is plausible
AND uncertainty is material
AND a small reversible test exists
```

Use `track` when:

```text
signal may matter
AND not actionable now
AND recurrence would change priority
```

Use `store` when:

```text
retrieval value is real
AND no active attention is justified
```

Use `incubate` when:

```text
item has potential
AND timing is wrong
AND a concrete trigger can be named
```

Use `drop` when:

```text
low relevance OR low transformability OR duplicate/stale/stimulus
AND no meaningful future retrieval value
```

Use `guard` when:

```text
risk is high OR claim asks for high-stakes action from weak evidence
```

Use `clarify` when:

```text
one missing field could change route materially
```

## 5. Anti-patterns

### Example overfitting

The user names a tool or method, and the skill turns that example into the core model.

Fix: keep product and method names in adapters or profile preferences.

### FOMO upgrading

Interesting items become `act_now` or `build` because they sound important.

Fix: require horizon fit and transformability.

### Method capture

A known productivity framework becomes mandatory.

Fix: treat it as an optional projection, not a kernel primitive.

### Topic-only tagging

The output says `AI`, `career`, or `investing`, but not what the item should become.

Fix: always output a route and no-action/action reason.

### Reference graveyard

`store` becomes a polite way to keep everything.

Fix: require retrieval intent; otherwise `drop` or `track`.

### False personalization

The agent invents a profile from stereotypes or one message.

Fix: mark assumptions, propose patches, ask only high-leverage questions.

### Silent mutation

The agent claims external systems are updated without approval or evidence.

Fix: dry-run, stable locators, exact batch approval, completion proof.
