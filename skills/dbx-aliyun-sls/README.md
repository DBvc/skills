# dbx-aliyun-sls

Read-only DBX skill for querying and diagnosing Alibaba Cloud Simple Log Service / SLS logs through Aliyun CLI, GetLogsV2, SDK, or approved Observability MCP tools.

It is designed for this shape:

```text
用户想查阿里云日志
-> Agent 先收敛 project / logstore / time / query intent
-> 生成安全查询计划
-> 用本地只读 CLI/API/MCP 执行
-> 摘要化、脱敏、带 caveat 地返回结果
```

## Install

This package is a repository overlay.

Unzip it at the root of `DBvc/skills` so it creates:

```text
skills/dbx-aliyun-sls/
```

Then run the normal DBX local checks:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## Runtime prerequisites

The skill itself is instruction-first. Actual querying needs one of these executors:

1. `aliyun` CLI with the SLS plugin installed.
2. A trusted SDK/OpenAPI wrapper using GetLogsV2.
3. A configured Alibaba Cloud Observability MCP server.
4. An installed official Alibaba Cloud SLS Agent Skill used as an executor/reference.

Recommended local path:

```bash
aliyun version
aliyun configure list
aliyun plugin install --names sls
aliyun sls --help
```

Never paste AccessKey ID, AccessKey Secret, STS token, cookies, or authorization headers into chat.

## Useful commands

Check local readiness:

```bash
python3 skills/dbx-aliyun-sls/scripts/check_runtime.py
```

Dry-run a query command:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project prod-web \
  --logstore nginx-access \
  --last-minutes 15 \
  --query 'status>=500' \
  --line 50 \
  --reverse \
  --dry-run
```

Execute a bounded read-only query:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project prod-web \
  --logstore nginx-access \
  --last-minutes 15 \
  --query 'status>=500' \
  --line 50 \
  --reverse
```

## Common invocations

```text
查一下 prod-web / nginx-access 最近 15 分钟 status>=500 的日志，先 dry-run。

帮我生成 SLS SQL：最近一小时每分钟的 p95 延迟和错误数。

根据 trace_id=abc123 在 order-service 的 logstore 下钻，按时间顺序列关键事件。

这个查询太慢了，帮我看是不是没走索引，先不要改任何配置。

我想把阿里云 SLS 接到 Agent 里，给我一个只读权限和 CLI/MCP 边界方案。
```

## What this skill adds

- Alibaba Cloud SLS-specific trigger boundary.
- Read-only credential and privacy guardrails.
- Time-range and raw-result limits to avoid accidental production log dredging.
- Query mode routing: raw retrieval, field filter, SQL analysis, SPL, trace drill-down, incident triage.
- Deterministic local wrapper scripts for runtime check and bounded `get-logs-v2` execution.
- DBX evals and repository integration snippets.

## Suggested next step after adding

Copy the snippets from `references/repo-integration.md` into:

- root `README.md`
- `DBX_SKILL_INDEX.md`
- `docs/DBX_ROUTING_MATRIX.md`

Then run repository validation.
