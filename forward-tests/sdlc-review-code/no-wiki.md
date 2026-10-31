# No wiki

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

none: `mkdir -p <dir>/plain && cp -R forward-tests/sources/orders-service <dir>/plain/`; start the agent in `<dir>/plain`

## Request
"Review ../plain/orders-service against the wiki"

## Answers
- (none)

## Expected
- Stops: "No project wiki is linked to this folder. Run sdlc-setup-wiki in this folder first." No review
