# A clean build worktree

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service --merged orders-service:orders-refund:TASK-refund-endpoint` (an `Approved` ChangeRequest with one `Todo` Task; its code is on `origin/main` of `<dir>/orders-service` in a commit that ends with `Task: TASK-refund-endpoint`); then `git -C <dir>/orders-service worktree add -b task/refund-endpoint .worktrees/refund-endpoint origin/main` (the worktree a build left).

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate
- Asked whether to remove the worktree: "yes"

## Expected
- After the commit, asks whether to remove `../orders-service/.worktrees/refund-endpoint`
- Removes it: `git -C <dir>/orders-service worktree list` shows one line
- The branch `task/refund-endpoint` still exists
