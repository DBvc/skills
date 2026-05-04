# DBX Skill Index

This file is the human-maintained map of the repository. It should be updated whenever a skill is added, renamed, removed, or significantly changed.

Generated inventories can be produced with:

```bash
python3 scripts/skill_inventory.py --root . --format markdown
```

## Current Skills

| Skill | Shape | Primary use | Current maturity estimate | Main risk | Next best improvement |
|---|---|---|---|---|---|
| `dbx-open-source-commit-pr` | procedure + transform | Generate public/open-source English commit messages and PR descriptions from final diffs. | L3 | Diff scope and validation proof still rely on model judgment. | Add git diff inspection and PR validation scripts; add trigger evals. |
| `dbx-work-commit-pr` | procedure + transform | Generate Chinese work-context commit/PR artifacts with contract-style review focus. | L2 | Final diff extraction, mixed-scope detection, and proof specificity are not mechanized. | Add references, scripts, and output evals for proof/risk/review-focus quality. |
| `dbx-linus-review` | review + rubric | Run strict pragmatic technical review focused on complexity, compatibility, data structures, and user impact. | L3 | Persona framing may over-influence tone and under-emphasize evidence format. | Convert into evidence-based strict review rubric; add finding schema and evals. |
| `dbx-skill-architect` | meta + procedure + eval | Create, critique, improve, and evaluate reusable skill packages from recurring scenarios. | L5 | Strong architecture can become too heavy if more concepts are added to runtime body. | Add lightweight shape/failure-mode classification and patch hypothesis references without bloating `SKILL.md`. |
| `dbx-conversation-align` | procedure + decision + safety | Diagnose stuck conversations, rewrite risky messages, and plan boundaries. | L5 | Boundary and trigger precision are more important than output volume. | Add explicit trigger evals and compact/standard/full output modes. |
| `dbx-decision-framing` | decision + gate | Frame high-impact decisions with gates, trade-offs, assumptions, and validation moves. | L5 | Can over-trigger for ordinary analysis if description or gates are too eager. | Add trigger evals focused on direct-answer vs quick/full decision boundaries. |
| `dbx-subagent-context-control` | coordination + context | Control subagent context inheritance, review independence, and synthesis boundaries. | L5 | Harness-specific assumptions may reduce portability. | Add compatibility notes and captured examples for supported agent environments. |

## Maturity Levels

| Level | Meaning |
|---|---|
| L0 | Idea only. |
| L1 | Checklist or prompt, not a valid skill package. |
| L2 | Valid `SKILL.md` with basic workflow. |
| L3 | References/examples/checklists/assets separated from runtime body. |
| L4 | Scripts/tools support fragile or mechanical steps. |
| L5 | Evals exist. |
| L6 | Baseline comparison exists. |
| L7 | Production regression suite and release process exist. |

The estimates above are intentionally conservative. Run the inventory and validator after each change, then update this file with actual scan results.

## Repository-Level Priorities

1. Keep the runtime skills small enough to use.
2. Move long methodology into `references/` or root-level docs.
3. Add trigger evals before expanding skill behavior.
4. Script only the parts that are mechanical, fragile, or repeatedly mis-executed.
5. Treat every major edit as a patch hypothesis, not as aesthetic gardening.

## Known Repository Gaps

- The root README should list every skill under `skills/`.
- Each serious skill should have `evals/triggers.json` for trigger precision and recall.
- Commit/PR skills should eventually have repo-aware diff inspection scripts.
- Review and decision skills should have near-miss evals to prevent over-triggering.
- A repo-wide validation command should be run before publish.
