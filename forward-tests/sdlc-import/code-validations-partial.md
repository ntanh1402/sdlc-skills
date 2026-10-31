# Code with validations the import cannot read

## Wiki
Seeding: `forward-tests/seed.sh <dir> --empty --source orders-service`. In `<dir>/orders-service`, before the run, add `src/main/java/com/acme/orders/RequestGuardFilter.java`: a servlet filter on `/orders/*` that only calls `GeneratedRequestGuard.check(request)`, a class that is not in the folder, and returns `400` when it fails; commit it. Neither `openapi.yaml` nor the README mentions it, so the rule it enforces cannot be read.

## Request
"Import the orders service code at ../orders-service"

## Answers
- Confirm each group
- At the gate, no answer for the validations that cannot be read

## Expected
- Every Endpoint written has `# Validations`, `# Flowchart` and `# Sequence diagram`; the two diagrams are drawn from the handler as read, with every branch and exit
- The rules found in the handler (body checks, state checks) and the `401` from `openapi.yaml` are listed, each with one status code
- For the rule hidden in `RequestGuardFilter`, each Endpoint's `# Validations` ends with the line `Not determined by the import.`; the gate asks about it once, in the same question as the other required sections
- No diagram holds `Not determined by the import.`; the import writes no placeholder diagram
- The run lists the Endpoint under "Could not determine" for the unread validation, and no file is left unwritten because of it
- No ADR is written
- `validate` ok
