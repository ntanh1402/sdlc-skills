# Paste story

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Give me the checkout user stories ready to paste into a ticket"

## Expected
- Prints `STORY-checkout-pay-and-confirm` and `STORY-checkout-retry-safely` as `paste-format.md` shows: the title as a heading, the sentence, numbered criteria, Requirement keys as plain text, no links, the wiki path
- `STORY-checkout-retry-safely` has its Notes line; both have `Priority: P1`
- Writes nothing; starts no draft
