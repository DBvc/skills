# DBX Skills

个人 Claude/Codex Skills 仓库，用于集中管理和版本控制。
稳定技能统一使用 `dbx-` 前缀，避免和外部安装的 skills 产生命名歧义。

Personal Claude/Codex Skills repository for centralized management and version control.
Stable skills use the `dbx-` prefix to avoid naming conflicts with third-party skills.

## Stable Skills

| Skill | 描述 / Description |
| --- | --- |
| [`dbx-open-source-commit-pr`](skills/dbx-open-source-commit-pr/) | 面向开源仓库的英文 commit/PR 写作。Generate English commit messages and PR descriptions for open-source repositories. |
| [`dbx-work-commit-pr`](skills/dbx-work-commit-pr/) | 工作场景的中文合同式 commit/PR 写作。Contract-style commit messages and PR descriptions for work contexts. |
| [`dbx-diff-review-control`](skills/dbx-diff-review-control/) | 精确选择 PR/diff/staged/commit/file review 范围，并输出高信号风险发现。Scoped code-change review control for concrete diffs. |
| [`dbx-linus-review`](skills/dbx-linus-review/) | 严格、实用主义、证据驱动的技术方案、模型和合并风险判断。Strict pragmatic technical judgment. |
| [`dbx-skill-architect`](skills/dbx-skill-architect/) | 场景优先的 skill 创建、评审、改进与评测。Scenario-first skill architecture, critique, improvement, and eval design. |
| [`dbx-skill-portfolio-auditor`](skills/dbx-skill-portfolio-auditor/) | 已安装技能组合审计与全局/项目/显式触发/禁用/卸载范围决策。Audit installed skill portfolios and recommend global, project, explicit-only, disable, or uninstall placement. |
| [`dbx-attention-control`](skills/dbx-attention-control/) | 混合输入的注意力分流内核：把收藏、想法、任务、课程、工具、消息等路由为行动、构建、实验、追踪、存档、孵化、丢弃、风险保护或澄清，并支持个人配置和外部系统 dry-run 映射。Product-agnostic attention-allocation controller for mixed inputs with profile and adapter layers. |
| [`dbx-conversation-align`](skills/dbx-conversation-align/) | 对话卡点诊断、措辞改写与边界沟通。Diagnose stuck conversations, rewrite risky messages, and plan boundaries. |
| [`dbx-decision-framing`](skills/dbx-decision-framing/) | 高影响真实决策的分支门禁、取舍分析与验证动作。Frame high-impact decisions with gates, trade-offs, and validation steps. |
| [`dbx-subagent-context-control`](skills/dbx-subagent-context-control/) | Codex subagent 上下文继承控制。Control Codex subagent context inheritance. |
| [`dbx-goal-writer`](skills/dbx-goal-writer/) | Codex goal 合同生成、启动与审计。Create, start, and audit Codex goal contracts. |
| [`dbx-agent-handoff`](skills/dbx-agent-handoff/) | AI agent/session 续跑交接包生成。Create restart handoffs for future AI sessions. |

## Repository Governance

This repository is not just a prompt collection. It is a set of reusable, evaluable, and evolvable agent work units.

DBX applies [Agent Skill Control Theory](https://github.com/DBvc/agent-skill-control-theory) as a practical skill-collection discipline. ASCT itself lives in the theory repository; this repository keeps only applied rules, routing policy, validation practice, and runtime skills.

Start here when creating or changing a skill:

- [`DBX_SKILL_STYLE_GUIDE.md`](DBX_SKILL_STYLE_GUIDE.md): operational writing, architecture, eval, placement, and release rules.
- [`DBX_SKILL_INDEX.md`](DBX_SKILL_INDEX.md): current skills, boundaries, maturity, routing notes, and next improvements.
- [`docs/DBX_ASCT_ADOPTION.md`](docs/DBX_ASCT_ADOPTION.md): how this repo applies ASCT 0.3 without duplicating the theory repo.
- [`docs/DBX_PLACEMENT_GUIDE.md`](docs/DBX_PLACEMENT_GUIDE.md): how to decide whether a control belongs in a skill, script, reference, command, hook, repo memory, or collection routing.
- [`docs/DBX_COLLECTION_DESIGN.md`](docs/DBX_COLLECTION_DESIGN.md): collection-level routing, skill graph, conflicts, installation scope, safety, and deprecation.
- [`docs/DBX_ROUTING_MATRIX.md`](docs/DBX_ROUTING_MATRIX.md): conflict resolution and chaining rules across DBX skills.
- [`docs/DBX_EVAL_GUIDE.md`](docs/DBX_EVAL_GUIDE.md): trigger, process, output, safety, regression, and collection-level evals.
- [`docs/DBX_STATEFUL_SKILLS.md`](docs/DBX_STATEFUL_SKILLS.md): state contracts for project memory, bootstrap, workflow state, and interaction modes.
- [`docs/DBX_HOST_ARTIFACTS.md`](docs/DBX_HOST_ARTIFACTS.md): commands, hooks, `AGENTS.md`, `CLAUDE.md`, `llms.txt`, status lines, planning files, and portability rules.
- [`docs/DBX_CODEX_COMPATIBILITY.md`](docs/DBX_CODEX_COMPATIBILITY.md): Codex feature drift and compatibility policy.
- [`docs/DBX_RELEASE_CHECKLIST.md`](docs/DBX_RELEASE_CHECKLIST.md): release checklist for adding or changing skills.
- [`SECURITY.md`](SECURITY.md): script, dependency, state, and third-party skill safety policy.

## Local Checks

```bash
# Check frontmatter, directory structure, eval JSON, and index consistency.
python3 scripts/validate_skills.py --root .

# Generate Markdown or JSON inventory.
python3 scripts/skill_inventory.py --root . --format markdown
python3 scripts/skill_inventory.py --root . --format json

# Validate evals/triggers.json files.
python3 scripts/run_trigger_evals.py --root . --validate-only
```

Strict mode is useful before release, but do not enable it in CI until warnings are intentionally cleaned up:

```bash
python3 scripts/validate_skills.py --root . --fail-on-warnings
```

## Usage

### Install with add-skill

```bash
# Install all skills.
npx add-skill dbvc/skills

# Install one skill.
npx add-skill dbvc/skills --skill dbx-open-source-commit-pr

# List available skills.
npx add-skill dbvc/skills --list
```

### Manual install

```bash
git clone https://github.com/dbvc/skills.git
cd skills

# Codex
for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.codex/skills/
done

# Cursor
for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.cursor/skills/
done
```

## Creating a New Skill

Do not copy an existing skill and start stacking rules. Start with the scenario and failure map:

```text
Scenario name:
Primary user:
Task distribution:
Typical inputs:
Expected outputs:
Base-agent failure modes:
Evidence sources:
Hard constraints:
Non-goals:
Success criteria:
Cost and risk budget:
```

Minimum expectations:

1. `skills/<name>/SKILL.md` has valid YAML frontmatter and `name` matches the directory.
2. `description` explains capability and trigger context, including near-miss boundaries.
3. Full skills have `evals/triggers.json` and `evals/evals.json`, or a written reason for deferring one.
4. Fragile, repeatable, mechanical, or checkable work belongs in `scripts/`, not prose.
5. Long knowledge, rubrics, examples, and gotchas belong in `references/`, not in a swollen `SKILL.md`.
6. Before adding a control, decide placement: skill, reference, script, asset, repo memory, command, hook, collection routing, or global instruction.

## Related Resources

- [Agent Skill Control Theory](https://github.com/DBvc/agent-skill-control-theory)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Evaluation Guide](https://agentskills.io/skill-creation/evaluating-skills)
- [Agent Skills Scripts Guide](https://agentskills.io/skill-creation/using-scripts)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [OpenAI Skills Repository](https://github.com/openai/skills)

## License

MIT
