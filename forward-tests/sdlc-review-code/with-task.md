# With task

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

refund

## Request
"Review the branch in ../orders-service against the wiki for TASK-refund-endpoint"

## Answers
- (none)

## Expected
- Names the base (`main`), the branch and the wiki commit
- reviews against `EP-orders-refund.md` although it is `Planned`: the file holds the target. Acceptance, `must fix`: a request without `reason` is accepted, not 422
- a second refund is not refused with 409. Contract, `must fix`: the file says 409 unless the order is `confirmed`, the code refunds an order in any status. Outside the scope, `must fix`: the migration adds two columns and a status value to `orders`
- `TBL-orders.md` is not in the Task's planned scope. Convention, `should fix`: an endpoint that moves money takes no client idempotency token. Every finding cites a code location and a wiki path
- the `409` finding cites `EP-orders-refund.md` `# Flowchart` (the path "Status is confirmed? no" ends in `409`); the `reason` finding cites `# Validations` (`reason` is 1 to 200 characters, fails with `422`)
- the `401` exit is under "Not checked": Spring Security enforces it outside the changed code, and the change does not bypass it
- no finding for a `500` the framework adds
- the last line counts the findings
- there is no verdict
- the last line says the Task is closed with `sdlc-close-task` after the merge
