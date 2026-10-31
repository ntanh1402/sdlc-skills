# Reject the Run plan

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service"

## Answers
- Design gate: "no, drop it"

## Expected
- The worktree and the branch made in the run are removed: `git -C <dir>/orders-service worktree list` shows one line and `git branch` only `main`
- No code was written
