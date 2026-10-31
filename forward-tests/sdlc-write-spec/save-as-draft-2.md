# Save as draft, then approve

## Wiki
The directory left by `save-as-draft.md`, after merging `wiki/spec-FEAT-gift-cards`
into `main` and pushing `main`.

## Request
"the gift cards requirements are agreed"

## Answers
- Every gate: approve
- Open questions, if asked: "they do not block design; leave them recorded as open"

## Expected
- Finds its own draft `wiki/spec-FEAT-gift-cards` merged: `draft discard spec-FEAT-gift-cards --remote`, then `draft start` again
- Asks the status question at the Design gate
- `FEAT-gift-cards` has `status: ReqApproved` on the new branch and still `version: 1` (only the status changed); `validate` ok
