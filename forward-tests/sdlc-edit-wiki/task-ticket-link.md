# A Task's ticket link

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"The ticket of TASK-sms-channel moved: it is SHOP-250 now, https://acme.atlassian.net/browse/SHOP-250"

## Answers
- Approve each gate

## Expected
- Draft `edit-TASK-sms-channel`
- `TASK-sms-channel.md` has `trackerKey: SHOP-250` and that `resource`; its `status` is still `Todo`
- Calls no Tracker
- `validate` ok
