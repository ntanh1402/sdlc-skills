# Reopen ReqApproved

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Gift cards expire one year after purchase; add that"

## Answers
- Confirm the recommendations
- Approve
- "keep it as a draft"

## Expected
- The first round says the Feature goes back to `Draft` unless approved again
- Status `Draft`, `version: 2`, `versionDate` today
- The summary lists nothing as outdated: the Feature had no design, stories, Tasks or test groups
