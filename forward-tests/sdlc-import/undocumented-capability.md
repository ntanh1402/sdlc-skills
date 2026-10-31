# Undocumented capability

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State B

## Request
"Order cancellation has no document; write its feature"

## Answers
- correct the wording of one proposed Requirement; add "an order can be cancelled only once"; then "the list is complete"

## Expected
- Finds the cancel Endpoint and `EXT-shipwell`
- proposes Requirements from them (only a confirmed order, the 30-minute window, a vendor failure leaves the order unchanged) and puts them to the person as one numbered round
- a `Released` Feature with no Reference
- `sources` repeats the code entries
- draft `import-FEAT-<name>`
