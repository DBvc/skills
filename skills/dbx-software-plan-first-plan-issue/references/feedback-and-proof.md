# 反馈和证据模型

Plan-first 的任务不是“写完代码”，而是“用合适证据证明目标行为成立”。

## 反馈回路优先

在实现前明确最快可信的 pass/fail 信号：

- bug/regression：先建立可复现信号和 root-cause 句子，再修复。
- UI/visual：先锁定真实 rendered surface、viewport/state 和具体缺陷，再改动。
- backend contract：先锁定 source of truth 和系统可见语义，再实现。
- fullstack：先锁定跨层 mapping 和集成验证，再分别改 UI 和服务端。
- tooling/config：先锁定受影响命令和可重复执行路径，再修改。

## 证据类型

- **behavior proof**：用户或系统可见行为被测试、手工验证或截图证明。
- **contract proof**：API/RPC/event/schema/request/response/error/auth 语义与 source of truth 一致。
- **data/state proof**：数据写入、迁移、状态转换、缓存、幂等性、回滚被验证。
- **runtime proof**：浏览器、设备、SSR/hydration、进程、部署、任务、性能、观测影响被验证。
- **visual proof**：截图、视觉 diff、story、设计对比、viewport/state 证据。
- **manual/review-only proof**：无法程序化验证时，必须写明原因、review 目标和证据路径。

## 测试关注公共行为

优先验证 public interface 或 public behavior：

- 前端：用户可见 UI、组件 contract、route 行为、表单交互、状态转换、服务/client boundary。
- 后端：API/service contract、数据状态、权限、错误、集成路径、后台任务可见结果。
- 工具链：命令输入输出、生成产物、失败模式、CI/local 一致性。

不要为了凑测试而测试私有实现形状。

## 垂直切片

任务应该按“一个行为切片 + 一个证明信号”推进。不要先写一大片想象中的测试，再写一大片实现，也不要把实现和验证拆成两个互不闭环的 task。

## prototype 边界

原型是为了回答一个明确问题的临时代码，不是生产实现的后门。

计划必须说明：

- 原型要回答的一个问题。
- 原型位置、运行入口或查看方式。
- 可见状态、variants 或输入。
- 删除、吸收或提升为正式实现的规则。

## bug/regression root-cause gate

调试类任务在 patch 前应写出 root-cause 句子：

```text
根因：<文件/函数/条件/路径> 在 <具体输入或状态> 下导致 <观察到的症状>。
```

如果无法建立根因，任务应保持 blocked 或改为探索/诊断 gate，不要直接猜修。
