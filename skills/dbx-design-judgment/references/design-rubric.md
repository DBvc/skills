# Design Rubric

Use this only when a deeper audit needs more structure. Do not run every question for every task.

## Task support

- Can the user understand the purpose of the surface within 5 to 10 seconds?
- Is the primary task visible or reachable without detours?
- Is there one clear next action when the page needs one?
- Are secondary actions clearly secondary?
- Are decision points reduced to the minimum useful set?
- Does the design explain consequences before high-risk actions?
- Does a high-blast-radius action show the affected scope before confirmation?
- Does it support both first-time and repeated use when both matter?

## Information architecture

- Are the primary objects named in user language?
- Are categories mutually understandable?
- Is navigation based on user tasks rather than internal teams or database tables?
- Are details progressively disclosed at the right moment?
- Are filters, search, sorting, grouping, and status labels meaningful for the task?
- Are defaults safe and useful?
- Are hidden items still discoverable when needed?

## Visual hierarchy

- Does the eye land on the most important information first?
- Is there a clear heading and content relationship?
- Do size, weight, color, spacing, and position agree on priority?
- Are too many elements styled as primary?
- Are icons adding recognition or just noise?
- Is empty space used to group information, or is it random air?
- Are dense areas dense for a reason?

## Interaction quality

- Are click targets and affordances obvious?
- From intention to available action, acknowledgement, state change, visible result, and next/correction action, where does the relevant path break?
- Are irreversible actions scoped, confirmed, or recoverable?
- Are error paths recoverable with clear next steps?
- Are long operations understandable, and are interruption controls shown only when the current system supports them?
- Do progress, cancel, retry, resume, and rollback claims match known capabilities or clearly named future dependencies?
- Are disabled controls explained?
- Are hover-only affordances avoided for mobile or keyboard users?
- Are keyboard and focus flows considered for task surfaces?

## State coverage

For each major component or flow, check:

```yaml
states:
  default: "What normal content looks like"
  loading: "What is happening and whether user can continue"
  empty: "Why empty, what to do next, and whether this is normal"
  error: "What failed, why if knowable, what recovery is available"
  success: "What changed and what next action is available"
  disabled: "Why unavailable and how to unlock if possible"
  permission: "What access is missing and who can resolve it"
  partial_success: "What succeeded, what failed, and how to retry or inspect"
```

For asynchronous work, distinguish request acknowledgement, durable task state, visible UI state, and final result. A returned ID or a refresh that changes the status can reveal a feedback or state-projection break without proving that progress or cancellation exists.

## Visual language

- Is the surface product, brand, or hybrid?
- Does tone fit the user's state of mind?
- Is density appropriate for frequency and expertise?
- Does color have semantic roles?
- Do typography and spacing create rhythm instead of monotony?
- Are motion and animation purposeful?
- Are decorative effects justified by context?
- Is the design avoiding category reflex and AI-template defaults?

## Design system consistency

- Does the same component role look the same across the surface?
- Are token values reused rather than invented locally?
- Are button hierarchy, form controls, dialogs, tables, cards, and feedback patterns consistent?
- Are semantic states visually stable: hover, focus, active, selected, disabled, loading, error, success, warning, info?
- Are exceptions visible and intentional?
- Would a new engineer know what component and token to use?

## Accessibility and readability

This skill can flag risks, but should not claim formal compliance without proper checks.

- Is text legible at target sizes?
- Is contrast likely adequate for important text and controls?
- Are focus indicators visible?
- Can the main path work without hover?
- Are form labels persistent or recoverable?
- Are error messages associated with controls?
- Are touch targets large enough for mobile use?
- Are motion-sensitive users considered?
- Does responsive layout preserve reading order and task priority?
- Are long strings, localization, and dynamic data ranges considered?

## Handoff readiness

A design handoff is ready when it specifies:
- Goal and non-goals.
- User and primary path.
- IA and screen structure.
- Component roles.
- Required states.
- Known interaction capabilities and any proposed upstream dependencies.
- Responsive behavior.
- Accessibility expectations.
- Copy and microcopy needs.
- Token and design-system decisions.
- Open questions and validation plan.

A handoff is not ready if it relies on adjectives such as clean, premium, delightful, simple, or modern without concrete design decisions.
