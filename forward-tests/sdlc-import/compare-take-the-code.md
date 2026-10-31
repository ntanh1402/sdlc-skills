# Compare take the code

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample + orders

## Request
"Import the code in ../orders-service"

## Answers
- "take what the code says" for both differences; approve the new files

## Expected
- Says `SVC-orders` is already in the wiki and that it will compare
- the findings list has `EP-orders-create.md` (the code accepts `giftNote`), `TBL-orders.md` (column `gift_note`), `EP-orders-get.md` matching, and as new the list and cancel Endpoints and `EXT-shipwell`
- asks about one difference at a time
- both files are corrected, still `Active`, still `verified`
- a `**Correction**` entry naming the commit in `SVC-orders/log.md` and `DB-shop/log.md`
- no ChangeRequest and no `# Pending changes` is written
