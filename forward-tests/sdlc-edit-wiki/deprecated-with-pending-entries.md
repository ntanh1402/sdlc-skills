# Deprecated refused while the design is pending

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature`.

## Request
"We dropped the order notes idea. Mark FEAT-order-notes deprecated"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Refuses: `TASK-order-note-put` and `TASK-order-note-get` are `Todo`, and `EP-orders-note-get.md`, `EP-orders-note-put.md` and `TBL-orders.md` have a pending entry for `FEAT-order-notes`
- Says no skill withdraws an approved design, and that a person removes the entries, the `Planned` files and the `Todo` Tasks by hand
- Does not offer to remove the entries itself
- No draft
