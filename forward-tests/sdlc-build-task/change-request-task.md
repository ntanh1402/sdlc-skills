# A ChangeRequest's Task

## Wiki
`forward-tests/seed.sh <dir> --fixture order-lookup-removal-cr --fixture conventions-no-branch-rule --code orders-service` (an `Approved` ChangeRequest that removes `EP-orders-get`, with one `Todo` Task). In every scenario also check that the wiki did not change: `git -C <dir>/shop-wiki status --short` is empty, no branch `wiki/*` exists, and the Task is still `Todo`.

## Request
"Build TASK-remove-order-lookup, the code is in ../orders-service"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Accepts the Task: its parent `CR-retire-order-lookup` is `Approved`
- Reads `EP-orders-get.md` as the target: `Removing`, so the endpoint is to be removed
- The Run plan removes the handler and its entry in `openapi.yaml`, and changes or removes the unit tests that used it
- One commit on `task/remove-order-lookup` ending with `Task: TASK-remove-order-lookup`; not pushed
