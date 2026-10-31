# Save as draft

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Write the spec for gift cards: customers pay part or all of an order with a gift card balance"

## Answers
- Status question: "keep it as a draft"

## Expected
- `status: Draft`, `version: 1`
- The summary's "Next" says `sdlc-design-arch` can start after the merge, even while it is a draft
- Then, after merging the branch and pushing `main`, a second run "the gift cards requirements are agreed" discards the merged `wiki/spec-FEAT-gift-cards`, starts it again and sets `ReqApproved`
