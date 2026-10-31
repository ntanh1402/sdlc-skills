# A parent that is not approved

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`); then in the wiki set `status: Deprecated` in `wiki/shop/features/FEAT-order-notes/overview.md`, commit and push.

## Request
"Build TASK-order-note-put in ../orders-service"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Refuses: `FEAT-order-notes` is `Deprecated`, so the work is closed
- Asks no question and no gate
- No branch and no worktree in `<dir>/orders-service`
