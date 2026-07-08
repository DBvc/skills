# Memory Candidate Policy

This skill may generate memory candidates. It must not silently update accepted memory.

## Memory layers

| Layer | Storage | Purpose | Authority |
| --- | --- | --- | --- |
| Accepted memory | Feishu Wiki/Doc or reviewed Base | Stable FAQ, business rules, known issues, glossary, module map | Medium to high, depending on owner and freshness |
| Candidate memory | Feishu candidate doc, local draft, report section | Proposed updates from a run | Low until reviewed |
| Runtime cache | local files, temp JSON, embeddings, sqlite | Speed, dedup, indexing | Not source of truth |
| Chat history | Feishu IM | Symptom and closure evidence | High for what was said, low for durable facts |

## Default write policy

```yaml
memory_policy:
  accepted_memory_write: requires_explicit_approval
  candidate_memory_write: preview_required
  local_cache_write: allowed_for_runtime_cache_if_no_sensitive_raw_messages
  raw_chat_log_storage: disabled_by_default
```

## Candidate format

Every candidate must be reviewable.

```yaml
memory_update_candidate:
  id: "MUC-20260708-001"
  type: faq | known_issue | business_rule | glossary | module_owner | classification_example | stale_memory_fix
  proposed_target: "FAQ / 订单导出"
  claim: "看不到导出按钮时先检查 order.export 权限。"
  conditions:
    - "用户在订单页面看不到导出按钮"
  source_evidence:
    - message_id: "om_xxx"
      create_time: ""
      paraphrase: "产品说明需要 order.export 权限"
    - doc_url: ""
  confidence: high | medium | low
  owner: "unknown"
  stale_policy: "权限模型变更后复查"
  requires_approval: true
  risks:
    - "不同租户权限名可能不同"
```

## Candidate types

- `faq`: improves support answer for repeated user question.
- `known_issue`: records confirmed or suspected recurring issue with workaround.
- `business_rule`: clarifies intended behavior or feature boundary.
- `glossary`: adds or corrects terminology.
- `module_owner`: adds routing hints and owners.
- `classification_example`: adds a labeled example for future triage.
- `stale_memory_fix`: updates or removes old knowledge.

## Approval rules

Before accepted memory is changed, show:

- exact target document/section;
- exact patch content;
- source evidence;
- risk and staleness notes;
- rollback path if known.

Do not write if:

- source evidence is only one ambiguous chat reply;
- the claim conflicts with official docs;
- owner or freshness is unknown for a high-impact business rule;
- the update would expose private raw chat content or personal data;
- the user asked for read-only output.

## Staleness policy

Every accepted memory item that can change should include one of:

```yaml
stale_policy: "version_release_review"
stale_policy: "monthly_review"
stale_policy: "owner_review_required"
stale_policy: "never_if_definitional"
```

If stale memory conflicts with newer evidence, do not overwrite it silently. Output a `stale_memory_fix` candidate.
