# The first subtask of a large Task

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`, and no branch `task/order-note-put`). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service, subtask SCRUM-175"

## Answers
- Which part SCRUM-175 covers: "the support_note column of TBL-orders, the migration only"
- Confirm the recommendations of each round
- Approve each gate

## Expected
- The first round asks which part of the Task SCRUM-175 covers, listing the Task's acceptance items and planned scope items, with no recommendation; nothing is planned or written before the answer
- The Intent gate restates `TASK-order-note-put`, the code folder, the branch `task/order-note-put`, the worktree `../orders-service/.worktrees/order-note-put`, the subtask `SCRUM-175` and its part (the `support_note` column of `TBL-orders`), and what is left for other subtasks: `EP-orders-note-put` (the route, `openapi.yaml` and its unit tests)
- The branch is new, made from `origin/main`
- The Run plan's title is `# Run plan: sdlc-build-task, TASK-order-note-put, subtask SCRUM-175`, a line `On:` names the commit of `origin/main`, `## Files` lists only the migration for `support_note`, and `## Not built here` lists `EP-orders-note-put` for other subtasks
- Writes the migration only: no change to `OrderController`, `OrderService`, `openapi.yaml` or the unit tests; runs no test, no build and no code
- The self review checks only the `support_note` part; the Change-set gate shows a commit message whose last three lines are an empty line, `Subtask: SCRUM-175` and `Task: TASK-order-note-put`
- `git -C <dir>/orders-service log --oneline origin/main..task/order-note-put` shows one commit; `git show --stat` has the migration and no `plan.md`; `git ls-remote origin` shows no such branch (not pushed)
- The summary's "Done" names the branch, the worktree and SCRUM-175; the endpoint is not under "Not done"; "Next" says build the next subtask the same way, push and review commit by commit, merge without squashing, then `sdlc-close-task`
