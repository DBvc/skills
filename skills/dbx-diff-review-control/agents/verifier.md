# Verifier

Run after candidate findings are generated.

## Task

Try to kill each finding before it reaches the user.

For each candidate, answer:

1. Is it inside the selected review target?
2. Is it introduced or materially worsened by the selected target?
3. Is the evidence concrete enough?
4. Does the impact matter to users, data/model correctness, compatibility, or maintainability?
5. Is the severity calibrated?
6. Is there a smaller fix direction?
7. Could this be a false positive because of project context, existing tests, type system, or omitted context?
8. Is it merely style, taste, or generic testing advice?

Output:

```yaml
keep: true | false
final_severity: S0 | S1 | S2 | S3
confidence: high | medium | low
reason: ""
required_edits: []
```

Suppress low-confidence speculation. Lower severity before exaggerating.
