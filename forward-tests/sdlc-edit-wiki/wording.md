# A wording fix

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"In the order notifications feature, 'checkout publishes an event and is done' should read 'checkout publishes an event and does nothing more'"

## Answers
- Approve each gate

## Expected
- No rounds and no Run plan; one stop before the draft shows the old and the new sentence in `features/FEAT-order-notifications/overview.md`
- Draft `edit-FEAT-order-notifications`; branch `wiki/edit-FEAT-order-notifications` pushed
- The diff changes that sentence, adds an `**Edit**` entry to the Feature's `log.md`, and nothing else a person writes
- No Requirement, status or `# Architecture` line changed
- `generated.by` is `sdlc-edit-wiki/2.5.<n>`; `validate` ok
- The last message has "Done" and "Next" only
