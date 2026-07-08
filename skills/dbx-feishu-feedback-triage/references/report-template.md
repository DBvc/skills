# Report Template

Default user-visible report for feedback triage.

```markdown
# <领域名> 反馈分诊报告

## 范围
- 领域：<domain_id / domain_name>
- 群：<chat name / chat_id>
- 时间：<from> 至 <to>
- 身份：user | bot
- 读取：消息 <n> 条，分析 <m> 条，跳过 <k> 条
- thread：展开 <n> 个，未展开 <n> 个
- 附件：未请求 / 已读取 / 部分失败
- 分页：complete / capped / unknown

## 总览
- 反馈 episode：<n> 个
- 已解决：<n> 个
- 可能已解决：<n> 个
- 未闭环：<n> 个
- 使用 / 配置问题：<n> 个
- 疑似 / 确认 bug：<n> 个
- 新需求 / 产品缺口：<n> 个
- 文档 / 知识库缺口：<n> 个
- 需要今天处理：<n> 个

## 需要今天处理
### 1. <case title>
- 分类：<category>，置信度：<confidence>
- 状态：<status>，置信度：<confidence>
- 严重级别：<severity>
- 模块 / owner：<module> / <owner or unknown>
- 影响：<affected users / repeated count / scope>
- 证据：<message_id>，<time>，<sender label>，<short paraphrase>
- 判断依据：<domain source or chat evidence>
- 缺口：<missing evidence>
- 下一步：<action>

## 未闭环反馈
<same compact case bullets>

## 已解决 / 可能已解决
- <case title>: <resolved/probably_resolved>, evidence, caveat.

## 新需求 / 产品缺口
- <case title>: why feature_request/product_gap, suggested handoff if needed.

## 重复 / 高频反馈
- <signature>: <count>, examples, suggested FAQ or escalation.

## 文档和知识库缺口
- <gap>: why it caused confusion, suggested target doc.

## 知识库更新候选
1. <candidate type>: <claim>
   - 来源：<evidence>
   - 置信度：<confidence>
   - 需要审批：是

## 完整性限制和不确定性
- <pagination/thread/resource/domain limitations>

## 可选后续动作
- <create project candidate later, crystallize requirement, update FAQ candidate, ask user for missing info>

## 已分析
- 领域：...
- 群：...
- 时间范围：...
- 消息：fetched / analyzed / skipped
- 写入：未写入
```

## Compact unresolved scan

```markdown
# 未闭环反馈扫描

范围：<chat>，<time range>，<domain>

## 需要跟进
1. <title> - <category/status/severity>
   - owner：<known/unknown>
   - 下一步：<action>
   - 证据：<message refs>

## 证据不足
- <title>: 缺少 <thread/attachment/domain rule/user confirmation>

## 已排除
- <duplicate/noise/resolved cases with one-line reason>
```

## Requirement intake report

```markdown
# 新需求 / 产品缺口整理

范围：...

## 明确新需求
- <title>
  - 用户想要：...
  - 当前不支持：...
  - 证据：...
  - 建议：进入 `dbx-crystallize` 澄清 scope 和验收标准

## 产品缺口
- <title>
  - 当前痛点：...
  - 不确定决策：...
  - 证据：...
  - 建议：产品判断或补充调研

## 不是需求
- <title>: 实际是使用/配置/bug，原因：...
```
