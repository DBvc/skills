# DBX Skills

个人 Claude/Codex Skills 仓库，用于集中管理和版本控制。稳定技能统一使用 `dbx-` 前缀，避免和外部安装的 skills 产生命名歧义。

Personal Claude/Codex Skills repository for centralized management and version control. Stable skills use the `dbx-` prefix to avoid naming conflicts with third-party skills.

## 稳定 Skills / Stable Skills

| Skill | 描述 / Description |
|---|---|
| [`dbx-open-source-commit-pr`](skills/dbx-open-source-commit-pr/) | 面向开源仓库的英文 commit/PR 写作。Generate English commit messages and PR descriptions for open-source repositories. |
| [`dbx-work-commit-pr`](skills/dbx-work-commit-pr/) | 工作场景的中文合同式 commit/PR 写作。Contract-style commit messages and PR descriptions for work contexts. |
| [`dbx-linus-review`](skills/dbx-linus-review/) | 严格、实用主义、证据驱动的技术方案评估。Strict pragmatic technical review. |
| [`dbx-skill-architect`](skills/dbx-skill-architect/) | 场景优先的 skill 创建、评审、改进与评测。Scenario-first skill architecture, critique, improvement, and eval design. |
| [`dbx-conversation-align`](skills/dbx-conversation-align/) | 对话卡点诊断、措辞改写与边界沟通。Diagnose stuck conversations, rewrite risky messages, and plan boundaries. |
| [`dbx-decision-framing`](skills/dbx-decision-framing/) | 高影响真实决策的分支门禁、取舍分析与验证动作。Frame high-impact decisions with gates, trade-offs, and validation steps. |
| [`dbx-subagent-context-control`](skills/dbx-subagent-context-control/) | Codex subagent 上下文继承控制。Control Codex subagent context inheritance. |

## 仓库治理 / Repository Governance

本仓库不只是 prompt collection，而是一组可复用、可评估、可演进的 agent work units。新增或修改 skill 时，优先遵守这些仓库级文件：

- [`DBX_SKILL_STYLE_GUIDE.md`](DBX_SKILL_STYLE_GUIDE.md): skill 写作、架构、评估和发布规范。
- [`DBX_SKILL_INDEX.md`](DBX_SKILL_INDEX.md): 当前 skill 的用途、边界、成熟度和下一步改造方向。
- [`docs/DBX_SKILL_ARCHITECTURE.md`](docs/DBX_SKILL_ARCHITECTURE.md): 仓库架构、目录约定和演进路线。
- [`docs/DBX_EVAL_GUIDE.md`](docs/DBX_EVAL_GUIDE.md): trigger eval、output eval、人工 rubric 和 baseline 对照方法。
- [`docs/DBX_RELEASE_CHECKLIST.md`](docs/DBX_RELEASE_CHECKLIST.md): 新增、修改、发布 skill 前的检查清单。

## 本地检查 / Local Checks

```bash
# 检查所有 skill 的 frontmatter、目录结构、eval JSON 和索引一致性
python3 scripts/validate_skills.py --root .

# 生成当前 skills 的 Markdown 或 JSON inventory
python3 scripts/skill_inventory.py --root . --format markdown
python3 scripts/skill_inventory.py --root . --format json

# 校验每个 skill 的 evals/triggers.json 结构
python3 scripts/run_trigger_evals.py --root . --validate-only
```

严格模式可以在发布前使用：

```bash
python3 scripts/validate_skills.py --root . --fail-on-warnings
```

## 使用方法 / Usage

### 使用 add-skill 安装（推荐）/ Install with add-skill (Recommended)

```bash
# 安装所有 skills / Install all skills
npx add-skill dbvc/skills

# 安装特定 skill / Install specific skill
npx add-skill dbvc/skills --skill dbx-open-source-commit-pr

# 查看可用 skills / List available skills
npx add-skill dbvc/skills --list
```

### 手动安装 / Manual Install

```bash
# 克隆后链接到 Codex skills 目录
git clone https://github.com/dbvc/skills.git
cd skills

for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.codex/skills/
done

# 或链接到 Cursor skills 目录
for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.cursor/skills/
done
```

## 创建新 Skill / Create New Skill

不要直接复制一个现有 skill 开始堆规则。先写 scenario card，再决定是否值得做成 full skill。

```text
Scenario name:
Primary user:
Real job to be done:
Typical inputs:
Expected outputs:
Recurring failure modes:
Evidence sources:
Hard constraints:
Non-goals:
Success criteria:
```

最小要求：

1. `skills/<skill-name>/SKILL.md` 必须包含合法 YAML frontmatter，且 `name` 和目录名一致。
2. `description` 必须说明 “做什么” 和 “什么时候用”。
3. full skill 必须有 `evals/evals.json` 或明确说明为什么暂时没有。
4. 脆弱、重复、可机械验证的步骤优先放进 `scripts/`。
5. 长知识、rubric、examples 和 gotchas 优先放进 `references/`，不要把主 `SKILL.md` 写成一团上下文年糕。

## 相关资源 / Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Evaluation Guide](https://agentskills.io/skill-creation/evaluating-skills)
- [Agent Skills Scripts Guide](https://agentskills.io/skill-creation/using-scripts)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [OpenAI Skills Repository](https://github.com/openai/skills)

## License

MIT
