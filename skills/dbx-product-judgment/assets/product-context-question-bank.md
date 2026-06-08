# Product Context Question Bank

Use this only when missing context would change the verdict. Ask no more than five blocking questions.

## Minimal product judgment questions

1. 你要我判断的是整个产品、某个功能、某条流程、PRD、UI/交互、信息架构，还是技术实现？
2. 目标用户是谁？他们在什么场景下使用？
3. 用户使用它之后，现实状态应该发生什么改变？
4. 当前替代方案是什么？用户为什么会换成这个产品？
5. 这个判断要支持什么决策：是否继续做、是否上线、怎么改、优先级、融资/立项、还是竞品对比？

## PRD review questions

1. PRD 的目标用户和非目标用户分别是谁？
2. 成功指标是什么，是否有 guardrail 指标？
3. 当前需求来自用户研究、客户要求、业务策略、竞品压力，还是内部假设？
4. 哪些边界必须先决策：权限、数据、异常态、定价、合规、运营？
5. 这次版本的最小可验证范围是什么？

## Live product questions

1. 我可以访问哪些 URL 或环境？
2. 是否允许登录、创建测试账号、提交表单、上传文件、支付或开始试用？默认我只做只读探索。
3. 重点看桌面、移动端，还是某个用户路径？
4. 是否有特定竞品或用户反馈要对照？
5. 哪些路径绝对不能操作或改变状态？

## Implementation alignment questions

1. 产品承诺或 PRD 在哪里？
2. 需要检查哪些模块、页面、API、数据模型或 diff？
3. 最担心的是状态一致性、权限、性能、可靠性、可观测性、扩展性，还是交付范围？
4. 是否允许运行测试、lint、build，还是只读代码？
5. 哪些文件或改动明确不在范围内？

## Competitive judgment questions

1. 竞品是用户真正会替代使用的产品，还是同类产品列表？
2. 用户选择时最在意什么：价格、效率、信任、集成、迁移成本、品牌、团队协作、合规？
3. 比较目的是定位、定价、功能优先级、销售话术，还是产品方向？
4. 是否需要当前公开资料调研？
5. 哪些竞品必须纳入，哪些只是参考？
