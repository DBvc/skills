# 中文使用指南

这个 skill 的目标不是“帮你把任何 prompt 包装成 skill”，而是判断一个场景是否值得沉淀成可复用、可评测、可维护的 skill。

v5 的核心变化：

1. 用 `mode / route / operation` 拆开“用户要做什么”“是否创建 skill”“本次具体执行什么动作”。
2. full skill 创建必须通过硬门槛：重复性、稳定任务、可评测、安全合法。
3. near-miss 默认不做完整 skill，例如一次性提示词、一次性写作、泛泛总结、隐私侵犯。
4. improve 模式默认 patch，不默认重写。
5. eval 模式必须区分 runner-compatible JSON 和 human rubric。
6. 每次都必须先输出 YAML contract，防止 agent 边想边飘。

推荐使用方式：

- 想创建 skill：先给场景、输入例子、成功标准、失败模式。
- 想评审 skill：提供 SKILL.md 和 evals.json。
- 想改进 skill：说明失败 case 和目标改动，默认让它 patch。
- 想设计 eval：明确要 runner JSON、human rubric，还是 both。
