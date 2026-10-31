# A concept that was to be removed

## Wiki
`forward-tests/seed.sh <dir> --fixture order-lookup-removal-cr --code orders-service --merged orders-service:orders-tidy-create:TASK-remove-order-lookup` (`EP-orders-get` is `Removing`).

## Request
"Close TASK-remove-order-lookup, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate

## Expected
- `EP-orders-get.md` is kept, with `status: Deprecated` and no `# Pending changes` section; the file is not deleted
- Says why: the Task and the ChangeRequest still link it
- `CR-retire-order-lookup` is `Implemented`; the Task is `Done`
- `validate` ok
