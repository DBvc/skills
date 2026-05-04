# Work Communication Evidence Preparation

Use before technical, product, delivery, quality, staffing, or ownership disputes. Good work communication is not only tone; it needs evidence.

## Evidence checklist

| Category | Examples |
|---|---|
| Incidents | bugs, outages, hotfixes, repeated support issues, missed handoffs |
| Frequency | how often it happened, over what period, trend |
| Impact | delay, rework, customer pain, team load, risk exposure |
| Scope | affected modules, teams, customers, workflows |
| Root pattern | duplication, unclear ownership, fragile API, missing tests, ambiguous requirements |
| Options | do nothing, minimal fix, incremental plan, full plan |
| Tradeoff | cost, time, risk reduction, opportunity cost |
| Validation | metric, timebox, owner, rollback, review point |

## Technical debt framing

Bad framing:

> 这个代码太烂了，必须重构。

Better framing:

> 过去三次需求都在同一类问题上返工：权限、样式覆盖、状态同步。我的判断是这已经从代码洁癖变成交付风险。建议先做两周小范围治理，用返工次数和新增需求开发时间验证收益。

## Demand change framing

> 当前变更会影响已承诺范围。我们可以做三件事之一：调整上线时间、砍掉部分范围，或接受质量/风险代价。建议先确认优先级，而不是默认研发直接吸收变化。

## Decision note template

> 背景：X。  
> 目标：Y。  
> 现状风险：A/B/C。  
> 证据：过去 N 次出现 M 问题，影响 Z。  
> 选项：1/2/3。  
> 推荐：选择 2，因为它在当前约束下风险最低。  
> 验证：到 D 日期看指标 K，不成立则回退。
