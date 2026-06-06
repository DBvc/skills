# Examples

## Good auto-fix candidate

Review finding:

```text
[S1] logout 后 permission cache 未清理。
Evidence: src/auth/logout.ts clears token but not permissionCache.
Impact: user switch can show old permissions.
Fix: clear cache on logout or bind key to session identity.
Confidence: high.
```

Ratchet triage:

```yaml
status: auto_fix
reason: current diff introduced, concrete evidence, local fix, no API/schema/dependency change
```

## Direction failure candidate

Review findings:

```text
[S1] logout stale cache
[S2] user switch stale permissions
[S2] permission downgrade requires manual sync
```

Strict direction signal:

```yaml
direction_health: failed
root_cause: wrong_state_owner
local_repair_recommended: false
```

Ratchet result:

```yaml
state: stopped-direction-failure
action: no automatic repair
```

## Not worth this ratchet

Review finding:

```text
[S3] variable name can be shorter.
```

Ratchet triage:

```yaml
status: defer_not_worth
reason: S3 style-only, no user-impact or future bug path
```

## False positive

Review finding:

```text
[S2] missing null check.
```

Counter-evidence:

```text
Existing schema guarantees non-null and generated type enforces it.
```

Ratchet triage:

```yaml
status: reject_false_positive
reason: contradicted by source-of-truth schema and type boundary
```

## Repair contract boundary

Accepted findings:

```yaml
accepted_findings: [F-001]
allowed_files:
  - src/auth/logout.ts
  - src/auth/cache.ts
forbidden_change_types:
  - new_dependency_without_user_approval
  - public_api_change_without_user_approval
  - unrelated_cleanup
```

If the repair worker wants to modify `src/shared/sessionModel.ts`, it must stop and escalate.
