# Ratchet Signals Schema

Reviewer skills may append this optional block when invoked by `dbx-code-ratchet` or when the user explicitly asks for machine-readable ratchet signals.

The block is optional. It should not make ordinary read-only reviews noisy.

Use fenced JSON:

````markdown
```ratchet_signals
{
  "ratchet_signals_version": 1,
  "producer_skill": "dbx-diff-review-control",
  "review_mode": "standard",
  "target": {
    "source": "staged",
    "scope": ["src/auth/session.ts"],
    "out_of_scope": []
  },
  "overall": {
    "highest_severity": "S1",
    "direction_health": "ok",
    "complexity_pressure": "low",
    "validation_confidence": "medium"
  },
  "findings": [
    {
      "id": "F-001",
      "severity": "S1",
      "category": "state_ownership",
      "title": "logout 后 session-scoped cache 没有失效",
      "confidence": "high",
      "introduced_by_current_diff": true,
      "local_fixable_signal": true,
      "direction_symptom_signal": false,
      "scope_expansion_required_signal": false,
      "human_decision_required_signal": false,
      "minimal_fix_hint": "清理 logout/session switch 路径，或把 cache key 绑定 session identity",
      "verification_hint": "增加 user switch/logout 后权限缓存失效的回归测试"
    }
  ]
}
```
````

## Field rules

Signals are not decisions. The ratchet gate makes final decisions.

Use `*_signal` fields to express reviewer judgment:

- `local_fixable_signal`: the reviewer believes a bounded local fix is plausible.
- `direction_symptom_signal`: the finding may be a symptom of wrong data model, state owner, source of truth, identity boundary, cache lifetime, or compatibility boundary.
- `scope_expansion_required_signal`: the likely fix needs new dependency, API, schema, migration, architecture layer, broad module move, or cross-module ownership change.
- `human_decision_required_signal`: the likely fix needs user/product/architecture/compatibility judgment.

Unknown is better than fake certainty. Omit a field or use `null` / `"unknown"` when evidence is insufficient.

## Direction finding extension

Strict reviewers may add `direction_findings`:

````markdown
```ratchet_signals
{
  "ratchet_signals_version": 1,
  "producer_skill": "dbx-linus-review",
  "review_mode": "diff_strict",
  "overall": {
    "direction_health": "suspect",
    "complexity_pressure": "high",
    "primary_root_cause": "wrong_state_owner",
    "local_repair_recommended_signal": false
  },
  "direction_findings": [
    {
      "id": "D-001",
      "severity": "S1",
      "title": "当前实现把 session state 放进了 module singleton",
      "confidence": "high",
      "symptom_finding_ids": ["F-001", "F-002"],
      "why_local_repairs_are_risky": "logout、user switch、permission downgrade 都需要补丁式清理，说明 owner 错了",
      "smaller_direction_hint": "先把 state owner 收敛到 session/user identity，再做局部缓存"
    }
  ]
}
```
````

## Compatibility

A reviewer can output normal Markdown only. `dbx-code-ratchet` should still work by parsing the human-readable findings, but it must lower parse confidence.
