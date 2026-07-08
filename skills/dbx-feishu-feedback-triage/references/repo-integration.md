# Repository Integration Snippets

These snippets are optional. Copy them into repository-level docs after adding `skills/dbx-feishu-feedback-triage/`.

## README.md Stable Skills snippet

```markdown
| `dbx-feishu-feedback-triage` | 飞书/Lark 业务反馈群分诊：基于有界群消息和领域知识包，把反馈整理为可追溯 case、未闭环项、新需求/产品缺口、知识库更新候选。Read-only Feishu feedback triage with domain packs. |
```

If the root README uses bullet-style lines instead of a table, use:

```markdown
- `dbx-feishu-feedback-triage`: 飞书/Lark 业务反馈群分诊：基于有界群消息和领域知识包，把反馈整理为可追溯 case、未闭环项、新需求/产品缺口、知识库更新候选。Read-only by default.
```

## DBX_SKILL_INDEX.md row

```markdown
| `dbx-feishu-feedback-triage` | Feishu/Lark business feedback group triage: converts bounded group chat windows plus domain packs into evidence-backed feedback cases, unresolved items, feature/product-gap intake, and memory candidates. | coordination + procedure + knowledge + external_system | L5 | Domain knowledge can be stale or shallow; chat replies may be mistaken for resolution; memory candidates can drift into accepted facts. | Use for business feedback classification and digest across bounded Feishu groups; delegate raw IM reads to `dbx-feishu-im`, doc reads/writes to `dbx-feishu-doc`, feature clarification to `dbx-crystallize`, and keep Feishu Project integration disabled until v0.2. | Add real sanitized group fixtures after first 5 to 10 reports and compare against human triage. |
```

## docs/DBX_ROUTING_MATRIX.md primary-intent row

```markdown
| Summarize, classify, deduplicate, or triage business feedback from bounded Feishu/Lark group chat windows using a domain knowledge pack | `dbx-feishu-feedback-triage` | `dbx-feishu-im` for generic chat summaries, `dbx-feishu-project` for project-item operations, `dbx-crystallize` for one extracted fuzzy requirement, `dbx-product-judgment` for product-worth verdicts. |
```

## docs/DBX_ROUTING_MATRIX.md graph rule

```markdown
| `dbx-feishu-feedback-triage` composes Feishu IM and docs | Use `dbx-feishu-im` to gather bounded chat evidence and `dbx-feishu-doc` to read domain packs or prepare approved report/memory writes. Do not query or mutate Feishu Project in v0.1. Handoff extracted product gaps or feature requests to `dbx-crystallize` when requirement clarity is needed. |
```

## Root README local check reminder

No new root-level script is required. Existing checks should cover frontmatter and eval JSON:

```bash
python3 scripts/validate_skills.py --root .
python3 scripts/run_trigger_evals.py --root . --validate-only
```
