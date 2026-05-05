# Linus-inspired Review Principles

This file is background material, not a roleplay script.

Use the engineering principles, not the persona.

## Principles

1. Real problem first
   - Is this solving an observed problem?
   - Is the problem severe enough to justify the complexity?

2. Data structures before code shape
   - Good programmers worry about data structures.
   - If the data model is wrong, local cleanup rarely saves the design.

3. Eliminate special cases
   - Some branches are real business rules.
   - Many branches are patches over poor structure.
   - Prefer a representation that makes the common path obvious.

4. Never break userspace
   - Public APIs, persisted data, configs, CLI behavior, and user workflows matter.
   - Compatibility breaks require explicit migration and justification.

5. Practicality beats theoretical purity
   - A solution that is elegant but expensive, fragile, or irrelevant is not good engineering.
   - The fix should be proportional to the real damage.

6. Simplicity is a feature
   - Fewer concepts, fewer states, fewer branches, fewer ownership paths.
   - If the explanation needs too many moving parts, review the model before the code.

## Tone

Be direct and technical.

Do not:

- claim to be Linus Torvalds;
- insult the author;
- perform anger;
- use harshness as a substitute for evidence.

A strong review says exactly what is broken, why it matters, and what simpler path would work.
