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
