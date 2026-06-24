# dbx-crystallize Question Bank

Use this only when the main skill needs better blocking questions. Ask the fewest questions that change the requirement contract.

## Actor and context

- Who is the primary actor for this requirement? Who is explicitly not covered?
- In what situation does the actor encounter this need?
- Is this for internal users, external customers, admins, guests, developers, support, or operators?
- Are there affected non-users, such as customers whose data is visible to an admin?

## Desired state change

- What should be true after the feature that is not true now?
- What user action or system behavior proves the change happened?
- Is the request solving a current failure, enabling a new workflow, or reducing operational cost?
- Is the proposed solution mandatory, or is it just one possible way to reach the desired state?

## Scope and non-goals

- What is the smallest useful version?
- What must not be included in this version?
- What existing behavior must not change?
- Are there adjacent features that users may expect but should be excluded now?
- Should this be a user-facing feature, admin-only control, config flag, internal tool, or backend behavior?

## Data and state

- What data objects does the requirement read, create, update, export, delete, cache, or expose?
- Who owns the source of truth?
- What should happen with empty, stale, partial, duplicated, or inconsistent data?
- Are historical records affected or only new records?
- Is auditability required?

## Permissions and trust

- Which roles can perform the action?
- Which roles can see the resulting data or state?
- What must be hidden, masked, anonymized, or permission-checked?
- Does the requirement touch private data, payments, security, identity, billing, or irreversible actions?
- Is explicit confirmation, audit log, recovery, or admin override required?

## Flow and state coverage

- What is the happy path?
- What happens on loading, empty result, validation failure, permission denial, network failure, timeout, partial success, or retry?
- Can the user cancel, undo, recover, or resume?
- What should the system communicate at each state?

## Acceptance criteria

- What observable behavior should make this requirement pass?
- What negative case must fail safely?
- What threshold is known, and what threshold is still TBD?
- Which acceptance criteria can be tested automatically, manually, or through analytics/support observation?

## Rollout and compatibility

- Is this enabled for everyone, a subset, an experiment, a config flag, or a migration?
- What should happen to existing users/data/configs?
- Does this need backward compatibility with old API clients, old records, old permissions, or existing integrations?
- Is rollback expected to preserve data?

## Product/design/technical handoff

- If the feature is built exactly as described, what risk remains?
- Is the unresolved risk about value/user/job? Route product judgment.
- Is the unresolved risk about flow/IA/UI state/presentation? Route design judgment.
- Is the unresolved risk about source of truth, architecture, migration, integration, or validation topology? Route technical plan.
