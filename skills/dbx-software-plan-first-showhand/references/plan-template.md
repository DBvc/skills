# Issue 计划

只有当 issue 已经讨论到足以执行时，才使用这个模板。
如果目标、范围、方案、验证、计划策略、影响画像、影响边界或适用的产物/证据边界仍不清楚，继续澄清，不要 seal。

## 目标

- 描述这个 issue 要达成的具体结果。

## 计划策略

- Plan Strategy: step-execution | loop-exploration | hybrid
- 选择原因：<为什么适合这个策略>

## 范围

- In-scope: <本 issue 要做什么>
- Out-of-scope: <本 issue 不做什么>

## 影响画像

- Primary: frontend | backend | fullstack | generic
- Secondary: <如无则写“无”>
- Why: <为什么这样分类>

## 影响边界

无关项可写“不适用”，相关未知项不能省略。

- Target surfaces: <目标 app/site/package/service/module/route/page/component/API/job/script/artifact>
- User/system-visible behavior: <用户或系统可观察行为>
- Contract/data/state boundary: <契约、数据、状态、权限、错误、缓存、mock/fixture 边界>
- Composition/ownership boundary: <模块、组件、服务、层级、共享抽象、所有权边界>
- Runtime/operational boundary: <浏览器、设备、SSR/hydration、进程、部署、迁移、回滚、环境、性能、观测影响>
- Content/design boundary: <文案、视觉、设计系统、品牌、内容、本地化来源；不适用则写“不适用”>
- Feedback/evidence boundary: <最快可信反馈回路、验证命令、手工 review、截图、trace、日志、报告>
- Artifact/evidence boundary: <过程产物、证据、生成文件、原型、写入边界；不适用则写“不适用”>

## 方案

- 总结实现策略。
- 点明会变化的关键文件、接口、组件、模块、服务、状态、样式、配置、脚本或系统。
- 如果存在项目原生方案、官方框架能力、平台能力或设计系统，优先使用；不用时说明原因。
- 写出最脆弱假设，以及它不成立时应该停止还是重新计划。
- bug/regression 工作：说明 root-cause proof loop。
- 视觉/UI 工作：说明 rendered surface、状态、viewport、截图或 review 证据。
- fullstack 工作：说明 contract source of truth、跨层顺序和集成验证。
- 原型工作：说明要回答的问题、临时位置、查看方式和删除/吸收规则。

## 产物和证据边界

用于 loop/hybrid、generated artifact、screenshot/trace evidence、visual baseline、prototype、import/export、batch processing、formal/destructive write 或证据本身是交付物的计划。没有独立产物或证据时写“不适用”。

- Source-of-truth refs: <真实存在的 requirement/design/contract/grounding/conversation refs 和优先级>
- Artifact paths: <产物路径，是否 committed/local/gitignored/transient/prototype-only/production source>
- Evidence paths: <截图、日志、报告、trace、run records、review artifacts，是否提交>
- State policy: <缓存、storage、数据库、临时目录、环境、cleanup、rollback>
- Validation gates: <task-local、shared、final、manual/review-only>
- Metadata/provenance: <commit、baseline、schema、fixture、design/source、viewport、browser、环境、批次信息>
- Batch/write boundary: <batch selection/size、stop/skip/retry、no-full-rerun、promotion、destructive/formal write>

## 约束

- 改动保持最小，并限制在本 issue 范围内。
- 不重写无关代码。
- 除非 issue 明确要求，否则保留现有 public/user-visible/system-visible behavior。
- 需要 source of truth 时，不发明 API、schema、design、content、permission、data 或 product semantics。
- 保护仓库中已有用户工作。未经当前回合明确批准，不要 clean、reset、stash、switch 或覆盖。

## 验收标准

- <具体用户可见或系统可见结果>
- <相关状态、交互、契约、数据、权限、错误、运行时或证据要求>
- <如何证明行为正确>

## 验证

在下面列出 issue-level reusable shared checks。每个 block 使用：

```text
检查: <id>
命令: <shell>
备注: <可选说明>
```

这里只放 task-safe checks，也就是在无关任务尚未完成前仍应通过的检查。没有 shared check 时留空。

示例：

```text
检查: fast
命令: <项目原生验证命令>
备注: 可被多个任务复用的快速检查
```

## 最终验证

在下面 fenced `sh` block 中，每行列出一个 issue-level final validation command。
`scripts/issue-workflow.sh review-ready <issue-id>` 只会在当前任务是最后一个未完成任务时执行这个 block。

对 documentation-only、design-only、prototype-only 或 manual-review-only issue，用一个且仅一个 marker comment 替代可执行命令：

```sh
# 无程序化验证: <原因>
```

```sh
echo "替换为项目最终验证命令"
```

## 风险 / 备注

- <已知风险、follow-up、假设或用户需要 review 的内容>
