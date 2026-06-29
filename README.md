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
| [`dbx-write`](skills/dbx-write/) | 中文为主的观点写作、技术博客、个人随笔、Markdown 草稿、改稿和英文转写。Chinese-first viewpoint writing for technical blogs, personal essays, Markdown drafts, editing, and occasional English versions. |
| [`dbx-read`](skills/dbx-read/) | 来源约束阅读：对 URL、PDF、论文、文档、GitHub、本地文件或粘贴文本做抓取证据化、摘要、精读、比较、Markdown 提取和可选笔记沉淀。Source-grounded reading for explicit source material. |
| [`dbx-feishu-project`](skills/dbx-feishu-project/) | 飞书项目 / Lark Project / Meegle 工作项读写、查询、评论、流转和字段更新控制器。Feishu Project / Meegle work item controller. |
| [`dbx-feishu-doc`](skills/dbx-feishu-doc/) | 飞书 Docx / Wiki 文档读取、创建、追加和安全局部更新控制器。Feishu Docx / Wiki document controller. |
| [`dbx-feishu-workflow`](skills/dbx-feishu-workflow/) | 飞书项目项与文档之间的研发流程联动编排。Workflow coordination across Feishu Project items and Feishu documents. |
| [`dbx-aliyun-sls`](skills/dbx-aliyun-sls/) | 阿里云 Simple Log Service / SLS 只读日志查询控制器：通过 Aliyun CLI、GetLogsV2、SDK 或可观测 MCP 安全生成、执行、总结日志查询，内置凭证、时间范围、成本、隐私和 handoff 护栏。Read-only Alibaba Cloud SLS log query controller with CLI/API/MCP execution boundaries. |
| [`dbx-crystallize`](skills/dbx-crystallize/) | 模糊产品/软件想法、需求草稿、issue 或前置讨论的需求结晶：澄清用户/场景/状态变化、scope、non-goals、验收标准、边界状态、开放决策和 handoff。Requirement crystallization before product judgment, design, technical planning, or implementation. |
| [`dbx-diff-review`](skills/dbx-diff-review/) | 精确选择 PR/diff/staged/commit/file review 范围，并输出高信号风险发现。Scoped code-change review for concrete diffs. |
| [`dbx-linus-review`](skills/dbx-linus-review/) | 严格、实用主义、证据驱动的技术方案、模型和合并风险判断。Strict pragmatic technical judgment. |
| [`dbx-technical-plan`](skills/dbx-technical-plan/) | 代码变更前的证据边界技术实施计划，明确 source of truth、不变量、实施切片、验证模型和 handoff。Evidence-bound technical implementation planning before coding. |
| [`dbx-code-ratchet`](skills/dbx-code-ratchet/) | 可修改代码的有界 review-repair-revalidation 元技能：调度 diff/Linus review，triage findings，局部自动修复，验证并在方向错误或风险发散时停止。Bounded code ratchet for concrete diffs. |
| [`dbx-architecture-health`](skills/dbx-architecture-health/) | 仓库/模块架构健康体检：识别长期腐化、状态 owner 混乱、验证拓扑缺口和 AI coding 可操作性风险，并给出只读防腐路线图。Read-only architecture health audits for repo decay and AI-coding operability. |
| [`dbx-skill-architect`](skills/dbx-skill-architect/) | 场景优先的 skill 创建、评审、改进与评测。Scenario-first skill architecture, critique, improvement, and eval design. |
| [`dbx-skill-portfolio-auditor`](skills/dbx-skill-portfolio-auditor/) | 已安装技能组合审计与全局/项目/显式触发/禁用/卸载范围决策。Audit installed skill portfolios and recommend global, project, explicit-only, disable, or uninstall placement. |
| [`dbx-product-judgment`](skills/dbx-product-judgment/) | 证据边界内判断产品、功能、PRD、交互、信息架构、实现对齐、路线图或竞品定位是否产品正确。Evidence-bounded product judgment across artifacts and decisions. |
| [`dbx-design-judgment`](skills/dbx-design-judgment/) | 证据边界内评审 UI、流程、截图、PRD、原型、设计系统或代码支撑的界面设计；只做设计判断和实现交接，不改代码。Evidence-bounded design judgment and handoff without implementation. |
| [`dbx-attention-routing`](skills/dbx-attention-routing/) | 混合输入的注意力分流内核：把收藏、想法、任务、课程、工具、消息等路由为行动、构建、实验、追踪、存档、孵化、丢弃、风险保护或澄清，并支持个人配置和外部系统 dry-run 映射。Product-agnostic attention router for mixed inputs with profile and adapter layers. |
| [`dbx-learn`](skills/dbx-learn/) | 持久学习控制器：用于真正理解概念、资料研究、练习 rep、主动复习和可选学习记录；不替代普通总结、直接编码或混合 inbox 分流。Durable learning controller for capability-building study. |
| [`dbx-conversation-align`](skills/dbx-conversation-align/) | 对话卡点诊断、措辞改写与边界沟通。Diagnose stuck conversations, rewrite risky messages, and plan boundaries. |
| [`dbx-decision-framing`](skills/dbx-decision-framing/) | 高影响真实决策的分支门禁、取舍分析与验证动作。Frame high-impact decisions with gates, trade-offs, and validation steps. |
| [`dbx-subagent-context`](skills/dbx-subagent-context/) | Codex subagent 上下文继承策略。Set Codex subagent context inheritance strategy. |
| [`dbx-goal-writer`](skills/dbx-goal-writer/) | Codex goal 合同生成、启动与审计。Create, start, and audit Codex goal contracts. |
| [`dbx-agent-handoff`](skills/dbx-agent-handoff/) | AI agent/session 续跑交接包生成。Create restart handoffs for future AI sessions. |
| [`dbx-software-plan-first-plan-issue`](skills/dbx-software-plan-first-plan-issue/) | 手动触发的软件 Plan-First 对话收敛阶段：不读仓库、不写计划文件、不实现代码。Manual-only plan convergence phase. |
| [`dbx-software-plan-first-ground-plan`](skills/dbx-software-plan-first-ground-plan/) | 手动触发的软件 Plan-First 只读 grounding 阶段：确认仓库事实、规则、source of truth 和验证模型。Manual-only read-only grounding phase. |
| [`dbx-software-plan-first-finalize-plan`](skills/dbx-software-plan-first-finalize-plan/) | 手动触发的软件 Plan-First 定稿阶段：写入中文 `plan.md` / `tasks.md` 并建立 workflow seal。Manual-only plan finalization phase. |
| [`dbx-software-plan-first-implement-feature`](skills/dbx-software-plan-first-implement-feature/) | 手动触发的软件 Plan-First 单任务实现阶段：只做第一个未完成 task，验证后等待 review。Manual-only review-gated implementation phase. |
| [`dbx-software-plan-first-showhand`](skills/dbx-software-plan-first-showhand/) | 手动触发的软件 Plan-First 安全自动执行阶段：仅在所有门禁满足时连续执行完整计划。Manual-only safe automation phase. |

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
# Check frontmatter, directory structure, eval JSON, README/index mentions,
# and plan-first shared-file sync.
python3 scripts/validate_skills.py --root .

# Generate Markdown or JSON inventory.
python3 scripts/skill_inventory.py --root . --format markdown
python3 scripts/skill_inventory.py --root . --format json

# Validate evals/triggers.json files.
python3 scripts/run_trigger_evals.py --root . --validate-only
```

For `dbx-aliyun-sls`, runtime checks require a local Aliyun CLI installation and SLS plugin when executing queries:

```bash
python3 skills/dbx-aliyun-sls/scripts/check_runtime.py
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

# Codex / Agent Skills current user scope
mkdir -p ~/.agents/skills
for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.agents/skills/
done

# Legacy or custom Codex setups
mkdir -p ~/.codex/skills
for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.codex/skills/
done

# Cursor
mkdir -p ~/.cursor/skills
for skill in skills/dbx-*; do
  ln -sf "$(pwd)/$skill" ~/.cursor/skills/
done
```

Use `~/.agents/skills` for the current Codex / Agent Skills user scope. Keep
`~/.codex/skills` only for legacy or custom Codex setups that still discover
skills there.

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
