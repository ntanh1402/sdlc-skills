# Requirement document service page only

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State A

## Request
"Import the checkout PRD, docs/checkout-prd.md"

## Answers
- Requirements 1 to 4 are built, 5 is not

## Expected
- Asks about each Requirement, since neither service has contracts
- `FEAT-checkout` is `Released` with four Requirements
- saved cards is left out and listed for a ChangeRequest
- `checkout-prd.md` is the content file of the Reference `references/REF-checkout-prd/`, which `FEAT-checkout` links under `# References`
- `# Architecture` names the two Service pages
- the missing contracts are under "Could not determine"
- draft `import-FEAT-checkout`
- `validate` ok
