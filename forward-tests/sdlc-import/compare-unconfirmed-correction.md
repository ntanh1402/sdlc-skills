# Compare unconfirmed correction

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample + orders; then remove the `verified:` line from `wiki/shop/services/SVC-orders/EP-orders-create.md`, commit, push

## Request
"Import the code in ../orders-service"

## Answers
- "take what the code says" for `giftNote`; when shown the file: "save it, I did not check it"

## Expected
- Shows the whole file, not only the difference
- the file is corrected and has no `verified`
