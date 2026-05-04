# Scenario Skill Architect v6

A scenario-first skill architect for creating, critiquing, improving, and evaluating reusable agent skill packages.

V6 adds **domain substance gates** so domain/content skills do not become merely well-structured but shallow. It requires domain variables, hidden failure modes, data-source policy, expert quality checks, worked examples, and content-quality evals before treating a domain skill as production-ready.

## Best use

Use for:

- creating a reusable skill from a recurring scenario;
- critiquing an existing skill;
- patch-first skill improvement;
- designing runner-compatible evals;
- triaging one-off / unsafe / underspecified requests;
- discovering domain substance before building travel, news, repair, relationship, prediction, content, or architecture skills.

Do not use to wrap one-off prompts into full skills.

## Key routes

- `full_skill`: all hard gates pass, and domain gates pass when applicable.
- `mini_skill`: lightweight reusable wrapper.
- `needs_clarification`: hard gates are unknown.
- `domain_discovery`: hard gates likely pass, but domain substance is unknown.
- `checklist`, `direct_answer`, `refuse_or_redesign`: triage alternatives.

## Validation

```bash
python scripts/lint_skill_package.py .
python scripts/run_skill_evals.py evals/evals.json --validate-only
python scripts/check_architect_output.py captured-output.md
```

## Core idea

Structure is necessary but not sufficient. A good skill must be:

1. reusable,
2. bounded,
3. evaluable,
4. safe,
5. content-substantive for its domain.

For domain skills, the architect must ask: what would make this output look complete but fail in real use?
