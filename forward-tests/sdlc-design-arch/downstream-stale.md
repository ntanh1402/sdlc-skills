# Downstream stale

## Wiki
`forward-tests/seed.sh <dir> --fixture checkout-endpoint-cr` (a `ReqApproved` ChangeRequest on `FEAT-checkout` that changes the order-creation endpoint).

## Request
"Design it"

## Answers
- Confirm the recommendations of each round
- No `Todo` Task has started
- Approve each gate

## Expected
- Lists `TASK-order-creation-endpoint` and `TS-checkout` as possibly out of date
- Asks in a round which `Todo` Tasks have started
- Does not edit them
- The Run plan has them under `## For other skills`, naming `sdlc-plan-tasks` and `sdlc-design-tests`
- The summary has a "For other skills" line
