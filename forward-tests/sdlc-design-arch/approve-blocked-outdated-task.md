# Approve blocked by an outdated task

An approved target has no outdated Task: a `ReqApproved` Feature whose spec
moved on after its Tasks were planned and built is not approved until the
Tasks are replanned.

## Wiki
`forward-tests/seed.sh <dir> --fixture order-notes-feature`; then in the wiki:

- in `wiki/shop/features/FEAT-order-notes/overview.md` set
  `status: ReqApproved`, `version: 2`, `versionDate: 2026-10-20` and
  `designBasedOn: { version: 2, at: 2026-10-20 }`;
- in `wiki/shop/features/FEAT-order-notes/TASK-order-note-put.md` set
  `status: Done` and add `mergeCommitSha: 3f2a91c0d4e5b6a7980112233445566778899aab`
  and `mergedAt: 2026-10-05T10:00:00+07:00` (its `basedOn` stays at version 1);

commit and push.

## Request
"Approve FEAT-order-notes"

## Answers
- None needed

## Expected
- Approves nothing: no draft is started and no file changes; `FEAT-order-notes` stays `ReqApproved`
- The summary lists `TASK-order-note-put` (`Done`) and `TASK-order-note-get` (`Todo`) as written from version 1 while the Feature is at version 2
- "For other skills" names `sdlc-plan-tasks`: it plans a Task for any difference and updates the `basedOn` of the `Done` Task once checked
- "Next" says to run `sdlc-design-arch` again to approve once that pull request is merged
- The pending entries on `EP-orders-note-put`, `EP-orders-note-get` and `TBL-orders` are untouched
