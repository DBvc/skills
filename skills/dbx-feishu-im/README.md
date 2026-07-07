# dbx-feishu-im

`dbx-feishu-im` is a Feishu/Lark IM control skill for bounded chat evidence and safe IM writes in development workflows.

Use it for:

- finding group chats, DMs, message IDs, or thread IDs;
- reading bounded chat history and search results;
- summarizing decisions, blockers, action items, risks, and incident timelines from chat evidence;
- expanding thread replies or reading message resources when needed;
- preparing confirmed sends, replies, reactions, pins, urgent notifications, or chat/member changes;
- consuming short, bounded realtime IM events for experiments;
- feeding chat evidence into `dbx-feishu-workflow`.

## Not for

- Feishu Project / Meegle work item changes: use `dbx-feishu-project`.
- Feishu Docx / Wiki document editing: use `dbx-feishu-doc`.
- Cross-system project/doc synchronization: use `dbx-feishu-workflow`, with this skill only as chat evidence collection.
- Unbounded monitoring or broad chat scans.

## Backend

The default backend is the official CLI:

```bash
lark-cli im --help
lark-cli event --help
```

This package currently ships no helper scripts. Use official CLI/MCP operations directly and keep reads bounded.

## Local checks

From the repository root:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

## Example prompts

```text
读一下“研发排期群”今天关于灰度发布的讨论，按决策/阻塞/owner 总结，带消息证据。

搜一下飞书群里最近一周包含 trace_id=abc123 的消息，看看事故排查链路。

展开这个 thread，判断最后的结论是什么，不要写回任何地方。

根据刚才的群消息证据，草拟一条回复给群里，我确认后再发。

监听一次 im.message.receive_v1 事件，最多 1 条或 30 秒，输出脱敏后的结构。
```

## Safety posture

The skill is read-only by default. External writes, chat administration, urgent notifications, and cross-system writes require exact target, exact content/change, identity choice, and explicit confirmation.
