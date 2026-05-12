---
name: dbx-agent-handoff
description: Use only when the user wants to hand off the current AI agent session state to another AI agent or a future AI session, including context compaction, restart packets, resume notes, or "下个 session/agent 继续". For ambiguous "handoff/交接文档" requests, use only to ask one clarification question and stop. Do not use for human-facing workplace handoff documents, onboarding docs, project transition memos, status reports, meeting summaries, or general summaries.
---

# Agent Handoff

Create a compact restart packet so a fresh AI agent can continue the same work without rediscovering context.

This skill is for AI-session continuity, not human workplace documentation.

## Activation Gate

Use this skill only when the target recipient is clearly one of:

- another AI agent;
- a future AI session;
- a resumed thread;
- a compacted context window for continuing the current task.

Typical triggers:

- "prepare a handoff for the next session"
- "compact this context"
- "write a handoff so another agent can continue"
- "下个 session 继续"
- "给下一个 agent 接手"
- "把当前进度交给新的 Codex/Claude/agent"

Do not use this skill for:

- workplace handoff documents between humans;
- team or project transition docs;
- employee departure handoffs;
- onboarding docs or SOPs;
- client status updates;
- meeting summaries;
- general conversation summaries.

If the user only says "write a handoff document", "handoff", "写交接文档", or "写个交接文档" without saying it is for another AI agent/session, ask exactly one clarification question and stop:

```text
这是给另一个 AI agent/session 继续当前任务用，还是给人看的工作交接文档？
```

If the user says it is for humans, do not use this skill. Handle it as a normal writing task.

## Workflow

1. Identify the continuation focus. If the user provided arguments, treat them as the next session's focus.
2. Collect only the context needed to resume: latest user goal, current workspace, relevant files, git state, important commands and outcomes, produced artifacts, decisions, blockers, and known risks.
3. Prefer references over copying. Link to PRDs, plans, ADRs, issues, commits, diffs, logs, screenshots, or generated files by absolute path, URL, commit, PR, or issue.
4. Exclude secrets. Do not include tokens, passwords, API keys, cookies, private keys, full `.env` files, or credential-bearing logs.
5. Create a new temporary Markdown file:

```bash
mktemp -t handoff-XXXXXX.md
```

6. Write the handoff using the template below.
7. Read the file back once and verify that it is coherent, structurally complete, and free of obvious secrets.
8. Report the saved path to the user.

Use this internal shape while collecting context:

```yaml
handoff_context:
  focus: ""
  current_state:
    done: []
    in_progress: []
    not_done: []
  key_context:
    workspace: ""
    git_state: ""
    files: []
    commands: []
    artifacts: []
  decisions: []
  blockers: []
  next_steps: []
  suggested_skills: []
  excluded_sensitive_material: []
```

## Handoff Template

```markdown
# Handoff

## Focus

What the next AI session should accomplish. If the user supplied a focus, reflect it here.

## Current State

- Done:
- In progress:
- Not done:

## Key Context

- Workspace/repo:
- Git state:
- Relevant files:
- Important commands and outcomes:
- Existing artifacts to read instead of duplicating:

## Decisions Made

- Decision:
  Reason:

## Open Questions And Blockers

- Question/blocker:
  Why it matters:

## Recommended Next Steps

1. First concrete action.
2. Next action.
3. Validation or stopping condition.

## Suggested Skills

- Skill:
  Why:
```

Omit `Suggested Skills` if no skill is relevant. Keep empty sections only when they communicate that nothing is known; otherwise remove empty bullets.

## Quality Bar

A good handoff lets the next AI agent answer these in under one minute:

- What is the user trying to achieve?
- What has already been done?
- Where should I start?
- What must I avoid redoing?
- Which files, commands, and artifacts matter?
- What risks or blockers are known?
- What is the next concrete action?

Revise before completion if the handoff cannot answer those questions.

## Reporting

Final response should be brief:

```text
Handoff written: <absolute path>
```

Add one short note only if there is a blocker, missing context, or important caveat for the user.
