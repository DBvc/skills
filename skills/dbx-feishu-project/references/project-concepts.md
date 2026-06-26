# Feishu Project concepts and vocabulary traps

Feishu Project / Lark Project / Meegle is highly configurable. Local teams may call the same underlying object by different business names.

## Stable concepts

- **Project space**: usually resolved to `project_key`.
- **Work item**: the common container behind many business names such as requirement, story, bug, ticket, task, defect, version, release, or iteration.
- **Work item type**: project-local type key. Do not infer from the display name.
- **Field**: configured field with `field_key`, value type, requiredness, enum options, and sometimes relation semantics.
- **Role**: project-local role assignment. Role writes may use a role-specific operation shape rather than ordinary field update.
- **Workflow**: node/status/transition model. A visible status label is not always the same as the transition action.
- **User key**: canonical user identifier used by the project system.
- **Relation**: dependency, parent-child, related item, duplicate, blocked-by, or local relation type.
- **View/chart/WBS/deliverable**: derived or structured project surfaces that may not map one-to-one to ordinary work item fields.

## Business words are not schema

Treat these as hints until metadata confirms them:

| User word | Possible project meaning | Required discovery |
| --- | --- | --- |
| story / 需求 | Work item type, field category, or issue label | work item types, fields |
| ticket / 工单 | Work item type, support item, task, bug, or custom type | work item types, fields |
| version / 版本 | Work item type, field, release object, WBS node, or tag | types, fields, relations |
| iteration / 迭代 | Field, sprint object, relation, custom type, or view filter | fields, views, relation |
| owner / assignee / 负责人 | role, field, or multiple role assignment | role metadata, fields, users |
| status / node / stage | status field, workflow node, transition, or custom enum | workflow metadata |

## Metadata-first rule

Before writing:

1. Resolve `project_key`.
2. Resolve work item type.
3. Resolve all field keys and enum values.
4. Resolve users and roles.
5. Resolve workflow transition if state changes.
6. Confirm required fields and side effects.

## Safe inference boundary

You may infer that a user-provided Feishu Project URL points to a work item or project page after URL decode confirms it. You may not infer that a display label is a valid API key.
