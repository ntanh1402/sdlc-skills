---
name: sdlc-close-task
description: Record in the project wiki that the code of one wiki Task is merged - set the Task Done with its merge commit, remove the pending entries of the Design files it covered and mark them live, and move its Feature to InDev or its ChangeRequest to Implemented. Use after a Task's pull request is merged, when a developer asks to close, finish or complete a Task in the wiki. Not for closing a ticket in a tracker, for merging or reviewing code, for marking a Feature released, or for any other change of status.
---

# Close a Task

This skill records that a Task's code is merged. Its input is a Task key and
the one code folder the Task was built in. Its output is one draft,
`wiki/close-<Task key>`, that changes:

- the Task: `status: Done`, `mergeCommitSha`, `mergedAt`;
- each Design file the Task covered: its pending entry removed and, when no
  entry is left, its status set to live;
- the parent: a Feature `Approved` becomes `InDev`; a ChangeRequest whose
  Tasks are now all `Done` becomes `Implemented`.

One Task per run. Section 6 lists what it never does.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. This skill uses the
**short form** of `flow.md` section 8: no rounds and no Run plan, one stop
that is the Intent and the Design gate together, then the Change-set gate.
Then read the schema pages `schema.md` ("Pending changes"), `task.md`,
`feature.md`, `change-request.md` and the page of each Design type in the
Task's scope, in the wiki's `.wiki-llm/schema/`.

The write protocol says never to edit another step's output. Closing is this
skill's own step: the edits listed above are its output, and it makes no
other edit to those files.

Other requests go elsewhere; say so and stop:

| Request | Answer |
|---|---|
| Close, move or comment a ticket in a Tracker | No skill does: a person follows the ticket by hand. Offer to record the merge in the wiki instead, and write nothing until asked |
| Write or fix the Task's code | `sdlc-build-task` |
| Review the code before the merge | `sdlc-review-code` |
| Mark a Feature released or deprecated; add a ticket link to a Task or a user story | `sdlc-edit-wiki` |
| The merged code differs from the design | `sdlc-import` on the code folder compares and corrects; a ChangeRequest with `sdlc-write-spec` when the design should change |
| Push, merge, or open a pull request | The person does that |

## 1. Look up

**The Task.** Find it on the wiki's default branch:
`git ls-tree -r --name-only "$DEFAULT" -- wiki | grep '/TASK-<name>.md$'`.
Refuse, as a refusal and not a question, when:

| Case | Say |
|---|---|
| The Task is `Done` | It is already closed; name its `mergeCommitSha` when it has one |
| The Task is not on the default branch | Name the draft that holds it and ask to merge it first |

When the user gave no code folder, ask for it once. Never guess it; "this
folder" is an answer.

**The merged commit.** In the code folder, read the default branch of the
remote, never a local branch that may hold unmerged work:

```bash
SRC=<the code folder>
git -C "$SRC" fetch --quiet origin
BASE=$(git -C "$SRC" symbolic-ref --quiet --short refs/remotes/origin/HEAD \
  || { git -C "$SRC" show-ref --verify --quiet refs/remotes/origin/main && echo origin/main; } \
  || { git -C "$SRC" show-ref --verify --quiet refs/remotes/origin/master && echo origin/master; })
git -C "$SRC" log "$BASE" --grep='^Task: <Task key>$' --format='%H %cI %s'
```

When the fetch fails or `BASE` is empty, refuse: the folder has no remote
this skill can read, and a commit that is only local is not merged.

- One or more lines: the Task's code is merged. The first line is the newest
  commit: its hash is `mergeCommitSha` and its committer date is `mergedAt`.
- No line: a squash merge dropped the trailer, or the code was written by
  hand. Ask for the commit, then check it is merged:
  `git -C "$SRC" merge-base --is-ancestor <commit> "$BASE"`. A commit that is
  not on `BASE` is not merged: refuse, and say the Task is closed after the
  merge. Read its hash and date with
  `git -C "$SRC" show -s --format='%H %cI %s' <commit>`.

Never call a hosting service, and never compare the code with the Design
files: that is a review.

**The wiki changes.** Read the Task's `# Planned scope`, each Design file it
links, the parent's `overview.md`, and every other Task file in the parent's
folder. Then work out, for each concept in the scope:

| The concept | Change |
|---|---|
| Another `Todo` Task of the same parent links it in its `# Planned scope` | Nothing: the entry stays until that Task is closed |
| No other `Todo` Task of the parent covers it | Remove the parent's entry from `# Pending changes` |
| It has no entry left | Remove the `# Pending changes` section. Status `Active`; or `Deprecated` when it was `Removing`. The file of a removed concept stays, because this Task and its parent link it |
| It still has an entry of another Feature or ChangeRequest | Keep the section and the status |

and for the parent:

| The parent | Change |
|---|---|
| A Feature that is `Approved` | `InDev` |
| A Feature that is `InDev` | Nothing, even when this was its last Task: code merged is not code deployed |
| A ChangeRequest whose other Tasks are all `Done` | `Implemented` |
| A ChangeRequest with another `Todo` Task | Nothing |

**Another close in progress.** `git -C "$WIKI" branch -a --list 'wiki/close-TASK-*' 'remotes/origin/wiki/close-TASK-*'`
lists the close drafts that are not merged. The table above reads the other
Tasks' status on the default branch, so two closes open at once can each keep
an entry the other one should have removed. When such a draft closes a Task
of the same parent that shares a Design file with this one, say so at the
stop of section 3: name the draft and the shared files, and go on. Do not
stop for it. `validate` reports an entry left behind as `pending.leftover`
once both are merged.

## 2. The question

Show the commit or commits found and ask one question: "Was this change
reviewed?"

| Answer | Do |
|---|---|
| Yes | Go on |
| No | Say that `sdlc-review-code` checks a change against the wiki, and ask: review first, or close anyway? "Review first" ends the run with nothing written. "Close anyway" goes on |

## 3. One stop: the Intent and the Design gate

Show the planned wiki changes, file by file, with the commit, and ask for
approval:

```text
Close TASK-coupon-api: merged as 3f2a91c "Add the apply-coupon endpoint" on origin/main.
  TASK-coupon-api.md     status Todo → Done; mergeCommitSha 3f2a91c…; mergedAt 2026-10-12T09:14:00+07:00
  EP-apply-coupon.md     pending entry for FEAT-coupons removed; Planned → Active
  TBL-coupons.md         pending entry kept: TASK-coupon-admin still covers it
  FEAT-coupons/overview  Approved → InDev
Approve?
```

An edit here is shown again before anything is written. A rejection writes
nothing.

## 4. Write, finish and commit

Start the draft `close-<Task key>` as `references/write-protocol.md` section 3
says. The input paths are the Task file, the other Task files of the parent,
the parent's `overview.md` and each Design file in the scope.

Write exactly the changes approved in section 3:

- the Task's frontmatter: `status: Done`, `mergeCommitSha` (the full hash)
  and `mergedAt` (the committer date, with its offset);
- the Design files and the parent, as the tables of section 1 say;
- an entry in the `log.md` of every concept folder you changed, naming the
  Task and the commit, for example
  `* **Close**: TASK-coupon-api is Done; its code is merged as 3f2a91c. EP-apply-coupon is live. Written by an AI model with sdlc-close-task.`

Change nothing else in those files, and write no `index.md`. Then follow
`references/write-protocol.md` section 4 from step 5: the input check,
`draft finish`, the Change-set gate, `draft commit`. Commit message:
`close(<Task key>): <the Task's title>`.

## 5. The build worktree, then the summary

`sdlc-build-task` builds a Task in `<code folder>/.worktrees/<Task name without TASK->/`.
When that folder exists, ask whether to remove it. Remove it only on a yes
and only when it has no uncommitted change
(`git -C "<the worktree>" status --porcelain` prints nothing):
`git -C "$SRC" worktree remove "<the worktree>"`. Otherwise leave it and say
so. Never delete its branch.

End with the summary of the short form, "Done" and "Next":

```text
Done: wiki/close-TASK-coupon-api, 4 files, pushed. Open the pull request.
Next: TASK-coupon-admin is the last Todo Task of FEAT-coupons.
```

When the close leaves every Task of an `InDev` Feature `Done`, "Next" says
that `sdlc-edit-wiki` sets the Feature `Released` when it ships.

## 6. What this skill never does

- It never compares the code with the Design files, and never edits code.
- It never sets a Feature `Released` or `Deprecated`.
- It never touches a TestCase or a TestSuite.
- It never writes `trackerKey`, `resource` or `prUrl`, and never calls a
  hosting service or a Tracker.
- It never deletes a concept's file, and never closes two Tasks in one run.

## Done when

- The merged commit was found by its trailer, or given by the person and
  checked to be on the remote's default branch.
- The person answered whether the change was reviewed.
- The wiki changes were approved file by file before the draft was started.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
- A build worktree was removed only after a yes and only when it was clean.
