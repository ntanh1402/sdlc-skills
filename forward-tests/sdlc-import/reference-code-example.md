# A code example as a Reference

## Wiki

Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample + orders

## Request
"Keep the orders service's OrderController as the example of how we validate a request body, so whoever builds the next endpoint follows it"

## Answers
- pin it at the commit the folder is at; follow the validation and the error body, do not copy the logging; link it from the Service `SVC-orders`
- Approve each gate

## Expected
- Kind reference; draft `import-REF-<name>`, a name about request validation, not the file name
- Does not ask whether the code is built and running
- `references/REF-<name>/overview.md`: `status: Active`, `resource` the repository URL with the path at the commit (no branch name), `stale_after` proposed, a description that says when to consult it, the summary says what to follow and what not to copy, `# Contents` `None`
- No code copied into the wiki; no Design file, Feature or decision written
- `SVC-orders/overview.md` gains `# References` with the Reference and a note; its `status` and `verified` are unchanged, and `SVC-orders/log.md` has a `**References**` entry
- the Reference's `# Referenced by` lists `SVC-orders`, written by the tool
- `validate` ok
