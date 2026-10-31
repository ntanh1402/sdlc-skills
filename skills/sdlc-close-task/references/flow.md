# How sdlc-close-task runs

This file gives the order of one run of `sdlc-close-task`: what to find out
first, what to ask, where to stop for approval, and what to say at the end.
`SKILL.md` gives the exact rules for each step.

Work is kept in the draft worktree `WIKI/.worktrees/close-<Task key>/`
(`write-protocol.md`, next to this file). Because closing a Task is a small,
exact change, this skill uses a short flow with no question rounds, no
`plan.md` Run plan, and no separate self-review log.

## 1. The steps

| Step | What you do | Gate |
|---|---|---|
| 1. Look up | Read the Task and its scope on the wiki's default branch, and find the merged commit on the code repository's remote default branch | |
| 2. Question | Show the merged commit(s) found and ask whether the change was reviewed | |
| 3. Review | Show the planned wiki changes file by file, with the commit | **Intent and Design** (one stop together, before starting the draft) |
| 4. Work | Start the draft `close-<Task key>`, write the approved changes, check that the input did not change, and run `draft finish` | |
| 5. Change-set | Show `draft diff` and the commit message | **Change-set** |
| 6. Summary | Commit, ask whether to remove a clean build worktree if one exists, then print the two-line summary ("Done" and "Next") | |

## 2. The gates

A gate is a stop for the person's explicit approval: first the combined Intent
and Design gate (file-by-file changes, before any draft is started), then the
Change-set gate (the diff and commit message, before committing).

- Approval is an explicit yes to the gate's question. "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just close it"),
  stop before the first gate and start no draft. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the changes at step 3, stop and write nothing. When
  the person rejects at the Change-set gate, discard a draft this run started.
- Being asked to run this skill does not approve anything it writes.
- A refusal `SKILL.md` states is a refusal. Do not turn it into a question.

## 3. Summary

End the run with "Done" and "Next" only:

```text
Done: wiki/close-TASK-coupon-api, 4 files, pushed. Open the pull request.
Next: TASK-coupon-admin is the last Todo Task of FEAT-coupons.
```
