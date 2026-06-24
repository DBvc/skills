# dbx-crystallize Quality Rubric

Use this as an internal checklist or for eval review.

## Minimum pass

A good output should answer:

1. What exactly is being defined?
2. Who is it for or who is affected?
3. What state change should happen?
4. What is in scope?
5. What is out of scope?
6. What must not be broken?
7. How can it be accepted or rejected?
8. What important assumptions remain?
9. What edge cases matter enough to affect implementation?
10. What should happen next?

## High-signal requirement signs

- The title names a behavior or outcome, not just a UI object.
- Scope and non-goals prevent at least one likely downstream mistake.
- Acceptance criteria include both happy path and one meaningful negative or boundary case.
- Unknown thresholds are marked `TBD` instead of invented.
- Permission, privacy, payment, destructive action, or trust concerns are surfaced when relevant.
- The output states whether product/design/technical judgment is still needed.

## Common anti-patterns

### Beautiful fog

A polished PRD with phrases like "seamless", "intuitive", "robust", "AI-powered", "delightful", and no testable state.

Fix: replace adjectives with observable behavior or mark as TBD.

### Solution lock-in

The output accepts "add a button" as the requirement.

Fix: name the actor, context, desired state, and whether the button is mandatory or just a solution guess.

### Scope black hole

The contract says what to build but not what to avoid.

Fix: add non-goals and must-not-change constraints.

### Question flood

The agent asks generic PM questions instead of producing a partial contract.

Fix: ask only decision-changing questions and give the current crystallized shape.

### Fake certainty

The agent invents target users, success metrics, market claims, or compliance rules.

Fix: separate facts, assumptions, unknowns, and handoff needs.

### Over-handoff

Everything becomes "needs product/design/technical judgment".

Fix: hand off only when that uncertainty changes correctness or implementation. Small unknowns can stay as assumptions or TODOs.

## Readiness checklist

Use `crystallized` only if:

- Requirement object is named.
- Actor/context is known or safely irrelevant.
- Desired state is clear.
- In-scope and non-goals are explicit.
- At least three meaningful acceptance criteria exist for non-trivial work.
- Blocking risks are absent or handled.
- Next downstream target is clear.

Use `assumption-bound` if:

- A useful contract exists, but at least one important assumption must be confirmed.

Use `blocked` if:

- Missing actor, desired state, scope, or safety decision would change the requirement.

Use `needs-product-judgment` if:

- The main uncertainty is whether this is valuable, worth building, coherent with product strategy, or right for the target user.

Use `needs-design-judgment` if:

- The main uncertainty is flow, IA, visual hierarchy, interaction states, accessibility, or design system fit.

Use `needs-technical-plan` if:

- Requirements are clear, but source-of-truth, architecture, migration, integration, or verification topology must be planned before coding.
