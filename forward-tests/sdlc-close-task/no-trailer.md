# No trailer; the person gives the commit

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service --merged orders-service:orders-refund` (the merged commit has no trailer).

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- Asked for the commit: the hash that `git -C <dir>/orders-service rev-parse origin/main` prints
- "yes, it was reviewed"
- Approve each gate

## Expected
- Says no commit on `origin/main` names the Task, and asks for the commit
- Checks that the commit is on `origin/main`, then goes on
- `mergeCommitSha` is that commit; the rest as `trailer-found.md`
