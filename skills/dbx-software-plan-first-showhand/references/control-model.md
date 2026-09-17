# Software Plan-First 控制模型

这套技能不是某种技术栈知识库，而是一个工作流控制器。它的目的不是告诉 agent “怎么写前端/后端代码”，而是防止 agent 在缺少边界、证据和 source of truth 时直接实现。

## 核心不变量

1. **先收敛，再实现**  
   目标、范围、方案、验证、影响画像、影响边界不完整时，不进入实现。

2. **按需 grounding，再写计划**
   需要仓库事实时，必须通过只读 grounding 确认项目规则、路径、命令、契约和验证方式；如果当前上下文或用户确认已经提供足够事实，可以直接进入 finalize。

3. **计划文件是执行契约**  
   `plan.md` 和 `tasks.md` 一旦 seal，不允许实现阶段静默改写。发现计划错误时，停止并重新 finalize/reseal。

4. **任务按顺序 review-gated 执行**  
   每次只执行 `tasks.md` 中第一个未完成任务。进入 implement phase 时脚本先封存不可重置的 repo HEAD、task-start Git baseline 和机器可读 allowed/required target paths。代码型 task 必须在验证前已经产生 scope 内、命中 required target 的可归因实现 delta；验证前证据冻结后，验证命令不得改变 HEAD、index 或 Git 可见 workspace。`review-ready` 生成已验证快照，`complete` 只能完成这个已 review 的任务。

5. **证据绑定完成声明**  
   不能只说“完成了”。必须记录验证命令、review-only 原因、变更文件和证据路径。

6. **Git 是适配器，不是工作流本体**  
   提交风格、是否自动提交、以及计划文档是否提升为可提交项目文档由 `.plan-first/config.toml` 控制。默认 `.plan-first/issues/<issue-id>/` 是本地 workflow 状态，不进入 task commit；显式 `plan_docs.mode = "tracked"` 时，只提交同步到项目文档路径的 `plan.md` 和 `tasks.md`。工作流完整性由 seal、root marker 和完整 review snapshot 保证。

7. **文档验收不等于可开工，但两者之间只有一次有界 preflight**
   当前 bundle receipt 必须复用。实现阶段只检查当前 task、seal、scope、验证和权限；没有新的矛盾证据时，不得重开通用 plan review。

## 主要失败模式

- 需求未收敛就进入仓库实现。
- 把某个路径、框架、命令、契约或设计规则当成“应该是这样”。
- 为了让实现通过而临时发明 API、字段、错误语义、UI 状态、数据迁移或部署假设。
- 只验证 happy path，不验证失败、边界、权限、异步、回归或系统可见影响。
- 把用户已有工作、未提交改动、生成产物或临时原型混入提交。
- 在 local 模式下把 commit message 指向 `.plan-first/` 本地过程文件，导致长期提交记录引用失效。
- `tasks.md` 被手动改写，导致 review 的任务和 complete 的任务不是同一个。
- showhand 在不适合自动化的高主观、高风险或 source-of-truth 缺失任务上一路执行。
- 把 phase entry gate 误读成每次必须跑满所有阶段，或反过来在证据门未满足时跳到 seal / implement。
- 把已通过的文档验收当成重新 full review 的理由，导致永远到不了第一个代码切片。
- 让验证命令、提前 commit、scope 外文件或无代码 task 的生产 delta 冒充可归因实现证据。

## 控制面

- **Activation Control**：只在需要 plan-first 的软件工程任务上触发。
- **State Control**：状态由 `plan.md`、`tasks.md`、`.plan-first` seal、sealed repo HEAD、机器可读 task scope、task-start baseline、验证前实现快照、review snapshot 和证据文件维护。
- **Trajectory Control**：强制按证据门推进：决策未收敛先 `plan-issue`，需要仓库事实先 `ground-plan`，完整决策和必要证据后才能 `finalize-plan`，sealed task 后才能 `implement-feature -> review/complete`。入口可以跳过已满足的上游阶段，但不能跳过证据门。
- **Execution Control**：任务只能按顺序执行，不能跳 task，不能静默改计划。
- **Completion Control**：`step` / `loop-batch` 的完成声明必须绑定验证前已有、完全位于 allowed scope 且命中全部 required targets 的实现 delta，以及真实程序化验证成功；`gate` / `promote` / `documentation-only` 只允许零 Git 可见实现 delta 完成。
- **Evolution Control**：通过 evals、配置边界和项目规则文档避免技能漂移。
