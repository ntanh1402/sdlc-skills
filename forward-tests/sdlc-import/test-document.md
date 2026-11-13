# Test document

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State C

## Request
"Import docs/orders-test-plan.md"

## Answers
- verifies `FEAT-checkout`; no runnable tests exist

## Expected
- the cases go into `TS-checkout`, with no `resource` when it is created; each group they go in is `Approved`; each case has `testType: e2e`, a `testCategory`, a `TC-<id>-<name>` key and a `STORY-*` or `GENERAL/` group
- `orders-test-plan.md` is the content file of the Reference `references/REF-orders-test-plan/`, which each group written links under `# References`
- four TestCases
- case 5 has no expected result: it is not written and is listed under "Could not determine"
- `risk` is proposed from the plan's priority and confirmed
