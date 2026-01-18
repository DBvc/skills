# Claude Skills

个人 Claude/Codex Skills 仓库，用于集中管理和版本控制。

Personal Claude/Codex Skills repository for centralized management and version control.

## Skills 列表 / Skill List

| Skill | 描述 / Description |
|-------|---------------------|
| [commit-pr-contract](skills/commit-pr-contract/) | 生成 commit message 与 PR 描述 / Generate commit messages and PR descriptions |
| [linus-tech-review](skills/linus-tech-review/) | Linus Torvalds 风格技术方案评估 / Linus-style technical review |

## 使用方法 / Usage

### 使用 add-skill 安装（推荐）/ Install with add-skill (Recommended)

```bash
# 安装所有 skills / Install all skills
npx add-skill dbvc/skills

# 安装特定 skill / Install specific skill
npx add-skill dbvc/skills --skill commit-pr-contract

# 查看可用 skills / List available skills
npx add-skill dbvc/skills --list
```

### 手动安装 / Manual Install

```bash
# 克隆后链接到 Codex skills 目录
git clone https://github.com/dbvc/skills.git
cd skills
ln -sf "$(pwd)/skills/commit-pr-contract" ~/.codex/skills/
ln -sf "$(pwd)/skills/linus-tech-review" ~/.codex/skills/

# 或链接到 Cursor skills 目录
ln -sf "$(pwd)/skills/commit-pr-contract" ~/.cursor/skills/
ln -sf "$(pwd)/skills/linus-tech-review" ~/.cursor/skills/
```

## 创建新 Skill / Create New Skill

复制现有 skill 作为模板：

```bash
cp -r skills/commit-pr-contract skills/my-new-skill
# 编辑 skills/my-new-skill/SKILL.md
```

## 相关资源 / Resources

- [Agent Skills Specification](https://agentskills.io)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)

## License

MIT
