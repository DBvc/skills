# Worked Example: From Better Coding Chat to a New Product Object

This is a synthetic example. It demonstrates the skill trajectory and does not claim current demand, uniqueness, or product correctness.

## 1. Seed

```yaml
arena: software development with coding agents
triggering_changes:
  - Agents can inspect repositories, invoke tools, edit multiple files, and continue for longer horizons.
  - Implementation generation is becoming cheaper than preserving shared intent and constraints.
human_situations:
  - Experienced engineers repeatedly correct plausible but directionally wrong changes.
  - Teams re-explain architecture, acceptance conditions, and prior decisions to fresh sessions.
creator_conviction:
  - The next useful developer product may change how intent survives across work, not merely improve chat.
evidence:
  - User-provided observations of context loss and review rework.
unknowns:
  - Frequency across teams.
  - Willingness to adopt another workflow object.
  - Whether existing issue, spec, and repository-memory tools solve enough of the problem.
```

## 2. Structural insight

Conventional framing:

```text
Developers need a more capable coding assistant.
```

Candidate structural insight:

```text
Because implementation generation is getting cheaper while intent, architectural constraints,
and decision history remain fragmented, teams can delegate larger changes but cannot reliably
preserve what “correct” means across sessions. Current tools remain organized around conversations,
tickets, plans, and diffs rather than a durable agreement governing the change.
```

This is an inference, not a proved market fact.

## 3. Distinct product logics

### Concept A: Coding cockpit

```yaml
core_object: agent conversation
primary_actor: individual developer
value_logic: combine model, terminal, diff, and files into one faster workspace
default_interaction: ask -> inspect -> approve
system_boundary: IDE and local repository
adoption_wedge: replace an existing coding assistant
```

**Experience specimen**

A developer asks for a feature, sees a plan and diff in one workspace, and approves the patch without switching tools.

**Magic moment**: no tool switching.

**Likely break point**: interaction becomes faster while direction drift remains unchanged.

### Concept B: Living change contract

```yaml
core_object: executable change contract
primary_actor: engineer or technical product owner
value_logic: compile fuzzy intent into a durable, inspectable agreement governing agent work
default_interaction: shape -> rehearse -> correct -> delegate -> prove
system_boundary: intent, repository facts, constraints, validation, and agent execution
adoption_wedge: consequential cross-file changes where wrong direction is expensive
```

**Experience specimen**

1. The user describes a change in ordinary language.
2. The product reconstructs the desired state change, repository surfaces, constraints, non-goals, and proof obligations.
3. Before code exists, it shows a change rehearsal: what changes, what remains fixed, where assumptions are unsupported, and where the design forks.
4. The user corrects one mistaken assumption.
5. The contract follows implementation and review, recording evidence against each obligation.

**Magic moment**: a direction error becomes visible before hundreds of plausible lines of code exist, and the correction survives later sessions.

**Likely break point**: the contract becomes ceremony or duplicates existing artifacts.

### Concept C: Ambient architecture sentinel

```yaml
core_object: evolving repository invariants
primary_actor: team and coding agents
value_logic: detect when proposed work violates architectural intent or creates drift
default_interaction: mostly ambient, intervening at plan and diff boundaries
system_boundary: repository, architecture memory, tests, and review pipeline
adoption_wedge: protect one high-churn module with known invariants
```

**Experience specimen**

An agent proposes a change. Before implementation, the sentinel identifies a second source of truth and points to the existing owner. During review it maps the diff to the violated invariant.

**Magic moment**: architecture knowledge behaves as an active constraint rather than a forgotten document.

**Likely break point**: stale or noisy rules turn the product into a sophisticated linter.

## 4. Creative selection

### A versus B

A is easier to explain and adopt, but mainly compresses an established workflow. B changes the center of gravity from a conversation to a durable change object and directly addresses intent continuity. B carries more ceremony risk but has the stronger product discontinuity.

**Advance B.**

### B versus C

C may be valuable infrastructure, but it begins from repository governance rather than the end-to-end human change. B can incorporate a narrow invariant check later without beginning as a general architecture platform.

**Advance B as the initial wedge.**

### Attack the winner

Teams already have issues, specs, plans, tests, and review templates. B may simply aggregate them and add another object to maintain.

The decisive proof is therefore not whether users like the concept. It is whether a minimal rehearsal catches a consequential direction error earlier than the existing workflow at acceptable authoring cost.

## 5. Selected conception

```yaml
product_thesis: >-
  A living change contract turns ambiguous intent into a durable, executable agreement
  that keeps humans and coding agents aligned from conception through implementation evidence.
initial_user:
  role: experienced engineer or technical product owner
  situation: delegating a cross-file change whose direction matters more than raw generation speed
before_state: repeated explanation, hidden assumptions, and late discovery of direction errors
after_state: one inspectable contract governs the change and records evidence that it is done
core_object: executable change contract
default_ritual: shape -> rehearse -> correct -> delegate -> prove
magic_moment: a wrong assumption becomes visible and correctable before implementation expands it
must_own:
  - intent and constraint representation
  - change rehearsal
  - evidence-to-obligation mapping
borrow_or_integrate:
  - issue tracker
  - repository search
  - tests and CI
  - existing coding agents
outside_initial_boundary:
  - replacing the IDE
  - general project management
  - autonomous production deployment
```

## 6. Kill list and non-goals

```yaml
kill_list:
  - A generic all-in-one coding cockpit as the product thesis.
  - A broad architecture-governance platform as the first wedge.
  - “Use a better model” as the primary solution.
deliberate_non_goals:
  - Eliminate all human review.
  - Generate perfect requirements from one prompt.
  - Prove market demand from internal enthusiasm.
  - Replace every existing artifact immediately.
```

## 7. Evidence, inference, conviction, and unknowns

```yaml
evidence:
  - Supplied observations describe repeated direction correction and context reconstruction.
inference:
  - Intent continuity may become a larger bottleneck as implementation generation improves.
conviction:
  - The durable center of gravity should move from chat history to an inspectable change object.
bet:
  - A lightweight rehearsal can expose enough costly mistakes to justify authoring overhead.
unknowns:
  - Which change classes benefit.
  - What minimum contract remains useful rather than ceremonial.
  - Whether users maintain it after coding begins.
  - How much can be inferred safely from repository evidence.
```

## 8. First proof

Use three previously completed changes and one forward-looking trial:

1. reconstruct a minimal contract from original request and repository state;
2. show the rehearsal to the engineer who performed the work;
3. ask what it would have caught, missed, or added unnecessarily;
4. compare authoring/review cost with actual rework;
5. run one new change using the specimen before implementation.

**Disconfirming signals**

- The specimen merely restates the issue and plan.
- It fails to surface the known direction mistake.
- Correcting the contract costs as much as correcting the implementation.
- Users stop maintaining it once coding begins.

## 9. Handoff

```yaml
state: concept_selected_unvalidated
next_skill: dbx-product-judgment
next_question: >-
  For which change classes does the living change contract produce enough earlier error detection,
  trust, and coordination value to justify setup and maintenance cost?
required_evidence:
  - three reconstructed cases
  - one forward-looking prototype trial
  - comparison against current issue/plan/review workflow
```

The example ends before PRD or implementation planning because the thesis still requires product judgment and prototype evidence.
