# Skill Portfolio Audit Report

Date: {{date}}
Auditor: {{agent_or_user}}
Roots inspected: {{roots}}
Sources used: {{sources}}
Scripts run: {{scripts_run}}
Changes applied: none unless explicitly listed

## Executive decision

Recommendation: {{recommendation}}
Confidence: {{confidence}}
Evidence quality: {{evidence_quality}}
Trigger overlap review: {{high_overlap_count}} high, {{medium_overlap_count}} medium

Do now:
1.
2.
3.

Do not do automatically:
- Do not uninstall or archive skills based only on inventory metadata.
- Do not inspect private chat, shell, browser, or log history without explicit consent.
- Do not merge skills on lexical overlap alone; confirm with trigger examples or user confusion evidence.

## Placement buckets

- Keep global:
- Move to project scope:
- Make explicit-only:
- Disable pending review:
- Uninstall/archive:
- Merge/refactor:
- Need more evidence:

## Summary counts

| Bucket | Count | Notes |
|---|---:|---|
| global_keep |  |  |
| project_scope |  |  |
| explicit_only |  |  |
| disable_pending_review |  |  |
| uninstall_or_archive |  |  |
| merge_or_refactor |  |  |
| needs_more_evidence |  |  |

## Skill-level recommendations

| Skill | Current scope | Recommendation | Confidence | Evidence | Reason | Main risk | Proposed action |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Trigger overlap review

| Skills | Severity | Type | Shared trigger terms | Evidence | Recommended action |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Top high-leverage changes

1.
2.
3.
4.
5.

## Dry-run implementation plan

```bash
# Commands are proposals only. Review before running.
```

## Explicit-only snippets

```yaml
# agents/openai.yaml
policy:
  allow_implicit_invocation: false
```

## Unknowns and interview questions

-

## Validation and limitations

- Commands run:
- Files inspected:
- Files not inspected:
- Web research:
- Usage evidence quality:
- Recommendations that need follow-up:
- Rollback path:
