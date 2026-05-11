# ASCT 0.3 Application for dbx-skill-architect

This file explains how to apply ASCT 0.3 inside this skill without copying the full theory into `SKILL.md`.

## Core stance

Use ASCT as a placement and evaluation discipline:

1. Define the task distribution.
2. Identify base-agent failure modes.
3. Choose the cheapest safe controller.
4. Place each control in the right artifact.
5. Demand completion proof and regression signals.

Do not add ASCT terminology unless it changes architecture, placement, evals, or output quality.

## Control surfaces

| Surface | Use in skill architecture |
|---|---|
| Activation | Description, trigger evals, routing matrix, near-miss cases. |
| Intent | Mode/route/operation selection and hard gates. |
| State | Evidence sources, state contracts, project memory, freshness policy. |
| Trajectory | Workflow, stop conditions, domain discovery, patch-first improvement. |
| Execution | Scripts, deterministic validators, CLI contracts, fixtures. |
| Completion | Output contract, validation proof, limitations, artifact-body checks. |
| Evolution | Patch hypotheses, evals, changelog, rollback conditions, maturity model. |

## Placement rule

Before writing a rule into `SKILL.md`, ask whether it is actually:

- a long rubric that belongs in `references/`;
- deterministic logic that belongs in `scripts/`;
- a reusable template that belongs in `assets/`;
- persistent knowledge that needs a state contract;
- a command/hook/global instruction that belongs outside the skill;
- a collection-level conflict that belongs in a routing matrix.

## Net-value gate

A full skill package is justified only when it improves reliability over a baseline enough to pay for its costs and risks.

Common baselines:

- base agent;
- current skill version;
- lighter checklist;
- script-only helper;
- human checklist;
- competing skill.

If the baseline plus a smaller controller is better, do not produce a full package.
