- [ ] [schema-additive] Add the optional `state` field
验收: 任务类型=step; request and response schemas retain `status` and add optional `state`
验证: cd packages/api && python -m openapi_spec_validator ../../api/schema/openapi.yaml
依赖: none

- [ ] [compat-adapter] Normalize and dual-emit status fields
验收: 任务类型=step; state wins, status is fallback, conflicts fail, and responses emit equal values
验证: cd packages/api && pytest tests/migration
依赖: schema-additive

- [ ] [validate-migration] Validate old/new client compatibility
验收: 任务类型=gate; status-only, state-only, equal dual-field, conflicting dual-field, and rollback paths are covered
验证: cd packages/api && pytest tests/migration
依赖: compat-adapter
