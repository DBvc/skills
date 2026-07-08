# dbx-feishu-feedback-triage

飞书业务反馈分诊 skill。给定领域知识包、飞书群和时间范围，把群聊里的业务反馈整理成可追溯的 feedback cases，判断类型、状态、优先级、未闭环项和知识沉淀候选。

## v0.1 boundary

This first version is deliberately read-only by default.

It does:

- bounded Feishu group feedback digest;
- domain-pack based classification;
- unresolved scan;
- requirement/product-gap intake;
- memory-update candidate generation;
- local validation helpers.

It does not:

- create or update Feishu Project items;
- rely on messy Feishu Project state as source of truth;
- reply to chats without explicit preview and approval;
- update accepted FAQ/known issues silently;
- read code by default.

## Install

Unzip this overlay at the root of `DBvc/skills` so it creates:

```text
skills/dbx-feishu-feedback-triage/
```

Then run your normal local checks:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```

Optional script checks:

```bash
python3 skills/dbx-feishu-feedback-triage/scripts/validate_domain_profile.py \
  skills/dbx-feishu-feedback-triage/assets/domain-profile.template.yaml

python3 skills/dbx-feishu-feedback-triage/scripts/validate_feedback_cases.py \
  skills/dbx-feishu-feedback-triage/evals/fixtures/sample_digest.json
```

## First real test

1. Create a Feishu Wiki page from `assets/domain-profile.template.yaml` and `assets/source-map.template.yaml`.
2. Fill only one real domain and one real feedback group.
3. Run a narrow window first:

```text
用「<domain_id>」领域，总结今天 10:00 到 12:00「<反馈群名>」里的反馈，只读，重点看未闭环和新需求。
```

4. Compare output manually against the group history.
5. Patch `references/feedback-taxonomy.md`, domain knowledge, or eval fixtures based on real misses.

## Common invocations

```text
初始化「交易系统」反馈分诊领域，领域入口文档是 <飞书文档链接>，先只读检查。
```

```text
用「交易系统」领域，生成昨天的反馈日报，只读，不写飞书项目。
```

```text
用「交易系统」领域，总结 7 月 8 日 10:00 到 18:00 反馈群里的问题，重点看未解决和新需求。
```

```text
用「交易系统」领域，扫描昨天到现在还没闭环的反馈。
```

```text
把这次日报里的 FAQ 候选整理成知识库更新候选，不要写入正式 FAQ。
```

## Suggested repository integration

See `references/repo-integration.md` for README, `DBX_SKILL_INDEX.md`, and routing matrix snippets.
