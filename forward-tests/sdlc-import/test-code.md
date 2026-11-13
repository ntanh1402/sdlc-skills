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
- refuses the unit folder ("unit and load tests are not imported")
- the cases go into `TS-checkout`, created with `resource` when it does not exist; each group they go in is `Implemented`
- three TestCases `TC-<id>-<test name>`, ids after the highest in the suite, each with `testType: e2e` and a `testCategory`, in the `STORY-*` group of the story the person confirms (linking it with `— AC <n>`) or in `GENERAL/`, each with a `# Steps` table read from the assertions with bold validations, no `# Test data`, and no wiki key in its steps
- `# Covers` links the confirmed Requirements
- draft `import-TS-<name>`
