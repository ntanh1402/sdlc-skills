# The next subtask on a branch that holds an earlier one

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --fixture conventions-no-branch-rule --code orders-service` (an `Approved` Feature `FEAT-order-notes` with two `Todo` Tasks; the code repository `<dir>/orders-service` has a remote and the default branch `main`); then build the first subtask as an earlier run would have left it, with no Run plan:

```bash
cd <dir>/orders-service
printf '.worktrees/\n/plan.md\n' >> .git/info/exclude
git worktree add -q -b task/order-note-put .worktrees/order-note-put origin/main
cd .worktrees/order-note-put
echo 'ALTER TABLE orders ADD COLUMN support_note text NULL CHECK (char_length(support_note) BETWEEN 1 AND 500);' > db/migration/V3__order_support_note.sql
git add -A
git commit -qm "Add the support_note column to orders" -m "$(printf 'Subtask: SCRUM-175\nTask: TASK-order-note-put')"
git rev-parse --short HEAD    # note it: the SCRUM-175 commit
```

In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-order-note-put in ../orders-service, subtask SCRUM-176: the PUT /orders/{id}/note endpoint, its openapi.yaml entry and its unit tests"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Finds the branch and the worktree; deletes neither and adds no second branch or worktree
- Treats it as a new subtask, not a resumed build: there is no Run plan and the branch's commit names SCRUM-175. The first round names that commit; it does not ask which part SCRUM-176 covers
- One Intent gate, after the rounds, restating the subtask `SCRUM-176`, its part, and that the `support_note` column was built by SCRUM-175
- The Run plan's title names SCRUM-176 and its `On:` line names the noted commit; `## Files` lists `OrderService`, `OrderController`, `openapi.yaml` and the unit tests, not the migration
- `db/migration/V3__order_support_note.sql` is not changed
- The self review checks the SCRUM-176 part, and that the SCRUM-175 commit is untouched (`HEAD` is still the noted commit before the new commit)
- `git -C <dir>/orders-service log --format='%h %s' origin/main..task/order-note-put` shows two commits; the older is the noted commit, with the same hash
- The new commit's message ends with an empty line, `Subtask: SCRUM-176` and `Task: TASK-order-note-put`; `git show --stat` has no migration and no `plan.md`; not pushed
- The summary's "Done" names SCRUM-176 and the SCRUM-175 commit kept on the branch
