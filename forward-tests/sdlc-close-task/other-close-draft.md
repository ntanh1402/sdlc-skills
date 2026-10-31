# Another close of the same parent is open

## Wiki
The directory kept by `entry-kept.md`, with `wiki/close-TASK-refund-endpoint` pushed and **not** merged; then in `<dir>/orders-service`: `git commit --allow-empty -m "Audit refunds" -m "Task: TASK-refund-audit"` and `git push`.

## Request
"Close TASK-refund-audit, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate

## Expected
- At the stop, warns: `wiki/close-TASK-refund-endpoint` is not merged and its Task shares `EP-orders-refund.md`
- Goes on; does not stop for it
- On `main` `TASK-refund-endpoint` is still `Todo`, so this draft keeps the entry too; says `validate` will report `pending.leftover` once both are merged
