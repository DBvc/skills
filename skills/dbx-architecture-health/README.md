# dbx-architecture-health

Read-only DBX skill for repository or module architecture health review in AI-coding-era codebases.

This version is based on the adjusted Agent-Operable Architecture frame:

1. start from likely future changes;
2. calibrate by the repo's actual risk profile;
3. review four core questions: TRUTH, LOCALITY, PROOF, CONTEXT;
4. treat compatibility, migration, rollout, and rollback as commitment-driven concerns, not universal rules.

## Install

From the root of the DBvc skills repository, unzip the package so it creates or overwrites:

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

```text
评估这个仓库适不适合长期用 AI agent coding：agent 会不会读错上下文、复制错误模式、漏掉真正的 source of truth？
```

## Optional script

```bash
python3 skills/dbx-architecture-health/scripts/collect-architecture-context.py --root . --format markdown
```

The script is read-only. It does not run tests, install dependencies, access the network, or modify files.
