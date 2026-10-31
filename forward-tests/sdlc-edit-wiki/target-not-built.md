# An edit that changes a target not built yet

## Wiki
`forward-tests/seed.sh <dir>` (`TBL-customers` is `Modifying`: `phone` and `sms_opt_out` belong to `CR-sms-notifications` and are not built).

## Request
"In TBL-customers, make the phone column required"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Refuses: the file holds a target not built yet, and the edit changes that target
- Routes to a ChangeRequest with `sdlc-write-spec`
- No draft
