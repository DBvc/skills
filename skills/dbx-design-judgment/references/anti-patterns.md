# Design Anti-Patterns

These are failure modes to catch, not universal bans. Always tie them to user, task, evidence, and register.

## Agent behavior anti-patterns

### Generic design advice

Symptom:

```text
"Improve hierarchy, make it cleaner, add whitespace, use consistent colors."
```

Correction:
- Name the exact broken path.
- Point to visible or documented evidence.
- Give a concrete design fix direction.

### Unsupported taste claim

Symptom:

```text
"This looks dated" or "users will prefer this" without evidence.
```

Correction:
- Mark as taste hypothesis or tie to target audience, reference, or design system.

### Role creep into implementation

Symptom:
- Writes JSX/CSS.
- Applies patch.
- Says files were changed.
- Turns code evidence into generic code review.

Correction:
- Stop at design handoff.
- Say implementation should be handled by a coding/frontend skill.

### Over-redesign

Symptom:
- Replaces whole page when the problem is spacing, hierarchy, copy, or state clarity.

Correction:
- Prefer smallest material design fix that addresses the observed defect.
- Escalate to redesign only when the IA, task path, or visual language is structurally wrong.

### Screenshot hallucination

Symptom:
- Infers hidden flow, analytics, or user behavior from one screenshot.

Correction:
- Separate visible facts from assumptions.
- Mark hidden behavior unknown.

## Interface anti-patterns

### Equal-weight everything

Symptoms:
- Every card, CTA, stat, and label has similar visual weight.
- No single reading path.

Risk:
- User cannot decide what matters or what to do next.

Fix direction:
- Define information priority.
- Demote secondary actions.
- Use size, weight, spacing, and position consistently.

### Card wallpaper

Symptoms:
- Every region is wrapped in a card.
- Nested cards create noisy surface boundaries.

Risk:
- Structure looks busy without adding meaning.

Fix direction:
- Use cards only when they group interactive or comparable objects.
- Use whitespace, headings, and separators for lighter grouping.

### Accent color inflation

Symptoms:
- Accent color used for decoration, links, icons, metrics, borders, and primary CTA.

Risk:
- Primary action and state indicators lose meaning.

Fix direction:
- Reserve accent for primary action, current selection, or semantic state.
- Use neutral hierarchy for decoration.

### State vacuum

Symptoms:
- Happy path only.
- Empty, error, loading, disabled, permission, and partial-success states missing.

Risk:
- Product feels broken the moment reality enters.

Fix direction:
- Add state model before visual polish.

### Unsafe simplification

Symptoms:
- Destructive or permission-changing tasks become one-tap without verification.
- Batch actions hide item identity.

Risk:
- User loses trust or takes wrong action.

Fix direction:
- Preserve verification, scoping, undo, confirmation, or explanatory grouping.

### Product/brand register confusion

Symptoms:
- Dashboard has landing-page drama.
- Marketing page looks like a settings screen.

Risk:
- Product UI becomes distracting, or brand surface becomes forgettable.

Fix direction:
- Reclassify the register.
- Separate expressive moments from task surfaces.

### AI-template reflex

Symptoms:
- Centered hero, three identical cards, generic gradients, random icons, glass panels, vague headings.

Risk:
- Surface feels average, ungrounded, and interchangeable.

Fix direction:
- Start from user task, content model, and specific references/anti-references.
- Remove decoration that has no job.

### Design system drift

Symptoms:
- Multiple radii, shadows, buttons, input styles, icon families, or status colors for the same roles.

Risk:
- Interface feels stitched together and becomes harder to extend.

Fix direction:
- Create or reuse semantic tokens and component roles.
- Document exceptions.
