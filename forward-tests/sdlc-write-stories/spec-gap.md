# Spec gap

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Break gift cards into user stories. Also add a criterion that a customer can top up a gift card at checkout."

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Says that no Requirement supports topping up a gift card, so it is not a criterion
- Names it under "For other skills" for `sdlc-write-spec`; the summary repeats it
- No story mentions topping up
- The stories for the existing Requirements are written; `validate` ok
