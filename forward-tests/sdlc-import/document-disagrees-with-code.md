# Document disagrees with code

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State B; then change "200 characters" to "500 characters" in `<dir>/workspace/docs/checkout-prd.md`

## Request
"Import the checkout PRD, docs/checkout-prd.md"

## Answers
- "keep the wiki"

## Expected
- "Disagreements" lists it: the document says 500, the create Endpoint (written from code) says 200
- proposes "keep the wiki" with the reason and does not decide itself
- the Requirement is written with 200
