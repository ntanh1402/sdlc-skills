# Flowchart exits

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr`. `CR-order-refund` is `Approved`.

## Request
"Design the tests for the order refund change"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- The coverage matrix at the Design gate lists every exit of `EP-orders-refund.md` `# Flowchart` (`200`, `401`, `404`, `409`, `422`) and every rule of its `# Validations`
- Each exit and each rule is covered by at least one TestCase, and the matrix names the case
- Cases with `testType: integration` exist, because a new Endpoint is in the design
- An exit with no case is shown as a gap and asked about; it is not dropped silently
- `validate` ok
