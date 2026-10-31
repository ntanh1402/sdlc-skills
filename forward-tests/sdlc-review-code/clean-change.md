# Clean change

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

sample, `--source orders-service --change orders-service:orders-tidy-create`

## Request
"Review the branch in ../orders-service against the wiki"

## Answers
- "there is no Task"

## Expected
- "0 must fix, 0 should fix". The `giftNote` field the code already accepts is not a finding of this change
- it may be named under "Not checked" as Drift for `sdlc-import`
