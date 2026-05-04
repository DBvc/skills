# DBX Skills

个人 Claude/Codex Skills 仓库，用于集中管理和版本控制。稳定技能统一使用 `dbx-` 前缀，避免和外部安装的 skills 产生命名歧义。

Personal Claude/Codex Skills repository for centralized management and version control. Stable skills use the `dbx-` prefix to avoid naming conflicts with third-party skills.

## 稳定 Skills / Stable Skills

| Skill | 描述 / Description |
|-------|---------------------|
| [dbx-open-source-commit-pr](skills/dbx-open-source-commit-pr/) | 面向开源仓库的英文 commit/PR 写作 / Generate English commit messages and PR descriptions for open-source repositories |
| [dbx-work-commit-pr](skills/dbx-work-commit-pr/) | 工作场景的中文合同式 commit/PR 写作 / Contract-style commit messages and PR descriptions for work contexts |
| [dbx-linus-review](skills/dbx-linus-review/) | Linus Torvalds 风格技术方案评估 / Linus-style technical review |
| [dbx-skill-architect](skills/dbx-skill-architect/) | 场景优先的 skill 创建、评审、改进与评测 / Scenario-first skill architecture, critique, improvement, and eval design |
| [dbx-conversation-align](skills/dbx-conversation-align/) | 对话卡点诊断、措辞改写与边界沟通 / Diagnose stuck conversations, rewrite risky messages, and plan boundaries |
| [dbx-subagent-context-control](skills/dbx-subagent-context-control/) | Codex subagent 上下文继承控制 / Control Codex subagent context inheritance |

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
ln -sf "$(pwd)/skills/dbx-open-source-commit-pr" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-work-commit-pr" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-linus-review" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-skill-architect" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-conversation-align" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-subagent-context-control" ~/.codex/skills/

# 或链接到 Cursor skills 目录
ln -sf "$(pwd)/skills/dbx-open-source-commit-pr" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-work-commit-pr" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-linus-review" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-skill-architect" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-conversation-align" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-subagent-context-control" ~/.cursor/skills/
```

## 创建新 Skill / Create New Skill

复制现有 skill 作为模板：

```bash
cp -r skills/dbx-work-commit-pr skills/dbx-my-new-skill
# 编辑 skills/dbx-my-new-skill/SKILL.md
```

命名约定：稳定的个人技能使用 `dbx-` 前缀；名字保持短而明确，具体边界写进 `description`。

## 相关资源 / Resources

- [Agent Skills Specification](https://agentskills.io)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)

## License

MIT
