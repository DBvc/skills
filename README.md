# DBX Skills

个人 Claude/Codex Skills 仓库，用于集中管理和版本控制。稳定技能统一使用 `dbx-` 前缀，避免和外部安装的 skills 产生命名歧义。

Personal Claude/Codex Skills repository for centralized management and version control. Stable skills use the `dbx-` prefix to avoid naming conflicts with third-party skills.

## 稳定 Skills / Stable Skills

| Skill | 描述 / Description |
|-------|---------------------|
| [dbx-pr-contract](skills/dbx-pr-contract/) | 合同式 commit message 与 PR 描述 / Contract-style commit messages and PR descriptions |
| [dbx-open-source-pr](skills/dbx-open-source-pr/) | 面向开源仓库的英文 commit/PR 写作 / Generate English commit messages and PR descriptions for open-source repositories |
| [dbx-linus-review](skills/dbx-linus-review/) | Linus Torvalds 风格技术方案评估 / Linus-style technical review |
| [dbx-skill-architect](skills/dbx-skill-architect/) | 场景优先的 skill 创建、评审、改进与评测 / Scenario-first skill architecture, critique, improvement, and eval design |

## 草稿 Skills / Draft Skills

这些目录仍在打磨中，暂时不加 `dbx-` 前缀。

| Skill | 描述 / Description |
|-------|---------------------|
| [communication-alignment](skills/communication-alignment/) | 复杂沟通对齐、表达改写与冲突处理 / Align communication, rewrite messages, and handle conflicts |
| [travel-guide-writer](skills/travel-guide-writer/) | 生成个性化旅游攻略与行程建议 / Write personalized travel guides and itineraries |

## 使用方法 / Usage

### 使用 add-skill 安装（推荐）/ Install with add-skill (Recommended)

```bash
# 安装所有 skills / Install all skills
npx add-skill dbvc/skills

# 安装特定 skill / Install specific skill
npx add-skill dbvc/skills --skill dbx-pr-contract

# 查看可用 skills / List available skills
npx add-skill dbvc/skills --list
```

### 手动安装 / Manual Install

```bash
# 克隆后链接到 Codex skills 目录
git clone https://github.com/dbvc/skills.git
cd skills
ln -sf "$(pwd)/skills/dbx-pr-contract" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-open-source-pr" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-linus-review" ~/.codex/skills/
ln -sf "$(pwd)/skills/dbx-skill-architect" ~/.codex/skills/

# 或链接到 Cursor skills 目录
ln -sf "$(pwd)/skills/dbx-pr-contract" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-open-source-pr" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-linus-review" ~/.cursor/skills/
ln -sf "$(pwd)/skills/dbx-skill-architect" ~/.cursor/skills/
```

## 创建新 Skill / Create New Skill

复制现有 skill 作为模板：

```bash
cp -r skills/dbx-pr-contract skills/dbx-my-new-skill
# 编辑 skills/dbx-my-new-skill/SKILL.md
```

命名约定：稳定的个人技能使用 `dbx-` 前缀；名字保持短而明确，具体边界写进 `description`。

## 相关资源 / Resources

- [Agent Skills Specification](https://agentskills.io)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)

## License

MIT
