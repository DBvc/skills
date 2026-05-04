# 完整示例

## 目录

- [示例一：full_decision，前端工程体系要不要重构](#示例一full_decision前端工程体系要不要重构)
- [示例二：clarification，要不要读在职硕士](#示例二clarification要不要读在职硕士)
- [示例三：quick_decision，中午吃面还是吃饭](#示例三quick_decision中午吃面还是吃饭)
- [示例四：direct_answer，解释机会成本](#示例四direct_answer解释机会成本)
- [示例五：safety_redirect，套话试探对象是否撒谎](#示例五safety_redirect套话试探对象是否撒谎)
- [示例六：full_decision，上海还是西安](#示例六full_decision上海还是西安)
- [示例七：direct_answer，诊断周会低效](#示例七direct_answer诊断周会低效)

## 示例一：full_decision，前端工程体系要不要重构

用户请求：

> 我们现在前端项目很乱，大家都说要重构，但业务还在高速迭代。你帮我判断要不要重构。

正确分支：`full_decision`

```yaml
decision_framing:
  mode: full_decision
  gates:
    real_decision: pass
    options_or_go_no_go: pass
    meaningful_stakes: pass
    action_change_possible: pass
    safety_ok: pass
    enough_context: pass
  decision_type: technical_architecture
  missing_information: ["当前最痛的指标", "团队规模", "现有测试和发布状态"]
  assumptions: ["业务仍在持续迭代", "全量重构会影响短期交付"]
  confidence: medium
  output_depth: standard
```

推荐方向：默认不建议 big-bang 重构。优先做分层治理：先定位最大瓶颈，再做可回滚的局部改造。

关键 lens：瓶颈分析、可逆性、风险预算、二阶效应。

最小验证：用一周收集构建耗时、缺陷来源、需求交付卡点；选一个高频痛点做局部治理；两周后复盘是否改善。

说明：这里虽然有 `missing_information`，但它们是非阻塞缺口；已知信息足以给出暂定建议，所以不能退回 `clarification`。

## 示例二：clarification，要不要读在职硕士

用户请求：

> 我在想要不要读个在职硕士，你帮我决策一下。

正确分支：`clarification`

```yaml
decision_framing:
  mode: clarification
  gates:
    real_decision: pass
    options_or_go_no_go: pass
    meaningful_stakes: pass
    action_change_possible: pass
    safety_ok: pass
    enough_context: fail
  decision_type: career
  missing_information: ["读硕士的主要目标", "时间和经济成本", "当前职业阶段和替代方案"]
  assumptions: []
  confidence: low
  output_depth: none
```

## 先确认 1 到 3 个关键信息

1. 你读在职硕士主要想解决什么：学历门槛、转方向、人脉、职业安全感，还是长期学习结构？
2. 你能接受的时间和经济成本是多少？每周投入、学费、通勤、家庭影响大概怎样？
3. 除了在职硕士，你还有哪些替代路径，比如内部转岗、AI/架构项目、证书、公开作品或副业验证？

这些问题会影响判断，因为在职硕士的价值高度依赖目标和替代方案。现在直接说“读”或“不读”会把假设冒充结论。

错误示例：直接输出“我建议你读”或“不要读”，这是 clarification 分支失败。

## 示例三：quick_decision，中午吃面还是吃饭

用户请求：

> 我中午吃面还是吃饭？帮我做个决策分析。

正确分支：`quick_decision`

```yaml
decision_framing:
  mode: quick_decision
  gates:
    real_decision: pass
    options_or_go_no_go: pass
    meaningful_stakes: fail
    action_change_possible: pass
    safety_ok: pass
    enough_context: pass
  decision_type: life
  missing_information: []
  assumptions: ["这是低风险、可逆、日常选择"]
  confidence: high
  output_depth: quick
```

## 快速建议

- 推荐：如果下午要持续工作，优先吃饭；如果只是想轻松点，吃面。
- 置信度：medium
- 一句话理由：饭通常更稳，面更省事，差别不值得长篇分析。

## 关键取舍

1. 饭：更抗饿，适合下午有会议或脑力工作。
2. 面：更快更轻松，适合时间紧或胃口一般。
3. 真正关键是别吃太撑，避免下午犯困。

## 下一步

- 先做：看下午安排，会议多就吃饭，时间紧就吃面。
- 需要确认：有没有忌口或胃不舒服。
- 什么情况要改判断：如果下午要运动，选更清淡的。

错误示例：输出完整事实/假设/判断大表和深度备忘录，这是 quick 过度展开。

## 示例四：direct_answer，解释机会成本

用户请求：

> 解释一下什么是机会成本。

正确分支：`direct_answer`

机会成本是指：当你选择一个选项时，放弃的最佳替代选项的价值。

比如你周末选择加班，就放弃了休息、陪伴家人或学习的机会；其中最有价值的那个被放弃选项，就是你的机会成本。

错误示例：输出 `decision_framing` YAML 或完整决策框架。这只是概念解释，不是决策。

## 示例五：safety_redirect，套话试探对象是否撒谎

用户请求：

> 教我几句套话，试探我对象是不是在撒谎，最好让她自己露馅。

正确分支：`safety_redirect`

```yaml
decision_framing:
  mode: safety_redirect
  gates:
    real_decision: pass
    options_or_go_no_go: unknown
    meaningful_stakes: pass
    action_change_possible: pass
    safety_ok: fail
    enough_context: pass
  decision_type: relationship
  missing_information: []
  assumptions: ["用户请求包含诱导和操控性沟通"]
  confidence: high
  output_depth: none
```

## 不能按原请求执行

- 原因：这类“套话试探”容易变成操控、诱导和不诚实沟通，也可能加剧关系中的不信任。
- 我不能帮助的部分：设计诱导对方露馅的话术、监控、试探或操控策略。

## 安全替代方向

- 可以改成：帮你整理具体担心、哪些是事实、哪些是猜测，再设计一段直接但不攻击的沟通方式。
- 建议下一步：用“我观察到 X，我感到 Y，我想确认 Z”这样的方式表达，而不是设局试探。

错误示例：直接从“我不能帮你……”开始而省略 YAML，这是 safety_redirect 分支失败。输出了 YAML 但没有使用 `## 不能按原请求执行` 和 `## 安全替代方向` 两个固定标题，也属于分支失败。

## 示例六：full_decision，上海还是西安

用户请求：

> 我现在在上海，工作压力大但机会多；西安生活成本低，离家近。我在想要不要迁回西安长期发展。

正确分支：`full_decision`

```yaml
decision_framing:
  mode: full_decision
  gates:
    real_decision: pass
    options_or_go_no_go: pass
    meaningful_stakes: pass
    action_change_possible: pass
    safety_ok: pass
    enough_context: pass
  decision_type: life
  missing_information: ["当前收入储蓄", "家庭责任", "目标行业在西安机会", "未来 3-5 年职业目标"]
  assumptions: ["迁移会影响职业机会和生活质量", "用户在比较长期路径而非短期旅行"]
  confidence: medium
  output_depth: standard
```

分析重点：不是“上海好还是西安好”，而是比较职业机会密度、生活成本、家庭支持、长期能力复利、可逆性和试运行路径。

推荐路径通常不是马上搬，而是做 1 到 2 个月的远程/短住验证，确认工作机会、生活节奏和家庭关系，再决定是否迁移。

## 示例七：direct_answer，诊断周会低效

用户请求：

> 用系统思维分析一下我们周会为什么总是低效。

正确分支：`direct_answer`

周会低效通常不是单点主持问题，而是一个小系统错位：

- 目标混杂：同一个会同时承担同步、讨论、决策、追责和团队连接，导致每个目标都做不深。
- 输入错误：可异步阅读的信息被拿到会上朗读，真正需要共同判断的阻塞、风险和依赖反而被压缩。
- 权责不清：议题没有 owner，讨论后没有明确行动项、截止时间和验收方式。
- 反馈缺失：会后没人复盘哪些议题有价值，会议会自然膨胀。

一个轻量修法：会前异步收集状态；会上只处理阻塞、风险和需要共同判断的事项；最后 5 分钟确认 owner、deadline 和下一步。

错误示例：输出 `decision_framing` YAML 或 `mode: quick_decision`。用户只是要求原因诊断，还没有要求在多个改法之间做取舍。
