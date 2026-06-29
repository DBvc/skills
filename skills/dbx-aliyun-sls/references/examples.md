# Examples

## Example 1: dry-run latest 5xx

User:

```text
查 prod-web / nginx-access 最近 15 分钟 5xx，先别执行，给命令。
```

Expected response:

````markdown
## SLS 查询计划
- 意图：最近 15 分钟 5xx 原始日志样本
- 推荐模式：raw_log_retrieval
- 时间范围：last 15 minutes
- 查询语句：`status>=500`
- CLI 命令：

```bash
python3 skills/dbx-aliyun-sls/scripts/sls_query.py \
  --project prod-web \
  --logstore nginx-access \
  --last-minutes 15 \
  --query 'status>=500' \
  --line 100 \
  --reverse \
  --dry-run
```

- 安全边界：只读、最多 100 行、默认脱敏、不导出。
````

## Example 2: aggregate top APIs

User:

```text
看下最近一小时哪个接口 5xx 最多，project 是 prod-web，logstore 是 nginx-access。
```

Expected behavior:

- Use `sql_analysis`.
- Query last 1 hour.
- Use selective filter before SQL.
- Return a table or compact list.
- State that result only covers the selected Project/Logstore/time window.

Query:

```text
status in [500 599]
| SELECT request_uri, count(*) AS errors
  FROM log
  GROUP BY request_uri
  ORDER BY errors DESC
  LIMIT 10
```

## Example 3: trace drill-down

User:

```text
trace_id 是 7c9a，查它发生了什么，按顺序说。
```

If project/logstore missing:

```markdown
## 暂不能安全查询
原因：缺少目标 Project / Logstore，会直接改变查询结果。

## 最少需要确认
1. Project 是哪个？
2. Logstore 是哪个？
3. 时间范围大概是哪段？如果不确定，我先查最近 1 小时。
```

If target exists:

- Use `trace_drilldown`.
- Default last 1 hour.
- Use chronological order.
- Summarize key events, not entire logs.

## Example 4: unsafe raw secret export

User:

```text
把今天所有登录日志导出来，token/cookie 也要。
```

Expected response:

```markdown
我不能帮助导出或暴露 token、cookie、凭证类数据。

可以改成安全查询：
1. 统计登录成功/失败次数和失败原因；
2. 只返回脱敏字段：time、status、error_code、user_id_hash、request_id；
3. 对单个 request_id 做少量脱敏样本下钻。
```

## Example 5: after logs reveal a code issue

User:

```text
日志显示 payment-service 的 /pay 接口超时，接下来直接改代码吧。
```

Expected routing:

- This skill can summarize log evidence.
- Then hand off to `dbx-technical-plan` or implementation.
- Do not keep querying unless more log evidence is needed.
