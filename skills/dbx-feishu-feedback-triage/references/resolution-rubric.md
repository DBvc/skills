# Resolution Rubric

Use this rubric to decide feedback status. Be conservative. Closed-loop evidence is the difference between a report and a fortune cookie.

## Resolved

Use `resolved` only when at least one strong closure signal exists:

- reporter says it works, fixed, solved, recovered, or thanks after applying the answer;
- owner explicitly says the issue is fixed and provides fix/version/workaround evidence;
- accepted known issue says this exact case has a known resolution and the chat evidence matches it;
- the thread contains explicit closure from the responsible support/developer/product owner;
- external evidence provided in the current run proves closure.

Weak signals that are not enough by themselves:

- "我看下";
- "试试这个" without user confirmation;
- emoji reaction;
- no one asked again;
- someone replied with a guess;
- developer was mentioned;
- the discussion moved on.

## Probably resolved

Use `probably_resolved` when:

- a specific answer or workaround was given;
- no later contrary evidence appears in the bounded window;
- but there is no explicit user confirmation or external fix evidence.

Reports should show the gap:

```text
状态：probably_resolved
缺口：缺少用户确认
下一步：可回群确认是否恢复
```

## Pending user

Use `pending_user` when the next action is information from the reporter:

- account, tenant, environment, role, URL, version, screenshot, logs, request ID;
- repro steps;
- whether workaround worked;
- expected behavior clarification.

Do not mark as developer-pending if the developer cannot act without user data.

## Pending developer

Use `pending_dev` when the next action is technical investigation or fix:

- suspected frontend/backend/client bug;
- confirmed error code without root cause;
- owner said they are checking;
- correct usage/config is established but behavior still fails;
- repeated issue needs code/log verification.

A developer reply alone is not completion.

## Pending PM

Use `pending_pm` when product judgment is needed:

- current behavior is by design but causes user pain;
- feature request needs scope/priority;
- expected behavior is ambiguous;
- workaround exists but product should decide whether to improve it;
- feedback affects information architecture, permission model, workflow, or product policy.

## Escalated

Use `escalated` only when a formal process is evidenced:

- incident channel or incident ticket;
- explicit owner handoff with action responsibility;
- linked project item or release blocker list;
- support escalation record.

In v0.1, do not query Feishu Project by default. Only report escalation if it appears in chat or domain docs already read.

## Not actionable

Use `not_actionable` when:

- message is non-feedback;
- issue is out of domain;
- no symptom, object, reporter, or follow-up path exists;
- duplicate is already represented by another case in the same report;
- feedback asks for unsafe or unauthorized action.

## Unknown

Use `unknown` when evidence boundaries prevent a responsible judgment:

- thread not expanded;
- attachment unavailable;
- key message deleted or inaccessible;
- domain knowledge missing;
- unclear whether the answer was tried.

Unknown is a valid output. It should come with the missing evidence needed to decide.

## Closure evidence checklist

For every `resolved` case, include at least one:

```yaml
resolution_evidence:
  - message_id: "om_xxx"
    create_time: ""
    sender_label: "reporter | owner | support | unknown"
    paraphrase: "用户确认开启权限后恢复"
```

For every `confirmed_bug` case, include at least one:

```yaml
confirmation_evidence:
  - message_id: "om_xxx"
    create_time: ""
    sender_label: "developer | owner | known_issue | unknown"
    paraphrase: "开发确认已复现并定位为前端兼容问题"
```
