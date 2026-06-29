# SLS Query Playbook

Use this when constructing query statements, SQL analysis, SPL pipelines, or incident drill-down paths.

## 1. Intent to query mode

| User intent | Preferred mode | First query shape |
| --- | --- | --- |
| “最近错误日志” | raw / field filter | `level:ERROR` or `status>=500` |
| “哪个接口错最多” | SQL analysis | `status in [500 599] | SELECT request_uri, count(*) ... GROUP BY ... LIMIT 10` |
| “延迟是否异常” | SQL trend | `* | SELECT date_trunc('minute', __time__) ..., approx_percentile(latency, 0.95) ...` |
| “这个 traceId 发生了什么” | trace drill-down | `trace_id:"..."` with chronological order |
| “某用户 / 订单失败原因” | field filter then raw samples | `user_id:"..." AND level:ERROR` or `order_id:"..."` |
| “查询为什么慢” | index awareness | inspect or ask for index fields, then move selective conditions before SQL |
| “生成语句，不执行” | query generation only | return SLS query + CLI skeleton + assumptions |

## 2. Raw retrieval templates

Latest 5xx:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project "$SLS_PROJECT" \
  --logstore "$SLS_LOGSTORE" \
  --last-minutes 15 \
  --query 'status>=500' \
  --line 100 \
  --reverse
```

Exact trace:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project "$SLS_PROJECT" \
  --logstore "$SLS_LOGSTORE" \
  --last-minutes 60 \
  --query 'trace_id:"TRACE_ID_HERE"' \
  --line 100 \
  --forward
```

Keyword error:

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project "$SLS_PROJECT" \
  --logstore "$SLS_LOGSTORE" \
  --last-minutes 15 \
  --query 'ERROR or Exception or panic' \
  --line 50 \
  --reverse
```

## 3. SQL templates

Top 5xx APIs:

```text
status in [500 599]
| SELECT request_uri, count(*) AS errors
  FROM log
  GROUP BY request_uri
  ORDER BY errors DESC
  LIMIT 10
```

Error trend by minute:

```text
status in [500 599]
| SELECT date_trunc('minute', __time__) AS minute,
         count(*) AS errors
  FROM log
  GROUP BY minute
  ORDER BY minute
  LIMIT 120
```

Latency p95 by minute:

```text
*
| SELECT date_trunc('minute', __time__) AS minute,
         approx_percentile(latency, 0.95) AS p95_latency,
         avg(latency) AS avg_latency,
         count(*) AS requests
  FROM log
  GROUP BY minute
  ORDER BY minute
  LIMIT 120
```

Top exception messages:

```text
level:ERROR
| SELECT exception_class,
         substr(message, 1, 160) AS message_prefix,
         count(*) AS cnt
  FROM log
  GROUP BY exception_class, message_prefix
  ORDER BY cnt DESC
  LIMIT 20
```

Status distribution:

```text
*
| SELECT status, count(*) AS cnt
  FROM log
  GROUP BY status
  ORDER BY cnt DESC
  LIMIT 20
```

## 4. Incident triage path

For “为什么报错 / 线上是否炸了 / 接口失败原因”:

1. Start with aggregate trend over the requested window.
2. Identify top endpoint / service / host / error class.
3. Drill into one representative slice with raw logs.
4. Reconstruct trace/request chronology when an id exists.
5. State probable cause only if logs support it.
6. Hand off code-level repair to `dbx-technical-plan` or implementation.

## 5. Query optimization heuristics

- Put selective indexed conditions before SQL.
- Avoid `* | SELECT ...` over long windows unless no selective field exists.
- Prefer exact fields for IDs: `trace_id`, `request_id`, `span_id`, `order_id`, `user_id`.
- Use SQL `LIMIT` for aggregate result size.
- Do not ask SLS for raw log dumps when the user wants a count, trend, or top-N.
- If field names are unknown, ask for schema/index fields or run a narrow sample query.

## 6. Output interpretation

Always distinguish:

- executed result;
- no rows returned in this scope;
- command/API failure;
- permission failure;
- query syntax failure;
- index missing or unknown;
- partial/sampled result.

Good wording:

```text
在 prod-web/nginx-access 的 2026-06-29 10:00:00 到 10:15:00 范围内，这个查询没有返回 5xx 样本。这个结论只覆盖该 Logstore、该时间窗和当前查询条件；如果 status 字段未索引或日志未采集到这里，需要继续确认。
```

Bad wording:

```text
线上没有错误。
```
