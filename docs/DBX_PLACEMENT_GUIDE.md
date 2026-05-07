# DBX Placement Guide

This document applies ASCT Placement Decisions to `DBvc/skills`.

A mature skill author does not only ask:

```text
What should this skill say?
```

They ask:

```text
Where should this control live?
```

## 1. Placement Options

| Placement | Use for | Avoid using it for |
| --- | --- | --- |
| Runtime skill | Task-specific recurring workflow with a stable trigger. | Always-on repo norms or deterministic checks. |
| `SKILL.md` | Activation aftermath, workflow, hard gates, output contract. | Long theory, huge examples, API manuals, validation logic. |
| `references/` | Long or conditional knowledge, rubrics, examples, gotchas. | Controls that must always run or be mechanically enforced. |
| `scripts/` | Deterministic, repeatable, fragile, mechanical, parse-heavy checks. | Human judgment disguised as code. |
| `assets/` | Templates, schemas, samples, starter files, static resources. | Runtime instructions. |
| Root docs | Repository governance, index, routing, security, release process. | Task-specific instructions needed only after activation. |
| Command | Explicit macro workflow or multi-skill orchestration. | Hidden or ambiguous background behavior. |
| Hook | Lifecycle gate, safety block, state refresh, required stop check. | Open-ended reasoning or surprising hidden work. |
| Repo memory | Glossary, ADR, agent brief, out-of-scope record, known constraints. | Volatile assumptions or private secrets. |
| Collection routing | Skill precedence, conflict resolution, chaining, install scope. | Full skill instructions. |
| Global/repo instruction | Always-on constraints such as secret safety or destructive-command approval. | Long task-specific workflows. |

## 2. Decision Procedure

### Step 1: Is the control always relevant?

If yes, prefer root docs, repo instructions, host instructions, or hooks.

Examples:

- Do not run destructive git commands without explicit approval.
- Protect secrets.
- Do not edit unrelated files.

### Step 2: Is the control deterministic?

If yes, prefer scripts, validators, CI, or hooks.

Examples:

- Validate JSON shape.
- Detect missing PR sections.
- Render or re-open a generated artifact.
- Block forbidden shell commands.

### Step 3: Is the control long or conditional knowledge?

If yes, prefer `references/`.

Examples:

- Domain rubric.
- Common gotchas.
- API usage details.
- Long examples.

### Step 4: Is the control reusable material?

If yes, prefer `assets/`.

Examples:

- PR template.
- JSON schema.
- Starter Markdown.
- Fixture file.

### Step 5: Is it persistent state?

If yes, use a state contract and prefer repo memory or external state with explicit ownership and rollback.

Examples:

- Project glossary.
- ADR.
- Agent brief.
- Out-of-scope record.
- Known constraints.

### Step 6: Does it coordinate several skills?

If yes, prefer routing matrix, collection design, command, or explicit workflow layer.

Examples:

- Review before PR writing.
- Decision before Codex goal writing.
- Skill architect triage before full skill creation.

### Step 7: Is it a task-specific recurring behavior?

If yes, a skill is appropriate.

Examples:

- Create a work PR description.
- Run strict evidence-based code review.
- Frame a high-impact decision.
- Control Codex subagent context.

## 3. Placement Anti-Patterns

### Everything in `SKILL.md`

The skill becomes long, brittle, and expensive to load.

### Everything as a skill

Always-on norms, deterministic checks, and dangerous action guards become unreliable because they depend on selective activation.

### Everything as a hook

The system becomes rigid and surprising. Hooks should enforce lifecycle constraints, not replace task reasoning.

### Everything as references

The agent has knowledge but no runtime control.

### Everything as scripts

The system has tools but no judgment layer for when and why to use them.

## 4. DBX Examples

### “Do not claim tests passed unless they were run.”

Best placement:

- General honesty rule in style guide/security policy.
- Skill-specific completion contract.
- Output checker or eval where possible.

Not enough:

- A buried sentence in a long reference.

### “Detect vague PR proof.”

Best placement:

- Commit/PR `SKILL.md` proof contract.
- `scripts/check_commit_pr_output.py`.
- Output eval regression.

### “Prefer strict review before PR writing.”

Best placement:

- `docs/DBX_ROUTING_MATRIX.md`.
- Optional future command if this becomes a frequent macro.

### “Codex `/goal` may be feature-gated.”

Best placement:

- `dbx-goal-writer` runtime rule.
- `docs/DBX_CODEX_COMPATIBILITY.md` for repository-level drift policy.
- Eval case for invented slash syntax.

## 5. Patch Hypothesis Requirement

Any non-trivial placement change should state:

```yaml
placement_hypothesis:
  target_failure: []
  old_placement: ""
  new_placement: ""
  expected_benefit: []
  expected_cost: []
  acceptance_signal: []
  rollback_condition: []
```

Moving text out of `SKILL.md` is not automatically better. It is better only if behavior remains reliable while context cost, friction, or maintenance cost decreases.
