# Ratchet Signals Addendum for dbx-diff-review-control

This reference is optional. Use it only when a meta workflow such as `dbx-code-ratchet` explicitly requests ratchet-compatible output.

Append normal review Markdown first. Then add a fenced `ratchet_signals` JSON block with signals, not decisions.

```ratchet_signals
{
  "ratchet_signals_version": 1,
  "producer_skill": "dbx-diff-review-control",
  "review_mode": "standard",
  "target": {
    "source": "staged",
    "scope": [],
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

Field intent:

- `local_fixable_signal`: a local bounded repair appears plausible.
- `direction_symptom_signal`: the finding may indicate wrong model, state owner, identity boundary, source of truth, or cache lifetime.
- `scope_expansion_required_signal`: likely fix crosses API, schema, dependency, architecture, or module ownership boundaries.
- `human_decision_required_signal`: the likely fix needs user, product, architecture, compatibility, or migration judgment.

Do not mark these fields as certain without evidence. Unknown is acceptable.
