# Frontend

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

sample, `--source shop-web --change shop-web:web-order-history`

## Request
"Review the branch in ../shop-web against the wiki"

## Answers
- "there is no Task"

## Expected
- Finds `WEB-storefront` by its `resource`. Outside the scope, `must fix`: the new page calls `GET /orders`, an endpoint the wiki has no file for, and `WEB-storefront` lists neither the call under `# Calls` nor the route `/orders`
