# Writing a task-close draft to the project wiki

This file says how `sdlc-close-task` drafts, checks, approves and commits its
changes to the wiki. `SKILL.md` says what to write; this file says how.

Read it at `SKILL.md` section 4.

## 1. The rules

- Every change goes into a **draft**: a branch `wiki/close-<Task key>` with its
  own worktree in `WIKI/.worktrees/close-<Task key>/`. The default branch
  changes only when the user merges the draft's pull request.
- Stop at the approval gates of `SKILL.md`: first the combined Intent and Design
  stop (showing the planned wiki changes file by file, before starting the
  draft), then the Change-set gate.
- Never merge, never open a pull request, never call a hosting service; the
  user does that.
- Edit only what `SKILL.md` lists for closing a Task: the Task's frontmatter
  (`status: Done`, `mergeCommitSha`, `mergedAt`), the `# Pending changes`
  entries and live statuses of the Design files in its scope (when the parent
  is `Approved` or `InDev`), the parent's `status` (`InDev` or `Implemented`),
  and the `log.md` of each concept folder changed. Never edit an `index.md` or
  any tool-written section; `draft finish` writes those.

## 2. The draft key

The key is `close-<Task key>`, for example `close-TASK-coupon-api`.

**First, look for a worktree.** When `WIKI/.worktrees/close-<Task key>/`
exists, an earlier run started this draft and did not commit it. Never discard
it automatically: show the user `git status` in it and ask whether to go on
from those files or to discard them.

Otherwise decide what to do after `git fetch --quiet origin 2>/dev/null`:

1. **The Task is not on the default branch.** Stop. If
   `git branch -a --list 'wiki/*-*' 'remotes/origin/wiki/*-*'` shows the draft
   that holds it, say: "<Task key> is in draft `wiki/<that branch>`, not on
   `<default>`. Merge its pull request first."
2. **`wiki/close-<Task key>` exists and is not merged** into the default branch
   (`git merge-base --is-ancestor wiki/close-<Task key> "$DEFAULT"` fails).
   This is a revision, for example after review:
   `$T draft resume close-<Task key>`. Tell the user that new commits join any
   pull request open for that branch.
3. **`wiki/close-<Task key>` exists and is merged.** Run
   `$T draft discard close-<Task key> --remote`, then
   `$T draft start close-<Task key>`. Everything on that branch is already on
   the default branch, so deleting it loses nothing. If your environment
   refuses the deletion, ask the user to run the same `draft discard` command,
   then continue.
4. **Otherwise** `$T draft start close-<Task key>`.

## 3. The commands of each section

Each part is for the section of `SKILL.md` it names.

### At section 4: Write, finish and commit

**Draft.** Start or resume `close-<Task key>` (section 2). Then:

```bash
cd "$WIKI/.worktrees/close-<Task key>"
READ=$(git rev-parse "$DEFAULT")
```

Read the input again here, from the default branch at `READ`.

**Write** the approved changes under `wiki/` in the worktree. Add an entry
to the `log.md` of every concept folder you change, under today's date,
newest first:

```markdown
## 2026-10-12

* **Close**: TASK-coupon-api is Done; its code is merged as 3f2a91c. EP-apply-coupon is live. Written by an AI model with sdlc-close-task.
```

**Input check.** Check whether the input changed on the default branch
since you read it:

```bash
git fetch --quiet origin 2>/dev/null
git diff --quiet "$READ" "$DEFAULT" -- <the input paths> || git diff --stat "$READ" "$DEFAULT" -- <the input paths>
```

If it changed, show the user what changed and return to the combined
Intent/Design gate (`SKILL.md`, section 3). Do not merge the default branch
in here: `$T refresh` is for a pull request that has conflicts (section 4).

**Finish.** Stamp, check and validate:

```bash
$T draft finish --by "sdlc-close-task/<the line in RELEASE>" --verified-by
```

`--verified-by` without a value records the person in
`git config user.email` as having confirmed the files; their approval at the
gates is that confirmation. If `ok` is false, fix what `missing_logs` and
`validate.errors` report and run it again. Never record a model name.

**Change-set gate.** Run `$T draft diff`. Show the files it lists (those
marked `authored: false` were written by the tool) and the commit message
`close(<Task key>): <the Task's title>`. Ask for approval.

**Commit, then the summary.**

```bash
$T draft commit -m "<message>"; cd "$WIKI"
```

Run both in one command: `draft commit` removes the worktree you are in.
Judge the result by the JSON it prints (`ok`, `branch`, `pushed`), not by an
error about the current directory. In the summary, "Done" names the branch
`wiki/close-<Task key>` and says the user opens the pull request. If there
is no remote, say the branch must be pushed first.

## 4. When a step goes wrong

| Situation | Do |
|---|---|
| `draft start` says the branch exists | Use section 2 again; never delete a draft that is not merged |
| The pull request has conflicts, because another draft was merged first | `$T draft resume close-<Task key>` if the worktree is gone, then `$T refresh` in it. It resolves conflicts in tool-written files itself; for a file a person writes it stops and names it: resolve it with git and run `$T refresh` again |
| `draft finish` says `git config user.email` is not set | Ask the user for the id to record, and pass it: `--verified-by human:<id>` |
| `draft commit` refuses because files changed after `finish` | Run `draft finish` again |
| The user abandons the change | `cd "$WIKI" && $T draft discard close-<Task key> --remote` |
