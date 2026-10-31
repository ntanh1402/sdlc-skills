# Uncommitted changes in the code folder

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`); then `echo "work in progress" >> <dir>/orders-service/README.md` (not committed). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Does not refuse and does not ask to commit or stash
- After the run `git -C <dir>/orders-service status --short` still shows only ` M README.md`
- The commit on `task/order-note-put` does not hold the `README.md` change
