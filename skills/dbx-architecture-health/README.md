# dbx-architecture-health

Read-only DBX skill for repository or module architecture health review in AI-coding-era codebases.

## Install

From the root of the DBvc skills repository, unzip the package so it creates:

```text
skills/dbx-architecture-health/
```

No external dependencies are required. The optional context collection script uses Python 3 standard library only.

## Typical prompts

```text
帮我对这个仓库做一次架构健康体检，重点看长期腐化和 AI coding 会不会放大问题。
```

```text
只审计 packages/web 的架构健康，不要 review 当前 PR。
```

```text
看一下这个 codebase 有没有状态 owner 混乱、source of truth 重复、领域模型被 API DTO 污染的问题。
```

## Optional script

```bash
python3 skills/dbx-architecture-health/scripts/collect-architecture-context.py --root . --format markdown
```

The script is read-only. It does not run tests, install dependencies, access the network, or modify files.
