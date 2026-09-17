# Design decision / 0.1.0 设计复核

## Go / no-go

判断：可以开始制作可手动试用的候选技能；没有需要用户先决策才能落地的阻塞项。
尚未确认的是净效果，而不是任务是否存在。净效果必须靠比较，不能靠继续讨论被证明。

任务：对明确观点/论证或用户主动提供的来源样本，实施有界、可追溯、会影响判断的关键检验。
非目标：诊断用户、长期认知治疗、算法推荐治理、改变用户价值排序、替人作出行动决定。

```yaml
skill_shape:
  primary: research
  secondary: [decision, procedure]
  dominant_failure_modes:
    - stance_following
    - reflexive_contrarianism
    - unsupported_inference
    - source_double_counting
    - personal_diagnosis
    - ceremonial_overanalysis
  implementation_implication: compact obligations plus conditional evidence checks and substantive evals
control_surfaces:
  activation: strong_manual_first
  intent: light_claim_scope
  state: strong_evidence_provenance
  trajectory: adaptive_checks_and_stop_conditions
  execution: host_tools_only
  completion: bounded_judgment_and_update_conditions
  evolution: baseline_and_metamorphic_tests
state_contract:
  required: false
  lifetime: single_task
  writes_to: []
  persistent_belief_profile: false
skill_value:
  baseline: direct_answer_and_strong_short_prompt
  expected_gain: fewer_material_evidence_and_inference_errors
  added_cost: [skill_context, optional_references, relevant_retrieval]
  added_risk: [overcontrol, false_balance, evaluator_bias, premature_stopping]
  status: plausible_but_unmeasured
```

上面是维护设计记录，不是普通用户每次必须看到的输出。

## 本轮落实的修正

1. 只控制 Agent 的取证与判断行为，不把用户的信念当成可直接控制、可诊断对象。
2. 先做轻量覆盖检查，再聚焦关键支点，防止挑最容易的反例而遗漏真正重要的问题。
3. 强反方不是必选栏目；检验的结论可以与用户相同，已解决的问题允许结束。
4. 事实、因果、预测、价值、体验使用不同证据义务；缺证据与已反证分开。
5. 以任务边界、取证记录和更新条件判定完成，不以字数或思想变化判定完成。
6. 手动调用与只读无状态减少邻接技能冲突；未来是否开放隐式触发单独评测。
7. 结构检查、文字断言、语义判断、因果净效果四层证据分别记录。

## 为什么不加更多系统

不加数据库、搜索供应商绑定、信念账本、立场画像、自动推荐修改或三角色辩论。它们没有被当前任务证明必要，增加权限、配置和评价成本。

不创造新 ASCT 控制面。这里需要的是任务专属 Success 定义，而非扩展理论核心。证据规则不等于已经验证的因果机制。

## 关键失败预案

若相对强简短提示没有稳定收益：压缩为 mini-skill 或命令。
若减少迎合却增加抬杠/虚假平衡：移除触发该行为的规则，不增加“更多反方”。
若来源检索是瓶颈：改进证据接入，不继续堆叠思维模型。
若简单题成本失控：缩短运行内核、收窄触发，不牺牲重要题的证据标准。
若多次在同一价值争议上替用户作主：将该失败加入回归集，并停止相关自动化用途。

## 来源使用边界

设计参考 DBX 当前仓库的结构/评测规则与 ASCT 价值函数；外部格式参考可访问的 OpenAI 技能文档。
用户提供的特定 `rethinking-skills-and-prompts-for-gpt-6-astra` 博客 URL 本轮无法重新获取，因此没有将上一轮对该文的转述写成已验证原文事实。
源文件与抓取边界见迁移包 `migration/SOURCE_LOCK.json`。不复制未经核实的模型效果或官方文章论断。
