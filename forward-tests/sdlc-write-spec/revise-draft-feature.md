# Revise draft feature

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`; then set the Feature to `status: Draft`, commit, push.

## Request
"Gift cards expire one year after purchase; add that"

## Answers
- Approve
- "approved for design"

## Expected
- Revises `FEAT-gift-cards` directly (no ChangeRequest)
- Adds a new `REQ-gift-cards-…` key
- Status `ReqApproved`
