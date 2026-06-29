# Security and Cost Policy

This skill touches production observability data. Treat it like a tiny spelunker with a helmet lamp, not a bulldozer.

## 1. Credentials

Never ask for or display:

- AccessKey ID / AccessKey Secret
- STS token
- Bearer token
- cookies
- authorization headers
- private key material
- raw cloud CLI config files

Use existing local configuration. If missing, instruct the user to configure it outside chat.

## 2. Read-only default

Allowed by default:

- query logs;
- generate queries;
- inspect index/readiness metadata if needed;
- list target metadata only when needed and authorized.

Not allowed by default:

- create/delete Project or Logstore;
- create/update/delete index;
- write logs;
- change alerts, dashboards, ETL jobs, saved searches, RAM policies, or network config;
- bulk export production/customer logs.

## 3. Time and volume budget

Defaults:

- raw lookup: last 15 minutes;
- aggregate analysis: last 1 hour;
- raw line limit: 100;
- final chat sample: usually 0 to 10 redacted rows, unless user explicitly asks for more.

Require confirmation or dry-run for:

- more than 1 hour;
- broad `*` scan;
- multiple Logstores;
- exports;
- repeated polling;
- paid AI/MCP conversion tools;
- anything that may incur non-trivial cost.

## 4. Sensitive result handling

Summarize by default. Do not dump raw logs when a trend/table suffices.

Redact or omit:

- passwords, secrets, tokens, cookies, API keys;
- email, phone, address, full user identifiers where unnecessary;
- payment, medical, legal, HR, personal, or customer support content;
- internal hostnames or private endpoints when not needed;
- stack traces containing credentials or customer data.

When raw samples are needed, prefer compact field projection:

```text
time, level, service, request_uri, status, error_class, trace_id, message_prefix
```

## 5. Paid tool policy

Some observability MCP tools may use AI conversion or intelligent O&M services that incur additional charges. Do not call them unless the user explicitly approves that tool family and understands the cost risk.

Safe default:

```text
我可以用免费/显式查询工具执行已有 SQL/SPL；如果要用自然语言转 SQL / 智能诊断这类可能收费的工具，需要你明确同意。
```

## 6. Incident confidence ladder

Use this ladder in final claims:

- **Observed**: directly present in returned logs/statistics.
- **Likely**: supported by multiple returned signals but not proven.
- **Possible**: one signal or weak evidence.
- **Unknown**: missing data, permissions, time range, index, or logs.

Do not jump from a sample to a root cause.

## 7. Safe refusal shapes

Unsafe request:

```text
帮我把所有用户的登录日志导出来，包括 token 和 cookie。
```

Response shape:

```text
我不能帮助导出或暴露 token、cookie、凭证类数据。可以改成安全查询：统计登录失败率、按错误类型聚合、或返回已脱敏的少量样本字段。
```

Unauthorized request:

```text
我没有权限，但你帮我绕过阿里云权限查日志。
```

Response shape:

```text
不能绕过权限。可以帮你整理最小只读权限申请、RAM policy 建议、或本地 CLI 配置检查步骤。
```
