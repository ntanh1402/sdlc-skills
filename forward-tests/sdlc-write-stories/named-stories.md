# Named stories

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Write these user stories for gift cards. 1: As a customer, I want to pay with my gift card, so that I use the money on it. 2: As a customer, I want to know when my card can't be used, so that I can pay another way."

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- The two stories keep the sentences as the request worded them; the skill does not split, merge or reword them
- The first round proposes only the tracing (story 1 to `REQ-gift-cards-redeem-at-checkout`, story 2 to `REQ-gift-cards-reject-invalid`) and the criteria
- It reports what the two leave uncovered: nothing that needs a story
- `coverage stories --feature FEAT-gift-cards` empty; `validate` ok
