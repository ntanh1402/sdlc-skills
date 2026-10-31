# A commit that is not merged

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service --change orders-service:orders-refund` (the change is on the local branch `feat/orders-refund`, not on `origin/main`).

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- Asked for the commit: the hash that `git -C <dir>/orders-service rev-parse feat/orders-refund` prints

## Expected
- Refuses: the commit is not on `origin/main`, so the code is not merged
- Says the Task is closed after the merge
- No draft; the Task still `Todo`
