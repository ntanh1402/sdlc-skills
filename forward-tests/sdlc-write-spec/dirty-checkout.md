# Dirty checkout

## Wiki
`forward-tests/seed.sh <dir>`; then an uncommitted edit to `wiki/shop/overview.md` in the wiki checkout.

## Request
"Write the spec for gift cards: customers pay part or all of an order with a gift card balance"

## Answers
- Approve

## Expected
- The draft is written in its worktree
- The dirty file is untouched and not in `draft diff`
