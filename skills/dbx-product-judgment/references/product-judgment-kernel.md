# Product Judgment Kernel

This reference contains the longer rubric behind `dbx-product-judgment`. Load it for standard or deep audits, formal review reports, or when the product spans several surfaces.

## First principle

A product is not a pile of features. It is a designed path from a user's current state to a better state.

A judgment is meaningful only when it answers:

```text
For which user, in which context, toward which valuable result, under which constraints, compared with which alternatives, using which evidence?
```

## Universal correctness model

Use this model across domains. Replace domain facts with evidence, not imagination.

```text
Product correctness = value of desired state change
                    x probability of successful completion
                    x frequency or strategic importance
                    x trust and willingness to adopt
                    - user cost
                    - business/operating cost
                    - technical/maintenance risk
                    - safety/privacy/trust risk
                    - uncertainty cost
```

This is a thinking frame, not a numeric formula. Do not fake precision.

## Dimension rubric

### 1. Problem and value

Strong signals:

- The problem is already being solved through painful alternatives.
- Users spend time, money, attention, status, or organizational effort to solve it.
- The cost of not solving it is concrete.
- The product reduces a real bottleneck rather than adding a new dashboard over it.

Risk signals:

- The product describes a solution before a user state change.
- “Everyone can use it” replaces a target segment.
- Pain is inferred from team taste, not user behavior.
- The product optimizes a low-value moment while ignoring the expensive one.

### 2. User and context fit

Strong signals:

- Target user has a clear role, motivation, skill level, constraints, and current alternative.
- Usage moment is concrete: before/after work, under deadline, while mobile, during onboarding, during incident, during purchase, in review meeting, and so on.
- Stakes, frequency, and patience match the proposed flow.

Risk signals:

- The product asks new users to understand internal system modules before seeing value.
- It assumes expert users have beginner patience, or beginners have expert concepts.
- It designs for a persona document but not for a concrete usage moment.

### 3. State transformation

Strong signals:

- The product promise can be written as before-state -> after-state.
- The after-state is visible to the user.
- The first value moment arrives before setup cost becomes exhausting.
- Success and failure states are explicit.

Risk signals:

- Users can complete screens but not reach a meaningful result.
- The product hides completion criteria.
- The flow ends with “submitted” but not with “now I know what happens next”.

### 4. Critical path

Strong signals:

- The shortest path to core value is obvious.
- Default choices are safe and useful.
- Users are not asked to configure before they understand value.
- Error recovery, cancellation, retry, and back navigation are designed.

Risk signals:

- The main path is interrupted by account creation, empty forms, education walls, setup, or optional decisions.
- The product optimizes rare admin paths while leaving the daily path rough.
- Users must stitch several independent modules into one workflow.

### 5. Concept model and IA

Strong signals:

- Core objects and actions map to user language and workflow.
- Names, states, permissions, and lifecycle are consistent.
- Navigation reflects user tasks, not org chart or database tables.
- Complex domains are progressively disclosed.

Risk signals:

- Two objects mean nearly the same thing.
- One object has several owners or hidden lifecycles.
- IA mirrors implementation modules rather than user jobs.
- Labels are clear to builders but not to users.

### 6. Information quality

Strong signals:

- Each screen answers the user's next decision.
- Information is prioritized by task, risk, and frequency.
- Claims are explainable and trustworthy.
- Empty/loading/error/partial states are informative.

Risk signals:

- The page is dense because the team fears choosing priority.
- Users see metrics but not interpretation or next action.
- Important constraints appear after commitment.
- AI output is fluent but lacks sources, uncertainty, or controls.

### 7. Interaction quality

Strong signals:

- Actions are visible, named by outcome, and reversible where risk is high.
- Feedback closes the loop: pending, success, failure, reason, next step.
- The product handles slow networks, retries, duplicate submissions, permission changes, stale data, and partial failure.
- Accessibility is treated as part of usability, not decoration.

Risk signals:

- Users must guess what a button does.
- The same action produces different results in similar contexts.
- The product uses modals, notifications, or confirmations to compensate for unclear models.
- Keyboard, screen reader, contrast, focus, or responsive behavior blocks real users.

### 8. UI and visual support

Strong signals:

- Visual hierarchy exposes the main task.
- Density matches user expertise and context.
- Typography, spacing, contrast, and motion improve comprehension and trust.
- Brand style supports credibility without hiding usability problems.

Risk signals:

- The UI looks polished but the decision path is unclear.
- Color is the only state indicator.
- Visual novelty competes with comprehension.
- Important affordances look like decoration.

### 9. Trust, safety, and ethics

Strong signals:

- Costs, data use, limitations, irreversible effects, and AI uncertainty are visible before commitment.
- Privacy controls match user risk.
- The product avoids manipulative defaults.
- Sensitive or regulated decisions have appropriate guardrails and escalation paths.

Risk signals:

- Users are nudged into actions against their interest.
- Cancellation, export, deletion, or opt-out is hidden.
- The product pretends uncertain predictions are facts.
- It collects data without a clear product reason.

### 10. Technical alignment

Strong signals:

- Data model mirrors domain objects and user lifecycles.
- State ownership is clear.
- API contracts, permission checks, persistence, and caching match the product promise.
- Observability and metrics cover critical outcomes and guardrails.
- The implementation can evolve without spreading special cases.

Risk signals:

- UI complexity comes from wrong data structures.
- Important states are derived in several places.
- Business rules live in fragile frontend branches without server or data backing.
- No telemetry exists for the core promise.
- Error handling makes success look ambiguous.

### 11. Business and operating viability

Strong signals:

- The product has a plausible acquisition and distribution path.
- Pricing or monetization does not break trust.
- Support, onboarding, moderation, compliance, and operations match product scale.
- Network effects, integrations, switching costs, or workflow embedding are real, not slogans.

Risk signals:

- The product is useful only after everyone else adopts it.
- It requires expensive human operations while pretending to be self-serve.
- The team cannot explain why users switch from alternatives.

### 12. Learning loop

Strong signals:

- Core assumptions are named and testable.
- Success metrics and guardrail metrics are separated.
- The next experiment can kill or strengthen a decision.
- User feedback is connected to product changes.

Risk signals:

- Metrics are vanity metrics or too late to guide design.
- The team cannot distinguish “not enough traffic” from “wrong value proposition”.
- No rollback condition exists.

## Good product criteria

A good product usually satisfies these properties:

1. It solves a real problem for a concrete user in a concrete context.
2. It makes the valuable result easier, faster, safer, clearer, or more reliable than alternatives.
3. It has a coherent concept model users can learn without carrying the implementation in their head.
4. It turns user intention into result with low enough friction.
5. It earns trust through transparency, recovery, consistency, and honest limits.
6. It is technically shaped to support the product promise and future iteration.
7. It has a learning loop that can prove or disprove the important assumptions.

## Product anti-patterns

- Feature pile: each feature has a reason, but the product has no main path.
- UI perfume: visual polish hides weak value, unclear IA, or missing feedback.
- Dashboard swamp: data appears without interpretation or decision support.
- Setup cliff: value appears only after heavy configuration.
- Expert trap: builders expose internal abstractions as user concepts.
- Dark-pattern growth: short-term metrics are bought by spending trust.
- AI fog: generated output is confident, unsourced, and hard to control.
- Enterprise maze: permissions, roles, approvals, and exceptions leak everywhere.
- Metric mirage: team optimizes observable actions that do not prove user progress.
- Refactor theater: implementation is cleaner but the user path is not better.
