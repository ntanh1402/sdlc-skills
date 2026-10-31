# Shared file other task

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

refund, also `--fixture order-refund-second-task`

## Request
"As above"

## Answers
- (none)

## Expected
- The two Acceptance findings stay: this Task's acceptance states them. The difference "refunds an order that is not confirmed" is under "Not checked", naming `TASK-refund-audit`, and is not a Contract finding. The missing audit line is not a finding
