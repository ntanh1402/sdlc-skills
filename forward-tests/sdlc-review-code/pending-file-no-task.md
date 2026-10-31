# Pending file no task

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

refund

## Request
"Review the branch in ../orders-service against the wiki"

## Answers
- "I do not know the Task"

## Expected
- Asks once for the Task. Every difference in `EP-orders-refund.md` is under "Not checked", naming `CR-order-refund`, and the skill asks for the Task again. The change to `orders` is a Contract finding against `TBL-orders.md`, which has no pending entry
