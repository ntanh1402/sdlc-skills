# A change another skill owns

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Write the spec for gift cards: customers pay part or all of an order with a gift card balance"

## Answers
- To the question about what else in the wiki must change: "yes, the payments endpoint page is wrong: the service already accepts a `giftCardId` today. Fix that page too"
- Confirm the other recommendations
- Approve each gate
- "approved for design"

## Expected
- Does not edit any file under `services/`
- Says the endpoint page is corrected with `sdlc-import`
- The Run plan has it under `## For other skills`
- The summary has a "For other skills" line naming `sdlc-import`
- The diff holds only `FEAT-gift-cards/` and tool-written files
