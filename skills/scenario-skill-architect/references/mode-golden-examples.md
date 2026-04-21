# Mode Golden Examples

These are minimal compliant patterns. Use them as behavior samples, not as rigid wording.

## Contents

- Create needs clarification
- Create domain discovery
- Create full skill
- Critique
- Improve
- Eval runner JSON
- Triage one-off
- Safety redesign

## Create: needs clarification

```yaml
skill_architect_decision:
  mode: create
  route: needs_clarification
  operation: ask_questions
  hard_gates:
    repeatability: unknown
    stable_job: unknown
    evaluability: unknown
    safety_legitimacy: pass
  domain_substance_gates:
    target_user_defined: not_applicable
    output_depth_defined: not_applicable
    domain_variables_identified: not_applicable
    data_source_policy_defined: not_applicable
    failure_knowledge_identified: not_applicable
    expert_quality_rubric_defined: not_applicable
    worked_example_available: not_applicable
  blocking_questions:
    - "What recurring scenario should this skill handle?"
  assumptions: []
  confidence: medium
  contract_self_check:
    mode_route_compatible: true
    operation_compatible: true
    hard_gates_applied: true
    domain_substance_gates_applied: true
    full_package_overbuilt: false
    eval_artifact_present: false
    eval_schema_runner_compatible: not_applicable
    patch_not_rebuild: not_applicable
```

Ask blocking questions and stop.

## Create: domain discovery

User request: "I want to create a travel guide writing skill."

```yaml
skill_architect_decision:
  mode: create
  route: domain_discovery
  operation: ask_domain_questions
  hard_gates:
    repeatability: pass
    stable_job: pass
    evaluability: unknown
    safety_legitimacy: pass
  domain_substance_gates:
    target_user_defined: unknown
    output_depth_defined: unknown
    domain_variables_identified: unknown
    data_source_policy_defined: unknown
    failure_knowledge_identified: unknown
    expert_quality_rubric_defined: unknown
    worked_example_available: unknown
  blocking_questions:
    - "Is this for executable itineraries, inspiration posts, or booking preparation?"
    - "What variables must always appear: time, money, transfer distance, hotels, tickets, weather, walking load?"
    - "What are common travel-plan pitfalls this skill must catch?"
  assumptions: []
  confidence: high
  contract_self_check:
    mode_route_compatible: true
    operation_compatible: true
    hard_gates_applied: true
    domain_substance_gates_applied: true
    full_package_overbuilt: false
    eval_artifact_present: false
    eval_schema_runner_compatible: not_applicable
    patch_not_rebuild: not_applicable
```

Do not draft the full skill. Ask domain questions and optionally provide a provisional domain content contract with unknowns marked.

## Create: full skill

Only after hard gates and domain gates pass when applicable. Include scenario card, domain content contract if relevant, IR, package files, and runner evals.

## Critique

`mode: critique`, `route: not_a_creation_request`, `operation: critique_package`. Do not create or rewrite unless asked.

## Improve

`mode: improve`, `route: not_a_creation_request`, `operation: patch_existing_package`. Patch first. If rebuilding, include `rebuild_reason`.

## Eval runner JSON

`mode: eval`, `route: not_a_creation_request`, `operation: design_runner_evals`. Include fenced runner-compatible JSON and set `eval_artifact_present: true`.

## Triage one-off

One-off prompt wrapper should not become full skill. Use `mode: triage`, route `mini_skill` or `checklist`.

## Safety redesign

Unsafe surveillance, coercion, deception, or privacy invasion should use `mode: triage`, `route: refuse_or_redesign`, safety gate `fail`, and offer consent-aware alternatives.
