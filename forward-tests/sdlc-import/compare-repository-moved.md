# Compare repository moved

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample + orders; then `git -C <dir>/orders-service remote set-url origin https://github.com/acme/orders.git`

## Request
"Import the code in ../orders-service"

## Answers
- confirm the match; "take what the code says" for `resource`

## Expected
- No `resource` matches
- proposes the key `SVC-orders`, finds it, and asks to confirm the match
- lists `resource` among the differences
