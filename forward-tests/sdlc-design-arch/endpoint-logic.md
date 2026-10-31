# Endpoint logic

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Design the gift cards feature"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`
- Every Endpoint written or changed has `# Validations`, `# Behavior`, `# Flowchart` and `# Sequence diagram`, in that order
- Every Subscription written or changed has `# Validations`, `# Handler`, `# Flowchart` and `# Sequence diagram`, and every path of its flowchart ends in `ack`, `drop`, `retry` or `dead letter`
- Each rule in `# Validations` names one status code from `## Status codes` (a Subscription: `drop`, `retry` or `dead letter`); a rule that cannot fail is in `# Behavior`, and a duplicate is in idempotency, not in `# Validations`
- Every status code in an Endpoint's `## Status codes` is an exit of its flowchart, and the flowchart has no exit that table lacks
- An endpoint with nothing to validate says `No validations.` and still has both diagrams
- The prose is authoritative: each diagram agrees with `# Behavior` or `# Handler`
- `validate` ok
