# Compare ssh remote

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample + orders; then `git -C <dir>/orders-service remote set-url origin git@github.com:acme/orders-service.git`

## Request
"Import the code in ../orders-service"

## Answers
- stop at the Intent gate

## Expected
- Matches `SVC-orders` by `resource` although the remote is an ssh URL
