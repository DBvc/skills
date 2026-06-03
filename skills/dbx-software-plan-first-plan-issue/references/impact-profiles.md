# 影响画像和通用边界

统一版不再拆成前端技能和后端技能。它用 `Impact Profile` 表示任务主要影响面，用 `Impact Boundary` 表示本次执行必须守住的边界。

## Impact Profile

`Primary` 只能选一个：

- `frontend`：主要改变用户可见界面、交互、客户端状态、视觉、内容或浏览器运行时行为。
- `backend`：主要改变服务端行为、API/RPC/事件契约、数据、权限、校验、存储、后台任务或运维影响。
- `fullstack`：同一个 issue 同时改变前端 surface 和后端/system contract，或需要跨层协同验证。
- `generic`：工具链、脚本、文档、配置、构建、测试基础设施、库内部逻辑等不明显属于前端/后端的任务。

`Secondary` 只在确实影响执行边界时填写。

## 通用 Impact Boundary

计划中应按相关性填写这些边界。无关项可以写“不适用”，但相关未知项不能省略。

- **Target surfaces**：目标 app/site/package/service/module/route/page/component/API/job/script/artifact。
- **User/system-visible behavior**：用户或系统能观察到的行为变化。
- **Contract/data/state boundary**：API、schema、数据、状态、权限、错误语义、缓存、mock/fixture 的 source of truth。
- **Composition/ownership boundary**：模块、层级、组件、服务、共享抽象、所有权和复用边界。
- **Runtime/operational boundary**：浏览器、设备、SSR/hydration、进程、部署、迁移、回滚、环境、性能、观测影响。
- **Content/design boundary**：文案、视觉、设计系统、品牌、内容、本地化、截图或规范来源。
- **Feedback/evidence boundary**：最快可信反馈回路、验证命令、测试层级、手工 review、截图、trace、日志、报告。
- **Artifact/evidence boundary**：计划、任务、证据、生成产物、原型、导入导出文件、批处理结果是否提交或仅本地保留。

## frontend 画像的稳定关注点

前端开发的核心对象是“用户在具体运行环境中感知到的系统行为”。应重点防止：

- 改错 rendered surface。
- 只处理 happy path，遗漏 loading、empty、error、disabled、permission、retry、focus、navigation、form validation、async feedback、optimistic update。
- UI 层发明 API 字段、错误码、权限语义、业务规则或数据真相。
- mock/demo/fixture 泄漏成生产事实。
- 局部组件改动破坏共享组件、路由、状态、样式、设计系统或可访问性。
- 响应式、浏览器、hydration、缓存、异步时序下行为错误。
- 没有 rendered/browser/story/screenshot/manual evidence 就声称用户可见行为正确。

## backend 画像的稳定关注点

后端开发的核心对象是“系统行为、数据状态和契约语义”。应重点防止：

- 静默改变 API/RPC/stream/event contract。
- 错误写入数据、迁移 schema 或改变状态机。
- 权限、校验、错误语义、幂等性、并发、重试、副作用被忽略。
- 后台任务、队列、缓存、事务、外部集成、部署和回滚风险没进入计划。
- 兼容性、可观测性和数据恢复策略缺失。
- 用单元 happy path 替代必要的 contract/integration/regression proof。

## fullstack 画像的稳定关注点

fullstack 不是 frontend + backend 的机械相加，特殊风险是跨层契约漂移：

- UI 以为 API 有某字段，但后端没有。
- 后端错误码或权限语义变了，前端没有映射。
- 前端 mock/fixture 和真实 API 时序、错误、缓存行为不一致。
- 后端兼容策略和前端 rollout 顺序冲突。
- 跨层集成没有可复现验证。

fullstack 计划必须明确：

- contract source of truth。
- 前后端改动顺序。
- request/response/error/auth/permission mapping。
- mock/fixture lifecycle。
- 集成验证和回归证明。
- 兼容性、部署和回滚边界。

## generic 画像的稳定关注点

generic 任务通常看起来低风险，但容易破坏工程系统：

- 脚本或配置影响 CI、本地开发、发布或缓存。
- 文档和实际命令不一致。
- 工具链升级改变 lockfile、编译产物或 lint/test 结果。
- 生成产物和 source-of-truth 混淆。
- 新抽象没有真实使用点或维护边界。

计划必须说明受影响命令、产物、兼容性、回滚方式和验证信号。
