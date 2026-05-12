# Interview Guide for Skill Portfolio Audits

Use interviews to fill gaps after inventory. Do not ask all questions by default. Pick the smallest set that changes a decision.

## Fast five

1. Which 5 to 10 skills do you remember using in the last month?
2. Which skills feel valuable enough that losing them would hurt?
3. Which skills do you only want to invoke manually?
4. Which repos or work domains should have their own project-scoped skills?
5. Are you willing to share redacted invocation evidence, or should the audit rely on your summary?

## Deeper questions

### Usage and value

- Which skills have produced outputs you actually shipped, merged, or reused?
- Which skills were interesting experiments but no longer part of your workflow?
- Which skills replaced old prompts or manual checklists?
- Which skills have caused wrong activation, annoying verbosity, or task derailment?

### Scope

- Which skills are useful across all coding work?
- Which are tied to one company, project, repo, framework, or stack?
- Which should live beside project code in `.agents/skills` rather than in user scope?
- Which skills are relevant only during releases, migrations, incidents, audits, or one-off setup?

### Risk and trust

- Which installed skills came from unknown third-party repos?
- Are any skills allowed to run scripts, network calls, package installs, or destructive commands?
- Are any skills handling credentials, private data, compliance, money, medical/legal/financial advice, or interpersonal risk?
- Do you want risky skills disabled first, then reviewed later?

### Desired operating model

- Do you prefer aggressive cleanup or reversible quarantine?
- Should recommendations optimize for minimal context, maximum availability, or balanced reliability?
- Should the audit create config snippets only, or also prepare a PR for the skills repo?
- What rollback path is acceptable if a skill is removed from global discovery?

## Observation window

When usage evidence is missing, propose a reversible observation window:

```yaml
observation_window:
  duration: "2-4 weeks"
  action: "disable or explicit-only low-confidence skills"
  evidence_to_collect:
    - explicit invocations
    - moments user misses a disabled skill
    - wrong-trigger incidents
    - tasks where project-scoped skill would help
  rollback: "restore from archive or re-enable config"
```
