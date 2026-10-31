# Compare designed suite

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample + orders; then set `status: Approved` and remove the `resource:` line in `wiki/shop/tests/TS-checkout/overview.md`, commit, push

## Request
"Import the tests in ../orders-service/tests/e2e; they implement TS-checkout"

## Answers
- "keep the wiki" for every difference

## Expected
- `TC-empty-cart-rejected` is reported as not written yet (no test in the code) and is never offered for deletion
