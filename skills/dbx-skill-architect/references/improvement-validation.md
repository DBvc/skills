# Improvement validation playbook

Use this file when critiquing or improving an existing skill. The goal is to prevent decorative complexity from masquerading as progress.

## Patch hypothesis

Every non-trivial change should be expressed as a falsifiable hypothesis:

```yaml
patch_hypothesis:
  target_failures:
    - "The concrete failure the current skill exhibits."
  target_files:
    - "skills/example-skill/SKILL.md"
    - "skills/example-skill/evals/evals.json"
  exact_edit_units:
    - "replace frontmatter description with trigger and non-trigger boundaries"
    - "add one near_miss eval that catches over-triggering"
  proposed_change: "The smallest change expected to reduce the failure."
  expected_benefit: "What should improve and for whom."
  expected_cost: "Extra context, maintenance, runtime, dependency, or UX cost."
  acceptance_tests:
    - "A test that should pass after the patch."
  rollback_conditions:
    - "A condition under which this patch should be reverted."
```

Good target failures:

- The skill triggers on one-off tasks.
- The skill creates full packages before domain variables are known.
- The skill says outputs are validated but no eval artifact exists.
- The skill relies on persona style rather than evidence-based review.
- The skill asks too many questions for low-risk tasks.
- The eval suite is schema-valid but only checks headings or file markers.

Weak target failures:

- Make it better.
- Improve quality.
- Add best practices.
- Make it more professional.
- Strengthen everything.

Good edit units:

- Replace `description` with one should-trigger sentence and one should-not-trigger sentence.
- Move the long taste rubric from `SKILL.md` to `references/taste-rubric.md` and add a one-line pointer.
- Add `evals/triggers.json` cases for positive explicit, positive implicit, negative, and near-miss prompts.
- Add a required `quality: behavior` regex check to the failure-mode eval.
- Add `scripts/validate_output.py` with `--help`, non-zero exit codes, and two fixtures.

Weak edit units:

- Improve the README.
- Add evals.
- Tighten quality.
- Make the workflow clearer.
- Refactor the skill.

## Before and after evaluation

For meaningful patches, compare at least two states:

```text
old_skill -> same prompt -> output A
new_skill -> same prompt -> output B
```

For stronger validation, compare three states:

```text
without_skill or baseline -> output A
old_skill -> output B
new_skill -> output C
```

Record:

- pass/fail against required checks;
- human rubric score when needed;
- token or context cost if available;
- latency or tool cost if relevant;
- any regression in old behavior.

## Broad cross-skill release gate

Apply this release gate when the proposed release either:

1. changes three or more skill packages; or
2. introduces or changes cross-skill state, protocol, or execution-authority behavior.

When either scope condition is true and `skill_value_check.net_value` is `uncertain` or `negative`, the change is not releasable as an improvement. Keep the value judgment honest; broad scope is not evidence of value.

### Machine-enforced change units

Do not rely on the review narrative to enforce this gate. Create a schema-v2 JSON manifest conforming to `assets/change-manifest.schema.json`. The manifest divides the current Git delta into independent change units. Each unit declares:

- exact path patterns;
- `kind` and `net_value`;
- cross-skill protocol, state, execution-authority, and routing surface paths;
- release mode and the four prohibited release effects;
- narrative evidence, machine-checkable release validation, measured costs, and executable rollback;
- an optional replacement unit.

Run the deterministic validator from the skill root:

```bash
python3 scripts/validate_change_manifest.py /path/to/change-manifest.json --repo-root /path/to/repo --scope working-tree
```

Use `--scope staged` to validate only the staged publication scope. The validator reads Git directly, requires every changed path in that scope to belong to exactly one unit, verifies surface declarations against those paths, and reports affected skill-root and surface counts. Broadness is also computed for the whole publication scope, so splitting a three-skill release into three nominal units cannot bypass the gate. It detects common routing paths such as agent activation metadata and routing/registry files; those paths must be declared as routing surfaces.

The manifest is an auditable declaration, not semantic omniscience. A maintainer must still declare cross-skill protocol, state, and authority changes honestly. The deterministic value is that declared scope and release claims can no longer contradict each other silently.

For every broad positive unit, stable registration, or improvement claim, schema v2 requires a separate `validation` contract:

- `baseline.ref` points to an existing repository file, optionally with a `#anchor`, and `baseline.check.argv` can verify the declared starting behavior;
- `outcomes` contains at least one `before_after` comparison or `operational` result with its own executable argv check;
- a before/after outcome names the exact baseline ref and a distinct candidate ref;
- `costs` contains at least one numeric measurement with unit, existing evidence ref, and check;
- `rollback.commands` contains executable argv arrays whose expected exit is zero.

The validator resolves every evidence and validation ref under the repository root and verifies that each argv executable exists on `PATH` or as an executable repository file. A URL, missing path, path traversal, prose-only rollback, unavailable command, arbitrary non-empty evidence entry, or schema/lint result without the baseline/outcome/cost contract fails the publication gate. The validator records commands but does not execute arbitrary manifest-provided argv; release automation or a maintainer runs the declared checks.

Allowed while the gate is closed:

- create an isolated prototype labeled `manual-only`;
- run same-prompt baseline, old-skill, and prototype comparisons;
- add fixtures, deterministic validators, and measurements that do not alter default routing;
- discard or revise the prototype after evaluating it.

Forbidden while the gate is closed:

- changing collection or default routing to select the prototype;
- removing, disabling, deprecating, or silently bypassing the existing path;
- calling the change an improvement, resolved, production-ready, or approved for rollout;
- treating schema, lint, or a self-authored example alone as proof of positive net value.

The prototype must have a containment note that names its manual entry point, confirms the existing path remains the default, and states how to remove it without migration. Open the release gate only when the declared machine-checkable baseline plus before/after or operational evidence supports `net_value: positive`, targeted regressions pass, added cost is measured, and the declared rollback commands remain executable.

If an existing default is independently proven harmful, do not fold its removal into the uncertain prototype. Record a separate `known_bad_default_removal` unit with:

- `net_value: positive`;
- changed default routing and existing-path removal declared explicitly;
- evidence identifying the observed failure;
- rollback trigger, steps, and executable commands;
- no uncertain, negative, or isolated prototype as its replacement.

This separation permits removing a known-bad default without pretending the experimental replacement has already earned rollout.

This is a release gate, not a planning loop. Do not stop at another proposal when a safe isolated prototype can produce the missing evidence.

## Acceptance-test design

A good acceptance test is specific enough to fail. Prefer tests that catch the targeted failure directly.

Examples:

```text
Failure: overbuilt full package for one-off prompt.
Acceptance test: prompt asks for one birthday message; output must route triage/direct_answer and must not produce SKILL.md.

Failure: domain skill lacks content substance.
Acceptance test: travel-skill prompt with no target user or variables must route domain_discovery and ask questions about season, visa/passport, transport, budget, mobility, booking windows, and source freshness.

Failure: improvement rebuilds unnecessarily.
Acceptance test: improve prompt for existing skill must set patch_not_rebuild: true unless rebuild_reason is present and must name target_files and exact_edit_units.

Failure: marker-only evals pass.
Acceptance test: evals/evals.json where every required check only tests headings or file names must fail eval_schema.py.

Failure: marker-only full package passes.
Acceptance test: captured full_skill output that only says it will provide SKILL.md and evals must fail check_architect_output.py because no fenced file blocks exist.

Failure: a broad cross-skill change with uncertain net value is shipped as an improvement.
Acceptance test: a manifest affecting at least three skills or cross-skill state/protocol/authority may contain an isolated manual-only prototype, but the validator must fail it if it changes default routing, removes the old path, registers stable, or claims improvement.

Failure: a broad positive unit cites an arbitrary evidence path and prose rollback, with no comparable baseline, operational result, measured cost, or executable command.
Acceptance test: schema v2 and the validator reject it; the positive unit passes only with existing repo-relative refs, baseline plus before/after or operational argv checks, numeric cost evidence, and zero-exit rollback argv.

Failure: an uncertain prototype is used to justify removing a known-bad default.
Acceptance test: the removal is a separate positive manifest unit with evidence and rollback; the validator rejects the uncertain or isolated prototype as its replacement.
```

## Cost model

A patch can make a skill worse by adding the wrong kind of structure. Track these costs:

- **Context cost**: main `SKILL.md` becomes longer or harder to scan.
- **Runtime cost**: more steps, questions, or tool calls.
- **Maintenance cost**: new scripts, schemas, or references need updates.
- **Trigger cost**: description becomes broader or more ambiguous.
- **UX cost**: user sees excessive YAML, tables, or ritual.
- **Portability cost**: skill depends on a local path or unavailable tool.

Accept a cost only when it buys a visible quality or reliability improvement.

## Rollback conditions

Define rollback before applying the patch. Common rollback conditions:

- The patch causes negative or near-miss cases to trigger.
- The patch blocks common happy-path tasks.
- The patch increases context substantially without output-quality gains.
- The new script fails in clean environments.
- The output becomes less handoff-ready.
- Human review prefers old output on the targeted scenario.

## Patch-first vs rebuild

Patch by default. Rebuild only when one of these is true:

1. The package is structurally invalid or cannot be linted.
2. The skill’s core job is wrong.
3. Multiple patches would create a more confusing structure than replacement.
4. The user explicitly asks for a full redesign.

If rebuilding, preserve what worked:

```yaml
rebuild_reason:
  why_patch_is_insufficient: "Patching would leave contradictory triggers and incompatible eval formats."
  what_is_preserved:
    - trigger intent
    - core domain rubric
    - existing scripts that work
  what_changes:
    - structure
    - gates
    - eval schema
```

## Improvement report format

```markdown
## Patch intent

Targeted failures:
- The skill over-triggers on unrelated one-off writing requests.

## Patch hypotheses

```yaml
patch_hypothesis:
  target_failures:
    - wrong_trigger on adjacent direct-answer prompts
  target_files:
    - skills/example-skill/SKILL.md
    - skills/example-skill/evals/triggers.json
  exact_edit_units:
    - replace frontmatter description with trigger and non-trigger boundaries
    - add two near-miss trigger cases for adjacent direct-answer prompts
  proposed_change: "Narrow the trigger and add regression cases for adjacent prompts."
  expected_benefit: "Higher trigger precision without reducing explicit-trigger recall."
  expected_cost: "Slightly longer description and two extra trigger evals."
  acceptance_tests:
    - "near-miss trigger evals remain false"
  rollback_conditions:
    - "explicit positive trigger case stops firing"
```

## Concrete edits

| File | Exact edit unit | Why |
|---|---|---|
| `skills/example-skill/SKILL.md` | replace frontmatter description | reduce over-trigger |
| `skills/example-skill/evals/triggers.json` | add two near-miss cases | prevent regression |

## Validation

- Lint: pass | fail | not_run
- Runner eval schema: pass | fail | not_run
- Trigger evals: pass | fail | not_run
- Manual rubric: pass | fail | not_run

## Regression plan

- Positive explicit trigger remains true.
- Negative unrelated trigger remains false.
- Existing happy-path output contract remains unchanged.
```
