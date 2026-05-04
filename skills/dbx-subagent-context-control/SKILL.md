---
name: dbx-subagent-context-control
description: Codex 专用的 subagent 上下文控制辅助技能。Use when 用户要求使用 Codex subagent delegation、Codex worker/explorer delegation、并行 review、独立 reviewer、隔离上下文、不要带上下文、fork_context=false，或把 review/dbx-linus-review/waza-check/plan-eng-review 等技能交给 Codex subagent 执行时。默认新开 Codex subagent 不继承父线程历史，只传最小任务摘要；只有用户明确要求继承父线程时才使用 fork_context=true。不要因为用户讨论业务代码里的 worker、browser worker、架构 explorer 概念而触发。
---

# Subagent Context Control

这个 skill 只约束 Codex 的 subagent 使用方式。不要把它泛化到 Claude、Cursor、Gemini CLI 或其他工具；其他工具的子代理上下文语义未知。

它是辅助 skill，不替代 review、dbx-linus-review、waza-check、plan-eng-review 等任务技能。使用方式是“本 skill + 其他任务 skill”：本 skill 管 subagent 怎么开、带多少上下文、是否复用；其他 skill 管具体怎么审、怎么查、怎么判断。

## When not to use

不要在这些情况使用本 skill：

- 用户只是讨论业务代码里的 worker、browser worker、任务调度 worker 或架构里的 explorer 概念。
- 用户明确说“你自己看”“不用搞复杂”“不要开 subagent”。
- 当前任务不需要 Codex subagent、并行 reviewer、上下文隔离或子任务委派。

## Hard gates

开 Codex subagent 前先过这几个门槛：

- 任务确实需要委派，不能只是为了显得更复杂。
- 能写出明确 scope、背景摘要、输出格式和停止条件。
- `fork_context=false` 时能给出不丢关键设计取舍的摘要。
- `fork_context=true` 只有在用户明确要求继承完整父线程历史时使用。

## IR

把委派请求先拆成这个中间表示：

```yaml
subagent_context_ir:
  task_goal: ""
  context_mode: "fork_context=false | fork_context=true"
  scope: []
  background_summary: []
  constraints: []
  output_contract: ""
  reuse_decision: "new | reuse_once | do_not_use_subagent"
  model_policy: "inherit_current | explicit_lightweight | user_specified"
```

不要混淆这些类型：父线程历史、任务本地背景摘要、review scope、模型选择、旧 subagent 复用理由。

## Workflow

1. 先判断是否真的需要 Codex subagent。
2. 如果需要，决定 `fork_context=false` 还是 `fork_context=true`。
3. 写出 3-8 行背景摘要，复杂技术方案最多 10 行。
4. 给每个 subagent 一个清晰 scope、约束和输出格式。
5. 父线程合并结果，去重，处理冲突，不把一个 reviewer 的结论泄漏给另一个独立 reviewer。

## Output contract

实际使用 subagent 时，面向用户的说明只需要包含：

- 开几个 Codex subagent
- 每个是否 `fork_context=false`
- 是否复用旧 subagent
- 背景摘要会控制在几行内
- 如果使用 `fork_context=true`，说明原因

没有使用 subagent 时，不输出这份 contract，直接完成原任务。

## Eval guidance

修改本 skill 后，至少验证这些回归场景：默认 `fork_context=false`、显式 `fork_context=true`、业务 worker 不误触发、用户要求自己看时不提 subagent、review 缺背景时先补背景、Cursor 边界不能泛化。

## 默认规则

新开 Codex subagent 时，默认使用 `fork_context=false`。

如果用户明确说“你自己看”“不用搞复杂”“不要开 subagent”，就不要开 subagent。此时直接处理原任务；除非用户正在问 subagent 策略，否则不要解释 `fork_context`、不要说“没有开 subagent”、也不要提这个 skill。

只有用户明确要求“继承父线程历史”“带完整上下文”“沿用这条主线程的全部讨论”时，才使用 `fork_context=true`。如果决定使用 `fork_context=true`，先在过程说明里写明理由。

开 subagent 前，先向用户说明本次上下文模式：

- `fork_context=false`：不继承父线程聊天历史，只给任务本地摘要。
- `fork_context=true`：继承父线程聊天历史，只用于强依赖前文推理链的任务。

## 最小任务摘要

使用 `fork_context=false` 时，只传必要信息：

- 任务目标
- 文件、diff、日志或数据范围
- 相关约束
- 3-8 行必要背景摘要
- 期望输出格式
- 停止条件或不要做什么

其中“必要背景摘要”不能省略。即使是只读 review，也要至少写 3-8 行背景，说明这次改动要解决什么、已经确定的技术取舍、明确不评审的范围、用户最关心的风险。

不要传整段聊天记录、长日志、完整文档、完整设计讨论、父线程推理过程，除非用户明确要求。

复杂技术方案可以写到 10 行。超过 10 行时，先压缩成摘要；如果压缩会丢掉关键设计取舍，再考虑 `fork_context=true` 或先向用户确认。

如果暂时无法可靠摘要背景，先在父线程补读相关文件或向用户确认；不要把缺背景的 review 直接扔给 subagent。

## Review 用法

当用户要求用多个 review 技能配合 subagent 时：

- 每个 reviewer 新开独立 subagent，默认 `fork_context=false`。
- 每个 subagent 只绑定一个 review 视角或一个技能。
- prompt 里写清楚 review 范围、基准分支或 diff、输出格式。
- 要求 findings 按严重程度排序，尽量给文件和行号。
- 父线程负责合并结论、去重、判断冲突，不把一个 subagent 的结论泄漏给另一个独立 reviewer。

给 subagent 的 brief 推荐使用这个骨架，按任务补齐即可，不要在面向用户的回复里整段展开：

```text
Use $review-skill as an independent Codex subagent.
Context mode: fork_context=false.
Scope: <files or diff>.
Background summary: <3-8 lines: goal, key decisions, non-goals, main risks>.
Output: concrete findings ordered by severity, with file/line evidence when possible.
Constraint: do not assume access to the parent thread history.
```

## 复用规则

只在同一范围、同一问题、同一 subagent 自己上一轮 finding 的一次复核中复用已有 subagent。

出现下面任一情况时，新开 `fork_context=false` subagent：

- review 范围变了
- 任务类型变了
- 已经复核过一轮
- 用户要独立第二意见
- 旧 subagent 已经积累了很多假设
- 需要避免前一轮结论影响判断

`resume_agent` 只用于继续同一件未完成的事。不要为了省事把新任务塞进旧 subagent。

## 模型选择

如果 `spawn_agent` 不显式传 `model`，Codex 会使用当前会话/配置的默认模型。不要把“省略 model”误解成用户主动选择了某个模型。

模型选择应跟任务难度匹配：

- review、架构判断、安全风险、复杂代码审查：默认不降级，通常直接继承当前强模型。
- 文件扫描、日志归类、简单复核：可以考虑轻量模型，但要明确这是为了成本和速度，不要牺牲判断质量。
- 用户指定模型时，按用户要求执行。

如果任务是多路 review，除非用户明确要求省成本，否则不要把 reviewer 自动降到轻量模型。

## 语气和长度

面向用户的过程说明和最终回复默认使用中文，保持短、硬、明确。

不要把内部 subagent brief、完整模板、长检查表直接摊给用户，除非用户明确要求看完整 prompt。用户要求或你实际决定使用 subagent 时，通常只说明：

- 开不开 subagent
- 用 `fork_context=false` 还是 `fork_context=true`
- 是否复用旧 subagent
- 给 subagent 的背景会控制在几行内
- 为什么这样做

避免把回复写成管理汇报腔。少用“落地、闭环、对齐、收口、接住、补一刀”等词；能说具体动作时，就说具体动作。

## 输出要求

父线程最终回复要说明：

- 开了几个 subagent
- 每个 subagent 是否使用 `fork_context=false`
- 是否复用了旧 subagent
- 如果使用 `fork_context=true`，说明原因

优先用 3-6 行说明。只有在用户要求审计、复盘或查看 prompt 时，才展开完整 brief。

如果没有开 subagent，也不需要提这个 skill 或 subagent 机制，直接完成原任务。
