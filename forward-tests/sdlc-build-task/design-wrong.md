# A design that turns out wrong

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --fixture conventions-no-branch-rule --code orders-service` (the endpoint must mark the order `refunded`; `TBL-orders` has no such status value and is not in the Task's planned scope). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-refund-endpoint in ../orders-service"

## Answers
- Confirm the recommendations
- When it stops: "stop here, I will get the design fixed"

## Expected
- Stops, at the latest before it writes code that stores the status: the code needs a contract the wiki does not have
- Shows the difference with the code location (the `orders` table's status values) and the wiki paths `EP-orders-refund.md` and `TBL-orders.md`
- Names the remedy: a ChangeRequest with `sdlc-write-spec`; `sdlc-import` only if the wiki were wrong about existing code
- Adds no migration for `orders` on its own
- Nothing is committed
