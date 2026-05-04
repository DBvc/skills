# Examples

## Example 1: Commit message from a bootstrap diff

Input:

- Added Electron, React Router, Tailwind, preload bridge, and TypeScript project setup
- Updated README and technical baseline docs

Output:

```text
inf: initialize nyx desktop app baseline

Background:
- bootstrap the first working desktop app foundation for Nyx v0
- lock in the engineering baseline before building chat features

Main changes:
- initialize the Electron, electron-vite, React Router, Tailwind v4, and TypeScript project structure
- add the preload bridge, sandbox-safe preload output, and explicit startup error handling
- add pnpm, Oxlint, Oxfmt, Lefthook, and baseline ignore/config files
- update the README, PRD, and v0 technical baseline docs
```

## Example 2: PR description with concrete validation

Input:

- Fixed a preload bridge regression
- Added an explicit startup error screen when preload is missing
- Restored sandbox mode
- Ran `pnpm lint`, `pnpm typecheck`, and `pnpm build`

Output:

```text
Summary:
- restore the preload bridge to a sandbox-compatible output format
- replace silent renderer fallback data with an explicit startup error state

Why:
- keep the Electron security boundary intact
- make bridge failures visible instead of silently degrading the UI

Validation:
- Automated: pnpm lint, pnpm typecheck, pnpm build
- Manual: started the app and confirmed the renderer no longer crashes on missing bridge state

Risks:
- the Electron and Vite toolchain is still on a relatively new stack, so future dependency bumps should be re-verified
```

## Example 3: Ignore process chatter

Do this:

- summarize the final diff
- mention the shipped behavior
- mention only the validation that actually happened

Do not do this:

- mention that the team debated two options in chat
- mention that the first preload fix was reverted
- mention review comments unless they changed the public result

## Example 4: Replace vague proof with useful validation

Weak:

```text
Proof:
- tested locally
- verified it works
```

Better:

```text
Validation:
- Automated: cargo test
- Manual: opened the settings screen, changed the default model, restarted the app, and confirmed the new setting persisted
- Not run: no end-to-end tests were run
```

## Example 5: Stop on mixed diffs

Input:

- One file hardens preload security
- Another file pins toolchain versions

Preferred output:

```text
This diff contains multiple unrelated themes. Split it before drafting a final commit message.

Suggested split:
- fix: require contextIsolation for the preload bridge
- chore: pin bootstrap toolchain versions
```

Only draft a single merged commit when the user explicitly asks for one.
