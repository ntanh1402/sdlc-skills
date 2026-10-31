# Released refused while a Task is open

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature`.

## Request
"Mark FEAT-order-notes released"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Refuses: the Feature is `Approved`, and `TASK-order-note-put` and `TASK-order-note-get` are `Todo`
- Says each Task is closed with `sdlc-close-task` after its code is merged
- No draft
