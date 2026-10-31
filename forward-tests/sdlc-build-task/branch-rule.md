# A branch naming rule in conventions.md

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --code orders-service` (the sample's `conventions.md` names branches `feat/<area>-<slug>`). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- The branch follows the rule, for example `feat/orders-order-note-put`; it is not `task/order-note-put`
- The worktree is still `../orders-service/.worktrees/order-note-put`
- The commit message still ends with `Task: TASK-order-note-put`
