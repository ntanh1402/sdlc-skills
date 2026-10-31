# Add a Reference and link it

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr`.

## Request
"Add our refund policy page https://wiki.acme.example/policies/refunds as a reference: refunds are allowed within 30 days and always go back to the original payment method. Link it from TASK-refund-endpoint"

## Answers
- Approve

## Expected
- Looks in `references/index.md` first and finds no Reference about refunds
- One stop shows the whole new folder (`overview.md`, `log.md`, and a content file only if the person gave the material) and the new `# References` entry on `TASK-refund-endpoint`, with its note
- `references/REF-<name>/overview.md`: `status: Active`, `resource: https://wiki.acme.example/policies/refunds`, a description that says when to consult it, `# Contents` `None` or the content file
- `TASK-refund-endpoint.md` gains `# References` as its last section; its `status`, `# Planned scope` and `# Acceptance` are unchanged
- `CR-order-refund/log.md` has a `**References**` entry
- the Reference's `verified.by` is `human:tester`; `TASK-refund-endpoint.md` is not stamped by `draft finish`
- Draft `edit-REF-<name>`; `validate` ok
