# Revise

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec --fixture gift-cards-stories`.

## Request
"Split the refused gift card story into one for an expired card and one for an unknown card"

## Answers
- Keep the key `STORY-gift-cards-refused-card` for the expired card
- Confirm the other recommendations
- Approve each gate

## Expected
- `READY` (a revision was asked for)
- `STORY-gift-cards-refused-card.md` is kept, now about an expired card; one new story for an unknown card
- `STORY-gift-cards-pay-with-card.md` is unchanged
- Both refused-card stories list `REQ-gift-cards-reject-invalid`
- The log entry says what was split; `validate` ok on branch `wiki/stories-FEAT-gift-cards`
