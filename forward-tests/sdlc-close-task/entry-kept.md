# A concept another Todo Task still covers

## Wiki
`forward-tests/seed.sh <dir> --fixture order-refund-cr --fixture order-refund-second-task --code orders-service --merged orders-service:orders-refund:TASK-refund-endpoint` (`TASK-refund-audit` is `Todo` and also covers `EP-orders-refund`). Keep the directory and do not merge the branch: `other-close-draft.md` starts from it.

## Request
"Close TASK-refund-endpoint, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate

## Expected
- The stop says the entry of `EP-orders-refund` is kept, naming `TASK-refund-audit`
- `TASK-refund-endpoint` is `Done`; `EP-orders-refund.md` still has its entry and `status: Planned`
- `CR-order-refund` stays `Approved`
- `validate` ok
