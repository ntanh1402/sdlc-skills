# Reject design

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

empty + orders

## Request
"Import the code in ../orders-service"

## Answers
- approve the Intent gate; at the first group: "no, stop the import"

## Expected
- No branch `wiki/import-*` and no worktree remain
- `main` unchanged
