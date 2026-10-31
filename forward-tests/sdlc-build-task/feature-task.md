# A Feature's Task

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Reads the Task, `EP-orders-note-put.md`, `TBL-orders.md`, `FEAT-order-notes` and `conventions.md` on the wiki's default branch
- Questions come in numbered rounds with a recommendation each; the first round names the Task, the code folder, the branch `task/order-note-put` and the worktree `../orders-service/.worktrees/order-note-put`
- One Intent gate, after the rounds
- The worktree is made from `origin/main`; `<dir>/orders-service/.git/info/exclude` holds `.worktrees/` and `/plan.md`; `.gitignore` of the repository is not created or changed
- At the Design gate the Run plan is shown alone and in full: `plan.md` at the root of the worktree lists each code file and unit-test file with the scope item and the acceptance item it serves
- Writes the endpoint, the migration for `support_note` and unit tests; runs no test, no build and no code
- The Change-set gate shows the diff, a commit message that ends with `Task: TASK-order-note-put`, and what the self review checked, fixed and could not check
- One commit on `task/order-note-put`; `git show --stat` has no `plan.md`; `git ls-remote origin` shows no such branch (not pushed)
- The checkout of `<dir>/orders-service` is still on `main` and unchanged
- The last message is the summary: "Done" names the branch and the worktree, "Next" says push, pull request, review, merge, then `sdlc-close-task`
