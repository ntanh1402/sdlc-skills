# A resumed build

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`); then `git -C <dir>/orders-service worktree add -b task/order-note-put .worktrees/order-note-put origin/main`, `cp <this repository>/forward-tests/sdlc-build-task/resume.plan.md <dir>/orders-service/.worktrees/order-note-put/plan.md`, and in that worktree write `db/migration/V3__order_support_note.sql` holding `ALTER TABLE orders ADD COLUMN support_note text NULL CHECK (char_length(support_note) BETWEEN 1 AND 500);` (a run that ended after its first file). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Continue building TASK-order-note-put in ../orders-service"

## Answers
- "yes, it still stands"
- Approve

## Expected
- Finds the branch and the worktree; deletes neither and makes no second branch
- Shows the branch's commits (none) and the Run plan, and asks one question: whether it still stands
- Asks no round and no Intent or Design approval again
- Continues at the first unticked file; keeps the migration as it is
- `plan.md` has a `## Self review` section, and the Change-set gate says only what it records
- One commit on `task/order-note-put` ending with `Task: TASK-order-note-put`, holding the five files and no `plan.md`; not pushed
