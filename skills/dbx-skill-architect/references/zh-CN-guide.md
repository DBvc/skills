# 中文使用指南

## 这个 skill 解决什么问题

`dbx-skill-architect` 用来把重复场景设计成可复用、可评估、可维护的 agent skill。它不是“提示词美化器”，也不是“把任何需求都包装成 skill 的机器”。

## 最重要的判断

先判断这件事是否值得做成 skill：

```text
是否重复？
任务目标是否稳定？
成功标准是否可评估？
是否安全、合法、尊重 consent？
skill 是否明显优于 checklist 或一次性回答？
```

如果答案不强，应该走 triage，不要硬做 full skill。

## V7 的新增重点

### Skill shape

先判断这个 skill 的主形态：流程、工具、知识、品味、决策、研究、协作、元技能，或混合型。

这不是分类游戏，而是为了决定：

```text
复杂度放在哪里？
需要 scripts 吗？
需要 references 吗？
需要 assets 吗？
需要什么 eval？
哪些自由度要收紧？
```

### Dominant failure modes

优秀 skill 的核心不是“更详细”，而是“更准确地防失败”。

常见失败包括：

```text
乱触发
上下文膨胀
领域空心
工具操作脆弱
输出不可验证
审美坍缩
安全越界
交接失败
维护漂移
```

### Patch hypothesis

优化已有 skill 时，不要凭感觉说“变好了”。每个非平凡改动都要写成假设：

```yaml
patch_hypothesis:
  target_failures: []
  proposed_change: ""
  expected_benefit: ""
  expected_cost: ""
  acceptance_tests: []
  rollback_conditions: []
```

也就是：这刀砍向哪里，怎么知道砍中了，砍歪了怎么撤。

## 输出建议

对复杂 skill 设计、评审、优化任务，开头 YAML contract 是有价值的。对纯解释型问题，不要强行展示 contract。

用户要的是交付物，不是流程烟花。结构化应该服务正确性，而不是装饰输出。
