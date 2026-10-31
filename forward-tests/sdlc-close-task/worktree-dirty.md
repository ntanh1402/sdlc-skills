# A build worktree with uncommitted changes

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service --merged orders-service:orders-refund:TASK-refund-endpoint` (an `Approved` ChangeRequest with one `Todo` Task; its code is on `origin/main` of `<dir>/orders-service` in a commit that ends with `Task: TASK-refund-endpoint`); then `git -C <dir>/orders-service worktree add -b task/refund-endpoint .worktrees/refund-endpoint origin/main` (the worktree a build left), and `echo draft > <dir>/orders-service/.worktrees/refund-endpoint/notes.txt`.

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate
- Asked whether to remove the worktree: "yes"

## Expected
- Does not remove the worktree: it has an uncommitted file; says so
- `notes.txt` is still there
