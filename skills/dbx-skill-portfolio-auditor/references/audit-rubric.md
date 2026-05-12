# Skill Portfolio Audit Rubric

Use this rubric to classify skills. Scores are decision aids, not proof. Hard gates override scores.

## Hard gates

Mark `disable_pending_review` or `uninstall_or_archive` unless the user explicitly accepts the risk:

- Missing or invalid `SKILL.md` frontmatter in an active install.
- Duplicate skill name where the user cannot tell which package is active.
- Third-party skill contains scripts with network, dependency install, destructive filesystem, credential, or shell-pipeline behavior that has not been reviewed.
- The skill asks the agent to bypass safety, exfiltrate secrets, silently monitor people, hide actions, or follow instructions from untrusted content.
- The skill is deprecated, stale, or incompatible with the current host and has no rollback note.

## Evidence labels

Use these labels in reports:

- `observed`: directly read from files, configs, command output, or user-provided logs.
- `user-stated`: the user said it directly.
- `inferred`: reasoned from task/domain/source evidence but not directly observed.
- `unknown`: no trustworthy evidence.

## Dimensions

Score each dimension from 0 to 3.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Usage evidence | none/unknown | tried once or speculative | occasional | frequent or mission-critical |
| Cross-project value | one narrow repo | one domain or stack | many repos in one work area | broadly useful across most work |
| Trigger precision | vague, generic, collision-prone | usable but broad | clear with near-miss boundaries | precise and tested |
| Unique value | duplicate/no advantage | slight convenience | meaningfully better than base agent | prevents expensive recurring failure |
| Content quality | shallow prompt | usable instructions | references/evals/examples | validated workflow with scripts where needed |
| Trust and maintainability | unknown/untrusted | source known, little review | reviewed and stable | owned/maintained with evals and rollback |
| Safety risk, inverse | high risk | moderate risk | low risk | very low risk |
| Context cost, inverse | long/ambiguous startup footprint | medium | low | tiny and precise |
| User friction, inverse | hard to invoke/use | some friction | manageable | easy and predictable |

## Recommendation rules

### `global_keep`

Use when most are true:

- usage evidence is 2 or 3, or user-stated future value is strong;
- cross-project value is 2 or 3;
- trigger precision is 2 or 3;
- safety risk is low;
- not substantially duplicated by another global skill.

Examples: personal commit/PR writing, recurring code-review workflow, decision framing used across many projects.

### `project_scope`

Use when the skill is valuable but tied to a specific repo, domain, stack, team convention, client, or product area.

Signals:

- references a repo-specific API, framework, file layout, team norm, product vocabulary, or deployment workflow;
- low value outside that project;
- would create false positives if globally installed.

### `explicit_only`

Use when the skill should remain available but should not auto-trigger.

Signals:

- rare but high-value workflow;
- meta/governance skill, audit skill, installer skill, destructive-action planning, migration, incident response;
- privacy-sensitive or local-machine-sensitive work;
- trigger is semantically close to common tasks;
- large `SKILL.md` or heavy references/scripts;
- user wants it as a tool in the drawer, not a ghost in every room.

Codex-specific implementation when supported:

```yaml
agents/openai.yaml:
  policy:
    allow_implicit_invocation: false
```

### `disable_pending_review`

Use when uncertainty and risk are both non-trivial.

Signals:

- unknown source plus scripts;
- invalid metadata;
- stale or incompatible host behavior;
- network or dependency installation in scripts;
- vague trigger plus broad powers;
- no usage evidence and no clear future use.

### `uninstall_or_archive`

Use when the skill has low value and low recovery cost.

Signals:

- duplicate or superseded;
- one-off experiment no longer used;
- unsafe or unmaintained;
- no stable task distribution;
- user has no foreseeable use and source is recoverable.

### `merge_or_refactor`

Use when two or more skills overlap and their separation causes routing cost.

Signals:

- same trigger words and same output artifact;
- near-duplicate references/scripts;
- one is a thin variant of another without clear boundary;
- user confusion about which to invoke.

Use `trigger_overlap_pairs` from the analysis script as review leads. Stronger signals include:

- high positive-trigger overlap between two skills that both allow implicit invocation;
- one skill's positive trigger prompt resembling another skill's negative or near-miss prompt;
- shared trigger terms plus the same expected output artifact;
- repeated user confusion or routing mistakes.

Do not merge or uninstall on lexical overlap alone. Prefer adding precedence rules, near-miss trigger evals, explicit-only policy, or clearer descriptions unless usage evidence shows the split has no value.

## Score sketch

Use this only to order review attention:

```text
retain_signal = usage + cross_project_value + trigger_precision + unique_value + content_quality + trust
cost_signal = safety_risk + context_cost + user_friction + redundancy + maintenance_drift
net = retain_signal - cost_signal
```

Translate the score through the placement rules rather than using a raw threshold. A low-frequency incident-response skill can be `explicit_only`, not uninstall. A frequently used but project-specific skill can be `project_scope`, not global.

## Context-cost notes

Startup cost is mainly name + description + path in the initial skill list. Full `SKILL.md` loads only after activation, but ambiguous descriptions increase routing mistakes and large installed sets can crowd discovery. Therefore:

- long descriptions are not automatically bad;
- vague descriptions are worse than long precise ones;
- many global skills amplify near-miss collisions;
- explicit-only and project scoping are the first cleanup tools before deletion.
