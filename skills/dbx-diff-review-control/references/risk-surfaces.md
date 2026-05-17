# Risk Surfaces

Use this file to decide review depth and specialist passes.

## High-risk surfaces

Trigger `deep` review when the selected target touches:

- authentication, authorization, permissions, sessions, tenants, roles;
- payments, billing, quotas, entitlements, invoices;
- migrations, persisted data, database schema, destructive data mutation;
- public APIs, SDKs, CLI behavior, exported types, config/env contracts;
- caches, global state, cross-tab/session state, offline/optimistic flows;
- external integrations, webhooks, queues, idempotency, retries;
- file system, path construction, shell commands, redirects, HTML injection, secrets;
- generated artifacts, release manifests, signing, appcast, package publishing.

## Frontend user-impact checks

- Loading/error/empty states.
- Double submit and optimistic rollback.
- Route guard and permission downgrade.
- Logout/login/user switch/tenant switch.
- Stale closure and request race.
- SSR/hydration mismatch.
- Local/session storage lifetime.
- Form validation, disabled states, focus, keyboard, accessibility.
- Large list rendering and expensive selectors.
- Feature flag and A/B branch consistency.

## Backend/full-stack checks

- Authorization before data access and mutation.
- Idempotency of commands, jobs, and webhooks.
- Transaction boundaries and partial failure.
- Schema compatibility and migrations.
- Retry behavior and duplicate messages.
- Error mapping to client-visible behavior.
- API response optionality and enum expansion.
- Rate limits, quotas, pagination, sorting, filtering.

## Maintainability checks that matter

Only report maintainability when it has a concrete future failure mode:

- duplicated source of truth;
- leaky abstraction that hides ownership;
- local helper that smuggles policy across modules;
- new concept without a lifecycle or boundary;
- unbounded branching around a bad representation;
- code path that future changes are likely to miss.

Do not report generic “this could be cleaner” comments.
