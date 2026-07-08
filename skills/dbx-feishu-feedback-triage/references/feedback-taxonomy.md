# Feedback Taxonomy

This reference defines the default classification vocabulary for `dbx-feishu-feedback-triage`.

Use domain-specific rules to refine these labels, but keep the global meanings stable so reports stay comparable across domains.

## Category labels

| Category | Meaning | Positive signals | Must not mean |
| --- | --- | --- | --- |
| `usage_question` | User asks how to use an existing capability. | "怎么操作", "在哪里配置", "这个入口在哪". | A bug just because the user is confused. |
| `misuse_or_config` | Correct behavior depends on permission, role, config, environment, data state, or process. | Missing permission, wrong tenant, unconfigured switch, unsupported environment. | A confirmed bug unless correct setup still fails. |
| `suspected_bug` | Behavior appears broken, but confirmation is missing. | Error, 500, blank page, wrong data, cannot reproduce yet, developer investigating. | Confirmed bug without evidence. |
| `confirmed_bug` | Bug is confirmed by reproducible evidence, owner statement, known issue, or fix evidence. | "已复现", "确实是 bug", linked fix, known issue entry. | Any complaint with strong tone. |
| `feature_request` | User asks for a new capability, extension, field, export, automation, or integration. | "能不能支持", "希望增加", "想要导出 xxx 字段". | Existing capability not working. |
| `product_gap` | Current product behavior causes recurring pain or ambiguity, but solution is not yet crystallized. | Repeated confusion, workaround burden, unclear expectation, needs PM decision. | A ready-to-build requirement by default. |
| `known_issue` | Matches accepted known issue or documented limitation. | Same error code/signature/workaround in accepted memory. | A rumor from one chat reply. |
| `incident` | Ongoing or recently active production-impacting failure with broad or urgent impact. | Many users, service unavailable, data loss, core path blocked. | One user's local setup problem. |
| `data_or_permission_issue` | Data visibility, account, tenant, role, ACL, sync, or permission boundary problem. | 403, no data, role mismatch, tenant mismatch. | Generic backend bug without permission/data clues. |
| `documentation_gap` | System works, but docs, FAQ, onboarding, or group announcement failed. | Multiple users ask same operation, answer exists but not discoverable. | Product gap if product behavior itself is poor. |
| `duplicate` | Same case as another case in the same report or historical ledger. | Same symptom/module/error code/business object. | A separate case with different root cause. |
| `noise_or_non_feedback` | Chatter, acknowledgement, social message, unrelated announcement, or non-actionable content. | No user problem, request, decision, or support value. | Low-detail feedback that still has a symptom. |
| `unknown` | Evidence is insufficient for category. | Missing context, unclear referent, inaccessible attachment. | An excuse to avoid useful partial extraction. |

## Status labels

Status is independent from category.

| Status | Meaning | Evidence requirement |
| --- | --- | --- |
| `resolved` | The feedback is closed. | User confirmation, successful workaround, explicit closure, fixed release, or accepted known-resolution evidence. |
| `probably_resolved` | A plausible answer/workaround was provided, but closure is not explicit. | Answer exists and no contrary evidence, but no user confirmation. |
| `pending_user` | User/reporter must provide missing information. | Developer/product asked for logs, screenshot, account, environment, repro, or confirmation. |
| `pending_dev` | Engineering action is next. | Developer investigating, suspected bug, fix needed, or technical confirmation missing. |
| `pending_pm` | Product decision is next. | Expected behavior, scope, priority, or UX/product policy is unclear. |
| `escalated` | Entered another formal process. | Incident channel, ticket, project item, release blocker list, or owner handoff. In v0.1, only report if directly evidenced. |
| `not_actionable` | No useful next action remains. | Not enough info and no way to ask, out of domain, duplicate already closed, or non-feedback. |
| `unresolved` | Open and not currently closed. | Explicit unresolved statement or no closure after meaningful issue. |
| `unknown` | Status cannot be determined. | Missing thread, inaccessible resource, ambiguous reply, or insufficient evidence. |

## Severity labels

Use severity only when helpful. Do not fake precision.

| Severity | Meaning |
| --- | --- |
| `p0` | Broad outage, security/privacy risk, data corruption/loss, payment/core transaction broken, or urgent incident. |
| `p1` | Important workflow blocked for multiple users or key customer, no clear workaround. |
| `p2` | User-impacting issue with workaround, limited scope, or non-core workflow. |
| `p3` | Low urgency, confusion, minor UX/documentation issue, small feature request. |
| `unknown` | Not enough evidence to grade. |

## Confidence labels

| Confidence | Use when |
| --- | --- |
| `high` | Chat evidence and domain source agree, or closure/confirmation is explicit. |
| `medium` | Evidence is plausible but one important signal is missing. |
| `low` | Label is mostly inference, domain knowledge is missing, or key artifact/thread is inaccessible. |

## Duplicate signature hints

Build duplicate signatures from stable business evidence, not raw prose:

```text
module + normalized symptom + expected/actual gap + error code + business object + category
```

Do not include personal names, phone numbers, tokens, tenant names, or full raw message text in the signature.

## Cross-label gotchas

- `usage_question` becomes `documentation_gap` when many users repeatedly ask the same thing and official docs/FAQ should have prevented it.
- `misuse_or_config` becomes `suspected_bug` when the user appears correctly configured and behavior still fails.
- `suspected_bug` becomes `confirmed_bug` only with reproducible, owner, known-issue, or fix evidence.
- `feature_request` is not a bug just because the user expected it.
- `product_gap` is not automatically a feature request. It may need `dbx-crystallize` first.
- `known_issue` requires accepted memory or official known-issue evidence, not one casual chat explanation.
