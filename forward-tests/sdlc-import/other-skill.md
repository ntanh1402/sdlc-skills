# A change another skill owns

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

empty + orders

## Request
"Import the code in ../orders-service"

## Answers
- To the question about what else in the wiki this source touches: "yes, we are about to add a refund endpoint to this service. Put it in as well"
- Confirm the other recommendations
- Approve every group and gate

## Expected
- Writes no file for a refund endpoint, and no file with `Planned` or a `# Pending changes` entry
- Says something not built yet is written with `sdlc-write-spec`
- The Run plan has it under `## For other skills`
- The summary has a "For other skills" line naming `sdlc-write-spec`
