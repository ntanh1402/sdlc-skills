# The trailer is found; the last Task of a ChangeRequest

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --code orders-service --merged orders-service:orders-refund:TASK-refund-endpoint` (an `Approved` ChangeRequest with one `Todo` Task; its code is on `origin/main` of `<dir>/orders-service` in a commit that ends with `Task: TASK-refund-endpoint`).

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate

## Expected
- Finds the commit on `origin/main` by its trailer and shows it; asks for no commit
- Asks one question: whether the change was reviewed; no rounds and no Run plan (`plan.md` is never written)
- One stop before the draft shows the wiki changes file by file: the Task `Todo` → `Done` with the commit, `EP-orders-refund` entry removed and `Planned` → `Active`, `CR-order-refund` `Approved` → `Implemented`
- Draft `close-TASK-refund-endpoint`; branch `wiki/close-TASK-refund-endpoint` pushed
- `TASK-refund-endpoint.md` has `status: Done`, `mergeCommitSha` (the full hash of that commit) and `mergedAt` (its committer date)
- `EP-orders-refund.md` has `status: Active` and no `# Pending changes` section
- `CR-order-refund/overview.md` has `status: Implemented`
- A `**Close**` entry in the logs of `CR-order-refund/` and `SVC-orders/`, naming the Task and the commit
- `generated.by` is `sdlc-close-task/2.5.<n>`; `validate` ok
- The last message has "Done" and "Next" only
- Nothing changed in `<dir>/orders-service`
