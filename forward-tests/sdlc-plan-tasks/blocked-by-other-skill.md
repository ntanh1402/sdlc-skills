# Blocked by another skill's change

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Replan the tasks of CR-sms-notifications"

## Answers
- To the first round: "the design is wrong. SMS is sent by a new service of its own, not by the notifications service. Plan it that way"

## Expected
- Does not plan Tasks for a service the design does not have
- Stops before the Intent gate: the design of an `Approved` ChangeRequest changes through a new ChangeRequest, with `sdlc-write-spec`
- No draft
