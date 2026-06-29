---
name: dbx-aliyun-sls
description: >-
  Read-only Alibaba Cloud Simple Log Service / SLS log query controller. Use when the user asks to query, generate, optimize, execute, summarize, or diagnose Alibaba Cloud SLS / Log Service / Logstore logs through Aliyun CLI, GetLogsV2, SDK, or Observability MCP. Produces a safe query plan, bounded command/API execution, structured findings, caveats, and next drill-down steps. Do not use for generic log files not stored in SLS, code implementation, destructive SLS management, credential collection, broad production data export, cloud cost optimization, or paid AI observability tools unless explicitly approved.
---

# DBX Aliyun SLS / 阿里云日志查询控制器

Core job:

```text
incident or log question
+ explicit Alibaba Cloud SLS target
+ bounded time range and safety budget
-> query plan
-> read-only CLI/API/MCP execution
-> redacted structured findings
-> next drill-down or handoff
```

This skill is a read-only observability controller. It helps an agent query Alibaba Cloud Simple Log Service safely. It is not a cloud admin bot, not a secret collector, not a production data exporter, and not a replacement for human incident ownership.

Default output language follows the user.

## 1. Use / do not use

Use this skill when the user asks to work with Alibaba Cloud SLS / Log Service / Logstore logs, for example:

- “查一下阿里云 SLS 里最近 15 分钟的 5xx。”
- “帮我写一个 SLS SQL，按分钟统计 P95 延迟。”
- “根据 traceId / requestId / userId 下钻日志。”
- “这个 Logstore 里 ERROR 最多的是哪些接口？”
- “用 aliyun cli 查询 project/logstore 的日志。”
- “帮我诊断 SLS 查询为什么慢，是否没走索引。”
- “我想让 Agent 查阿里云日志，先生成安全的查询命令。”

Do not use this skill when the dominant task is:

- local log file reading, pasted log analysis, or non-SLS logs: answer directly or use source-reading/log-analysis tools;
- code implementation, bug fixing, or refactor planning after logs reveal a code issue: hand off to `dbx-technical-plan` or implementation;
- PR/diff review: use `dbx-diff-review` or `dbx-linus-review`;
- SLS resource creation, deletion, index mutation, alert mutation, dashboard changes, or data writes unless the user explicitly requests a separate admin workflow;
- collecting AccessKey ID, AccessKey Secret, STS token, cookies, authorization headers, private endpoints, or internal log payloads in chat;
- exporting large volumes of production data, customer data, secrets, credentials, or personal data;
- using paid AI conversion / STAROps-backed observability tools without explicit user approval.

If the user only asks “阿里云日志有没有 CLI 或接口？” answer normally. Use the full skill when there is an actual query, query design, incident, or reusable Agent workflow.

## 2. Role boundary

Allowed:

- Generate SLS index query, SQL, or SPL statements.
- Execute bounded read-only log queries through local `aliyun sls get-logs-v2`, `scripts/sls_query.py`, SDK wrappers, or approved MCP tools.
- Check local runtime readiness without exposing secrets.
- Inspect index/readiness metadata only when needed and authorized.
- Summarize query results, anomalies, trends, samples, and uncertainty.
- Recommend the next drill-down query.

Forbidden by default:

- Asking the user to paste cloud secrets into chat.
- Printing secrets or sensitive raw logs back to chat.
- Performing write operations such as create/update/delete Project, Logstore, index, alert, dashboard, ETL job, or log data.
- Querying unbounded time ranges or huge result sets without confirmation.
- Claiming “no error exists” when the query scope, indexing, sampled output, or permissions are incomplete.
- Treating model-generated query text as verified execution evidence.

## 3. Hard gates

Before executing or claiming results, pass these gates.

1. **Target gate**: project and logstore are known, or the user authorizes a read-only discovery step.
2. **Credential gate**: credentials are already configured locally through Aliyun CLI profile, environment variables, RAM role, STS, or MCP config. Never request raw secrets in chat.
3. **Time gate**: the time window is explicit or safely defaulted. Default: last 15 minutes for raw/error lookup, last 1 hour for aggregate analysis. Ask or dry-run before querying more than 1 hour unless the user already specified the range.
4. **Query gate**: the query mode matches the intent: raw retrieval, field filter, SQL aggregation, SPL pipeline, trace drill-down, or query generation only.
5. **Cost gate**: avoid broad `*` scans, long ranges, missing-index SQL, large exports, and paid AI/MCP conversion tools unless approved.
6. **Privacy gate**: results must be summarized and redacted by default. Raw samples are limited and should not include credentials, tokens, cookies, full personal data, or business secrets.
7. **Completion gate**: only claim what the executed query supports. Include scope, time range, command/API path, caveats, and next action.

If gates 1 to 4 are missing and cannot be inferred, produce a dry-run query plan or ask at most three blocking questions.

## 4. Runtime preference order

Choose the safest available executor.

1. **Local wrapper script**: use `scripts/sls_query.py` for bounded `get-logs-v2` calls when available. It normalizes time windows, limits raw line count, supports dry-run, and redacts common secrets.
2. **Aliyun CLI directly**: use `aliyun sls get-logs-v2` when the wrapper is unavailable or the user wants the raw CLI command.
3. **SDK or OpenAPI**: use SDK/GetLogsV2 when building a durable integration or when the host has a trusted SDK environment.
4. **Observable MCP**: use only when already configured and the tool set is understood. Prefer free, explicit query execution tools. Do not silently call paid AI conversion tools.
5. **Official Alibaba Cloud skill**: if `alibabacloud-sls-query` or `alibabacloud-sls-cli-guidance` is installed, it can be used as an executor or reference, while this DBX skill still controls scope, safety, and handoff.

Before first execution in a repo or machine, use `scripts/check_runtime.py` or equivalent commands:

```bash
python3 skills/dbx-aliyun-sls/scripts/check_runtime.py
aliyun version
aliyun plugin list
aliyun sls --help
aliyun configure list
```

Do not read or print `~/.aliyun/config.json` directly.

## 5. Modes

Choose the smallest mode that satisfies the user.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `runtime_check` | User needs setup validation | Check `aliyun`, SLS plugin, profile readiness, and missing pieces without secrets. |
| `query_generation_only` | User wants query/SQL/SPL text only | Produce query, command skeleton, assumptions, and caveats. Do not execute. |
| `raw_log_retrieval` | User wants log samples/details | Use narrow time range, `line <= 100`, reverse order when latest matters, redact output. |
| `field_filter` | User gives status, level, keyword, traceId, requestId, userId, host, path, etc. | Prefer indexed field filters; fall back with caveats when index facts are unknown. |
| `sql_analysis` | User asks top-N, group-by, trend, avg, p95, count, distribution, projection | Use `index query | SELECT ... LIMIT ...`; do not rely on raw pagination for SQL. |
| `spl_pipeline` | User asks row-level extraction or pipeline processing | Use SPL only when it is clearly the right query model. |
| `trace_drilldown` | User gives traceId/requestId/orderId/correlation id | Query exact field across narrow time range and sort chronologically unless latest-first is requested. |
| `incident_triage` | User asks why errors or latency spiked | Start with aggregate trend/top-N, then drill into representative raw samples. |
| `mcp_handoff` | User wants MCP-based integration | Give config/permission/read-only/paid-tool boundaries, not hidden execution. |
| `blocked` | Missing target/time/permission/scope would flip the query | Ask minimal blocking questions or produce dry-run. |
| `safety_stop` | Request is secret exfiltration, unauthorized access, destructive operation, or deceptive monitoring | Refuse unsafe shape and offer a safe read-only alternative. |
| `direct_answer` | It is only conceptual Q&A | Answer without query contracts. |

## 6. Query contract

Internally compile this contract before executing. Print it only for dry-runs, high-risk queries, or when the user asks for auditability.

```yaml
sls_query_contract:
  mode: runtime_check | query_generation_only | raw_log_retrieval | field_filter | sql_analysis | spl_pipeline | trace_drilldown | incident_triage | mcp_handoff | blocked | safety_stop | direct_answer
  executor: scripts/sls_query.py | aliyun_cli | sdk_getlogsv2 | observability_mcp | official_skill | none
  target:
    project: ""
    logstore: ""
    region: ""
    profile: ""
  time_range:
    from: "unix_seconds_or_iso"
    to: "unix_seconds_or_iso"
    duration_minutes: 0
    source: user_supplied | defaulted | inferred | unknown
  query:
    kind: index | sql | spl | mixed | unknown
    text: ""
    line_limit: 0
    offset: 0
    reverse: true
  safety:
    read_only: true
    broad_scan: false
    paid_tool: false
    raw_output_allowed: false
    redaction_required: true
    approval_needed: []
  evidence:
    executed: false
    command_or_api: ""
    stdout_coverage: full | partial | sampled | failed | not_run
    caveats: []
  assumptions: []
  blockers: []
```

## 7. Query construction rules

### 7.1 Time range

- If not specified, default to:
  - last 15 minutes for raw errors, trace drill-down, exact identifiers;
  - last 1 hour for trend/top-N aggregate analysis.
- Require confirmation or dry-run before querying more than 1 hour by default.
- Use Unix seconds for CLI/API execution.
- State the exact time range in output.

### 7.2 Raw logs

- Use `line <= 100`.
- Prefer `reverse=true` for “latest errors”.
- Prefer `reverse=false` for trace/story reconstruction.
- Show at most a small redacted sample in chat. Summarize patterns instead of dumping logs.

Template:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project "$SLS_PROJECT" \
  --logstore "$SLS_LOGSTORE" \
  --last-minutes 15 \
  --query 'status>=500' \
  --line 100 \
  --reverse
```

### 7.3 SQL analysis

Use SQL when the user asks for count, top-N, percentile, trend, grouping, sorting, projection, or distribution.

- Put a selective index query before SQL when possible.
- Use SQL `LIMIT` for result size.
- For SQL mode, do not use raw pagination as the primary result limit.
- If index/analytics configuration is unknown, state that the SQL may scan or fail.

Example:

```text
status in [500 599]
| SELECT request_uri, count(*) AS errors
  FROM log
  GROUP BY request_uri
  ORDER BY errors DESC
  LIMIT 10
```

### 7.4 Trace/correlation drill-down

- Prefer exact field query: `trace_id:"..."`, `request_id:"..."`, `order_id:"..."`.
- Use chronological order for path reconstruction.
- If the field name is unknown, generate candidate queries rather than pretending.

### 7.5 Index awareness

When optimizing or diagnosing query performance:

- Check index configuration if the user allows and runtime supports it.
- Prefer indexed fields for the first-stage filter.
- Distinguish “query may be slow because index facts are unknown” from “query is definitely slow”.
- Do not create or modify indexes in this skill.

## 8. Execution rules

### Wrapper command

Use this when possible:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project prod-web \
  --logstore nginx-access \
  --last-minutes 15 \
  --query 'status>=500' \
  --line 50 \
  --reverse
```

Dry-run first for uncertain scope:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project prod-web \
  --logstore nginx-access \
  --last-minutes 60 \
  --query 'status in [500 599] | SELECT request_uri, count(*) AS errors FROM log GROUP BY request_uri ORDER BY errors DESC LIMIT 10' \
  --dry-run
```

### Direct CLI equivalent

```bash
aliyun sls get-logs-v2 \
  --project prod-web \
  --logstore nginx-access \
  --from 1777016700 \
  --to 1777017600 \
  --query 'status>=500' \
  --line 100 \
  --offset 0 \
  --reverse true
```

Never include secrets, raw AccessKey, tokens, cookies, or authorization headers in command text.

## 9. Output contracts

### Executed query output

```markdown
## SLS 查询结果
- 状态：executed / partial / failed
- 执行方式：scripts/sls_query.py / aliyun cli / SDK / MCP
- 目标：project / logstore / region / profile
- 时间范围：from -> to
- 查询语句：`...`
- 结果范围：raw sample / SQL rows / partial / not available

## 关键发现
1. ...
2. ...

## 样本或统计
...

## 不确定性
- ...

## 下一步下钻
1. ...
```

### Query generation only output

```markdown
## SLS 查询计划
- 意图：
- 推荐模式：raw / field filter / SQL / SPL / trace drill-down
- 时间范围：
- 查询语句：
- CLI 命令：
- 安全边界：
- 执行前需确认：
```

### Blocked output

```markdown
## 暂不能安全查询
原因：缺少会改变查询范围、安全性或成本的信息。

## 当前可确定
- ...

## 最少需要确认
1. Project / Logstore 是哪个？
2. 时间范围？
3. 是否允许本地只读 CLI 执行？
```

## 10. Completion policy

You may say the SLS query work is complete only when:

- target, time range, query text, executor, and read-only boundary are clear;
- executed commands/API calls are actually run, or the output explicitly says dry-run / query-only;
- result claims are supported by returned data;
- secrets and sensitive fields are not exposed;
- limitations such as index unknown, partial results, permission failure, timeout, or parse failure are stated;
- next drill-down or handoff is explicit.

You may not say:

- “没有错误” unless the queried scope, time range, logstore, permissions, and index behavior support that claim;
- “已经全量检查” when line limits, sampling, SQL limits, failed pages, or broad time ranges apply;
- “安全 / 合规 / 无隐私风险” as a blanket claim;
- “已配置好阿里云权限” unless the runtime check confirms it in the current session.

## 11. References and scripts

Load only when needed:

- `references/install-and-runtime.md`: Aliyun CLI, SLS plugin, profile, SDK, MCP setup boundaries.
- `references/query-playbook.md`: common SLS query/SQL/SPL templates and incident drill-down paths.
- `references/security-cost-policy.md`: read-only, credential, privacy, range, result, and paid-tool guardrails.
- `references/repo-integration.md`: snippets for README, index, and routing matrix.
- `references/examples.md`: realistic prompts and expected response shapes.
- `scripts/check_runtime.py`: local runtime readiness check without reading secret files.
- `scripts/sls_query.py`: safe wrapper around `aliyun sls get-logs-v2`.
