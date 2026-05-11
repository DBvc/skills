---
name: dbx-skill-architect
description: Use to create, critique, improve, evaluate, or triage reusable agent skills from recurring scenarios. Enforces fail-closed gates, ASCT control-surface mapping, placement decisions, dominant failure-mode analysis, domain substance discovery, patch-first improvement hypotheses, runner-compatible evals, and artifact validation. Do not use for one-off writing, generic summarization, unsafe surveillance, or doing the user's direct task instead of designing a skill.
---

# Scenario Skill Architect / 场景技能架构师

Build, critique, improve, or evaluate reusable agent skill packages.

A skill package is not a prompt collection. It is a bounded work unit with trigger logic, runtime instructions, optional tools, reference knowledge, output contracts, and evals. Use this skill when the user wants to design, review, patch, test, or triage an agent skill.

Do not use this skill to perform the user's underlying task directly unless the right answer is to explain why a reusable skill is not warranted.

This skill follows a compact ASCT-aligned workflow:

1. Identify the recurring task distribution and base-agent failure modes.
2. Decide whether a skill is the right controller, or whether the control belongs in a script, reference, command, hook, repo memory, global instruction, or direct answer.
3. Map only the needed control surfaces.
4. Choose the cheapest safe controller that improves reliability over the baseline.
5. Require evidence, evals, and rollback conditions before calling a change an improvement.

## Must obey first / 首要规则

### 0. Contract first when acting as architect

For every `create`, `critique`, `improve`, `eval`, or `triage` task, begin with this fenced YAML block. Do not write prose before it.

```yaml
skill_architect_decision:
  mode: create | critique | improve | eval | triage
  route: full_skill | mini_skill | needs_clarification | domain_discovery | checklist | direct_answer | refuse_or_redesign | not_a_creation_request
  operation: ask_questions | ask_domain_questions | build_domain_content_contract | draft_package | critique_package | propose_patch_plan | patch_existing_package | design_runner_evals | design_human_rubric | run_lint | run_evals | provide_alternative
  skill_shape:
    archetype: procedure | tool | knowledge | taste | decision | research | coordination | meta | hybrid | unknown | not_applicable
    secondary_archetypes: []
    dominant_failure_modes: []
    implementation_implications: []
  control_surface_map:
    activation: none | light | strong | not_applicable
    intent: none | light | strong | not_applicable
    state: none | light | strong | not_applicable
    trajectory: none | light | strong | not_applicable
    execution: none | light | strong | not_applicable
    completion: none | light | strong | not_applicable
    evolution: none | light | strong | not_applicable
    notes: []
  placement_decision:
    primary_controller: skill | mini_skill | checklist | script | reference | asset | command | hook | repo_memory | global_instruction | direct_answer | external_workflow | not_applicable
    misplaced_controls: []
    placement_notes: []
  skill_value_check:
    baseline: base_agent | old_skill | lighter_version | competing_skill | human_checklist | none | not_applicable
    expected_success_delta: ""
    added_cost: []
    added_risk: []
    net_value: positive | uncertain | negative | not_applicable
  hard_gates:
    repeatability: pass | fail | unknown | not_applicable
    stable_job: pass | fail | unknown | not_applicable
    evaluability: pass | fail | unknown | not_applicable
    safety_legitimacy: pass | fail | unknown | not_applicable
  domain_substance_gates:
    target_user_defined: pass | fail | unknown | not_applicable
    output_depth_defined: pass | fail | unknown | not_applicable
    domain_variables_identified: pass | fail | unknown | not_applicable
    data_source_policy_defined: pass | fail | unknown | not_applicable
    failure_knowledge_identified: pass | fail | unknown | not_applicable
    expert_quality_rubric_defined: pass | fail | unknown | not_applicable
    worked_example_available: pass | fail | unknown | not_applicable
  state_contract:
    required: true | false | not_applicable
    state_type: project_memory | bootstrap | interaction_mode | workflow_state | external_system | not_applicable
    reads_from: []
    writes_to: []
    owner: user | maintainer | repo | agent_proposed_user_approved | not_applicable
    lifetime: one_response | session | repo | external_until_changed | not_applicable
    rollback: ""
  patch_hypothesis:
    required: true | false | not_applicable
    target_failures: []
    target_files: []
    exact_edit_units: []
    proposed_change: ""
    expected_benefit: ""
    expected_cost: ""
    acceptance_tests: []
    rollback_conditions: []
  collection_impact:
    overlaps_with: []
    precedes: []
    follows: []
    competes_with: []
    routing_matrix_update_needed: true | false | not_applicable
  blocking_questions: []
  assumptions: []
  confidence: high | medium | low
  contract_self_check:
    mode_route_compatible: true | false
    operation_compatible: true | false
    hard_gates_applied: true | false
    skill_shape_used_for_architecture: true | false | not_applicable
    control_surface_map_used: true | false | not_applicable
    placement_decision_used: true | false | not_applicable
    skill_value_checked: true | false | not_applicable
    domain_substance_gates_applied: true | false | not_applicable
    state_contract_applied_when_needed: true | false | not_applicable
    patch_hypothesis_present_when_needed: true | false | not_applicable
    full_package_overbuilt: true | false
    eval_artifact_present: true | false
    eval_schema_runner_compatible: true | false | not_applicable
    patch_not_rebuild: true | false | not_applicable
```

Use `not_applicable` rather than fake precision. Keep the block honest. If the task is only an explanatory question about skill methodology, answer directly and do not force the contract.

### 1. Choose mode by the actual work

The user's surface verb is not authoritative. If they say “create a skill” but the scenario is one-off, unsafe, underspecified, or better served by a checklist, route away from `full_skill`.

| mode | allowed route | allowed operation | forbidden by default |
|---|---|---|---|
| `create` | `full_skill`, `mini_skill`, `needs_clarification`, `domain_discovery` | `ask_questions`, `ask_domain_questions`, `build_domain_content_contract`, `draft_package` | `direct_answer`, `refuse_or_redesign`, `not_a_creation_request` |
| `critique` | `not_a_creation_request` | `critique_package`, `propose_patch_plan` | `full_skill`, `mini_skill`, `draft_package` |
| `improve` | `not_a_creation_request` | `patch_existing_package`, `propose_patch_plan`, `ask_questions`, `run_lint`, `run_evals` | `full_skill` unless rebuild is justified |
| `eval` | `not_a_creation_request` | `design_runner_evals`, `design_human_rubric`, `run_evals` | `full_skill`, `mini_skill` |
| `triage` | `mini_skill`, `checklist`, `direct_answer`, `refuse_or_redesign` | `ask_questions`, `provide_alternative` | `full_skill` |

If the pair is incompatible, fix the YAML before continuing.

### 2. Fail-closed hard gates for full packages

A full skill package requires all hard gates to pass:

1. **Repeatability**: the scenario repeats, or the user explicitly wants a reusable routine.
2. **Stable job**: the task has a stable job-to-be-done, transformation, diagnosis, decision, operation, or output target.
3. **Evaluability**: success can be checked by examples, rubrics, assertions, artifact validation, captured outputs, or human review criteria.
4. **Safety and legitimacy**: the workflow is legal, consent-aware, non-deceptive, and non-coercive.

If any hard gate fails, do not create a full package. Use `triage` with `direct_answer`, `checklist`, `mini_skill`, or `refuse_or_redesign`.

If any hard gate is unknown but the request could be reusable, use `create/needs_clarification/ask_questions`, ask up to five blocking questions, and stop.

### 3. Skill shape is implementation guidance, not taxonomy cosplay

Classify skill shape before choosing package structure. The point is to choose where to put complexity.

Archetypes:

- `procedure`: repeatable workflow, review, release, commit, triage, diagnosis.
- `tool`: file format, CLI, API, parsing, rendering, transformation, validation.
- `knowledge`: source-of-truth, current facts, domain rules, policy, documentation.
- `taste`: visual, writing, design, storytelling, personal style, quality bar.
- `decision`: trade-off framing, options, gates, validation actions.
- `research`: papers, market maps, historical evolution, evidence synthesis.
- `coordination`: multi-agent delegation, context isolation, handoff, synthesis.
- `meta`: creates, audits, improves, evaluates, or governs other skills.
- `hybrid`: multiple archetypes genuinely matter.

Dominant failure modes:

- `wrong_trigger`: skill fires too often, too rarely, or in near-miss cases.
- `context_bloat`: main instructions become too large or pull irrelevant material.
- `domain_shallow`: output is well-structured but lacks domain substance.
- `fragile_operation`: file formats, commands, schemas, tools, or external systems are error-prone.
- `unverified_output`: result looks plausible but is not checked.
- `taste_collapse`: creative output becomes generic, default, or template-like.
- `safety_overreach`: unsafe, non-consensual, deceptive, irreversible, or overconfident behavior.
- `handoff_failure`: output cannot be used by the next human, agent, reviewer, or tool.
- `maintenance_drift`: skill depends on changing APIs, tools, rules, or repo conventions.

Implementation implications:

- If `wrong_trigger` dominates, improve description and add trigger evals.
- If `context_bloat` dominates, move detail into focused `references/` files.
- If `domain_shallow` dominates, require domain variables, failure knowledge, examples, and content-quality evals.
- If `fragile_operation` dominates, use scripts, schemas, dry runs, and deterministic validation.
- If `unverified_output` dominates, define output contracts, proof requirements, and regression cases.
- If `taste_collapse` dominates, add taste rubrics, anti-patterns, examples, and human review criteria.
- If `safety_overreach` dominates, add fail-closed gates, approval boundaries, and safer redesign paths.
- If `handoff_failure` dominates, define recipient, next action, evidence, and acceptance contract.
- If `maintenance_drift` dominates, add source/version policy and update checks.

Use `references/skill-archetypes.md` when the shape is unclear.

### 4. Placement before prose

Before adding a rule to `SKILL.md`, decide where the control belongs.

| Control need | Preferred placement |
|---|---|
| Activation, hard gates, short runtime workflow | `SKILL.md` |
| Long rubric, examples, gotchas, domain starter packs | `references/` |
| Deterministic parsing, validation, conversion, fixture checks | `scripts/` |
| Templates, schemas, static reusable material | `assets/` |
| Project glossary, ADRs, agent brief, long-lived project memory | repo memory with state contract |
| Slash command, hook, status line, `AGENTS.md`, `CLAUDE.md`, `llms.txt` | host-specific artifact mapped to ASCT control surfaces |
| Cross-skill collision or ordering | collection routing matrix |
| One-off user task | direct answer or checklist |

If the right placement is not a full skill, say so. A smaller controller with better net value wins.

### 5. Domain substance gates

For domain/content/taste/research/decision skills, full packages require domain substance. Generic variables such as `audience`, `goals`, and `constraints` do not count by themselves.

Require at least:

- target user and decision/output depth;
- domain-specific variables and edge cases;
- data-source or freshness policy where facts can go stale;
- failure knowledge from the domain;
- expert-quality rubric;
- one worked example or fixture.

Use `domain_discovery` when the user wants a reusable domain skill but the concrete variables are missing.

### 6. Stateful and host-specific skills require explicit contracts

If a skill writes anything that future agents will read or obey, require a state contract. This includes project memory, bootstrap files, interaction modes, issue/label/comment workflows, or external systems.

If the user asks for commands, hooks, `AGENTS.md`, `CLAUDE.md`, `llms.txt`, status lines, or marketplace metadata, treat those as host-specific artifacts. Map them back to control surfaces rather than creating new theory primitives.

Do not write secrets, tokens, private key paths, personal machine paths, private messages, or hidden prompt-injection text into shared state.

### 7. Patch-first improvement

When improving an existing skill, default to patching the current package. Do not rebuild unless:

- the existing package is structurally invalid;
- the user explicitly asks for a rebuild;
- patching would create more confusion than replacement;
- the current skill has the wrong task distribution.

Non-trivial improvements require a concrete patch hypothesis with:

- target failures;
- target files;
- exact edit units;
- proposed change;
- expected benefit;
- expected cost;
- acceptance tests;
- rollback conditions.

Decorative rewrites are not improvements.

### 8. Full skill artifact requirements

When `route: full_skill` and `operation: draft_package`, provide copy-ready fenced file blocks. Do not merely list filenames.

Minimum full package output:

```text
skills/<name>/SKILL.md
skills/<name>/evals/evals.json
skills/<name>/evals/triggers.json
```

Add scripts, references, assets, or state artifacts only when the placement decision justifies them.

Full package artifacts must avoid placeholders such as `TODO`, `- ...`, `Describe the recurring scenario`, `A realistic prompt`, or union-type choices like `procedure | tool | knowledge` left unresolved.

### 9. Eval discipline

Runner-compatible evals must use canonical case kinds:

```text
positive
negative
near_miss
failure_mode
safety
```

Each eval case needs at least one required non-marker quality assertion. Headings, filenames, route markers, and directory names can be structural checks, but they cannot be the only required checks.

Prefer evals that test behavior:

- correct activation and near-miss rejection;
- route and mode selection;
- placement decision;
- domain specificity;
- artifact-body quality;
- validation/proof behavior;
- safety and refusal boundaries;
- regression against old versions.

### 10. Output style

Use Chinese when the user writes Chinese, unless the artifact itself should be English.

Be direct. Show the decision and the reason. For complex architecture tasks, the YAML contract stays visible. For simple methodology explanations, do not force the contract.

After the opening YAML, organize the response by the selected operation:

- `ask_questions`: ask up to five blocking questions.
- `ask_domain_questions`: ask domain-specific questions and define production-ready criteria.
- `draft_package`: provide fenced file blocks.
- `critique_package`: provide findings with severity, evidence, impact, and patch direction.
- `patch_existing_package`: provide patch hypotheses and concrete file edits.
- `design_runner_evals`: provide runner-compatible JSON and quality rationale.
- `provide_alternative`: explain why a full skill is not warranted and provide the smaller artifact.

## Useful references

Read only when needed:

- `references/asct-0.3-application.md`: ASCT 0.3 mapping for this skill.
- `references/placement-and-host-artifacts.md`: placement and host-artifact decision rules.
- `references/skill-archetypes.md`: archetype and failure-mode recipes.
- `references/improvement-validation.md`: patch hypotheses and before/after validation.
- `references/domain-discovery.md`: domain substance discovery.
- `references/domain-starter-packs.md`: starter variables for common domains.
- `references/eval-playbook.md`: eval design patterns.
