# Source and State Policy

This reference controls evidence, freshness, persistent learning state, and privacy for `dbx-learn`.

## 1. Source hierarchy

Prefer sources in this order:

1. User-provided artifacts in the current task.
2. Current repository files, code, docs, tests, logs, or rendered output.
3. Official docs, standards, specs, release notes, source code, papers, and author-maintained material.
4. High-quality books, courses, technical articles, and expert explanations.
5. Community threads, examples, anecdotes, and model inference.

When the user asks about current or changing topics, use available browsing or repository tools. If no such tool is available, say that current verification was not performed.

## 2. Freshness rules

Freshness is required for:

- API and framework behavior that may have changed;
- library versions, toolchain features, release status, pricing, schedules, policy, laws, standards, medical, legal, finance, security, and current events;
- “latest”, “recent”, “today”, “this year”, “current best practice”, or similar wording;
- niche repositories, papers, or products when exact details matter.

Stable conceptual explanation can proceed without fresh lookup, but version-sensitive claims should be marked as unverified.

## 3. Evidence labels

Use simple labels when helpful:

```text
source_claim      directly supported by a provided or fetched source
inference         reasoned from supported facts
experience_rule   common engineering judgment, not source-specific
assumption        needed to proceed, may be wrong
unverified        not checked against current sources
```

Do not over-label every sentence in casual mode. Use labels when claims could mislead the user or when the output is a research memo.

## 4. Conflict handling

When sources conflict:

1. Name the conflict.
2. Compare source authority, date, scope, and evidence.
3. Give a temporary working model.
4. Suggest the smallest verification action.

Never hide conflict just to make a cleaner story.

## 5. Persistent state contract

Default behavior: no persistent state write.

Allowed persistent state only when the user asks for it, approves it, or the current repo explicitly defines a learning workspace contract.

State fields:

```yaml
state_contract:
  owner: user
  lifetime: session | project | until_replaced
  read_from: []
  write_to: []
  approval_required: true
  update_when: demonstrated_understanding | corrected_misconception | completed_rep | goal_changed
  stale_policy: "Review before reuse if older than the project or topic context allows."
  rollback: "Remove or mark stale when contradicted by later evidence."
```

Recommended workspace:

```text
learning/
  MISSION.md          why this learning effort exists, success criteria, non-goals
  RESOURCES.md        curated sources, not every link seen
  GLOSSARY.md         terms and distinctions the user wants to retain
  REVISIT.md          spaced review candidates
  learning-records/   demonstrated understanding and corrected misconceptions
  practice/           reps, feedback, and artifacts
  research/           source digests and research memos
```

## 6. Write approval

Before writing or modifying state, report:

- target path;
- whether the file exists, if known;
- summary of proposed content;
- why the content deserves persistence;
- whether this overwrites or appends;
- rollback or deletion method.

If the user explicitly says “create the workspace and files”, that counts as approval for those named files. Still report what was written.

## 7. Privacy and safety

Do not write private messages, secrets, credentials, private identifiers, or sensitive personal details into reusable learning state unless the user explicitly asks and the location is private.

For high-risk domains:

- Convert unsafe operational requests into safe educational learning goals.
- Do not provide actionable wrongdoing, exploitation, evasion, manipulation, or guaranteed financial/medical/legal conclusions.
- For investment, medical, legal, or security topics, distinguish education from advice or operational action.
