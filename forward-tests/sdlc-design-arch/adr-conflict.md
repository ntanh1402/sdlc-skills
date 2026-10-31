# Adr conflict

## Wiki
`forward-tests/seed.sh <dir> --fixture checkout-double-order-cr` (a `ReqApproved` ChangeRequest on `FEAT-checkout` whose Requirement says "a repeated checkout submission creates a second order").

## Request
"Design it"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- `CONFLICT` with `ADR-idempotent-checkout`
- Shows both with paths
- Asks before designing
