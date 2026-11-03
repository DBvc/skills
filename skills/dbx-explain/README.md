# dbx-explain · 讲明白

轻量的中文表达技能，用于复杂概念解释、方案分析、改写和工程汇报。

## 用法

```text
$dbx-explain 为什么接口返回“已接收”不能叫“任务已完成”？
$dbx-explain 把下面的交接说明改得清楚一些，保留负责人、时间和未完成事项。
```

默认只作用于当前任务。明确要求“讲清楚”“说人话”或指出难懂时可隐式匹配；
仅介绍、评审技能名称不表示启用。没有设成永久生效的全局风格。

需要手动专用时，可把 `agents/openai.yaml` 的 `policy.allow_implicit_invocation` 改为 `false`。
这不会影响显式 `$dbx-explain` 调用。该手动策略未做宿主实测。

## 与其他 DBX 技能组合

本技能只改善面向用户的表达，不替代研究、学习、评审、实现和验证流程。
`dbx-learn` 仍负责学习目标与练习，`dbx-write` 仍负责文章，
`dbx-read` 仍负责来源读取，`dbx-diff-review` 仍负责范围和证据。
任务技能要求的严重性、证据和结论不能因压缩而删除。

## 设计与作用范围

这是按需加载的轻量表达技能：同一类难懂、冗长或失真的解释会反复出现，
可通过事实保留、因果完整和读者复述来评估；不增加运行时工具或全局规则。

```yaml
skill_shape:
  primary: taste
  secondary: [interaction_mode]
  dominant_failure_modes: [wrong_trigger, taste_collapse, unverified_output]
  implementation_implication: "正文保持精简；使用边界放在路由与用例中，质量判断使用独立语义评分。"
state_contract:
  state_type: interaction_mode
  reads_from: [current_task, user_requested_scope]
  writes_to: []
  owner: user
  lifetime: "当前任务；只有用户明确要求时延续到指定范围。"
  rollback: "用户要求停止时立即退出；不写入全局配置或持久记忆。"
```

## 版本与证据

包版本：0.1.0-preview，2026-11-03。
正文沿用留存实验中的 `ours-v2`，只把 frontmatter 名称改为 `dbx-explain`。
没有按最终测试题继续调规则。正文为24行左右，无运行时工具、额外词典或必读参考文件。

旧记录包含174份回答，但只有最终6题直接测试了v2，不能说v2通过了174题。
留存匿名评分未显示v2胜过Humanizer或简短提示；四道普通题的平均输出较短。
这是候选版本，不是已证明跨模型最优或已验证真人理解率的版本。

本次交付重新核算旧输出和评分并检查安装包，没有启动新一轮独立模型生成。
重命名后的触发行为、Codex真实加载、多轮持续性和与其他技能组合仍待运行验证。
评测材料放在 `evals/`，不属于每次使用都应加载的正文。

## 仓库迁移与验证

2026-11-03 迁入候选区，保留原包 `SKILL.md` 正文内容和 `agents/openai.yaml`；
仅移除 `SKILL.md` 末尾多余空行以通过提交格式检查。
修复输出评测与现有 runner 的兼容性：`interaction` 改为 `behavior`，
`calibration` 改为 `validation`，断言内容不变。
补充原样输出负例、评审结果组合用例，以及阅读／学习／文章写作的触发边界。
当前共 14 条输出用例、13 条触发用例；新增用例均未生成模型答案。

这些修改只保证可检查和边界明确，不代表表达质量已经提升。
如果组合测试发现事实遗漏或误触发，应停用候选技能，再据失败样例修改。
原包 `evaluation/` 与 `tools/` 是历史交付附件，未迁入运行时包；
上文历史实验数字是原交付记录的说明，不是本仓库重新生成或独立评分的结果。
迁移时核对了原包 19 个文件的 SHA-256，原包离线检查 26 项、辅助测试 8 项通过。

在仓库根目录运行已有工具：

```bash
python3 scripts/validate_skills.py --root . --fail-on-warnings
python3 scripts/run_trigger_evals.py --root . --validate-only
python3 skills/dbx-skill-architect/scripts/run_skill_evals.py skills/dbx-explain/evals/evals.json --validate-only
python3 scripts/skill_inventory.py --root . --format markdown
```

前两项检查结构及触发用例格式，第三项只检查输出用例格式；都不调用模型。
输出用例中的字符串检查只是烟雾检查，语义通过仍须按 `evals/rubric.md` 逐项核对。
迁移不自动安装、不修改全局配置、不提交或推送。

仓库路径是 `skills/dbx-explain/`；Codex自动发现的本地路径是 `.agents/skills/dbx-explain/`
或 `~/.agents/skills/dbx-explain/`。仅放入普通 `skills/` 目录不等于已安装到Codex。
