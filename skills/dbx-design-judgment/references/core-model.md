# Core Model

## Thesis

Design judgment is the control layer between product intent and frontend implementation.

It should answer:

```text
For this target user and task, does the current or proposed interface make the right action understandable, safe, efficient, and coherent?
```

It should not answer by taste alone.

## Minimal design frame

A useful judgment needs at least:

```yaml
target_surface: ""
target_user: ""
user_task: ""
usage_context: ""
primary_path: []
evidence: []
register: product | brand | hybrid | unknown
confidence: high | medium | low
```

If these are missing, either ask focused questions or give a bounded partial judgment with unknowns marked.

## Five-lens kernel

### 1. Task support

Ask:
- What is the user trying to finish?
- What should they understand first?
- What should they do next?
- What decision cost, input cost, trust cost, and error cost does the design impose?
- Does the design optimize the actual task, or only the screenshot?

Common failures:
- Multiple competing primary CTAs.
- UI explains features but not next action.
- Critical action hidden under decorative layout.
- User must infer state from vague labels.
- High-risk action made fast but not verifiable.

### 2. Information structure

Ask:
- Are objects, categories, labels, and navigation coherent?
- Does the page have a clear reading path?
- Are primary, secondary, and tertiary information visually separated?
- Is progressive disclosure used to reduce noise without hiding essential verification?
- Does the structure match the user's mental model, not just the data model?

Common failures:
- Equal-weight cards for unequal information.
- Repeated sections that restate the same point.
- Data model leaked directly into UI labels.
- Status, action, and explanation mixed in one noisy block.
- Details shown too early, essentials shown too late.

### 3. Interaction and states

Ask:
- Are actions discoverable and predictable?
- Does every important action produce clear feedback?
- Are destructive or irreversible paths confirmable, reversible, or scoped?
- Are loading, empty, error, success, disabled, permission, and partial-success states designed?
- Does the interaction work for first-time users and repeated users?

Common failures:
- Only happy path exists.
- Empty state says "nothing here" without teaching what to do.
- Error message explains failure but not recovery.
- Loading state blocks orientation.
- Disabled controls give no reason.
- Success state celebrates but does not confirm what changed.

### 4. Visual language and system

Ask:
- Does visual tone fit the register: product, brand, or hybrid?
- Are typography, spacing, radius, elevation, color roles, icons, motion, and density consistent?
- Are components reused intentionally, or re-invented per section?
- Does visual weight match information priority?
- Is decoration carrying meaning, or only hiding weak structure?

Common failures:
- Same button role has different styles.
- Accent color used for decoration and action, weakening action meaning.
- Shadows, borders, and cards used as wallpaper.
- Rounded corners, icons, and gradients chosen by AI default rather than product need.
- Product UI tries to look like a marketing page.

### 5. Trust, accessibility, and handoff readiness

Ask:
- Is important text readable under realistic conditions?
- Are touch targets, focus order, keyboard path, contrast, and motion sensitivity considered?
- Does responsive behavior preserve task structure, not merely shrink the layout?
- Does the design avoid dark patterns, hidden costs, ambiguous state, and false confidence?
- Is the design specific enough for implementation without inventing missing decisions?

Common failures:
- Mobile layout collapses hierarchy.
- Important copy is too low contrast.
- Keyboard/focus behavior is unspecified.
- Dynamic text length and localization are ignored.
- Handoff says "make it clean" instead of specifying states, components, and hierarchy.

## Register rule

### Product register

Product UI includes app UIs, admin dashboards, settings, forms, developer tools, authenticated workflows, and task surfaces.

Goal:

```text
Earned familiarity. The interface should disappear into the task.
```

Prefer:
- Clear information hierarchy.
- Consistent component vocabulary.
- Standard affordances.
- Dense information when users need it.
- Complete states and feedback.
- Motion that conveys state, not decoration.

Avoid:
- Display fonts in controls and labels.
- Decorative motion on routine tasks.
- Heavy color on inactive states.
- Re-invented form controls, scrollbars, or modals.
- Marketing-page hero logic inside a work surface.

### Brand register

Brand surfaces include landing pages, marketing pages, campaigns, portfolios, public storytelling, and impression-led surfaces.

Goal:

```text
Memorable product promise. The design helps communicate the product or brand.
```

Prefer:
- Distinct point of view.
- Strong voice and pacing.
- Intentional color strategy.
- Imagery or expressive typography when it serves the promise.
- Clear audience fit.

Avoid:
- Generic SaaS template reflex.
- Adjectives without concrete visual decisions.
- Timid sameness presented as refinement.
- Decoration with no relationship to promise.

### Hybrid register

Hybrid surfaces often have a brand shell around a task area, such as onboarding, public demo flows, pricing configurators, or AI tool landing-to-workflow transitions.

Rule:

```text
Let brand expression introduce value, then let product clarity carry the task.
```

## P-level severity

Use P-level design severity for consistency with DBX product judgment.

- `[P0 blocker]`: likely blocks the core task or creates serious trust, safety, accessibility, comprehension, or irreversible-action risk.
- `[P1 high]`: critical path, hierarchy, state, affordance, IA, or design system issue likely causes confusion, abandonment, wrong action, or high support cost.
- `[P2 medium]`: bounded weakness increasing friction, inconsistency, cognitive load, responsive risk, or implementation ambiguity.
- `[P3 low]`: local polish, copy, spacing, typography, alignment, or consistency improvement.

Fix order is not severity alone. Sort by:

```text
severity + confidence + user-path frequency + expected effort + blast radius
```

## Confidence

- `high`: direct artifact, screenshot, browser observation, code, user data, or authoritative source supports the claim.
- `medium`: evidence is plausible but partial, or inference bridges are needed.
- `low`: hypothesis needing user research, analytics, domain review, or deeper access.

Do not upgrade confidence because a design principle sounds familiar.
