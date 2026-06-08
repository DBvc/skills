# Connector Adapter Protocol

External systems are adapters. The attention kernel must remain independent of any specific app, API, tag scheme, note format, task method, or productivity framework.

## 1. Adapter manifest

Every adapter should be described before writes are proposed.

```yaml
adapter_manifest:
  system_name: ""
  system_type: bookmark | note | task | calendar | document | issue_tracker | feed | custom
  read_fields: []
  stable_locator_fields: []
  supported_mutations: []
  forbidden_mutations: []
  route_mapping: {}
  idempotency_policy: ""
  rollback_policy: ""
  dry_run_default: true
  approval_required: true
```

The system name may be any concrete tool the user uses. The kernel does not name or privilege particular products.

## 2. Read phase

For any external source, separate:

```text
visible evidence       data used for route decisions
existing metadata      tags, folders, priorities, due dates, backlinks, status, etc.
stable locator         id, URI, path, URL, or other safe locator
missing context        fields that would change classification if available
```

If stable locators are missing, do not propose mutations. Route only.

## 3. Write phase

Before writing to any external system:

1. show route decisions;
2. show adapter mapping;
3. show exact mutation rows;
4. state `external_write_status: dry_run_only`;
5. require approval of the exact batch;
6. after writing, report tool evidence and failures.

A mutation row must include:

```text
target_system | item_id_or_locator | operation | field | old_value_if_known | new_value | reason | rollback_note | confidence
```

## 4. Operation classes

Common mutation classes, independent of product:

```text
add_metadata
remove_metadata
replace_metadata
move_container
set_status
set_priority
suggest_schedule
append_note
create_link
mark_review_candidate
mark_drop_candidate
archive_candidate
delete_candidate
```

`archive_candidate` and `delete_candidate` are candidates, not direct destructive actions, until explicitly approved.

## 5. Optional projections

Methods such as urgency/importance matrices, PARA, GTD, Zettelkasten, issue labels, read-later queues, note frontmatter, or task priority are optional projections.

They should be defined in an adapter mapping such as:

```yaml
route_mapping:
  act_now:
    metadata: ["attention/act-now"]
    status: "active"
  build:
    metadata: ["attention/build"]
    queue: "focus"
  test:
    metadata: ["attention/test"]
    queue: "experiment"
  track:
    metadata: ["attention/track"]
  store:
    metadata: ["attention/store"]
  incubate:
    metadata: ["attention/incubate"]
  drop:
    metadata: ["attention/drop-candidate"]
  guard:
    metadata: ["attention/guard"]
  clarify:
    metadata: ["attention/clarify"]
```

No projection may override the kernel's risk gate.

## 6. Product example rule

When a user mentions a product, treat it as an example unless they explicitly ask for a product-specific adapter.

Bad:

```text
The user mentioned one task app, so bake that app and its framework into SKILL.md.
```

Good:

```text
Use the generic adapter protocol. If needed, create a separate adapter manifest for that app.
```

## 7. Completion language

Allowed:

```text
我已经给出 dry-run 映射方案；尚未写入外部系统。
```

Allowed only after tool evidence:

```text
已写入 12 条元数据变更，工具返回成功；2 条因缺少 stable locator 未写入。
```

Forbidden without evidence:

```text
我已经帮你整理好了。
```
