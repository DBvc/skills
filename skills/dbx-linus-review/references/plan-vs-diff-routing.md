# Plan vs Diff Routing

The same engineering judgment applies to both plans and diffs, but the control loop is different.

## Shared judgment substrate

Both plan review and diff review care about:

- real problem;
- correct data model;
- state ownership;
- invariants;
- special cases;
- compatibility;
- complexity budget;
- practical rollout and validation.

## Different inputs

| Review type | Evidence source | Main failure mode | Better controller |
| --- | --- | --- | --- |
| Plan/proposal review | assumptions, diagrams, API sketches, migration plan, stated trade-offs | approving a wrong direction because it sounds coherent | `dbx-linus-review` |
| Diff/PR review | actual changed lines, call paths, tests, project rules, dirty/staged state | reviewing wrong target or producing generic comments | `dbx-diff-review-control` |

## Decision rule

Use `dbx-linus-review` when the user asks:

- “这个方案值得做吗？”
- “是不是过度设计？”
- “用 Linus 风格批一下。”
- “这个模型/抽象对不对？”
- “这个改动够不够合并？别客气。”

Use `dbx-diff-review-control` when the user asks:

- “review 这个 PR/diff。”
- “只看 staged。”
- “只看这几个文件。”
- “review main..HEAD。”
- “看有没有用户功能问题、数据模型问题、可维护性问题。”

If both are requested, first establish the concrete target with diff-review control, then apply strict pragmatic judgment to the selected target.

## Replacement policy

`dbx-linus-review` should not be replaced by a diff-only skill. It should be enhanced into the stricter strategy/model judgment skill. The diff skill should absorb its judgment lens, not its persona name.
