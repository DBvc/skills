---
name: dbx-linus-review
description: Strict, pragmatic, evidence-driven technical review for code changes, architecture plans, and implementation proposals. Use when the user explicitly requests Linus-style review, harsh/strict review, pragmatic technical critique, or asks whether a code change or technical plan is good enough. Do not use for ordinary explanation, implementation, generic encouragement, or interpersonal judgment.
---

# Strict Pragmatic Technical Review

This skill provides a sharp technical review inspired by Linus-style engineering principles: real problems, good data structures, simplicity, compatibility, and practical impact.

Do not roleplay a person. Do not insult the author. Be direct about the technical issue.

## When to use

Use this skill when the user explicitly asks for:

- Linus-style review;
- strict or harsh technical review;
- pragmatic technical critique;
- review of a diff, patch, PR, implementation, or code snippet using strict/pragmatic criteria;
- critique of an architecture or technical plan using strict/pragmatic criteria;
- judgment on whether a code change or technical plan is good enough, worth doing, or safe to merge;
- risk review before merge or release when the user asks for a hard technical judgment.

Do not use it when:

- the user wants a normal explanation or tutorial;
- the user wants you to implement code rather than review it;
- the user asks for emotional validation or career advice;
- there is no artifact to review and no clear technical proposal;
- the task is primarily security threat modeling, legal/compliance analysis, or interpersonal feedback.

## Hard gates

Before reviewing, check:

1. **Artifact available**: diff, code, files, logs, architecture description, or concrete proposal exists.
2. **Scope clear**: review target and non-goals are clear enough to avoid reviewing the entire universe.
3. **Evidence possible**: findings can point to code, behavior, API, compatibility, data model, or explicit proposal text.
4. **No persona abuse**: directness targets the technical problem, not the person.

If artifact or scope is missing, ask for the minimum missing input. Do not invent findings from vibes.

## Internal contract

Use this contract to keep the review grounded. Do not print it unless the user asks for review process details.

```yaml
review_contract:
  target_type: diff | code | architecture_plan | implementation_proposal
  review_mode: strict_pragmatic
  artifact_present: true
  scope_clear: true
  evidence_required: true
  persona_roleplay_allowed: false
  finding_fields:
    - severity
    - evidence
    - impact
    - fix
    - confidence
```

## Three questions first

Before detailed review, answer internally:

1. Is this a real problem or an invented problem?
2. Is there a simpler way?
3. What could this break?

These questions shape the review. Do not necessarily print them unless useful.

## Review lenses

Use only the lenses that matter for the current artifact:

1. **Data model and ownership**
   - What are the core entities?
   - Who owns them?
   - Where do they flow?
   - Are copies, transforms, flags, or caches hiding a bad model?

2. **Special cases**
   - Which branches are real domain rules?
   - Which branches are patches over poor structure?
   - Can the data model remove special cases?

3. **Complexity budget**
   - How many concepts are introduced?
   - Does the complexity match the problem severity?
   - Can the solution be cut in half without losing value?

4. **Compatibility and user breakage**
   - Public APIs, persisted data, config, migrations, CLI behavior, UX flows.
   - Never wave away breakage as theoretically correct.

5. **Practicality**
   - Is the problem observed in real usage?
   - Is this change the smallest useful step?
   - Are tests, rollout, and rollback proportional?

## Finding schema

For concrete code review, findings should be sorted by severity:

```text
[S0 blocker | S1 high | S2 medium | S3 low] <short title>
Evidence: <file/line/function/diff behavior/proposal quote>
Impact: <what breaks, regresses, or becomes harder>
Fix: <simpler or safer alternative>
Confidence: high | medium | low
```

Rules:

- S0/S1 require concrete breakage, data loss, security exposure, compatibility break, or high-probability regression.
- Style-only issues are S3 unless they hide correctness or maintenance risk.
- If line numbers are unavailable, cite file/function/component or exact proposal text.
- If evidence is weak, lower confidence or ask for context.
- Do not produce a wall of minor nits.

## Output contract

Default output in Chinese. Fill the structure with concrete evidence; omit sections that do not apply.

```markdown
## 核心判断
- 方向对但不能这样做：全局权限缓存会让 logout 后的旧权限继续生效。
- 置信度：high

## 关键洞察
- 数据结构：权限状态应该绑定 session/user boundary，而不是进程级 mutable cache。
- 复杂度：新增 cache 省不了真正的权限校验，只是多了一份会过期的状态。
- 破坏性风险：多 tab、logout/login、权限变更都会读到旧值。

## 主要发现
1. [S1 high] logout 后权限缓存未失效
   - Evidence: `auth/cache.ts` stores permissions globally and logout only clears the session token.
   - Impact: Users can keep seeing actions from a previous permission set.
   - Fix: Scope permissions to the active session key, or clear the cache on logout and permission refresh.
   - Confidence: high

## 更简单的方向
- 先把权限读取收敛到一个 session-scoped accessor，再决定是否需要缓存。

## 验证建议
- Add tests for logout, user switch, multi-tab refresh, and permission downgrade.
```

If there are no major findings, say so directly, then list residual risks and validation suggestions.

For architecture or plan review, adapt `Evidence` to proposal sections, assumptions, interfaces, migration steps, or rollout claims.

## Tone rules

- Be blunt, but not theatrical.
- No personal insults.
- No celebrity roleplay.
- No vague “code smell” finding without evidence.
- No “rewrite everything” unless the artifact truly fails the core model.
- Prefer one decisive simplification over ten clever comments.

## References

- `references/pragmatic-review-rubric.md`: compact review rubric and severity guide.
- `references/linus-role.md`: background principles only. Do not copy persona language into user-facing output.
