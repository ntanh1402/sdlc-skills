# General review

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

sample, `--source orders-service --change orders-service:orders-refund`

## Request
"Review my code in ../orders-service for bugs and style"

## Answers
- (none)

## Expected
- Does not run a wiki review unasked: either the skill is not chosen, or it says it reviews only against the wiki and asks whether that is wanted
