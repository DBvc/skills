# Additive API status migration

## Goal and constraints

Introduce `state` as the replacement for `status` without breaking existing clients. During this release, requests may send either field and responses emit both fields with the same value.

## Scope and ownership

- Owner: `packages/api`
- Schema source of truth: `api/schema/openapi.yaml`
- Compatibility adapter: `packages/api/src/status_compat.py`
- Non-goals: database changes, removing `status`, or changing status values

## Approach

1. Add optional `state` beside `status` in the request and response schema.
2. Normalize requests with `state` first and `status` as fallback; reject conflicting dual values.
3. Emit both fields from the normalized value so old and new clients observe identical state.
4. Keep the adapter for the whole release; removal requires a separate usage review and plan.

## Rollout and rollback

Deploy the additive schema and adapter together. No persisted data changes. Roll back by reverting both files; old clients continue using `status` throughout.

## Validation

- `cd packages/api && pytest tests/migration`
- `cd packages/api && python -m openapi_spec_validator ../../api/schema/openapi.yaml`
