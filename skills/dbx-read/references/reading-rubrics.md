# Reading Rubrics

Use this reference when deeper judgment is needed.

## 1. Technical article rubric

Ask these questions:

1. What concrete bottleneck, risk, contradiction, or failure mode is the source addressing?
2. Is the problem real under the user's likely engineering context?
3. What assumptions are required for the argument to hold?
4. What is the mechanism, not just the conclusion?
5. Where does complexity move?
6. What does the solution optimize for: speed, correctness, operability, cognition, cost, leverage, trust, adoption?
7. What does it degrade or make harder?
8. What would be the smallest safe experiment?
9. Which part is transferable, and which part is local to the author's context?
10. What question should the user ask next?

Output should make the user's future technical judgment sharper.

## 2. Architecture / engineering system rubric

Look for:

- source of truth and ownership;
- state boundaries;
- dependency direction;
- feedback loops and validation topology;
- migration path and reversibility;
- operational failure modes;
- team cognition and maintenance cost;
- observability and debugging surface;
- AI-agent operability where relevant.

Avoid declaring a pattern “good” without context. Architecture is not a museum label; it is a bet under constraints.

## 3. AI / agent article rubric

Check:

- What capability is being claimed?
- Is it demo, product behavior, research result, anecdote, or benchmark?
- What is the trust boundary: model output, tool output, human review, eval, sandbox, permissions?
- What data leaves the user's environment?
- What failure modes are measured versus hand-waved?
- What changes in workflow adoption, not just model performance?
- What would a small local pilot need to prove?

## 4. Paper rubric

Read papers by separating claim, method, and validity.

Key questions:

1. What is the paper trying to establish?
2. What would count as evidence against it?
3. Are baselines fair and current?
4. Are metrics aligned with the real-world use case?
5. Are experiments reproducible from the information provided?
6. Does the paper overclaim outside the tested distribution?
7. Is the contribution conceptual, empirical, algorithmic, dataset/tooling, or position-setting?
8. What should a practitioner actually do differently?

## 5. Essay / book chapter rubric

For non-technical essays or books:

- What pressure or question animates the text?
- What distinction does it introduce?
- What belief is it trying to loosen or strengthen?
- What would be lost if this section were removed?
- Which claims are argument, observation, metaphor, memoir, or mood?
- What can be accepted without accepting the whole worldview?

## 6. Translation-for-understanding rubric

When translating to understand:

- Preserve conceptual structure before polish.
- Explain terms with cultural, domain, or historical distance.
- Mark ambiguity instead of flattening it.
- Give literal translation only when wording matters.
- Do not turn translation into publication copy unless routed to a writing/transcreation skill.

## 7. Anti-patterns

Avoid:

- Summary confetti: many bullets with no hierarchy.
- Equal-weight disease: treating every paragraph as equally important.
- Source soup: blending multiple sources before showing individual positions.
- False mastery: reading note presented as learning completion.
- Trend smoke: confident claims about current products/APIs without current evidence.
- Quote wallpaper: long excerpts used instead of analysis.
- Vibe critique: saying “有启发/有问题” without mechanism, boundary, or evidence.
