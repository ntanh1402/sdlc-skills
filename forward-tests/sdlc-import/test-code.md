# Test code

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State C

## Request
"Import the tests in ../orders-service/tests"

## Answers
- verifies `FEAT-checkout`; confirm the Requirements proposed for each test; accept the proposed risks

## Expected
- Sees `e2e` and `unit`
- refuses the unit folder ("unit tests are not imported")
- one TestSuite, `Implemented`, `suiteType: e2e`, with `resource`
- three TestCases keyed from the test names, each with a `# Steps` table read from the assertions
- `# Covers` links the confirmed Requirements
- draft `import-TS-<name>`
