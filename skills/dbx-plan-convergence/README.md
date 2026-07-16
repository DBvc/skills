# dbx-plan-convergence

Provider-agnostic、manual-only 的技术方案收敛控制器。

它不负责“把方案写好”，而负责判断：

- 当前是在探索还是收敛；
- review finding 应该推动局部修订、补证据、找人决策、换方向还是停止；
- 当前循环是否有信息增益；
- 何时可以 handoff，何时只是文档变胖；
- 高影响方案如何提高严谨度，而不是盲目增加相同轮数。

## Install

从 `DBvc/skills` 仓库根目录解压，使目录成为：

```text
skills/dbx-plan-convergence/
```

然后运行：

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

这个 ZIP 只包含 skill 目录，不修改根 README、index 或 routing 文档。首次合入时按本文末尾的建议补充 collection metadata。

## No hard dependency

运行时不引用任何固定 planner、reviewer 或模型名称。

Provider 可以是：

- 人工作者或 reviewer；
- 当前 agent 的不同角色；
- 独立 agent；
- 任意 planning / review / repository-grounding skill；
- 文档、代码库、测试、日志或外部工具。

组合依赖一个小协议，而不是具体名称。换 provider 不需要修改本 skill 的核心控制逻辑。

## Core model

```text
direction epoch
  -> review
  -> finding triage
  -> next-state decision
  -> optional revision contract
  -> scoped re-evaluation
  -> progress gate
  -> continue / pivot / finalize / stop
```

“同一方向两轮”是默认 soft checkpoint，不是质量上限。Pivot 开启新 epoch，但总预算不会清零。

## Typical use

### Gate only

```text
对下面的方案和 review report 跑 dbx-plan-convergence gate-only。
只判断应该局部修、补证据、找人决策、换方向还是停止，不要改方案。
```

### Bounded loop

```text
对这个现有技术方案跑 dbx-plan-convergence bounded loop。
Provider 不要写死，最多按 high-impact profile 执行。
只有每轮有新证据、关闭决策、减少 blocker 或提高行动性时才继续。
```

### Diagnose a stuck loop

```text
这个方案已经 review、修改、再 review 三轮了。
用 dbx-plan-convergence 判断是在进步，还是 flat、oscillation 或 bloat。
```

### Continue after a pivot

```text
旧方向已经因 state owner 错误被否决。
以新方向开启下一个 epoch，但保留总预算和旧方向淘汰理由。
```

## Package layout

```text
skills/dbx-plan-convergence/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── assets/
│   ├── convergence-state-template.json
│   └── revision-contract-template.md
├── evals/
│   ├── evals.json
│   └── triggers.json
└── references/
    ├── convergence-model.md
    ├── default-policy.yaml
    ├── examples.md
    ├── output-contract.md
    ├── progress-and-stop-gates.md
    └── provider-protocol.md
```

## Suggested repository entries

### README stable skills

```markdown
| `dbx-plan-convergence` | 手动触发、provider-agnostic 的技术方案收敛控制器：区分探索与收敛，triage review findings，用 evidence / decision / direction / progress gates 控制 revision loop，并在打转、膨胀或方向错误时停止。Manual-only provider-agnostic convergence control for existing technical plans. |
```

### DBX skill index

```markdown
### `dbx-plan-convergence`

- Position: manual-only, provider-agnostic plan convergence controller.
- Trigger: explicit 方案收敛 / plan convergence / 方案棘轮 / controlled plan review-revision loop.
- Near miss: first-draft planning, standalone review, brainstorming, code repair, implementation.
- Maturity: L5 package with references, assets, trigger evals, and output evals.
- Main risk controlled: false convergence through local patching, evidence invention, decision substitution, oscillation, and document bloat.
```

### Routing note

```markdown
Use `dbx-plan-convergence` only when the user explicitly wants to control an existing plan's review-revision loop. Planning, review, evidence gathering, and decision ownership remain replaceable provider capabilities. Do not activate it for first-draft planning or one-pass review.
```
