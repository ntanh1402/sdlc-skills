# A Task that links a code example

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service`; then, on the wiki's default branch, add the Reference of `forward-tests/sdlc-build-task/uses-reference.ref.md` as `wiki/shop/references/REF-request-validation-example/overview.md` with a `log.md`, link it from `TASK-refund-endpoint.md` under `# References` with the note "take the request validation and the error body; ignore its logging", run `python3 .wiki-llm/tools/wiki_llm.py sync`, and commit.

## Request
"Build TASK-refund-endpoint in the orders-service folder"

## Answers
- Approve each gate

## Expected
- Reads `REF-request-validation-example` and the code at its `resource` before planning the files
- The plan names the validation and error-body pattern it takes from the example, and does not copy its logging
- Where the example and `EP-orders-refund.md` differ, the code follows `EP-orders-refund.md`
- The self review reports no finding that cites the Reference as evidence
