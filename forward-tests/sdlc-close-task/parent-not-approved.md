# Parent not approved yet

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --code orders-service --merged orders-service:orders-tidy-create:TASK-order-note-put`; then in the wiki set `status: Draft` in `wiki/shop/features/FEAT-order-notes/overview.md`, commit and push.

## Request
"Close TASK-order-note-put, the code is in ../orders-service"

## Answers
- Was this change reviewed? "yes"
- Approve each gate

## Expected
- Closes `TASK-order-note-put`: `status: Done`, `mergeCommitSha` and `mergedAt` set; `basedOn` unchanged
- Leaves `FEAT-order-notes/overview.md` at `status: Draft` and leaves the `# Pending changes` entry on `EP-orders-note-put` untouched until the Feature is approved
- "Next" says `sdlc-design-arch` removes the Design files' pending entries when it approves the Feature
- `validate` ok on branch `wiki/close-TASK-order-note-put`
