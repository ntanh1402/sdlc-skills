# Input changed

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Design the gift cards feature"

## Answers
- After the Design gate, before saying yes: in another shell change `REQ-gift-cards-reject-invalid` on `main` and push
- Then approve

## Expected
- Detects the change at the input check, shows it, returns to the Design gate
