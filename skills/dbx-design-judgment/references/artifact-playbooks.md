# Artifact Playbooks

Use the smallest playbook that fits the evidence.

## PRD or spec to design brief

Goal:

```text
Convert intent into design decisions, not UI decoration.
```

Extract:
- Target user and usage context.
- Primary job and desired state change.
- Entry points and exit states.
- Core objects and content model.
- Information priority.
- Required user decisions.
- Required states: default, loading, empty, error, success, disabled, permission, partial success.
- Risk actions: delete, pay, publish, invite, permission changes, irreversible changes.
- Constraints: device, accessibility, localization, performance, platform, existing design system.
- Unknowns that would change the design.

Output:
- Design goal.
- IA and flow.
- Screen or section structure.
- State model.
- Visual language and register.
- Component needs.
- Handoff decisions.
- Validation plan.

Do not:
- Restate the PRD as if it were a design.
- Invent user research.
- Jump directly to component styling.

## Screenshot review

Goal:

```text
Turn visible design evidence into specific diagnosis.
```

Procedure:
1. Describe the visible surface in neutral terms.
2. Name the exact problem: hierarchy, spacing, density, contrast, typography, alignment, affordance, copy, or state ambiguity.
3. Tie it to the likely user task.
4. Give the smallest design fix direction first.
5. Mark hidden behavior as unknown.

Good finding shape:

```text
The primary CTA competes with two same-weight secondary buttons in the header, so first-time users cannot identify the next action. Reduce the header to one primary CTA, demote secondary actions to links or overflow, and validate with first-click testing.
```

Bad finding shape:

```text
Make it more modern and clean.
```

## Live product walkthrough

Default is read-only.

Allowed without extra approval:
- Open public pages.
- Navigate public read-only flows.
- Take screenshots if tools allow.
- Record visible states, labels, hierarchy, and transitions.

Requires explicit approval:
- Login.
- Account creation.
- Form submission.
- Payment.
- Delete, publish, invite, export, send, or any remote state change.
- Using credentials or private data.

Record:
- URL or route.
- Steps taken.
- Viewport if relevant.
- State reached.
- Evidence observed.
- Paths not covered.

## Code design alignment

Read code only as design evidence.

Look for:
- Token sources: colors, spacing, typography, radius, elevation, motion.
- Component vocabulary: buttons, forms, dialogs, cards, tables, nav, feedback, empty/error states.
- State coverage: loading, empty, error, success, disabled, permission, partial success.
- Responsive behavior: breakpoints, layout collapse, overflow rules, mobile patterns.
- Accessibility affordances: labels, focus, keyboard paths, contrast-related tokens, ARIA usage when relevant.
- Drift: multiple button systems, duplicated token values, local magic numbers, inconsistent styles for same role.

Do not:
- Review algorithms or backend logic unless it affects design behavior.
- Suggest refactors without design impact.
- Produce patches.
- Claim rendered quality from code alone.

## Design system review

Build a system map:

```yaml
design_system_map:
  typography: []
  color_roles: []
  spacing_scale: []
  radius_scale: []
  elevation_or_surface_layers: []
  component_roles: []
  state_vocabulary: []
  iconography: []
  motion: []
  responsive_rules: []
  accessibility_rules: []
  known_exceptions: []
```

Judge:
- Are tokens semantic, or just raw values?
- Are component roles clear?
- Are states consistent across components?
- Are exceptions intentional and documented?
- Can a future implementer extend the system without inventing new visual language?

## Reference and anti-reference handling

When users name references such as Linear, Vercel, Notion, GitHub, Apple, Stripe, or a competitor:
- Extract concrete properties instead of copying the brand.
- Ask what should carry forward if the reference is ambiguous.
- Use anti-references to define boundaries.

Example extraction:

```text
"Linear-like" might mean compact density, low-shadow surfaces, crisp typography, restrained accent use, keyboard-first workflows, and quiet transitions. It does not automatically mean black-and-purple, identical spacing, or copying UI.
```
