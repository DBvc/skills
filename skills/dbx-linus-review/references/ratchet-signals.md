# Ratchet Signals Addendum for dbx-linus-review

This reference is optional. Use it only when a meta workflow such as `dbx-code-ratchet` explicitly requests ratchet-compatible strict signals.

Append normal strict pragmatic Markdown first. Then add a fenced `ratchet_signals` JSON block.

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

Signals are not final ratchet decisions. `dbx-code-ratchet` still performs triage, direction gate, and progress gate.

Use `direction_health` conservatively:

- `ok`: local repair is probably appropriate.
- `suspect`: local repair may work, but direction or complexity deserves gate scrutiny.
- `failed`: continuing local repair is likely to make the code worse.
