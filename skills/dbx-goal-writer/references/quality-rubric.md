# Goal quality rubric

A goal is ready when it answers:

1. What outcome should exist?
2. What files, directories, or discovery boundaries are relevant?
3. What may change?
4. What must not change?
5. Which constraints matter?
6. What observable behavior proves completion?
7. Which commands or manual checks validate it?
8. When should Codex pause and ask?
9. What budget or stop rule prevents unproductive continuation?
10. What final report should Codex provide?

Common failure modes:

- Vague objective: "optimize", "clean up", "make better".
- No non-goals.
- No validation.
- Validation commands invented without checking the repo.
- Scope too broad for one `/goal` run.
- Goal file contradicts `AGENTS.md` or repository conventions.
- A huge goal file with no summary in the actual `/goal` command.
- No instruction for budget exhaustion, blocked progress, or incomplete verification.
