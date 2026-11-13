# A change another skill owns

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Replan the tasks of CR-sms-notifications"

## Answers
- `TASK-sms-channel` has started
- To the question about what else in the wiki must change: "yes, `TS-sms-notifications` has no case for a customer who opted out of SMS. Add one"
- Confirm the other recommendations
- Approve each gate

## Expected
- Does not edit any file under `tests/`
- Says the case is designed with `sdlc-design-feature-tests`
- The Run plan has it under `## For other skills`
- The summary has a "For other skills" line naming `sdlc-design-feature-tests`
- The diff holds only `CR-sms-notifications/` and tool-written files
