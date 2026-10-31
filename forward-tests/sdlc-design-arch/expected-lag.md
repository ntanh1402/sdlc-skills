# Expected lag

## Wiki
`forward-tests/seed.sh <dir> --fixture push-notifications-cr` (a `ReqApproved` ChangeRequest on `FEAT-order-notifications` adding push notifications).

## Request
"Design it"

## Answers
- Approve

## Expected
- Classifies `SVC-notifications`'s pending entry for `CR-sms-notifications` as expected lag
- Adds a second entry, keeps the first
