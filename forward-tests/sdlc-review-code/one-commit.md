# One commit of a Task's branch

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service`; then make a Task branch of two subtask commits, the first a tidy-up, the second the refund endpoint:

```bash
cd <dir>/orders-service
ME=(-c user.name="Forward Tester" -c user.email="tester@example.com")
git checkout -q -b task/refund-endpoint
git apply <this repository>/forward-tests/changes/orders-tidy-create.patch
git add -A
git "${ME[@]}" commit -qm "Rename the counts in OrderService.create" -m "$(printf 'Subtask: SCRUM-201\nTask: TASK-refund-endpoint')"
git apply <this repository>/forward-tests/changes/orders-refund.patch
git add -A
git "${ME[@]}" commit -qm "Add the refund endpoint" -m "$(printf 'Subtask: SCRUM-202\nTask: TASK-refund-endpoint')"
git checkout -q main
```

The checkout is left on `main`, as `sdlc-build-task` leaves it.

In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

## Request
"Review the SCRUM-201 commit in ../orders-service against the wiki"

## Answers
- After the first report: "Now review the SCRUM-202 commit"

## Expected
- Finds the commit by its `Subtask: SCRUM-201` line on `task/refund-endpoint`, although the checkout is on `main`; takes `TASK-refund-endpoint` from its `Task:` line and does not ask for the Task
- The first line names the commit's short hash, `Subtask: SCRUM-201` and the Task, and the wiki commit
- The change is that commit's diff only: no finding about the refund endpoint, `reason`, the `409` or the migration `V3__order_refund.sql`
- The Task's acceptance items are under "Not checked" as not in this change; "0 must fix, 0 should fix"
- The second report names the SCRUM-202 commit; its findings are those of `with-task.md`: `reason` not refused with 422, the `409` of `# Flowchart`, the migration outside the scope, the missing idempotency token; the renames of SCRUM-201 are not part of the change
- Every finding cites a code location and a wiki path; each report's last line counts the findings; there is no verdict
