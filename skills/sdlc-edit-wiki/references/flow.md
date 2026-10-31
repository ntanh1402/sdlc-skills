# How sdlc-edit-wiki runs

This file gives the order of one run of `sdlc-edit-wiki`: what to find out
first, when to ask, where to stop for approval, and what to say at the end.
`SKILL.md` gives the allowed edits, refusals and rules for each step.

Work is kept in the draft worktree `WIKI/.worktrees/edit-<key>/`
(`write-protocol.md`, next to this file). Because an allowed wiki edit is
small and exact, this skill uses a short flow with no multi-round interview,
no `plan.md` Run plan, and no separate self-review log.

## 1. The steps

| Step | What you do | Gate |
|---|---|---|
| 1. Look up | Read the target file or files on the wiki's default branch, and check the allowed/refused rules of `SKILL.md` | |
| 2. Question | Ask only when the lookup leaves something undecided (such as which file matches, exact wording, or `releasedAt`), with your proposal | |
| 3. Review | Show the exact changes file by file (old text and new text, or a new Reference in full), plus any refused part and the skill that owns it | **Intent and Design** (one stop together, before starting the draft) |
| 4. Work | Start the draft `edit-<key>`, write the approved changes, check that the input did not change, and run `draft finish` | |
| 5. Change-set | Show `draft diff` and the commit message | **Change-set** |
| 6. Summary | Commit, then print the summary ("Done", "Next", and "For other skills" when part of the request was refused) | |

## 2. The gates

A gate is a stop for the person's explicit approval: first the combined Intent
and Design gate (exact file-by-file changes, before any draft is started),
then the Change-set gate (the diff and commit message, before committing).

- Approval is an explicit yes to the gate's question. "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just write it"),
  stop before the first gate and start no draft. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the changes at step 3, stop and write nothing. When
  the person rejects at the Change-set gate, discard a draft this run started.
- Being asked to run this skill does not approve anything it writes.
- A refusal `SKILL.md` states is a refusal. Do not turn it into a question.

## 3. Summary

End the run with "Done" and "Next", plus "For other skills" when part of a
mixed request was refused:

```text
Done: wiki/edit-FEAT-catalog, 2 files, pushed. Open the pull request.
For other skills: "add a requirement for search filters" (sdlc-write-spec)
Next: Open and merge the pull request for wiki/edit-FEAT-catalog.
```
