---
name: dbx-conversation-align
description: Diagnose communication intent, disagreement layer, correction timing, boundary needs, and response strategy for relationship, work, and conflict conversations.
---

# Communication Alignment

## Purpose

Help the user understand what a conversation is really doing, choose whether to listen, comfort, analyze, advise, correct, negotiate, repair, or set a boundary, and produce wording that preserves clarity without unnecessary damage.

The goal is not to win arguments. The goal is to align world models, protect trust where appropriate, and move the real problem forward.

## When to Use

Use this skill when the user asks to:

- analyze where a conversation got stuck;
- decide whether to comfort, analyze, advise, correct, negotiate, repair, or set a boundary;
- rewrite a risky message for a relationship, family, friend, or work context;
- prepare for a difficult conversation or conflict;
- understand another person's likely needs, assumptions, fears, or communication parameters;
- express disagreement without turning the discussion into a fight;
- convert a vague interpersonal issue into a concrete next step.

## Non-use Boundary / When Not To Use

Do not use this skill to manipulate, coerce, gaslight, guilt-trip, deceive, exploit insecurity, extract compliance, or bypass another person's stated boundary.

Do not treat this skill as therapy, legal advice, medical advice, emergency response, workplace investigation, or professional mediation. It may help structure communication, but it must not replace qualified support when risk is high.

When the user describes immediate danger, violence, coercive control, credible threats, self-harm risk, stalking, blackmail, severe abuse, or illegal conduct, switch from ordinary communication optimization to safety, documentation, support resources, and appropriate professional or emergency channels.

## Hard Gates

Run these gates before giving tactics. If a gate triggers, adapt the answer and do not proceed as if this were a normal disagreement.

### Gate 1: Safety and crisis

If there is immediate danger, threats, violence, severe intimidation, self-harm risk, or coercive control, prioritize safety over persuasion. Recommend contacting local emergency services, trusted people, professional support, or formal reporting channels as appropriate. Do not provide scripts that keep the user in a dangerous exchange.

### Gate 2: Consent and autonomy

If the user's goal is to make someone comply, hide intent, provoke jealousy, punish silence, pressure intimacy, or override a clear no, refuse the manipulative framing. Redirect to honest expression, boundary-setting, or accepting non-consent.

If the request mixes a legitimate need with a manipulative tactic, refuse only the manipulative part and continue with the legitimate part. Example: do not help "trap them in public", but do help produce a factual timeline, written clarification, boundary, or request for a third party.

### Gate 3: Evidence strength

Do not present guesses about another person's inner state as facts. Separate observable behavior, possible explanations, validating questions, and conclusions that are not warranted.

### Gate 4: Correction timing

Before correcting another person, check stakes, invitation, emotional temperature, and motive. Small conceptual errors inside venting usually do not deserve immediate correction. Safety, major decisions, and concrete harm may require correction, but still start with respect and context.

### Gate 5: Boundary escalation

If the other person repeatedly insults, mocks, stonewalls,翻旧账, shifts blame, or ignores stated limits, stop optimizing for better explanation. Recommend boundary, pause, written clarity, third-party support, or exit from the exchange.

### Gate 6: Work and professional stakes

Do not treat every work conversation as an HR or legal matter. Match the level of support to the stakes:

| Level | Signal | Allowed help | Limit |
|---|---|---|---|
| Ordinary feedback | manager feedback, collaboration friction, unclear expectations | clarify examples, ask for expectations, prepare wording, align next step | do not over-formalize or assume bad faith |
| Performance or written-record risk | promotion, performance review, written improvement plan, deadline miss record, repeated blame, ownership dispute, public accusation | separate facts from interpretation, prepare evidence, write calm record, suggest manager/HR-adjacent escalation if needed | do not make legal/HR conclusions |
| Formal investigation or regulated domain | HR investigation, legal claim, medical/financial/regulatory decision, domestic violence, mental health crisis | provide communication structure only, encourage qualified support and formal channels | do not advise on substantive legal, medical, financial, or investigative decisions |

For legal, medical, financial, HR investigation, domestic violence, mental health crisis, or regulatory issues, provide communication structure only at a general level and advise qualified professional support for substantive decisions.

For ordinary manager feedback, do not suppress legitimate self-advocacy. First understand the feedback and expected behavior, then help the user add concise contribution facts or missing context without turning the reply into a defensive counterattack.

## Domain Content Contract

```yaml
domain_content_contract:
  target_user: "A user preparing or repairing a relationship, friend, family, or work conversation."
  artifact_type: "conversation diagnosis, message rewrite, correction decision, boundary plan, or difficult-conversation prep"
  output_depth: "quick to standard unless the user asks for deep preparation"
  required_variables:
    - conversation function
    - emotional temperature
    - main stuck layer
    - stakes and reversibility of the next action
    - evidence strength for inferred motives
    - boundary repetition or safety risk
    - relationship or work context
  hidden_failure_modes:
    - correcting a concept error before validating a venting person
    - turning weak evidence into a confident motive claim
    - optimizing for winning, humiliation, guilt, jealousy, or compliance
    - continuing to explain after repeated contempt or ignored boundaries
    - making work disputes about personality instead of evidence, risk, options, and ownership
    - treating ordinary work feedback as a formal investigation, or treating formal risk as casual feedback
  expert_quality_checks:
    - validates feelings without endorsing unsupported judgments
    - names uncertainty and what evidence would update it
    - separates legitimate self-protection from manipulative tactics
    - prioritizes safety, boundary, and irreversible-action risks before analysis
    - provides wording that is sendable in the user's context
    - includes escalation or documentation paths when repetition, threats, or formal stakes appear
  data_source_policy:
    realtime_required: []
    user_provided_required:
      - exact words or behavior when available
      - relationship or work context
      - stakes of the next action
      - repeated pattern or one-off incident
    can_estimate_with_label:
      - likely conversation function
      - emotional temperature
      - possible explanations for behavior
    must_not_fabricate:
      - the other person's motive
      - legal, medical, financial, HR, or safety conclusions
      - facts not present in the user's account
  uncertainty_policy:
    - "Use observable behavior, possible explanations, evidence strength, and validating questions."
    - "Do not turn hypotheses into labels or diagnoses."
  must_not_omit:
    - directly usable wording when the user asks what to say
    - one avoid warning
    - boundary or safety note when a gate triggers
  worked_examples_needed:
    - relationship correction
    - cold replies and over-inference
    - repeated sarcasm and old grievances
    - work evidence dispute
  domain_eval_cases:
    - venting with a concept claim
    - imminent public escalation with weak evidence
    - repeated boundary violation or digital flooding
    - manager feedback with identity threat
    - performance or written-record risk
    - workplace intimidation without a manipulative user goal
    - manipulative request with legitimate documentation need
```

## Core Model

A message often carries several functions at once. Respond to the active function, not only to the literal claim.

### Conversation Functions

| Function | Signals | Best first response |
|---|---|---|
| Venting | strong emotion, scattered details, no clear ask | listen, reflect, validate feeling |
| Comfort-seeking | “气不气”, “我是不是很倒霉” | stay with the feeling before analysis |
| Validation-seeking | asks whether reaction is reasonable | validate feeling; separate judgment later |
| Analysis-seeking | asks “我想得对吗”, “帮我拆一下” | analyze facts, concepts, logic, evidence |
| Advice-seeking | asks “我该怎么办” | clarify goal, give options and tradeoffs |
| Decision-making | needs next step, owner, deadline | align criteria and action |
| Conflict/defense | sarcasm, silence, repeated rebuttal | stop proving; repair safety |
| Boundary issue | repeated disrespect or unreasonable demand | state limit and consequence |

### Disagreement Layers

Locate the main layer before responding:

1. Emotion: what feeling needs to be recognized?
2. Relationship: does the person need support, respect, or reassurance?
3. Goal: what are they trying to achieve now?
4. Facts: do both sides know the same events?
5. Concepts: do key words mean the same thing?
6. Logic: is the inference chain different?
7. Values: are fairness, efficiency, autonomy, stability, or respect weighted differently?
8. Interests: who bears cost, risk, or loss?
9. Identity: does anyone feel stupid, weak, ignored, controlled, or disrespected?
10. Action: what should happen next?

When emotion, relationship, or identity is active, pure logic usually lands badly.

### Communication Parameters

Avoid fixed personality labels. Infer current parameters from behavior:

| Parameter | Signals | Adaptation |
|---|---|---|
| Result-first | asks for conclusion | lead with conclusion |
| Process-first | asks why, wants details | show reasoning chain |
| Emotion-sensitive | asks whether you understand | reflect feeling first |
| Risk-sensitive | asks “万一呢” | name risks and fallback |
| Autonomy-sensitive | resists being taught | ask permission; give choices |
| Identity-sensitive | hears correction as insult | de-personalize the issue |
| Evidence-oriented | wants data/examples | show evidence and limits |
| Relationship-oriented | tracks tone and stance | confirm care and respect |
| Time-sensitive | impatient with detail | compress and give next step |

## Workflow / Runtime Procedure

### Step 1: Classify the task

Identify whether the user needs diagnosis, rewrite, preparation, correction decision, boundary plan, work alignment, relationship repair, or practice guidance.

If the user asks for wording, give wording first and keep theory short.

### Step 1.5: Resolve competing functions

When several functions are active, use this priority order. Name only the relevant top one or two in the answer.

1. Safety or crisis: immediate danger, credible threats, violence, coercive control, self-harm risk, stalking, blackmail, or illegal conduct.
2. Boundary failure: repeated insults, contempt, ignored limits, digital flooding / 数字骚扰 / 信息轰炸 / 刷屏 / 连环电话 / 切换渠道追问, stonewalling, blame loops, or coercive pressure.
3. Irreversible or high-cost action: public accusation, breakup message, resignation, formal complaint, legal/HR escalation, major decision, financial cost, or reputational harm.
4. Emotional containment: venting, comfort-seeking, identity threat, shame, fear, or relationship reassurance.
5. Evidence and uncertainty: weak motive inference, missing facts, alternative explanations, validating question.
6. Concept, logic, or wording correction.
7. Style polish.

If a lower-priority function is tempting but a higher-priority risk is present, handle the higher-priority risk first. For example, if someone is venting and about to publicly accuse another person based on weak evidence, validate the feeling, then slow the irreversible action and separate evidence before discussing the concept.

When identity threat is active, give at least one identity validation before listing possible explanations or correcting the claim. Example: recognize that the person may feel their effort, competence, dignity, or belonging is being dismissed.

### Step 2: Infer the other person's current function

Use observable signals and a low-cost probe. Prefer: “你是想先吐槽一下，还是想让我帮你分析？” or “我先确认一下，你现在更需要被理解，还是需要建议？”

### Step 3: Estimate emotional temperature

| Level | State | Strategy |
|---|---|---|
| 0 | calm | direct analysis is acceptable |
| 1 | mild emotion | reflect once, then analyze |
| 2 | clear emotion | validate, then ask permission |
| 3 | defensive or escalating | stop proving; repair first |
| 4 | crisis or threat | safety gate; pause ordinary tactics |

### Step 4: Choose mode

Choose one or combine:

- Listen: let the person finish; summarize only.
- Validate: confirm feeling without necessarily agreeing with judgment.
- Explore: ask one or two background questions.
- Ask permission: request consent before analysis, advice, or correction.
- Analyze: separate facts, concepts, logic, evidence, and uncertainty.
- Advise: offer options, costs, risks, and recommendation.
- Negotiate: align goals, constraints, tradeoffs, and next step.
- Repair: name the interaction problem and reduce threat.
- Boundary: state what is acceptable, what is not, and what happens next.

### Step 5: Produce the answer

Be concise. Give the diagnosis, reason, recommended action, usable wording, and one avoid warning. State uncertainty when inferring motive.

## Correction Decision Rule

Before pointing out an error, answer four questions:

1. Does the error affect safety, major decisions, real harm, or important trust?
2. Did the other person invite analysis or correction?
3. Is the emotional temperature low enough for analysis?
4. Am I correcting to help the situation, or to relieve my discomfort with imprecision?

| Decision | Use when | Response |
|---|---|---|
| Do not correct now | venting, small concept issue, no real consequence | listen and maybe reflect the feeling |
| Light correction | low stakes but may confuse later | validate first, then soft distinction |
| Delayed correction | issue matters but emotion is high | mark it for later; repair now |
| Must correct | safety, major decision, real harm, public accusation, formal escalation, financial or reputational cost, explicit analysis request | be clear, respectful, and specific |

When the issue is a public post, formal complaint, breakup, resignation, financial choice, or other hard-to-reverse action, do not rely only on permission prompts. Validate briefly, then slow the action and name the evidence gap or risk.

Correction template:

> 我理解你为什么会这么想，这件事确实容易让人不舒服。你的感受我觉得成立。  
> 如果讨论这个判断本身，我可能有一点不同看法。  
> 你现在想听我分析这个点，还是先把这件事说完？

## Anti-mind-reading and Evidence Strength

Use this structure when the user infers motives such as “他是不是不爱我了”, “她是不是故意针对我”, or “老板是不是看不起我”.

1. Observable behavior: what actually happened?
2. Plausible explanations: list several, not only the threatening one.
3. Evidence strength: weak, medium, strong.
4. Validating question: ask something that can update the belief.
5. Unsafe conclusion: name what cannot be concluded yet.

Example:

> 行为是“回复变慢”。可能解释包括忙、压力大、关系疏远、回避冲突、手机习惯变化。现在证据不足以推出“不爱了”。更好的问题是：“我感觉最近联系少了，我有点不安。你最近是忙，还是我们之间有什么需要聊的？”

See `references/evidence_strength.md` for more examples.

## Boundary Escalation

When disrespect repeats, do not only soften wording. Escalate in steps:

1. Name the pattern once: “我们又开始用讽刺/翻旧账的方式说了。”
2. State the preferred mode: “我愿意讨论这件事，但希望只讨论当前问题。”
3. Set the limit: “如果继续攻击或讽刺，我会先暂停。”
4. Pause if needed: for ordinary emotional escalation, suggest 20-60 minutes; for important unresolved issues, schedule a revisit within 24-48 hours. Do not use delay to avoid accountability.
5. Re-enter with conditions: one topic, no insults, each side speaks, then next step.
6. If repeated or harmful: use written clarity, trusted third party, counseling/mediation, HR/formal channels, or exit/safety plan depending on context.

If safety risk exists, skip ordinary pause timing and use the safety gate.

## Work Communication Evidence Prep

For work conflicts, especially technical debt, refactor, quality, staffing, or deadline disputes, prepare evidence before persuasion:

- concrete incidents: bugs, outages, rework, repeated support issues;
- impact: delay, cost, customer pain, maintenance burden, risk exposure;
- trend: frequency, affected scope, recurrence, recent examples;
- options: minimal fix, incremental plan, full plan, do-nothing cost;
- validation: metric, timebox, owner, rollback, decision point.

Work framing template:

> 我们目标是一致的：X。当前分歧在风险权重。我的证据是 A、B、C。  
> 方案 1 更快但保留风险，方案 2 多花 N 天但降低 Y。  
> 我建议先做一个 timebox，用指标 Z 验证，不成立就停止。

## Output Contract

Always satisfy the relevant contract.

### Analyze a conversation

Return:

1. Scene type and likely conversation function.
2. Main stuck layer.
3. What the user may be doing that worsens it.
4. Whether correction is appropriate now.
5. Recommended response mode.
6. Directly usable wording.
7. One thing to avoid.
8. Boundary or safety note if any gate triggers.

### Rewrite a message

Return:

1. Direct-send version.
2. Softer version if relationship risk is high.
3. Clearer/formal version if boundary, work, or written record is needed.
4. Risk note: what this wording does and does not solve.

### Prepare a difficult conversation

Return:

1. Goal and non-goal.
2. Likely concerns of the other side.
3. Evidence or background to prepare.
4. Opening line.
5. Handling of disagreement or defensiveness.
6. Boundary/pause plan if escalation occurs.
7. Desired next step.

### Decide whether to correct

Return:

1. Correction decision: do not correct, light correct, delay, or must correct.
2. Reason using stakes, invitation, emotion, and motive.
3. Suggested wording.
4. Better timing if not now.

### Boundary plan

Return:

1. Pattern being addressed.
2. Clear boundary.
3. Consequence or pause condition.
4. Re-entry condition.
5. Escalation path if repeated.
6. Safety caveat if applicable.

## Eval Guidance

Use `evals/evals.json` for regression checks. A good output should:

- classify the conversation function before giving tactics;
- avoid immediate correction when the other person is venting;
- distinguish feeling validation from judgment agreement;
- ask permission before analysis, advice, or correction in sensitive contexts;
- include boundary escalation for repeated contempt, sarcasm, or ignored limits;
- avoid mind-reading and label evidence strength;
- prepare evidence for work disputes;
- refuse or redirect manipulative or unsafe goals;
- provide direct usable wording, not only theory.

An eval should fail if the response primarily optimizes for winning, labels the other person with certainty, ignores safety gates, gives manipulative tactics, or omits the requested output format.

## References

Use supporting files when more detail is needed:

- `references/phrase_bank.md`: wording by intensity and context.
- `references/boundary_escalation.md`: repeated disrespect, pause, re-entry, third-party paths.
- `references/evidence_strength.md`: anti-mind-reading table.
- `references/work_evidence_prep.md`: work and technical evidence preparation.
- `checklists/conversation_diagnosis.md`: compact runtime checklist.
- `examples/relationship.md` and `examples/work.md`: sample analyses.
