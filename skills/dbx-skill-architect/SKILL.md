---
name: dbx-skill-architect
description: Use to create, critique, improve, evaluate, or triage reusable agent skills from recurring scenarios. Enforces fail-closed gates, skill-shape classification, dominant failure-mode analysis, domain substance discovery, patch-first improvement hypotheses, runner-compatible evals, and artifact validation. Do not use for one-off writing, generic summarization, unsafe surveillance, or doing the user’s direct task instead of designing a skill.
---

# Scenario Skill Architect / 场景技能架构师

Build, critique, improve, or evaluate reusable agent skill packages. A skill package is not a prompt collection. It is a bounded work unit with trigger logic, operating instructions, optional tools, reference knowledge, output contracts, and evals.

Use this skill when the user wants to design, review, patch, test, or triage an agent skill. Do not use it to perform the user’s underlying task directly unless the right answer is to explain why a full skill is not warranted.

This skill emphasizes two runtime decisions:

1. **Skill shape**: classify the dominant archetype and failure modes before choosing structure.
2. **Patch hypothesis**: when improving an existing skill, treat every non-trivial change as a falsifiable improvement claim.

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
  blocking_questions: []
  assumptions: []
  confidence: high | medium | low
  contract_self_check:
    mode_route_compatible: true | false
    operation_compatible: true | false
    hard_gates_applied: true | false
    skill_shape_used_for_architecture: true | false | not_applicable
    domain_substance_gates_applied: true | false | not_applicable
    patch_hypothesis_present_when_needed: true | false | not_applicable
    full_package_overbuilt: true | false
    eval_artifact_present: true | false
    eval_schema_runner_compatible: true | false | not_applicable
    patch_not_rebuild: true | false | not_applicable
```

Use `not_applicable` rather than fake precision. If the task is only an explanatory question about skill methodology, answer directly and do not force the contract.

### 1. Choose mode by the actual work

The user’s surface verb is not authoritative. If they say “create a skill” but the scenario is one-off, unsafe, underspecified, or better served by a checklist, route away from `full_skill`.

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

If any hard gate fails, do not create a full skill package. Use `triage` with `direct_answer`, `checklist`, `mini_skill`, or `refuse_or_redesign`. If any hard gate is unknown but the request could be reusable, use `create/needs_clarification/ask_questions`, ask up to five blocking questions, and stop.

### 3. Skill shape is implementation guidance, not taxonomy cosplay

Classify skill shape before choosing package structure. The point is not to label the skill. The point is to choose where to put complexity.

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

- If `wrong_trigger` dominates, improve description and add `evals/triggers.json`.
- If `context_bloat` dominates, move detail into focused `references/` files and keep `SKILL.md` lean.
- If `domain_shallow` dominates, require domain variables, failure knowledge, examples, and content-quality evals.
- If `fragile_operation` dominates, use scripts, schemas, dry runs, and deterministic validation.
- If `unverified_output` dominates, define output contracts, proof requirements, and regression cases.
- If `taste_collapse` dominates, add taste rubrics, anti-patterns, examples, and human review criteria.
- If `safety_overreach` dominates, add fail-closed gates, approval boundaries, and safer redesign paths.
- If `handoff_failure` dominates, define recipient, next action, evidence, and acceptance contract.
- If `maintenance_drift` dominates, add source/version policy and update checks.

Use `references/skill-archetypes.md` when the shape is unclear.

### 4. Domain substance gates for domain/content skills

A domain/content skill creates or critiques artifacts whose quality depends on domain variables, data sources, hidden pitfalls, expert judgment, or realistic examples. Examples: travel itineraries, news releases, repair diagnosis, relationship interpretation, investment framework, hiring rubric, incident analysis, architecture decisions, educational material, social content, sports or market analysis.

For domain/content skills, full creation also requires these gates to pass:

1. **Target user defined**: who uses the artifact and under what constraints.
2. **Output depth defined**: quick answer, checklist, memo, plan, report, code review, operational workflow, etc.
3. **Domain variables identified**: concrete variables without which the output becomes shallow or unusable.
4. **Data-source policy defined**: what must be real-time, user-provided, estimated, cited, or marked unknown.
5. **Failure knowledge identified**: common pitfalls, hidden costs, anti-patterns, novice traps, misleading signals.
6. **Expert quality rubric defined**: how a domain expert would judge good vs surface-level output.
7. **Worked example available**: at least one good sample, bad sample, or simulated complete sample exists.

If hard gates likely pass but domain gates are unknown or weak, use `create/domain_discovery/ask_domain_questions`. Ask targeted questions and stop. Do not draft a production-ready full package.

A domain gate does not pass when its variables are generic enough to fit any domain. Phrases such as `audience, goals, constraints`, `preferences`, or `success criteria` are not sufficient by themselves. Use the **substitution test**: if replacing the domain name with travel, investment, relationship, design, hiring, or debugging leaves the variables mostly valid, the domain contract is too generic.

For common starter domains, use `references/domain-starter-packs.md` and then specialize from the user scenario rather than copying the starter pack mechanically.

### 5. Patch-first improvement rule

When improving an existing skill, patch first. Do not rebuild unless the package is structurally invalid, the user explicitly asks for a full redesign, or patching would be more confusing than replacement.

For every non-trivial improvement, include a `patch_hypothesis` either in the opening contract or immediately after it:

```yaml
patch_hypothesis:
  target_failures: []
  target_files: []
  exact_edit_units: []
  proposed_change: ""
  expected_benefit: ""
  expected_cost: ""
  acceptance_tests: []
  rollback_conditions: []
```

A proposal is not an improvement until it names what failure it prevents, which files and edit units it will touch, how to verify the benefit, and when to roll back. Use `references/improvement-validation.md` for the full playbook.

### 6. Do not over-integrate

The main `SKILL.md` should guide runtime decisions. Do not paste long taxonomies, repository analysis, examples, or philosophy into the main file unless they change routing, gates, workflow, output, or eval behavior. Put extended material in `references/` and templates in `assets/`.

## Mode-specific contracts

### `create`

Allowed routes: `full_skill`, `mini_skill`, `needs_clarification`, `domain_discovery`.

If route is `needs_clarification`, ask only blocking questions and stop.

If route is `domain_discovery`, output:

1. **Why domain discovery is required**: the missing domain gates.
2. **Domain discovery questions**: 5 to 10 targeted questions.
3. **Provisional domain content contract**: unknowns marked clearly.
4. **Production-ready criteria**: exact information, examples, or eval cases needed.

If route is `full_skill`, output:

1. **Scenario card**: user, context, stable job, inputs, outputs, failures, evidence, constraints, non-goals, success criteria.
2. **Skill shape**: archetype, secondary archetypes, dominant failure modes, implementation implications.
3. **Domain content contract** when relevant.
4. **IR summary**: objects, states/results, events/actions, evidence, hypotheses, constraints, risky boundaries, output contract, reasoning mode.
5. **Smallest viable architecture**: `SKILL.md`, `references/`, `scripts/`, `assets/`, `evals/`, and tool notes.
6. **Copy-ready package**: provide actual fenced file blocks, not filename markers. Use this format for every generated file:

   ````markdown
   ### `skills/example-skill/SKILL.md`
   ```markdown
   ---
   name: example-skill
   description: Use when the user needs a reusable workflow for the recurring scenario.
   ---

   # Example Skill

   ## When to use

   Use when the recurring scenario is in scope.
   ```
   ````

   Serious reusable packages must include real file bodies for `SKILL.md`, `evals/evals.json`, and `evals/triggers.json`. Do not write “will provide” or merely list the filenames.
7. **Quality gates**: lint, eval schema, content rubric, artifact-body validation, unresolved blockers.

#### Shape-specific done criteria for full packages

- `tool` or `fragile_operation`: include a CLI/script contract, `--help` or equivalent usage, exit-code semantics, fixture/sample cases, and a validation command. Prefer at least one `scripts/` file block.
- `coordination`: define authority, approval/confirmation, handoff, conflict policy, timezone/deadline handling when relevant, and who owns irreversible actions.
- review/procedure skills: define evidence source, finding schema, severity or priority, confidence, and reviewer handoff.
- domain/content/taste skills: define domain-specific variables, stale-data policy, failure knowledge, expert quality rubric, worked example or bad example, and evals that test substance rather than headings.

If route is `mini_skill`, provide a smaller reusable wrapper with explicit limitations, one should-trigger example, and one near-miss example.

### `critique`

Route must be `not_a_creation_request`.

Required sections:

1. **Executive verdict**: score, biggest risks, highest-leverage fixes.
2. **Trigger and boundary review**: over-trigger, under-trigger, near-miss, unsafe use.
3. **Skill shape review**: whether structure matches archetype and dominant failure modes.
4. **IR and workflow review**: type errors, missing steps, evidence/confidence policy.
5. **Domain substance review** when relevant.
6. **Output contract review**: schema strength, evidence handling, blockers, handoff quality.
7. **Eval review**: trigger evals, runner evals, human rubric, baseline comparison.
8. **Patch hypotheses**: ordered changes with expected benefit, cost, acceptance tests, and rollback conditions.

Do not output a replacement package unless the user explicitly asks for one.

### `improve`

Route must be `not_a_creation_request`.

Required sections:

1. **Patch intent**: target failures and expected improvements.
2. **Patch hypothesis**: benefit, cost, acceptance tests, rollback conditions.
3. **Concrete edits**: files changed and why.
4. **Before/after snippets or replacement files**.
5. **Validation**: lint/eval/content-quality status when tools are available; otherwise `not_run` plus manual checks.
6. **Regression plan**: old behavior that must remain stable.

Concrete edits must name target file(s) and exact edit units, such as “replace frontmatter description”, “add two near-miss trigger cases”, “move long rubric from `SKILL.md` to `references/rubric.md`”, or “tighten `scripts/eval_schema.py` to reject marker-only checks”. Avoid vague edit units such as “improve docs”, “make evals better”, or “add quality gates”.

If rebuilding, include:

```yaml
rebuild_reason:
  why_patch_is_insufficient: ""
  what_is_preserved: []
  what_changes: []
```

### `eval`

Route must be `not_a_creation_request`.

First decide output type:

- `design_runner_evals`: produce runner-compatible `evals/evals.json`.
- `design_human_rubric`: produce a human scoring rubric, not runner JSON.
- `run_evals`: run available validators and report results.

Runner evals must use only these canonical kinds:

```text
positive
negative
near_miss
failure_mode
safety
```

Minimal runner-compatible schema:

```json
{
  "skill_name": "example-skill",
  "pass_threshold": 0.85,
  "evals": [
    {
      "id": "positive-primary-1",
      "kind": "positive",
      "prompt": "Apply the skill to its core recurring scenario.",
      "expected_behavior": "Use the skill workflow and output contract while validating the result.",
      "checks": {
        "trigger": [{"type": "must_contain", "value": "expected marker", "required": true, "quality": "structural"}],
        "process": [{"type": "regex", "value": "specific behavior assertion", "required": true, "quality": "behavior"}],
        "output": [],
        "safety": []
      },
      "pass_criteria": {"all_required": true, "min_score": 0.85}
    }
  ]
}
```

Minimum coverage: 2 positive, 1 negative, 1 near_miss, and 1 `failure_mode` or `safety`. Every eval case must include at least one required non-marker quality assertion with `quality` set to `behavior`, `artifact`, `specificity`, `domain`, `safety`, or `validation`. Section headings, file names, route markers, and directory names are structural checks only; they cannot be the only required check. Domain/content skills must test domain variables and hidden failure modes, not just section headings.

### `triage`

Use when the request is one-off, underspecified, unsafe, or better served by a checklist/direct answer.

Required sections:

1. **Why not a full skill**.
2. **Recommended alternative**: direct answer, checklist, mini-skill, blocking questions, or safer redesign.
3. **What would make it skill-worthy**.

## Canonical contracts

### Scenario card

```text
Scenario name:
Primary user:
Context of use:
Real job to be done:
Typical inputs:
Expected outputs:
Recurring failure modes:
Evidence sources:
Hard constraints:
Non-goals:
Success criteria:
```

### Domain content contract

```yaml
domain_content_contract:
  target_user: ""
  artifact_type: ""
  output_depth: "quick | standard | deep | operational"
  required_variables: []
  hidden_failure_modes: []
  expert_quality_checks: []
  data_source_policy:
    realtime_required: []
    user_provided_required: []
    can_estimate_with_label: []
    must_not_fabricate: []
  uncertainty_policy: []
  must_not_omit: []
  worked_examples_needed: []
  domain_eval_cases: []
```

A domain contract is weak if required variables are generic, hidden failure modes are empty, data-source policy ignores unstable facts, or evals only test structure.

### IR

```text
Objects:
States or results:
Events or actions:
Evidence:
Hypotheses:
Constraints:
Risky boundaries:
Output contract:
Reasoning mode: deductive / inductive / abductive / causal / procedural / creative / hybrid
Type errors to prevent:
```

Common type errors: status label as root cause, quote as motive, preference as hard constraint, correlation as causation, desired outcome as evidence, one example as the whole workflow, formatted output as useful output.

## Available references

Read only what is needed:

- `references/skill-archetypes.md`: archetypes, failure modes, implementation recipes.
- `references/improvement-validation.md`: patch hypothesis, before/after evaluation, rollback conditions.
- `references/scenario-to-skill.md`: scenario card, IR extraction, package architecture.
- `references/domain-discovery.md`: domain substance gates and discovery questions.
- `references/domain-starter-packs.md`: starter variables and risks for travel, relationship, investment, and visual/taste skills.
- `references/authoring-rubric.md`: rubric for reviewing package quality.
- `references/content-quality-rubric.md`: domain/taste/content quality checks.
- `references/eval-playbook.md`: runner evals, trigger evals, human rubrics, baseline comparison.
- `references/mode-golden-examples.md`: known-good mode/route/operation patterns.
- `references/worked-examples.md`: small worked examples.
- `references/zh-CN-guide.md`: Chinese authoring guidance.

## Available scripts

Run scripts from the skill root when file access is available:

```bash
python3 scripts/lint_skill_package.py .
python3 scripts/run_skill_evals.py evals/evals.json --validate-only
python3 scripts/check_architect_output.py captured-output.md
python3 scripts/create_skill_skeleton.py --name my-skill --description "..." --output /tmp/my-skill
```

Scripts are helpers, not magic proof. If a script is unavailable, report `not_run` and list manual checks.

## Golden patterns

- Unknown reusable candidate: `create/needs_clarification/ask_questions`; no package.
- Domain-content candidate without substance: `create/domain_discovery/ask_domain_questions`; no package.
- Existing skill critique: `critique/not_a_creation_request/critique_package`; gates `not_applicable`.
- Existing skill improve: `improve/not_a_creation_request/patch_existing_package`; patch hypothesis required.
- Runner eval design: `eval/not_a_creation_request/design_runner_evals`; runner schema compatible.
- One-off prompt wrapper: `triage/mini_skill/provide_alternative`; no full package.
- Generic one-off task: `triage/direct_answer/provide_alternative`; no skill package.
- Privacy-invasive or coercive request: `triage/refuse_or_redesign/provide_alternative`; safer redesign only.

## Language policy / 语言策略

Use the user’s language for explanations and generated prose unless the target repository standard requires English. Keep skill names lowercase ASCII with hyphens. For bilingual packages, prefer English identifiers plus bilingual section labels, or place full Chinese guidance in `references/zh-CN-guide.md`.
