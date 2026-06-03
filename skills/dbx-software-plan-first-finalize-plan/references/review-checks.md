# Review 检查清单

review 时按影响画像选择相关项目，不要机械套用全部检查。

## 通用

- Goal、Scope、Approach 和当前 task 是否一致。
- 是否只改了当前 task 允许的 surface。
- 是否保护了用户已有 worktree 改动。
- 是否遵守项目规则文档和 source of truth。
- 是否有清晰的验证结果或 review-only 原因。
- 是否没有静默扩展 scope、发明契约、发明设计或发明数据。

## frontend 相关

- 目标 rendered surface 是否正确。
- 相关 UI states/interactions 是否覆盖。
- API/data/mock/fixture 边界是否清楚。
- 可访问性、焦点、键盘、语义、响应式、浏览器或 hydration 影响是否按相关性验证。
- 视觉、文案、设计来源是否来自项目或用户确认。
- 证据是否能证明用户可见行为。

## backend 相关

- contract、权限、校验、错误、幂等性、副作用是否清楚。
- 数据状态、迁移、事务、缓存、后台任务、外部集成是否按相关性验证。
- 兼容性、回滚、部署、观测和运维影响是否进入计划。
- 测试是否覆盖系统可见语义，而不是只覆盖内部实现。

## fullstack 相关

- 前后端 contract source of truth 是否一致。
- request/response/error/auth/permission mapping 是否明确。
- mock/fixture 是否与真实服务端行为一致或有明确生命周期。
- 跨层集成验证是否足够。
- rollout、兼容性和回滚顺序是否清楚。

## generic 相关

- 工具链、配置、脚本、文档和 CI/local 命令是否一致。
- 生成产物是否与 source-of-truth 区分。
- lockfile、缓存、构建输出和发布影响是否按相关性验证。
