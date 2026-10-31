# Revise removes a Requirement

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec --fixture gift-cards-stories`.

## Request
"Gift cards no longer need to refuse invalid cards at checkout; the provider does that. Remove that requirement."

## Answers
- Confirm the recommendations of each round
- Approve the PRD; approved for design
- Approve each gate

## Expected
- Revises `FEAT-gift-cards`; says in the first round that it goes back to `Draft` until approved again
- `REQ-gift-cards-reject-invalid` is removed from the Requirements and described in the PRD
- The Design gate lists the story fix: `STORY-gift-cards-refused-card` is deleted (it lists no other Functional Requirement); `STORY-gift-cards-pay-with-card` is unchanged
- The log records the deleted story
- `validate` ok on branch `wiki/spec-FEAT-gift-cards`
