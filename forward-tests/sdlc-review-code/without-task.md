# Without task

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

sample, `--source orders-service --change orders-service:orders-refund`

## Request
"Review the branch in ../orders-service against the wiki"

## Answers
- "there is no Task"

## Expected
- Finds `SVC-orders` by its `resource`. Outside the scope, `must fix`: the new endpoint `POST /orders/{id}/refund` has no file in the wiki. Contract, `must fix`: `TBL-orders.md` lacks `refunded_at`, `refund_reason` and the status `refunded`. Acceptance: none, there is no Task
