# Approve with a Done task

A Feature whose Tasks were built and closed while its spec was a draft is
approved straight to `InDev`, and the pending entries of what is built go.

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature`; then in the wiki:

- set `status: ReqApproved` in `wiki/shop/features/FEAT-order-notes/overview.md`;
- in `wiki/shop/features/FEAT-order-notes/TASK-order-note-put.md` set
  `status: Done` and add `mergeCommitSha: 3f2a91c0d4e5b6a7980112233445566778899aab`
  and `mergedAt: 2026-10-05T10:00:00+07:00`;

commit and push.

## Request
"Approve FEAT-order-notes"

## Answers
- Approve each gate

## Expected
- The short run (`APPROVE`): no rounds and no redesign; the one stop shows the changes file by file
- `FEAT-order-notes/overview.md` goes from `ReqApproved` straight to `status: InDev`, not `Approved`
- `EP-orders-note-put`: the pending entry for `FEAT-order-notes` is removed with the section; `Planned` → `Active`
- `TBL-orders`: the pending entry for `FEAT-order-notes` is removed; with no entry left, `Modifying` → `Active`
- `EP-orders-note-get` keeps its pending entry and `status: Planned`: `TASK-order-note-get` is still `Todo`
- No Task file changes
- `validate` ok on branch `wiki/arch-FEAT-order-notes`, with no `pending.*` or `basis.*` finding
