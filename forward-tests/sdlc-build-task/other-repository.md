# Scope that is in another repository

## Wiki
`forward-tests/seed.sh <dir> --code orders-service` (`TASK-sms-channel` changes the notifications service, which is another repository).

## Request
"Build TASK-sms-channel in ../orders-service"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Says every scope item of the Task is "not in this folder": `SVC-notifications` has another repository as its `resource`
- Writes no code for them in `orders-service`
- Says a Task changes one repository and asks for the right folder
- No commit
