# Feishu Project auth and secret policy

## Principle

This skill may control an external work system. Authentication is a local runtime concern, not repository content.

Allowed in the skill repo:

- Empty example config.
- Environment variable names.
- Installation notes.
- Redaction rules.
- Local-only path patterns such as `~/.config/dbx/feishu-project.env` when no real username or machine-specific path is embedded.

Forbidden in the skill repo and final answers:

- `app_secret`, `access_token`, `refresh_token`, `user_access_token`, `tenant_access_token`.
- `Authorization: Bearer ...`.
- Cookies, session identifiers, exported credential cache content.
- Device code values or verification URLs with sensitive query parameters.
- Private tenant data copied only for debugging without user request.

## Runtime configuration

Preferred local variables:

```bash
DBX_MEEGLE_BIN=meegle
MEEGLE_HOST=https://project.feishu.cn
MEEGLE_USER_ACCESS_TOKEN=
MEEGLE_USER_AGENT=dbx-feishu-project
```

Keep real values outside git. A safe local pattern:

```bash
cp skills/dbx-feishu-project/assets/env.example ~/.config/dbx/feishu-project.env
chmod 600 ~/.config/dbx/feishu-project.env
set -a
. ~/.config/dbx/feishu-project.env
set +a
```

## Authentication checks

Before an operation that requires live Feishu Project access:

1. Check that `meegle` or `meegle-cli` exists, or `DBX_MEEGLE_BIN` points to an executable.
2. Check auth state with the CLI's auth/status command if available.
3. If auth is missing, ask the user to complete the official CLI auth flow locally.
4. If permission is denied, report the missing project/object and stop. Do not suggest bypasses.

## Redaction policy

All command output in responses must be redacted. Use `scripts/redact_output.py` or `scripts/meegle_call.py` for risky outputs.

Redact these patterns even when nested in JSON:

- keys containing `secret`, `token`, `authorization`, `cookie`, `session`, `password`, `credential`;
- bearer tokens;
- long opaque strings after known auth keys;
- device code values.
