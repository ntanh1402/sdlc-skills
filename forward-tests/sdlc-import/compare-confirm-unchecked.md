# Compare confirm unchecked

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State E

## Request
"Import the code in ../orders-service"

## Answers
- "yes, confirm it"

## Expected
- Everything matches
- says nobody confirmed the Table file and offers to confirm it
- afterwards the file has `verified` and the same `generated` as before
- the folder's log has a `**Verification**` entry
