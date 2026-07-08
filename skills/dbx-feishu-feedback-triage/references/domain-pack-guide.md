# Domain Pack Guide

A domain pack is the swappable business-knowledge layer used by `dbx-feishu-feedback-triage`.

The generic skill should work across feedback groups. The domain pack tells it what the domain means.

## Design principle

Do not create a product encyclopedia. Create a triage knowledge pack.

Only include knowledge that helps answer:

- What module or surface is this feedback about?
- Is this existing behavior, misuse/config, suspected bug, confirmed bug, feature request, product gap, or documentation gap?
- What source is authoritative for the claim?
- What status can be safely inferred?
- What evidence is missing?
- What should be suggested as next action?

## Recommended Feishu Wiki structure

```text
业务反馈分诊知识库 / <domain name>
  00. Domain Profile
  01. Source Map
  02. Glossary
  03. Module / Owner / Keyword Map
  04. Business Rules and Boundaries
  05. FAQ
  06. Known Issues and Workarounds
  07. Classification Examples
  08. Memory Update Candidates
  09. Historical Reports
```

## 00. Domain Profile

The entry document. Keep it compact.

Required fields:

```yaml
domain_id: "trade-system"
domain_name: "交易系统"
timezone: "Asia/Shanghai"
scope:
  includes: []
  excludes: []
default_chats:
  - name: "交易系统业务反馈群"
    chat_id: "oc_xxx"
    purpose: "daily business feedback"
knowledge_sources:
  source_map: "feishu_doc_url"
  faq: "feishu_doc_url"
  known_issues: "feishu_doc_url"
  business_rules: "feishu_doc_url"
  module_map: "feishu_doc_url"
memory_policy:
  accepted_memory: "feishu_doc_url"
  candidate_memory: "feishu_doc_url"
  write_mode: "candidate_only"
report_profile:
  default_window: "yesterday 00:00-23:59"
  audience: "研发 / 产品 / 支持"
  output_language: "zh-CN"
```

## 01. Source Map

Source Map says where to look and how much to trust each source.

Recommended source hierarchy:

```text
P0 official docs, release notes, accepted business rules
P1 code behavior when actual implementation must be verified
P2 accepted FAQ, known issues, support playbooks
P3 current bounded chat evidence
P4 historical chat memory
P5 model inference
```

Chat is high authority for symptoms and user confirmation. Chat is low authority for durable product facts unless confirmed elsewhere.

## 02. Glossary

Only include terms that may cause misclassification.

Example:

```markdown
## 商户
业务含义：...
常见别名：客户、门店、租户
容易混淆：不是飞书租户
反馈判断：涉及商户不可见时，优先检查权限、数据同步、租户范围。
```

## 03. Module / Owner / Keyword Map

This is often the highest-value file.

```yaml
modules:
  order-export:
    name: "订单导出"
    owners:
      product: "张三"
      frontend: "李四"
      backend: "王五"
    keywords:
      - "导出"
      - "订单导出"
      - "导出字段"
      - "下载失败"
    common_error_codes:
      - "ORDER_EXPORT_403"
      - "ORDER_EXPORT_TIMEOUT"
    triage_hints:
      likely_misuse:
        - "没有 order.export 权限"
      likely_bug:
        - "有权限但按钮不展示"
      likely_feature_request:
        - "希望新增导出字段"
```

## 04. Business Rules and Boundaries

Write rules in feedback-decision form, not product-manual form.

Good:

```markdown
## 订单导出
当前能力：支持单租户导出，不支持跨租户导出。
使用前提：需要 order.export 权限。
判为使用/配置问题：无权限、未选择租户、时间范围超出限制。
判为疑似 bug：有权限且合法范围，仍然返回 500 或按钮不展示。
判为新需求：希望跨租户导出、希望增加字段、希望定时导出。
需要产品确认：导出字段是否应该默认包含成本价。
```

Bad:

```markdown
订单导出是一个方便用户导出订单的功能。
```

## 05. FAQ

FAQ entries should include conditions and escalation triggers.

```markdown
## 看不到导出按钮
分类倾向：misuse_or_config / data_or_permission_issue
判断条件：用户缺少 order.export 权限。
处理建议：检查角色和权限配置。
升级为 suspected_bug：用户有权限但按钮仍不可见。
证据来源：权限说明文档。
```

## 06. Known Issues and Workarounds

Known issue entries require explicit source and freshness.

```yaml
known_issue:
  id: "KI-20260708-001"
  title: "订单导出偶发超时"
  status: active | fixed | stale | unknown
  affected_versions: []
  symptoms: []
  workaround: "缩小时间范围后重试"
  owner: ""
  source: "doc/release/message id"
  stale_policy: "下次发布后复查"
```

## 07. Classification Examples

Examples calibrate the model better than abstract rules.

```yaml
examples:
  - input_summary: "用户说看不到导出按钮，产品提醒需要开权限，用户确认好了"
    expected_category: "misuse_or_config"
    expected_status: "resolved"
    reason: "权限规则 + 用户确认"
  - input_summary: "用户希望导出新增字段，当前系统不支持"
    expected_category: "feature_request"
    expected_status: "pending_pm"
    reason: "不是已有能力失效"
```

## Codex bootstrap guidance

Use `assets/codex-domain-bootstrap.prompt.md` when asking Codex to inspect a codebase. Tell Codex to produce a triage pack, not a full project encyclopedia.

Review Codex output before moving it into accepted memory. Code-derived conclusions should say whether they reflect current implementation, intended behavior, or low-confidence inference.
