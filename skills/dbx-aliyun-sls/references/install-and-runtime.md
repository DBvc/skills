# Install and Runtime Notes

This reference is for the agent or maintainer when the user wants Alibaba Cloud SLS querying to work from a local Agent environment.

## Preferred executor

Prefer the official Aliyun CLI plus the SLS plugin for a first DBX version:

```bash
aliyun version
aliyun configure list
aliyun plugin install --names sls
aliyun sls --help
```

The wrapper scripts in this skill assume `aliyun sls get-logs-v2` is available.

## Authentication policy

Never ask the user to paste secrets into chat.

Acceptable credential sources:

- Existing Aliyun CLI profile.
- Environment variables already present in the local shell.
- RAM role / ECS RAM role / STS credentials configured outside chat.
- A trusted MCP server config controlled by the user.

Forbidden in chat:

- AccessKey ID.
- AccessKey Secret.
- STS token.
- Cookies.
- Authorization headers.
- Raw `~/.aliyun/config.json` content.

If credentials are missing, say:

```text
本地阿里云凭证还没有配置。请在终端里用 aliyun configure 或你们公司的 RAM/STS/OAuth 流程配置；不要把密钥贴到对话里。配置完成后我可以继续做只读查询。
```

## Permission floor

For read-only log querying, the most important permission is the ability to query logs from the selected Project/Logstore. If index inspection is needed for query optimization, index read permission is also needed.

A practical minimum often includes:

```text
log:GetLogStoreLogs
log:GetIndex
```

Scope permissions as tightly as possible to the specific Project and Logstore rather than the entire account.

Do not use this skill to create or mutate RAM policies. Produce a policy suggestion only if the user asks.

## Runtime check

Use:

```bash
python3 skills/dbx-aliyun-sls/scripts/check_runtime.py
```

The script checks command availability and prints command output with simple redaction. It does not read config files directly.

## Direct CLI command pattern

Raw query:

```bash
aliyun sls get-logs-v2 \
  --project "$SLS_PROJECT" \
  --logstore "$SLS_LOGSTORE" \
  --from "$FROM" \
  --to "$TO" \
  --query 'status>=500' \
  --line 100 \
  --offset 0 \
  --reverse true
```

SQL query:

```bash
aliyun sls get-logs-v2 \
  --project "$SLS_PROJECT" \
  --logstore "$SLS_LOGSTORE" \
  --from "$FROM" \
  --to "$TO" \
  --query 'status in [500 599] | SELECT request_uri, count(*) AS errors FROM log GROUP BY request_uri ORDER BY errors DESC LIMIT 10'
```

## MCP path

If the user has Alibaba Cloud Observability MCP configured:

- Prefer explicit query execution tools over natural-language paid AI conversion tools.
- Confirm whether paid tools are enabled before using them.
- Keep the same DBX gates: target, time, query, cost, privacy, completion.
- Do not treat MCP output as magically complete. State scope and caveats.

## Official Alibaba Cloud skills

Alibaba Cloud has official SLS/Cloud Agent skills. They can be installed and used as execution/reference skills, but DBX should still enforce:

- no pasted secrets;
- bounded time range;
- read-only default;
- dry-run for broad queries;
- redacted final output;
- explicit completion caveats.
