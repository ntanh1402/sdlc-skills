# Code after architecture

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State A

Keep the directory.

## Request
"Import the code in ../orders-service"

## Answers
- approve

## Expected
- Finds `SVC-orders` by `resource` and says it will compare
- the Service page's new fields and links are shown as differences
- the Endpoints, the Table, the Channel and the external are new files at the Design gate
- the call to the payments service is under "Could not determine" (`SVC-payments` has no Endpoint)
- draft `import-SVC-orders`
