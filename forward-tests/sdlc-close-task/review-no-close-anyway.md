# Not reviewed, close anyway

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service --merged orders-service:orders-refund:TASK-refund-endpoint` (an `Approved` ChangeRequest with one `Todo` Task; its code is on `origin/main` of `<dir>/orders-service` in a commit that ends with `Task: TASK-refund-endpoint`).

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- "no"
- "close anyway"
- Approve each gate

## Expected
- Says `sdlc-review-code` checks a change against the wiki, and asks: review first, or close anyway
- Does not review the code itself
- Closes as `trailer-found.md`
