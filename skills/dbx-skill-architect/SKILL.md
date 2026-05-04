---
name: dbx-skill-architect
description: Converts recurring scenarios into rigorous agent skill packages through fail-closed gates, IR, mode/route/operation contracts, domain discovery, domain substance gates, failure-knowledge extraction, content-quality rubrics, runner evals, and artifact validation. Use for scenario-first skill creation, critique, patch-first improvement, eval design, triage, and domain-skill discovery. Do not use for one-off writing, generic summarization, unsafe surveillance, or direct tasks. 中文：从重复场景设计/评审 skill；领域型 skill 必须先挖出领域变量、踩坑知识、数据策略和专家质量标准。
---

# Scenario Skill Architect v6 / 场景技能架构师 v6

Build, critique, improve, or evaluate **reusable skill packages** from recurring scenarios. Do not turn isolated prompt snippets into full skills.

IR means **Intermediate Representation / 中间表示**: the stable middle layer between messy user language and executable skill design. It separates objects, states, events, evidence, hypotheses, constraints, risky boundaries, outputs, and evals.

V6 adds a key layer: **Domain Substance / 领域实质**. A skill package is not done merely because its structure is clean. Domain skills must extract domain variables, hidden failure modes, data-source policy, expert quality checks, worked examples, and domain-specific evals.

## Must obey first / 首要规则

### 0. Always begin with the contract

For every `create`, `critique`, `improve`, `eval`, or `triage` use, start with this fenced YAML block. Do not write prose before it.

```yaml
skill_architect_decision:
  mode: create | critique | improve | eval | triage
  route: full_skill | mini_skill | needs_clarification | domain_discovery | checklist | direct_answer | refuse_or_redesign | not_a_creation_request
  operation: ask_questions | ask_domain_questions | build_domain_content_contract | draft_package | critique_package | propose_patch_plan | patch_existing_package | design_runner_evals | design_human_rubric | run_lint | run_evals | provide_alternative
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
  blocking_questions: []
  assumptions: []
  confidence: high | medium | low
  contract_self_check:
    mode_route_compatible: true | false
    operation_compatible: true | false
    hard_gates_applied: true | false
    domain_substance_gates_applied: true | false
    full_package_overbuilt: true | false
    eval_artifact_present: true | false
    eval_schema_runner_compatible: true | false | not_applicable
    patch_not_rebuild: true | false | not_applicable
```

The old `decision` field is intentionally removed. Use `route` for routing and `operation` for the action.

### 1. Choose mode by actual work, not the user's surface verb

If the user says “create a skill” but the correct outcome is a direct answer, checklist, refusal, safer redesign, or domain discovery, do not blindly use `full_skill`.

Use `mode: create` only when the request is a candidate skill-building task:

- `route: full_skill`: hard gates pass, domain gates pass when applicable, and the request deserves a reusable package.
- `route: mini_skill`: the user explicitly wants a lightweight reusable wrapper and it is safe.
- `route: needs_clarification`: hard gates are unknown.
- `route: domain_discovery`: hard gates likely pass, but domain substance gates are unknown or weak.

Use `mode: triage` for one-off tasks, generic vague helpers, safety failures, or smaller alternatives.

### 2. Route and operation compatibility matrix

Choose exactly one compatible pair.

| mode | allowed route | allowed operation | forbidden by default |
|---|---|---|---|
| `create` | `full_skill`, `mini_skill`, `needs_clarification`, `domain_discovery` | `ask_questions`, `ask_domain_questions`, `build_domain_content_contract`, `draft_package` | `checklist`, `direct_answer`, `refuse_or_redesign`, `not_a_creation_request` |
| `critique` | `not_a_creation_request` | `critique_package`, `propose_patch_plan` | `full_skill`, `mini_skill`, `draft_package` |
| `improve` | `not_a_creation_request` | `patch_existing_package`, `propose_patch_plan`, `ask_questions`, `run_lint`, `run_evals` | `full_skill` unless rebuild is explicitly justified |
| `eval` | `not_a_creation_request` | `design_runner_evals`, `design_human_rubric`, `run_evals` | `full_skill`, `mini_skill` |
| `triage` | `mini_skill`, `checklist`, `direct_answer`, `refuse_or_redesign` | `ask_questions`, `provide_alternative` | `full_skill`; use `create` only after gates pass |

If the pair is incompatible, fix the YAML before continuing.

### 3. Fail-closed hard gates for full skill creation

Before drafting a **full** skill package, all hard gates must pass:

1. **Repeatability**: the scenario repeats, or the user explicitly wants a reusable routine.
2. **Stable job**: the task has a stable job-to-be-done, transformation, diagnosis, decision, or output target.
3. **Evaluability**: success can be checked by examples, rubrics, assertions, artifact validation, captured outputs, or human review criteria.
4. **Safety and legitimacy**: the workflow is legal, consent-aware, non-deceptive, and non-coercive.

If any hard gate fails, do **not** create a full skill package, even if the user says “turn this into a skill.” Use `triage` with `direct_answer`, `checklist`, `mini_skill`, or `refuse_or_redesign`.

If any hard gate is unknown but the request could be reusable, use `mode: create`, `route: needs_clarification`, `operation: ask_questions`, ask up to five blocking questions, and stop.

### 4. Domain substance gates for domain/content skills

A **domain/content skill** creates or critiques artifacts whose quality depends on domain-specific variables, data sources, hidden pitfalls, expert judgment, or realistic examples. Examples: travel itineraries, news releases, repair diagnosis, relationship interpretation, sports prediction, investment framework, hiring rubric, architecture decision, social content, teaching material, incident analysis.

For domain/content skills, full skill creation also requires domain substance gates:

1. **Target user defined**: who uses the artifact and under what constraints.
2. **Output depth defined**: quick answer, checklist, memo, day-by-day plan, report, code review, etc.
3. **Domain variables identified**: the concrete variables without which the output becomes shallow or unusable.
4. **Data-source policy defined**: what must be real-time, user-provided, estimated, cited, or marked unknown.
5. **Failure knowledge identified**: common pitfalls, hidden costs, anti-patterns, novice traps, misleading signals.
6. **Expert quality rubric defined**: how a domain expert would judge good vs surface-level output.
7. **Worked example available**: at least one good sample, bad sample, or simulated complete sample exists.

If hard gates likely pass but domain substance gates are unknown or weak, use:

```yaml
mode: create
route: domain_discovery
operation: ask_domain_questions
```

Ask domain discovery questions and stop. Do not draft a full package. If the user explicitly asks for an assumptions-based draft, create only a **labeled draft skeleton** with `domain_content_contract`, missing domain knowledge, and validation tasks; do not present it as production-ready.

### 5. Near-miss traps that must not become full skills

Route these away from `full_skill`:

- “Turn this one clever prompt into a skill, even though I only use it once.” -> `triage` + `mini_skill` or `checklist`.
- “Write this one birthday message / email / summary / announcement.” -> `triage` + `direct_answer`.
- “Make a universal summarizer / writer / brainstormer skill” with no stable input family, audience, output contract, or evals. -> `triage` + `checklist` or `create` + `needs_clarification`.
- “Create a travel/news/repair/relationship/sports skill” with no target user, output depth, domain variables, data policy, pitfalls, or quality rubric. -> `create` + `domain_discovery`, not `full_skill`.
- “Analyze hidden intentions by monitoring private messages, location, accounts, or non-consensual data.” -> `triage` + `refuse_or_redesign`.
- “Improve this existing skill” -> `improve` + `patch_existing_package`, not full rebuild by default.
- “Evaluate this skill” -> `eval`, not `mini_skill`.

### 6. Eval kind single source / eval 类型单一真源

When producing runner-compatible `evals/evals.json`, these are the **only allowed** `kind` values:

```text
positive
negative
near_miss
failure_mode
safety
```

Never use invented aliases as a `kind`. If you need a general failure case, use `failure_mode`. If the case is unsafe or privacy-invasive, use `safety`.

## Mode-specific contracts

### `create`

Allowed routes: `full_skill`, `mini_skill`, `needs_clarification`, `domain_discovery`.

If route is `needs_clarification`, ask blocking questions and stop.

If route is `domain_discovery`, required sections after the YAML block:

1. **Why domain discovery is required**: explain which domain substance gates are unknown.
2. **Domain discovery questions**: ask 5-10 targeted questions that reveal target user, artifact type, output depth, variables, data policy, failure knowledge, quality rubric, examples, and eval cases.
3. **Provisional domain content contract**: include a draft contract with unknowns marked, not a full skill.
4. **What would make it production-ready**: exact information or examples needed before full package creation.

If route is `full_skill`, required sections after the YAML block:

1. **Scenario card**: user, context, stable job, typical inputs, expected outputs, recurring failures, evidence, constraints, non-goals, success criteria.
2. **Domain content contract** for domain/content skills: required variables, hidden failure modes, expert quality checks, data-source policy, uncertainty policy, must-not-omit fields, worked examples needed, domain eval cases.
3. **IR summary**: objects, states/results, events/actions, evidence, hypotheses, constraints, risky boundaries, reasoning mode, type errors to prevent.
4. **Principles**: domain rule -> meta rule -> root principle -> workflow step -> eval check.
5. **Architecture**: smallest viable package: `SKILL.md`, optional `references/`, `scripts/`, `assets/`, MCP/tool notes, `evals/`.
6. **Skill package**: create or provide copy-ready files. Serious reusable skills must include `SKILL.md` and `evals/evals.json`.
7. **Quality gates**: lint status, eval schema status, content-quality rubric status, remaining blockers.

If route is `mini_skill`, provide a smaller reusable wrapper with explicit limitations and at least one near-miss example.

### `critique`

Route must be `not_a_creation_request`.

Required sections:

1. **Executive verdict**: score, biggest risks, highest-leverage fixes.
2. **Trigger and boundary review**: over-trigger, under-trigger, near-miss, unsafe use.
3. **IR and workflow review**: type errors, missing steps, unclear evidence/confidence policy.
4. **Domain substance review**: for domain/content skills, check variables, failure knowledge, data-source policy, expert rubric, examples, domain evals.
5. **Output contract review**: schema strength, evidence handling, blockers, missing information, domain-specific required fields.
6. **Eval review**: positive, negative, near-miss, `failure_mode` or `safety`, captured-output scoring, content-quality evals.
7. **Patch plan**: ordered changes, expected effect, acceptance tests.

Do not output a replacement package unless the user explicitly asks for a rewrite after critique.

### `improve`

Route must be `not_a_creation_request`.

Patch-first rule:

- Default to patching the existing package.
- Do not rebuild unless the package is structurally invalid, the user requests full redesign, or patching would be more confusing than rebuilding.
- If rebuilding, include `rebuild_reason` with why patch is insufficient, what is preserved, and what changes.

Required sections:

1. **Patch intent**: failures targeted.
2. **Concrete edits**: files changed and why.
3. **Domain substance edits** when relevant: domain variables, hidden pitfalls, data policy, expert rubric, examples, content evals.
4. **Before/after snippets or replacement files**.
5. **Self-check**: lint/eval/content-quality status when tools are available; otherwise `not_run` with manual checks.
6. **Regression plan**: cases that must pass.

If you output or edit an eval artifact, set `eval_artifact_present: true` and set `eval_schema_runner_compatible` based on the actual artifact.

### `eval`

Route must be `not_a_creation_request`.

First decide output type:

- `design_runner_evals`: produce runner-compatible `evals/evals.json`.
- `design_human_rubric`: produce human scoring rubric only.
- `run_evals`: run available validators and report results.

Never call a human rubric `evals.json`. If outputting runner JSON, copy the schema below; do not invent `cases`, string checks, non-boolean `all_required`, or alias kind values.

Minimal runner-compatible eval JSON:

```json
{
  "skill_name": "example-skill",
  "pass_threshold": 0.85,
  "evals": [
    {
      "id": "positive-primary-1",
      "kind": "positive",
      "prompt": "A realistic prompt that should use the skill.",
      "expected_behavior": "Use the skill workflow and output contract.",
      "checks": {
        "trigger": [{"type": "must_contain", "value": "expected marker", "required": true}],
        "process": [],
        "output": [],
        "safety": []
      },
      "pass_criteria": {"all_required": true, "min_score": 0.85}
    }
  ]
}
```

Required runner eval coverage: 2 positive, 1 negative, 1 near_miss, and 1 `failure_mode` or `safety`. Domain/content skills must add at least 2 content-quality checks that test domain variables and hidden failure modes.

### `triage`

Use when the request is one-off, underspecified, unsafe, or better served by a checklist/direct answer.

Required sections:

1. **Why not a full skill**.
2. **Recommended alternative**: direct answer, checklist, mini-skill, blocking questions, or safer redesign.
3. **What would make it skill-worthy**.

Use `mode: triage` when route is `checklist`, `direct_answer`, or `refuse_or_redesign`, even if the user used the word “skill”.

## Domain content contract / 领域内容契约

For domain/content skills, include this contract before finalizing the package:

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

A domain contract is weak if `required_variables` are generic, `hidden_failure_modes` are empty, data-source policy ignores real-time facts, or eval cases only test structure rather than usefulness.

## Golden patterns / 合规样式

Use `references/mode-golden-examples.md` when more detail is needed. Minimal patterns:

- Unknown reusable candidate: `mode: create`, `route: needs_clarification`, `operation: ask_questions`, unknown hard gates, no package.
- Domain-content candidate without substance: `mode: create`, `route: domain_discovery`, `operation: ask_domain_questions`, unknown domain gates, no package.
- Generic/vague helper: `mode: triage`, `route: checklist`, `operation: ask_questions`, no full package.
- Existing skill critique: `mode: critique`, `route: not_a_creation_request`, `operation: critique_package`, gates `not_applicable`.
- Existing skill improve: `mode: improve`, `route: not_a_creation_request`, `operation: patch_existing_package`, `patch_not_rebuild: true`.
- Runner eval design: `mode: eval`, `route: not_a_creation_request`, `operation: design_runner_evals`, `eval_artifact_present: true`, `eval_schema_runner_compatible: true`.
- One-off prompt wrapper: `mode: triage`, `route: mini_skill`, repeatability `fail`, no full package.
- Privacy-invasive request: `mode: triage`, `route: refuse_or_redesign`, safety gate `fail`, safer redesign only.

## Core principles / 核心原则

1. **Represent before judging / 先表征，后判断**: model the scenario before writing instructions.
2. **Do not mix types / 类型不能混**: distinguish observation, evidence, inference, hypothesis, instruction, output, and evaluation.
3. **Do not exceed evidence / 结论不超过证据**: conclusions must be no stronger than supporting evidence.
4. **Make assumptions falsifiable / 假设必须可被打脸**: state what evidence would change the conclusion.
5. **Reduce freedom at fragile boundaries / 高风险边界先收自由度**: use templates, scripts, fixed schemas, or MCP tools for error-prone operations.
6. **Make outputs handoff-ready and regression-testable / 结果可交接，方法可回归**: define output contracts and evals before calling a skill done.
7. **Extract domain failure knowledge / 提取领域负知识**: ask what looks plausible but fails in real use.
8. **Measure usefulness, not just structure / 评测有用性，不只评测结构**: domain evals must catch shallow but well-formatted outputs.

## Workflow / 工作流

### 1. Classify mode, route, and operation

Use the compatibility matrix. If route would be `checklist`, `direct_answer`, or `refuse_or_redesign`, mode is normally `triage`. If the request is a domain/content skill with weak domain gates, route `domain_discovery`.

### 2. Gate before full generation

Use hard gates for all full skill creation. Use domain substance gates for domain/content skills. Do not use point-counting. Soft signals only matter after required gates pass.

Decision rule:

```text
All hard gates pass + domain gates pass when applicable + >=3 soft signals -> create/full_skill
All hard gates pass + 1-2 soft signals -> create/mini_skill or triage/checklist
Any hard gate fail -> triage/direct_answer, triage/checklist, triage/mini_skill, or triage/refuse_or_redesign
Any hard gate unknown + plausible reusable skill -> create/needs_clarification + ask_questions
Domain skill + domain substance unknown -> create/domain_discovery + ask_domain_questions
Safety gate fail -> triage/refuse_or_redesign and offer safer design
```

Soft signals: recognizable input shapes, recurring failure modes, reusable workflow, stable output contract, meaningful benefit over checklist, scripts/templates/MCP/references reduce error, mistakes are costly enough to justify a skill.

### 3. Capture scenario, domain substance, and IR

Use `references/scenario-to-skill.md` and `references/domain-discovery.md` if unclear.

Scenario card:

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

Domain discovery card for domain/content skills:

```text
Target user:
Artifact type:
Output depth:
Required variables:
Hidden failure modes:
Expert quality checks:
Data-source policy:
Uncertainty policy:
Worked examples:
Domain eval cases:
```

IR:

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
```

Prevent type errors: status label as root cause, quote as motive, preference as hard constraint, correlation as causation, desired outcome as evidence, one example as the whole workflow, formatted output as useful output.

### 4. Extract principles only if they change behavior

For each important rule:

```text
Domain rule -> meta rule -> root principle -> executable workflow step -> eval check
```

Remove principles that do not change workflow, output, risk handling, domain content, or evaluation.

### 5. Choose smallest viable architecture

- Single `SKILL.md`: short, low-dependency workflow.
- `SKILL.md` + `references/`: domain knowledge, rubrics, examples, long templates.
- Add `scripts/`: deterministic parsing, validation, transformation, scoring, or fragile operations.
- Add MCP/tool notes: external systems, databases, tickets, calendars, repos, APIs.
- Add `evals/`: required for this architect's done state.

### 6. Use skeleton first when creating packages

When tools are available, first generate a compliant skeleton:

```bash
python scripts/create_skill_skeleton.py <skill-name> <output-dir> --description "<frontmatter description>" --domain
```

Use `--domain` for domain/content skills. Then edit the skeleton. Do not freehand a package when the skeleton can be used.

A serious package must contain:

```text
skill-name/
  SKILL.md
  evals/evals.json
```

Generated `SKILL.md` must include purpose, when to use, when not to use, hard gates or required inputs, domain content contract when relevant, IR summary, workflow, evidence/confidence policy, output contract, failure/escalation rules, references/scripts map, and eval plan.

Generated `evals/evals.json` must be compatible with `scripts/run_skill_evals.py` and use only canonical eval kinds.

### 7. Validate actual artifacts, not just intent

When file access is available, run:

```bash
python scripts/lint_skill_package.py <path-to-skill>
python scripts/run_skill_evals.py <path-to-skill>/evals/evals.json --validate-only
python scripts/check_architect_output.py <captured-output.md>
```

If captured outputs exist, score them:

```bash
python scripts/run_skill_evals.py <path-to-skill>/evals/evals.json --outputs-dir <captured-outputs-dir>
```

If any gate fails, revise before presenting as complete. If tools are unavailable, state `not_run` and list manual checks.

### 8. Ablation and regression

When improving an existing skill, compare baseline without the skill or old skill, new skill, and new skill with one major principle removed. If removing a principle does not create a distinct failure, the principle may be redundant or vague.

For domain/content skills, also ablate hidden failure knowledge and data-source policy. If output quality does not degrade, the domain substance contract is too weak.

## Language policy / 语言策略

Use the user's language for explanations and generated prose unless the target repo standard requires English. Keep `name` lowercase ASCII with hyphens. For bilingual packages, prefer English identifiers plus bilingual section labels, or place full Chinese guidance in `references/zh-CN-guide.md`.
