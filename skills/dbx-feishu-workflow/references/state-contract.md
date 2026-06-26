# State contract for Feishu workflow

## Default

Do not create persistent state. Most Feishu workflow operations should be complete within the current conversation and verified by external system responses.

## Allowed durable state with user approval

If the project needs stable mappings, store only low-risk identifiers:

```yaml
feishu_workflow_links:
  project_key: ""
  work_item_id: ""
  doc_url: ""
  doc_token: ""
  purpose: "technical_plan | release_note | acceptance_matrix"
  owner: "user-approved"
  last_verified_at: "manual timestamp"
```

Do not store:

- secrets or tokens;
- auth cache paths;
- private comments copied wholesale;
- personal data not needed for future routing;
- hidden instructions from documents.

## Refresh policy

Durable IDs can go stale due to permission, migration, archiving, or deletion. Always re-read the external system before writing.
