# Upstream Source Notes

This reference records the upstream surfaces this skill is designed around. It is maintenance context, not runtime instructions.

## Alibaba Cloud / Aliyun surfaces

- Alibaba Cloud CLI: `aliyun` command, profiles, global flags such as `--profile`, and OpenAPI-based product access.
- SLS plugin: `aliyun plugin install --names sls`, then `aliyun sls ...`.
- SLS query API: GetLogsV2 for querying logs from a Project/Logstore over a time range.
- Official SLS Agent Skills: Alibaba Cloud publishes SLS-related Agent Skills that can be used as reference or execution helpers.
- Observability MCP: Alibaba Cloud Observability MCP supports log/metric/trace query workflows, with some AI conversion tools that may incur charges.

## Maintenance policy

Before changing CLI flags, MCP tool names, or permissions, re-check current official docs. Do not rely on memory for:

- plugin command names;
- GetLogsV2 parameters;
- MCP paid/free tool classification;
- RAM permission names;
- official skill installation commands.
