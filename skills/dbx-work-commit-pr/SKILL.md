---
name: dbx-work-commit-pr
description: |
  用中文生成或评审工作场景的 commit message 与 PR 描述。适用于用户请求根据最终 diff、
  staged changes、working tree changes 或指定 commit 生成 `M-xxx(type): title` commit，
  以及中文合同式 PR 四块结构。只以最终变更集为事实边界，忽略聊天过程、失败尝试、
  被否决方案和临时调试。不要用于公开开源英文 PR、普通代码 review、实现任务或泛泛解释 commit 概念。
---

# Work Commit/PR Contract

生成中文工作场景的 commit message 与 PR 描述。

核心分工：

- commit 是长期证据，服务未来追溯；
- PR 是 reviewer 视角说明，服务理解、验证和评审。

不要把聊天记录写成工程事实。最终变更集才是事实边界。

## Trigger boundary

使用本 skill：

- 用户要中文工作 commit message；
- 用户要 `M-xxx(type): title` 格式；
- 用户要中文 PR 描述、合同式 PR、Proof/Risk/Review focus；
- 用户要根据最终 diff、staged changes、working tree changes、指定 commit 生成 commit + PR；
- 用户要评审或改写已有工作 PR 文案。

不要使用本 skill：

- 用户要公开开源英文 commit/PR；用 `dbx-open-source-commit-pr`；
- 用户要代码 review、技术方案评审或 bug 修复；
- 用户只是问 commit/PR 概念；
- 用户要把聊天过程、失败尝试、被否决方案、临时调试包装成长期事实。

## Source of truth

按这个优先级收集事实：

1. 最终变更集：用户提供的 diff、指定 commit、staged changes、working tree changes；
2. 用户明确提供且属于最终事实的信息：ticket、type、AI 是否参与、已执行验证；
3. 必须明确标注的不确定推断。

默认排除：

- 讨论过程；
- 失败尝试；
- 被否决方案；
- review 往返；
- 临时调试；
- “为了回应某人反馈”这类协作过程描述。

除非用户明确要求，并且这些内容确实属于最终公开记录的一部分。

## Minimal input contract

优先从最终变更获取信息。缺失时只问会影响输出正确性的最少问题：

- ticket 编号：`M-xxx`；未知时可保留 `M-xxx`，不要臆造；
- commit type：`feat|fix|inf|chore|test|docs`；不确定时基于 diff 推断或询问；
- AI 是否参与：默认写“AI 参与：有”，除非用户明确没有；
- 验证证据：命令、测试、日志、截图、手动步骤；没有就写未验证，不要编；
- 风险和 review focus：优先从最终变更推断，无法推断就少写或标缺口。

不要为了追求模板完整而盘问一长串问题。

## Workflow

1. 判断输出范围：commit only、PR only、both、review existing text。
2. 确认最终变更集。
3. 提取事实：改了什么、为什么有必要、影响面、验证、风险、AI 参与、review focus。
4. 识别是否多主题。多主题时建议拆分 commit；不强制，但要明确风险。
5. 生成 commit message。
6. 生成 PR 描述。
7. 检查 proof 是否具体，是否泄漏过程，是否把推断写成事实。
8. 如输出已保存为文件，可选运行 `scripts/check_commit_pr_output.py` 做质量门检查。

## Commit message rules

格式：

```text
M-xxx(type): {title}

{optional body}
```

规则：

- 使用中文。
- 不臆造 ticket 编号；未知时保留 `M-xxx`。
- type 从 `feat|fix|inf|chore|test|docs` 中选。
- title 写“做了什么 + 影响对象”，不要写评审动作。
- body 只写长期有价值的信息，不写临时协作过程。
- body 小节按需选用，不强行全写：
  - `Why/Context:` 最终变更或用户明确最终事实能支撑的动机；
  - `What:` 关键实现或行为变化；
  - `Proof:` 具体证据或明确未验证；
  - `Risk:` 长期有效风险与缓解；
  - `Notes:` 兼容性、迁移、行为差异。

Proof 要具体：

```text
Proof:
- 自动：pnpm lint && pnpm test
- 手动：创建订单并确认状态流转为 paid
- 未验证：未跑端到端用例
```

不要写：

```text
Proof: 已测试
Proof: 测试通过
Proof: 本地测过
```

## PR description rules

使用四块结构：

```markdown
## 做了什么/为什么
- ...

## 证明它可行
- 自动验证：...
- 手动验证：...
- 未验证：...

## 风险与 AI 参与
- 风险：...
- AI 参与：有/无，作用范围：...

## 评审关注点
- ...
```

规则：

- 第二块固定写具体证据，不能写“验证通过”。
- 完全没有验证时只写 `未验证：...`。
- 风险写给 reviewer 看：影响范围、失败方式、缓解/回滚。
- AI 参与要短，不写模型表演，不把 AI 当免责牌。
- Review focus 只选 1-2 个具体、可行动、可检查的点。
- 不复制 commit body；PR 要帮助 reviewer 快速理解和评审。

## Risk and review focus hints

从最终变更中找这些信号：

- 接口、数据结构、配置、权限、支付、计费、安全；
- 兼容性、迁移、版本依赖、灰度；
- 异常处理、边界条件、超时、重试、并发、竞态；
- 热点路径、缓存、批量规模、N+1；
- 日志、指标、告警；
- 是否可回滚，是否需要数据修复。

只写最重要的，不要把清单机械搬进 PR。

## Mixed diff rule

多主题改动时先提示：

```text
这个变更集包含多个主题，建议拆成多个 commit，原因是：...
建议拆分：
- M-xxx(type): ...
- M-xxx(type): ...
```

如果用户明确要求合并，再生成单个 commit，但要让 PR body 说明主要影响面。

## Output contract

commit only：只输出 commit title + optional body。

PR only：只输出四块 PR 描述。

both：先 commit，再 PR。

review existing text：输出问题列表 + 改写版本，不要重讲全部规则。

## Available helper script

`scripts/check_commit_pr_output.py` 可检查保存后的工作 PR 文案：

```bash
python3 scripts/check_commit_pr_output.py --artifact both --file /path/to/output.md
```

它只检查常见文字质量门，不替代最终 diff 阅读。
