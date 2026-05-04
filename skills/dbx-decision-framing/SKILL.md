---
name: dbx-decision-framing
description: 当用户面对高影响、不确定、有真实行动后果的决策，需要在多个选项或 go/no-go 之间取舍时使用。适用于职业去留、技术架构、产品方向、团队组织、生活迁移、投资框架等。先做门禁，再决定 full_decision、quick_decision、clarification、direct_answer 或 safety_redirect。不要用于单纯概念解释、翻译润色、机械代码、一次性写作、低风险日常小事或没有行动后果的泛泛分析。
---

# 决策框架技能

## 0. 最高优先级：先分支，后分析

这个技能不是“思维模型大全”，也不是“把任何问题都分析得很长”。

它只服务于一种任务：**在真实决策里，把模糊问题转成可比较、可行动、可复盘的判断**。

每次看到用户请求，先做分支判断：

```text
full_decision      高价值、信息足够支持暂定判断，需要完整决策分析
quick_decision     低到中等价值、有取舍但不值得长篇分析
clarification      高价值决策，但缺少会翻转结论的阻塞信息，必须先问问题
direct_answer      不是决策任务，只是解释、翻译、写作、代码或事实查询
safety_redirect    请求包含违法、隐私侵犯、操控、医疗/法律/投资确定性承诺等风险
```

**不要因为用户说“帮我分析”“用第一性原理”“用系统思维”“做个决策分析”，就自动进入完整决策框架。**

## 1. 硬门禁

只有以下条件基本成立时，才允许进入 `full_decision`：

1. **真实决策**：用户确实要选择、取舍、推进、暂停、拒绝、迁移、投入或重新设计。
2. **存在选项**：至少有两个可行选项，或一个明确的 go/no-go 判断。
3. **有实际代价**：选择会影响时间、金钱、机会、关系、风险、长期路径或组织资源。
4. **输出能改变行动**：分析结果能改变下一步、验证方式、优先级、投入规模或停止条件。
5. **安全边界可控**：不要求违法、侵犯隐私、操控他人、医疗/法律/投资确定性承诺。
6. **信息足够支持暂定判断**：已知信息足以给出有边界的建议；仍可列出非阻塞缺口。

如果第 1 到 5 条基本通过，但缺少会直接翻转结论的阻塞信息，进入 `clarification`，不要直接给结论。

阻塞信息和非阻塞信息要分开：

- **阻塞信息**：没有它就会把建议从 A 翻成 B，例如目标完全未知、风险承受度未知且代价不可逆、选项本身不清楚。
- **非阻塞信息**：会影响置信度、执行细节或验证动作，但不妨碍给出暂定建议。把它写进 `missing_information`，继续 `full_decision`。
- 技术架构、团队组织、生活迁移这类问题，如果用户已经给出主要痛点和候选方向，通常可以进入 `full_decision`，以 medium/low confidence 输出暂定路径和验证动作。

如果第 1 到 4 条明显不通过，进入 `direct_answer` 或 `quick_decision`，不要输出完整决策备忘录。

如果第 5 条不通过，进入 `safety_redirect`，拒绝不当部分并给安全替代路径。

诊断类请求不是默认决策：如果用户只是问“为什么低效”“用系统思维分析原因”“帮我理解现象”，但没有要求在多个行动方案中取舍、是否推进/停止/重构/迁移，进入 `direct_answer`，给轻量结构化分析，不输出 YAML。只有当用户明确要决定怎么改、先改哪个、要不要取消/投入时，才进入 `quick_decision` 或 `full_decision`。

## 2. 五个分支的强制输出规则

### 2.1 full_decision

适用：高影响、有代价、多选项或 go/no-go，且信息足够支持暂定判断。

**必须先输出 fenced YAML 边界块，然后使用标准输出契约。**

`full_decision` 必须完整保留标准输出契约里的所有二级标题。即使置信度是 low，也不能漏掉“已知事实 / 假设 / 判断”“关键目标和约束”“关键思维方式”等段落；如果这些段落不值得展开，通常说明应该选择 `quick_decision` 或 `clarification`。

### 2.2 quick_decision

适用：有一点取舍，但低风险、低成本、可逆，或用户明确要快速判断。

**必须先输出 fenced YAML 边界块，但只能使用 quick 模板。不要复用标准/深度契约。**

quick 输出最长建议 6 到 10 个短 bullet，不要包含完整的事实/假设/判断表、方案大表、深度备忘录。

### 2.3 clarification

适用：看起来是高价值决策，但缺少会改变结论的阻塞信息。

**必须先输出 fenced YAML 边界块，然后只问 1 到 3 个阻塞问题并停止。**

clarification 模式禁止直接给推荐，例如“你应该选 A”“我建议你读/不读”“直接拆/不拆”。可以给一句“为什么这些问题会改变判断”。

解释问题为什么重要时，不要写“如果目标是 X，可能值得；如果目标是 Y，可能不值得”这类提前分支建议。只说明哪些变量会翻转结论，不要提前模拟结论。

### 2.4 direct_answer

适用：概念解释、事实查询、翻译、润色、机械代码、普通写作、原因诊断。直接回答，不输出 YAML，不套决策框架。

### 2.5 safety_redirect

适用：请求涉及违法、隐私侵犯、操控他人、监控、医疗/法律/投资确定性承诺等。

**必须先输出 fenced YAML 边界块，然后拒绝不当部分，转为安全、非操控、可验证的替代方案。即使开头是拒绝，也不能省略 YAML。**

YAML 后必须逐字使用两个二级标题：`## 不能按原请求执行` 和 `## 安全替代方向`。不要用普通段落替代固定标题，也不要只写安全建议而省略明确拒绝。

## 3. YAML 边界块

除 `direct_answer` 外，`full_decision`、`quick_decision`、`clarification`、`safety_redirect` 的第一段必须是以下 fenced YAML：

```yaml
decision_framing:
  mode: full_decision | quick_decision | clarification | safety_redirect
  gates:
    real_decision: pass | fail | unknown
    options_or_go_no_go: pass | fail | unknown
    meaningful_stakes: pass | fail | unknown
    action_change_possible: pass | fail | unknown
    safety_ok: pass | fail | unknown
    enough_context: pass | fail | unknown
  decision_type: career | technical_architecture | product | organization | finance_framework | life | relationship | other | not_applicable
  missing_information: []
  assumptions: []
  confidence: high | medium | low
  output_depth: quick | standard | deep | none
```

分支约束：

- 完整决策必须写 `mode: full_decision`；前五个 gates 应为 `pass`，`enough_context` 不能是 `fail`。可以有非阻塞 `missing_information`。
- 快速决策必须写 `mode: quick_decision`；`meaningful_stakes` 通常是 `fail` 或 `unknown`，`output_depth` 必须是 `quick`。
- 信息不足必须写 `mode: clarification`；`enough_context` 必须是 `fail` 或 `unknown`，`missing_information` 必须列出具体阻塞缺口。
- 安全重定向必须写 `mode: safety_redirect`；`safety_ok` 必须是 `fail`，第一段仍然必须是 YAML。

## 4. 工作流

1. **门禁和分支**：先决定 full、quick、clarification、direct 或 safety。
2. **重定义问题**：把表面问题改写成真正要决策的对象。
3. **分离类型**：区分事实、假设、判断、目标、约束、风险、未知。
4. **明确成功标准**：说明什么结果算好，不只是“感觉更好”。
5. **列出可行选项**：不要只分析用户已经偏好的单一方案。
6. **选择少数关键 lens**：只用 2 到 5 个真正改变判断的思维方式。
7. **比较收益、代价、风险、可逆性和机会成本。**
8. **给出推荐和置信度**：结论强度不能超过证据强度。
9. **给出最小验证动作**：让用户知道下一步怎么降低不确定性。
10. **写出反证条件和复盘点**：什么证据会推翻当前建议，什么时候回看。

## 5. 标准输出契约：full_decision

```markdown
## 结论

- 推荐：
- 置信度：high / medium / low
- 当前建议成立的前提：
- 不建议直接做的事：

## 我对问题的重新定义

- 表面问题：
- 真实决策：
- 成功标准：
- 非目标：

## 已知事实 / 假设 / 判断

| 类型 | 内容 | 依据 | 置信度 |
|---|---|---|---|
| 事实 |  |  | high/medium/low |
| 假设 |  |  | high/medium/low |
| 判断 |  |  | high/medium/low |

## 关键目标和约束

- 目标：
- 时间范围：
- 资源约束：
- 风险承受度：
- 不可逆因素：
- 利益相关方：
- 关键未知：

## 可选方案比较

| 方案 | 收益 | 代价 | 主要风险 | 可逆性 | 适合条件 |
|---|---|---|---|---|---|

## 关键思维方式

| Lens | 为什么选它 | 它如何改变判断 |
|---|---|---|

## 推荐路径

- 先做：
- 暂缓：
- 不做：
- 最小验证动作：
- 需要补充的信息：

## 风险、反证和复盘

- 最大风险：
- 最容易被低估的风险：
- 什么证据会推翻当前建议：
- 何时复盘：
```

## 6. quick_decision 专用模板

`quick_decision` 只能使用这个短模板，不要输出标准契约。

```markdown
## 快速建议

- 推荐：
- 置信度：high / medium / low
- 一句话理由：

## 关键取舍

1.
2.
3.

## 下一步

- 先做：
- 需要确认：
- 什么情况要改判断：
```

## 7. clarification 专用模板

`clarification` 只能问阻塞问题，不要提前给结论。

```markdown
## 先确认 1 到 3 个关键信息

1.
2.
3.

这些问题会影响判断，因为：
```

最后一句只能解释“哪些信息会改变判断”，不要写条件式推荐。

## 8. safety_redirect 专用模板

`safety_redirect` 必须先输出 YAML，再逐字使用这个模板里的两个标题。不要直接从“我不能……”开始，也不要把拒绝和替代方案揉成普通段落。

```markdown
## 不能按原请求执行

- 原因：
- 我不能帮助的部分：

## 安全替代方向

- 可以改成：
- 建议下一步：
```

## 9. 不要做什么

- 不要机械罗列很多思维模型。
- 不要把“听起来聪明”的模型当作结论。
- 不要只输出正反方长列表，却不给行动建议。
- 不要把假设写成事实。
- 不要把低风险小事写成深度决策备忘录。
- 不要在 clarification 模式提前给强建议。
- 不要因为有非阻塞缺口就放弃给出暂定建议。
- 不要在证据不足时给出确定性承诺。
- 不要在投资、医疗、法律、心理、关系等高风险领域给越界建议。
- 不要用操控性话术帮助用户控制、试探、监控他人。

## 10. 关键原则

### 10.1 先表征，后判断

先把问题表示成：目标、选项、约束、证据、假设、风险、时间范围、利益相关方。不要直接跳到“我觉得应该选 A”。

### 10.2 类型不能混

事实不是假设。愿望不是约束。结果不是原因。短期情绪不是长期价值。单次反馈不是稳定规律。

### 10.3 结论不超过证据

证据只支持到哪里，结论就写到哪里。必要时使用：已确认事实、高概率判断、弱推断、当前未知。

### 10.4 选择 lens，不堆 lens

每个被选中的思维方式都必须回答：**它如何改变当前判断？** 如果一个模型没有改变取舍、风险识别或下一步，就不要使用。

### 10.5 高风险先降自由度

涉及不可逆、高成本、外部专业领域或他人权益时，优先输出：边界、风险、验证、咨询专业人士、低风险试验，而不是直接给强建议。

### 10.6 好建议必须可执行、可复盘

每个重要建议都应包含：下一步、停止条件、复盘触发条件、反证条件。

## 11. Reference 加载规则

按需读取，不要一次性读取所有 reference。

- 需要选择思维方式：读 `references/model-catalog.md`。
- 需要领域适配：读 `references/domain-adapters.md`。
- 需要输出格式：读 `references/output-contracts.md`。
- 需要看完整示例：读 `references/worked-examples.md`。

## 12. 高风险领域边界

### 投资 / 财务

可以提供决策框架、风险预算、资产负债匹配、回撤约束、再平衡原则。不要承诺收益，不要把单个产品当作完整答案，不要替代持牌金融顾问。

### 医疗 / 法律 / 税务

可以帮助整理问题、风险、待确认事项和咨询专业人士的问题清单。不要提供确定诊断、法律结论或合规承诺。

### 关系 / 家庭

不要读心，不要把对方意图写成事实，不要提供操控、监控、诱导、试探或侵犯隐私的策略。应该转为沟通、边界、价值冲突和不确定性澄清。

### 职业 / 团队

不要只给鸡血或泛泛建议。必须考虑个人优势、机会成本、下行风险、可逆性、长期复利和现实约束。

## 13. 结束前自检

输出前快速检查：

```yaml
contract_self_check:
  branch_selected_before_analysis: true | false
  required_yaml_present_when_needed: true | false | not_applicable
  quick_not_overbuilt: true | false | not_applicable
  clarification_stopped_after_questions: true | false | not_applicable
  safety_redirect_yaml_first: true | false | not_applicable
  safety_redirect_required_headings: true | false | not_applicable
  full_contract_complete: true | false | not_applicable
  diagnosis_not_overtriggered: true | false | not_applicable
  facts_assumptions_judgments_separated: true | false | not_applicable
  conclusion_bounded_by_evidence: true | false
  risks_and_counterevidence_included: true | false | not_applicable
  minimal_next_action_present: true | false | not_applicable
  high_stakes_boundary_handled: true | false | not_applicable
```

不要把这个自检写成长篇解释。若发现 `false`，先修正输出。
