# Software Plan-First 控制模型

这套技能不是某种技术栈知识库，而是一个工作流控制器。它的目的不是告诉 agent “怎么写前端/后端代码”，而是防止 agent 在缺少边界、证据和 source of truth 时直接实现。

## 核心不变量

1. **先收敛，再实现**  
   目标、范围、方案、验证、影响画像、影响边界不完整时，不进入实现。

2. **先 grounding，再写计划**  
   需要仓库事实时，必须通过只读 grounding 确认项目规则、路径、命令、契约和验证方式。

3. **计划文件是执行契约**  
   `plan.md` 和 `tasks.md` 一旦 seal，不允许实现阶段静默改写。发现计划错误时，停止并重新 finalize/reseal。

4. **任务按顺序 review-gated 执行**  
   每次只执行 `tasks.md` 中第一个未完成任务。`review-ready` 生成已验证快照，`complete` 只能完成这个已 review 的任务。

5. **证据绑定完成声明**  
   不能只说“完成了”。必须记录验证命令、review-only 原因、变更文件和证据路径。

6. **Git 是适配器，不是工作流本体**  
   提交风格、是否自动提交、计划文件是否进入仓库由 `.plan-first/config.toml` 控制。工作流完整性由 seal 和 review snapshot 保证。

## 主要失败模式

- 需求未收敛就进入仓库实现。
- 把某个路径、框架、命令、契约或设计规则当成“应该是这样”。
- 为了让实现通过而临时发明 API、字段、错误语义、UI 状态、数据迁移或部署假设。
- 只验证 happy path，不验证失败、边界、权限、异步、回归或系统可见影响。
- 把用户已有工作、未提交改动、生成产物或临时原型混入提交。
- `tasks.md` 被手动改写，导致 review 的任务和 complete 的任务不是同一个。
- showhand 在不适合自动化的高主观、高风险或 source-of-truth 缺失任务上一路执行。

## 控制面

- **Activation Control**：只在需要 plan-first 的软件工程任务上触发。
- **State Control**：状态由 `plan.md`、`tasks.md`、`.plan-first` seal、review snapshot 和证据文件维护。
- **Trajectory Control**：强制 `plan-issue -> ground-plan -> finalize-plan -> implement-feature -> review/complete`。
- **Execution Control**：任务只能按顺序执行，不能跳 task，不能静默改计划。
- **Completion Control**：完成声明必须绑定验证结果和证据。
- **Evolution Control**：通过 evals、配置边界和项目规则文档避免技能漂移。
