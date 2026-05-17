# Target Selection and Scope

Use this reference when the review target is not a simple pasted diff.

## Principle

Review the code change the user intends, not every dirty file and not whatever default `git diff` returns.

A review target is a contract:

```yaml
review_target:
  source: staged | unstaged | local | branch | commit | commit_range | selected_files | pasted_patch | pr
  base: ""
  head: ""
  included_files: []
  context_files_read: []
  out_of_scope_dirty_files: []
  target_assumption: ""
```

## Common target phrases

| User wording | Target |
| --- | --- |
| “看看我要提交的改动” | staged/index diff first. If nothing staged, ask whether to review local changes. |
| “只 review staged” / “只看已暂存” | `git diff --cached` only. |
| “看当前工作区” / “current changes” | local changes. Separate staged and unstaged if both exist. |
| “这个 PR” | PR diff or branch diff against merge base. |
| “main..HEAD” / “这几个 commit” | commit range or named commits only. Ignore dirty working tree unless asked. |
| “只看这几个文件” | selected files only, with a selected source such as staged/local/branch. |
| “我贴了 diff” | pasted patch only, unless user asks for repo context. |

## Staged subset handling

Partial staging is common. A file can contain:

- staged hunks intended for commit;
- unstaged hunks kept for debugging or later work;
- untracked files unrelated to the commit.

For commit-ready review, prefer `git diff --cached`. This reviews only the staged hunks, even if the same file has additional unstaged changes.

Report this shape when relevant:

```text
Review 目标: staged/index diff
未纳入范围: 2 个 unstaged 文件、1 个 untracked 文件。它们没有被纳入本次 review。
部分未纳入: `src/foo.ts` 还有 unstaged hunks；本次只 review 它的 staged hunks。
```

Do not criticize unstaged debugging code when the staged target is explicit.

## Selected files

When the user names files, review only those files' changes. It is still valid to read context files to understand data flow, but context files are not target findings unless the selected diff makes them unsafe.

Example:

```text
用户: 只 review src/store/user.ts 和 src/api/user.ts
可读上下文: src/types/user.ts, src/components/Profile.tsx
不能做: 对 src/components/Profile.tsx 中已有坏味道输出普通 finding，除非 selected diff 会触发它。
```

## Commit and range review

For one commit, inspect its patch and affected files. For a range, review the net diff and, when useful, inspect individual commit intent. Uncommitted local changes are out of scope.

Use commit review when the user asks:

- “review abc123”;
- “review HEAD~3..HEAD”;
- “看最近三个 commit 有没有问题”.

## Dirty-state disclosure

Dirty state is not automatically in scope, but it matters because it can confuse the review.

Disclose when relevant:

```text
本次只 review staged diff。当前还有 unstaged: src/debug.ts, src/foo.ts；untracked: tmp.json。它们未纳入结论。
```

If out-of-scope dirty files appear to be required to make the selected diff compile or run, say that the selected target may be incomplete and ask whether to include them.

## Scope drift vs out-of-scope work

Do not confuse these two:

- **Scope drift**: unrelated work inside the selected review target.
- **Out-of-scope work**: dirty or changed files not included in the selected target.

Only scope drift is a finding. Out-of-scope work is a review boundary note unless it creates immediate merge/commit risk.
