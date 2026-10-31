# The first Task of a Feature

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature --code orders-service --merged orders-service:orders-tidy-create:TASK-order-note-put` (an `Approved` Feature with two `Todo` Tasks). Keep the directory: merge the branch into `main` and push; `feature-last-task.md` starts from it.

## Request
"Close TASK-order-note-put, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate

## Expected
- `FEAT-order-notes` goes `Approved` → `InDev`
- `EP-orders-note-put.md` and `TBL-orders.md` are `Active` with no `# Pending changes` section; `EP-orders-note-get.md` is unchanged
- "Next" names `TASK-order-note-get`, the Task still `Todo`
- `validate` ok
