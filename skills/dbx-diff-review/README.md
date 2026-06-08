# dbx-diff-review

High-signal concrete code-change review for PRs, branch diffs, staged/index changes, working-tree changes, commit ranges, selected files, and pasted patches.

## Primary value

This skill prevents three common review failures:

1. reviewing the wrong target, especially when only staged hunks should be committed;
2. producing generic checklist comments instead of user-impact/data-model findings;
3. claiming verification without evidence.

## Use with explicit targets

```bash
# Review staged/index diff only. Handles partial staged hunks.
python3 scripts/collect-review-context.py --root /path/to/repo --target staged

# Review branch diff against origin/main.
python3 scripts/collect-review-context.py --root /path/to/repo --target branch --base origin/main

# Review only selected files in staged diff.
python3 scripts/collect-review-context.py --root /path/to/repo --target files --file-scope staged --files src/a.ts src/b.ts

# Review a commit range.
python3 scripts/collect-review-context.py --root /path/to/repo --target commit-range --commit-range main..HEAD
```

The collector is read-only. It does not run test/build commands and does not modify files.

## Relationship to dbx-linus-review

Use this skill for ordinary concrete diff review. Use `dbx-linus-review` for explicit strict pragmatic judgment of diffs, plans, proposals, or over-engineering decisions.
