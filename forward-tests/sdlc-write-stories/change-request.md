# Change request

## Wiki
`forward-tests/seed.sh <dir> --fixture checkout-retry-change-cr`.

## Request
"Write the user stories for CR-checkout-retry-window"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`; the first round names `CR-checkout-retry-window` (`ReqApproved`) and the Feature stories that list `REQ-checkout-pay-before-confirm`: `STORY-checkout-pay-and-confirm` and `STORY-checkout-retry-safely`
- `STORY-checkout-*.md` files in `CR-checkout-retry-window/` only; their `# Requirements` link `overview.md` of the ChangeRequest, never the Feature's
- Both Requirements of the ChangeRequest are listed by a story
- A story that lists `REQ-checkout-pay-before-confirm` names the affected Feature stories under `# Affects`
- The Feature's stories are unchanged except the tool-written `# Changed by`, which lists the ChangeRequest story
- `coverage stories --change CR-checkout-retry-window` empty; `validate` ok on branch `wiki/stories-CR-checkout-retry-window`
