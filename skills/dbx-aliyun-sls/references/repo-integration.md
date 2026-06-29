# Repository Integration Snippets for dbx-aliyun-sls

This file is not required at runtime. It gives copy-paste snippets for repository-level docs after adding `skills/dbx-aliyun-sls/`.

## README Stable Skills row

```markdown
[`dbx-aliyun-sls`](skills/dbx-aliyun-sls) 阿里云 Simple Log Service / SLS 只读日志查询控制器：通过 Aliyun CLI、GetLogsV2、SDK 或可观测 MCP 安全生成、执行、总结日志查询，内置凭证、时间范围、成本、隐私和 handoff 护栏。Read-only Alibaba Cloud SLS log query controller with CLI/API/MCP execution boundaries.
```

## DBX_SKILL_INDEX.md row

```markdown
| `dbx-aliyun-sls` | Read-only Alibaba Cloud SLS / Log Service query controller for safe query generation, bounded execution, result summarization, incident drill-down, and Agent workflow integration. | tool + procedure + knowledge + safety | L4 | External CLI/API behavior can drift; credentials and log privacy are high-risk; broad queries may cost money or leak sensitive data. | Use for Alibaba Cloud SLS/Logstore query tasks; route code fixes to `dbx-technical-plan`, raw local/pasted logs to direct log analysis or `dbx-read`, cloud administration to a separate explicit admin skill, and product/design/review tasks to matching DBX skills. | Add real trigger evals from first 10 production query sessions; keep CLI wrapper aligned with current `aliyun sls get-logs-v2`. |
```

## DBX_ROUTING_MATRIX.md primary intent row

```markdown
| Query, generate, optimize, execute, summarize, or diagnose Alibaba Cloud SLS / Log Service / Logstore logs through Aliyun CLI, GetLogsV2, SDK, or Observability MCP | `dbx-aliyun-sls` | `dbx-technical-plan` after logs reveal a code change; `dbx-read` or direct answer for non-SLS log files; explicit cloud-admin workflow for SLS mutations; refuse credential exfiltration or unauthorized access. |
```

## DBX_ROUTING_MATRIX.md chaining rule

```markdown
### Alibaba Cloud SLS log querying
Use `dbx-aliyun-sls` when the task depends on Alibaba Cloud SLS/Logstore data. It owns target/time/query/cost/privacy gates and read-only execution. It may hand off to `dbx-technical-plan` when logs identify a code or architecture change, or to implementation only after the user explicitly asks for code changes. Do not use it for generic local logs, direct cloud resource mutation, credential capture, or broad production exports.
```

## README local checks note

````markdown
For `dbx-aliyun-sls`, runtime checks require a local Aliyun CLI installation and SLS plugin when executing queries:

```bash
python3 skills/dbx-aliyun-sls/scripts/check_runtime.py
```
````
