# Missing tasks

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Plan the missing tasks for FEAT-order-notifications"

## Answers
- Approve
- Asked whether to plan CR-sms-notifications instead: "no, just the Feature"

## Expected
- Runs `coverage tasks --feature FEAT-order-notifications`, which reports nothing uncovered
- Plans no Task: nothing is missing for the Feature
- Points to the real gap: `coverage tasks --change CR-sms-notifications` reports `TBL-notifications`
- No draft

The plan first expected Tasks for `CHAN-order-created`, `TBL-customers` and
`EXT-twilio`, which `coverage tasks --feature` reported in an earlier release.
The Task schema forbids those Tasks: a Task's planned scope links only
concepts with a pending entry for the Task's parent. Later releases count
only those concepts (decision P17).
