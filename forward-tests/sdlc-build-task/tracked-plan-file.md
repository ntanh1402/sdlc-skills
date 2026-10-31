# A repository that tracks its own plan.md

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`); then in `<dir>/orders-service` write `plan.md` holding "# Roadmap", commit it on `main` and push. In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- The Run plan is `sdlc-plan.md` at the root of the worktree; `info/exclude` holds `/sdlc-plan.md`
- `plan.md` in the worktree still holds "# Roadmap"
- The commit changes neither `plan.md` nor holds `sdlc-plan.md`
