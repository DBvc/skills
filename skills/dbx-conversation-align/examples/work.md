# Example: Component Library Refactor Disagreement

## Input

用户认为组件库需要治理/重构。对方说“别折腾了，现在能用就行”。

## Diagnosis

Scene: work decision.

Likely disagreement layer: risk weighting, not pure technical correctness.

User risk: framing it as code quality or architecture taste.

Evidence to prepare:

- repeated rework count;
- bug/hotfix history;
- duplicated logic examples;
- affected teams/components;
- estimated cost of do-nothing;
- incremental plan and rollback.

## Better response

> 我们目标一致，都是保证业务交付。分歧可能在风险权重：你更担心当前排期，我更担心后续重复返工。过去三次需求都在权限、样式覆盖和状态同步上返工。我的建议不是大重构，而是用两周治理三个高频组件，用返工次数和新增需求开发时间验证收益。不成立就停止。

## Avoid

> 你不懂，这个技术债很严重。

It turns a work tradeoff into an identity conflict.

# Example: Aggressive Product Feedback Rewrite

## Input

“这个需求又没想清楚，别天天拍脑袋改。”

## Direct-send version

> 这个需求方向我理解，但目前还缺少目标用户、成功指标和优先级依据。没有这些信息，研发侧很难评估成本和风险。建议先补齐这三点，再确认是否进入开发。

## Clearer formal version

> 当前需求信息不足以支持排期。需要补齐：目标用户、验收标准、优先级依据、影响范围。补齐前研发可以参与评估，但不建议进入开发承诺。

# Example: Deadline Pressure

## Input

业务要求增加范围但不调整时间。

## Response

> 这个变更可以评估，但它会影响原交付承诺。现在有三个选项：延期、减少其他范围，或者接受更高质量风险。我不建议默认研发直接吸收变化。我们先确认优先级和责任，再决定怎么排。
