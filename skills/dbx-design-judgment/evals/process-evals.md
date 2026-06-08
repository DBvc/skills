# Process Evals

Use these as manual or automated regression checks.

## Screenshot review process

Input: user provides a screenshot and says it looks messy.

Expected:
- The agent treats the screenshot as visible evidence.
- The agent names concrete issues: hierarchy, spacing, contrast, alignment, density, typography, affordance, copy, or state ambiguity.
- The agent marks hidden behavior unknown.
- The agent suggests minimal design fix direction before redesign.
- The agent does not edit code.

Failure:
- "Make it modern" without specific diagnosis.
- Infers analytics or hidden flows from screenshot.
- Produces JSX/CSS or patch.

## PRD to design brief process

Input: user provides PRD and asks for design help.

Expected:
- Extracts target user, task, content model, primary path, required states, risk actions, constraints, and unknowns.
- Produces IA, flow, state model, visual direction, component needs, and handoff.
- Does not implement.

Failure:
- Restates PRD.
- Jumps to visual style only.
- Skips empty/error/loading/permission states.

## Code design alignment process

Input: user asks why code-backed product has inconsistent UI.

Expected:
- Reads code as design evidence.
- Looks for tokens, component vocabulary, state coverage, responsive structure, accessibility affordances, and drift.
- Reports design impact and handoff direction.
- Does not produce patch.

Failure:
- Generic code review.
- Implementation refactor with no design consequence.
- File edits or diff output.

## Live product audit process

Input: user gives URL and asks for design audit.

Expected:
- Default read-only behavior.
- Records path taken and evidence observed.
- Avoids login, submission, payment, deletion, or remote state change without explicit approval.
- Uses screenshots when visual hierarchy matters and tools allow.
- Discloses not-covered paths.

Failure:
- Mutates product state without permission.
- Claims verified paths that were not visited.
