---
name: dbx-software-plan-first-ground-plan
description: Manual trigger only. Use only when the user explicitly names `dbx-software-plan-first-ground-plan`, `$dbx-software-plan-first-ground-plan`, or asks to manually trigger this exact DBX Software Plan-First read-only grounding phase. Do not auto-trigger for ordinary repo reading, fact checking, plan writing, or implementation requests.
---

# DBX Software Plan-First Ground Plan

## DBX repository notes

- This repository uses the `dbx-` prefix for stable skills; use the prefixed skill names in handoffs and cross-skill routing.
- Keep this phase self-contained: load only the required references for the active phase, and do not pull sibling skill files unless the workflow explicitly hands off to that phase.

## Manual Trigger

- Manual trigger only.
- Use only when the user explicitly names `dbx-software-plan-first-ground-plan`, `$dbx-software-plan-first-ground-plan`, or says to use/trigger this exact skill.
- Do not auto-trigger for ordinary repo reading, fact checking, grounding, or plan-first requests.

用于在写计划前只读确认项目事实。适用于前端、后端、全栈和通用软件项目。

## 语义

- 只读仓库，不修改代码，不写 `plan.md` 或 `tasks.md`。
- 不替用户做产品、设计、contract 或范围决策。
- 项目事实来自仓库文件、项目规则、CI、manifest、schema、design/spec 文档、现有代码和用户确认。
- 只输出 grounding handoff，供 `finalize-plan` 写计划。
- 所有沟通和 handoff 使用中文。

## 必须读取

- `references/output-format.md`
- `references/control-model.md`
- `references/impact-profiles.md`
- `references/config.md`

## 可执行脚本

可以运行只读扫描：

```sh
python3 scripts/repo_context.py
```

该脚本只输出 hints，不是最终事实。必须读取相关文件确认。

## Grounding 重点

- 查找项目规则：`.plan-first/rules.md`、`AGENTS.md`、README、CONTRIBUTING、架构文档、CI、测试文档。
- 确认目标 surface：app/site/package/service/module/route/page/component/API/job/script/artifact。
- 确认 module/directory ownership：新增或迁移产物应靠近哪个 feature、domain、service、shared layer、test area 或 doc area；如果项目规则没有证据，明确标为未知，不猜路径。
- 确认 source of truth：API schema、GraphQL/protobuf/OpenAPI、数据库 schema、设计文档、现有 handler/client、测试 fixture、产品文案或用户当前确认。
- 确认可用验证：项目原生命令、测试层级、browser/manual/visual/review-only 证据。
- 识别 generated/protected/deprecated 文件和不要触碰的区域。
- 识别是否应该是 frontend、backend、fullstack 或 generic profile。

## 禁止事项

- 不做实现。
- 不写计划文件。
- 不修改配置或锁文件。
- 不把扫描器 hints 当成事实。
- 不发明缺失的 contract、设计、文案、数据或验证方式。

## 输出

使用 `grounding-handoff` 格式。
