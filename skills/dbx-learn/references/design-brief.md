# DBX Learn Design Brief

This is a maintenance note for reviewers. It is not required at runtime unless someone is changing the skill.

## Scenario

Repeated task distribution: users ask an agent to help them learn technical concepts, research domains, source material, or skills in a way that should improve durable capability rather than only produce a fluent answer.

Stable job-to-be-done:

```text
Convert learning intent into a bounded mode, source policy, learning action, and completion proof.
```

Primary users:

- technical practitioners;
- researchers and builders;
- people who want durable mental models and practice loops rather than summaries.

## Worthiness gates

| Gate | Verdict | Notes |
| --- | --- | --- |
| Repeated task | pass | Learning requests recur across concepts, docs, courses, papers, and practice. |
| Stable job | pass | The transformation is stable: intent -> mode -> learning artifact/action. |
| Evaluability | pass | Trigger, mode selection, source policy, active recall, practice reps, and state safety can be checked. |
| Domain substance | pass | Learning mechanics, evidence policy, source digestion, practice reps, and state rules are concrete. |
| Safety budget | pass | Unsafe learning requests redirect; no silent persistent memory or external writes. |
| Maintenance owner | user/repo | DBX repo owner can evolve via evals and patch hypotheses. |

Verdict: `create`.

## Skill shape

```yaml
skill_shape:
  primary: knowledge
  secondary:
    - procedure
    - research
    - interaction_mode
    - project_memory
  dominant_failure_modes:
    - wrong_trigger
    - context_bloat
    - domain_shallow
    - unverified_output
    - state_drift
    - handoff_failure
  implementation_implication: "Keep SKILL.md operational, split learning principles and state/source policy into references, use evals for near-miss trigger control."
```

## Control surfaces

| Surface | Need | Mechanism |
| --- | --- | --- |
| Activation | strong | Narrow description, do-not-use list, trigger evals, adjacent skill routing. |
| Intent | strong | Mode selection and direct_answer escape hatch. |
| State | medium | Default stateless, explicit state_update contract. |
| Trajectory | strong | Learning kernel, mode workflows, stop conditions. |
| Execution | low | No scripts initially; deterministic validation is limited to eval JSON validity. |
| Completion | strong | Learning win, recall/practice, evidence boundary, state write status. |
| Evolution | medium | Trigger and output evals, design brief, changelog. |

## Placement decision

Selected placement: `skill`.

Why not only a global instruction:

- The behavior should activate for durable learning tasks, not every explanation or summary.

Why not only a command:

- Users may ask naturally for learning help; requiring a command would increase friction.

Why not only references:

- The task requires mode routing and output contracts, not only learning theory.

Why no scripts yet:

- The core failure modes are judgment, routing, pedagogy, and source/state boundaries. There is no fragile deterministic operation worth scripting in v0.1.0.

## Baseline comparison

Baseline agent risks:

- answers too fluently without testing understanding;
- produces long summaries instead of practice;
- invents current facts or citations;
- over-asks setup questions;
- writes or implies durable memory without approval;
- triggers for ordinary summaries or one-off definitions.

Expected improvement:

- better trigger boundaries;
- mode-specific learning actions;
- explicit source and state policy;
- more compact, user-friendly learning sessions;
- evals for near misses and safety redirects.

Expected cost:

- small context cost when activated;
- possible friction from active recall if the user wanted only a quick answer. The `direct_answer` escape and user preference rule reduce this cost.

## Acceptance tests

Minimum acceptance:

- positive learning requests activate;
- ordinary summaries and short factual questions do not force learning ceremony;
- concept outputs include boundaries, misconceptions, and recall;
- research outputs mention source hierarchy and freshness;
- practice outputs include artifact, success signal, stop condition, and reflection;
- state updates are candidate-only unless approved;
- unsafe learning requests redirect safely.
