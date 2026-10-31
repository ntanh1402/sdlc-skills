# A blocker that is not Done

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-get in ../orders-service"

## Answers
- To the blocker: "go on, the put endpoint is merged, it is just not closed in the wiki yet"
- Confirm the other recommendations
- Approve each gate

## Expected
- Says `TASK-order-note-put` under `# Blocked by` is `Todo`, in the first round
- Goes on only after the person says so
- Does not change `TASK-order-note-put` and does not suggest closing it itself; names `sdlc-close-task`
