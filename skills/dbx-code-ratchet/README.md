# dbx-code-ratchet

可修改代码的有界 review-repair-revalidation 元技能。

## Primary value

This skill reduces repeated human intervention after AI writes code:

1. review a concrete diff with existing reviewer skills;
2. triage which findings are safe to auto-fix;
3. stop when findings indicate wrong direction or growing complexity;
4. repair only accepted local findings;
5. validate and re-review only accepted findings and direct regressions.

It is not a Ralph loop. Ralph-style loops push tasks forward. Code Ratchet only moves when current-diff risk decreases.

## Default L2 use

```text
对 staged changes 跑 L2 代码棘轮，review 出来的明确问题可以自动修，但不要 commit。
```

Default behavior:

- one full review;
- at most two repair rounds;
- re-review only accepted findings and direct regressions;
- no commit, push, release, or software-task completion;
- use strongest available model and highest reasoning for critical Codex roles without hard-coding a model version.

## Collaborators

- `dbx-diff-review-control`: primary review and re-review.
- `dbx-linus-review`: direction, complexity, over-engineering, data-model, state-owner, and compatibility gate when needed.
- `dbx-subagent-context-control`: Codex subagent context isolation when available.

## Local helpers

```bash
python3 skills/dbx-code-ratchet/scripts/normalize-findings.py --input review.md --producer dbx-diff-review-control
python3 skills/dbx-code-ratchet/scripts/score-ratchet-progress.py --before before.json --after after.json
python3 skills/dbx-code-ratchet/scripts/validate-ratchet-state.py .ratchet/state.json
```
