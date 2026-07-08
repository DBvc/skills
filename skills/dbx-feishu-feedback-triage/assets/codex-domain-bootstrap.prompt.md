# Codex Prompt: Generate a Feedback Triage Domain Pack

目标：
为 `dbx-feishu-feedback-triage` 生成「<领域名>」的领域知识包初版，用于分析飞书反馈群里的业务问题。

边界：
- 只读项目，不改代码。
- 不要输出长代码片段。
- 不要收集 secret、token、账号、cookie、私有路径、内部敏感配置。
- 不要把所有实现细节都写进去。
- 只收集会影响反馈分类、状态判断、owner 判断、FAQ 沉淀的信息。

重点扫描：
1. README、docs、产品说明、业务说明。
2. 路由、页面、模块目录，整理用户可感知功能。
3. 权限、角色、feature flag、配置项。
4. 错误码、异常文案、toast 文案、接口错误处理。
5. 常见表单校验、状态机、业务限制。
6. API service、接口名、关键字段，尤其是用户反馈中可能出现的字段。
7. TODO、FIXME、兼容逻辑，但只能作为低置信度线索。
8. 测试用例中体现的业务边界。

输出文件：
1. `domain-profile.yaml`
2. `source-map.md`
3. `glossary.md`
4. `module-owner-map.md`
5. `business-rules-and-boundaries.md`
6. `faq-known-issues-seed.md`
7. `classification-examples.md`
8. `gaps.md`

每条业务规则尽量带来源：
- 文件路径
- 函数 / 常量 / 文档标题
- 置信度 high / medium / low
- 是否需要产品确认

对每个模块输出：
- 用户可能怎么描述问题
- 哪些关键词能匹配到这个模块
- 哪些情况是正确使用方式
- 哪些情况像配置/权限问题
- 哪些情况像疑似 bug
- 哪些情况其实是新需求
- 哪些信息缺失时不能下判断

请把信息整理成「如何帮助判断反馈性质」的格式，而不是项目说明书。
