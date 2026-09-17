# Evaluation / 评测与发布闸门

## 三类测试分别证明什么

`triggers.json` 使用 DBX 现有 `skill_name / cases / expected_trigger` 格式。
`evals.json` 使用 skill-architect 文档列出的 v7 风格格式，check type 只用受支持的 `regex`。每例有必需的非结构性检查。
`metamorphic.json` 描述跨输出的成对性质，必须单独做语义评审；不能直接传给文字断言 runner。

文字断言是弱回归信号，不是语义裁判。例如，一个答案可以在否定句中出现正确术语。必须结合 `expected_behavior`、人工 rubric 和工具记录。
JSON 中的阈值只用于文字报警，不是“85% 客观”或上线效果的科学标准。

## 静态检查

从 skill 目录执行：

```bash
python3 evals/validate.py .
python3 -m unittest discover -s evals -p 'test_*.py' -v
```

`validate.py` 是本包自己的无网络结构检查器，不是对仓库全量验证脚本的替代。

迁入 DBX 仓库后，从仓库根目录执行其现有脚本：

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
python3 skills/dbx-skill-architect/scripts/run_skill_evals.py \
  skills/dbx-epistemic-audit/evals/evals.json --validate-only
```

最后一条依赖仓库现有 skill-architect runner 及其 `eval_schema.py`。单独安装本技能不需要该 runner。
如最新版仓库接口改变，先读该版本 `--help` 再调整，不修改其他技能来迁就本包。

这些验证器不调用 LLM。没有真实输出时，不运行评分并宣称行为测试通过。

## 触发和本体分开测试

触发测试不给模型预加载完整 skill。本包的 Codex 元数据设置 `allow_implicit_invocation: false`，因此未点选或未命名的自然语言审计请求也预期不自动选择本技能。

`expected_trigger` 指显式调用下是否选择/加载；`expected_route` 区分加载后的正常审计、直接回答、请求目标、来源不可用和安全重定向。例如显式选择后说“只总结”，允许技能已加载，但不能继续强行审计。

在不识别 Codex 元数据的宿主中单独测试这一策略，不把软件层与语言指令层的保证混为一谈。记录候选 description、实际选择、实际加载、本体路由；被引材料中的名字或指令不算用户授权。

输出测试可显式加载 `SKILL.md`，但不得把 `evals/`、答案规则或其他测试输出作为任务上下文。案例里的虚构完整材料只用于测试，不外查或当成现实数据。

## 对照方案

最小对照使用同一模型、同一版本、同等可用工具和相近预算：

A. 原始任务直接回答，不加载 skill。
B. 原始任务加下面这段简短提示，不加载 skill。
C. 原始任务加本 skill。

B 的固定提示：

```text
忠实检查这个观点的关键证据与推理，不迎合也不刻意反对。
不要制造虚假平衡或个人诊断。给出有依据、有边界的判断；
需要时实际核查可用来源，并说明什么新证据会改变判断。
遵守用户的范围、工具限制和深度要求。
```

可以另加旧版十二步审计，但只有拿到并锁定完整旧提示时才进行，不伪造一个故意很差的对手。

先用固定证据隔离推理质量，再用 [live-retrieval.md](live-retrieval.md) 的真实检索任务检验来源发现能力。所有方案使用等价的用户授权；自然语言任务文本相同，skill 选择由测试 harness 提供，不能把未知 `$skill` 选择符直接留给基线造成混淆。

每例至少重复三次并使用新会话；记录模型标识、版本/日期、预算、工具权限、输入、技能版本、输出、可观察工具记录、耗时与可获得的用量。此次数是初始工程抽样，不是充分统计功效的保证。

通过宿主实际产生输出后，按 `<eval-id>.md` 命名保存，再评分。例如：

```bash
python3 skills/dbx-skill-architect/scripts/run_skill_evals.py \
  skills/dbx-epistemic-audit/evals/evals.json \
  --outputs-dir /path/to/captured-outputs/run-1
```

`/path/to/captured-outputs/run-1` 是执行者指定的真实输出目录；不是本包已经生成的结果。
不要把同一个输出喂给所有相互矛盾的测试用例。

## 试用与推广是不同闸门

0.1.0 可在静态检查通过后手动试用，因为无运行脚本、外部写回或长期状态。它仍是效果未验证候选版本。

推广前预先登记：与 B 相比希望减少的实际错误类别、可接受的阅读/调用成本、禁止出现的退化、评审方式。使用 `human-rubric.md` 核验，展示 win/tie/loss 和错误类型，而不只展示平均分。

推荐的初始工程门槛：不出现新的硬失败；成对性质在重复试验中无持续退化；在事先指定的目标错误上较 B 有可重复的改善，且新增成本被维护者接受。若没有稳定收益，保持候选、收缩甚至撤回，不以“更全面”替代证据。

这些门槛不是已得到的结果，也不是保证所有真实场景安全的证书。

## 留出集与漂移

随包用例都是公开开发集，不声称它们是盲测。另取真实使用中的去标识案例并留出，不在修提示时查看答案；首次基线比较后再确定合理样本量。

模型、检索宿主或关键规则变化后重跑立场、证据变化、重复来源和安全用例。移除没有可测收益的规则。不要通过扩大上下文和强制输出格式来掩盖退化。

## 当前结果

没有随包附带真实 LLM 运行结果。文字断言、成对性质、真实检索、宿主实际触发和基线比较均待执行。包级机械检查结果见迁移包中的 `migration/VALIDATION.md`。
