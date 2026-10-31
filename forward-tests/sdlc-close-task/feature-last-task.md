# The last Task of a Feature

## Wiki
The directory kept by `feature-first-task.md`, with its branch merged into `main`; then in `<dir>/orders-service`: `git commit --allow-empty -m "Read the order note" -m "Task: TASK-order-note-get"` and `git push`.

## Request
"Close TASK-order-note-get, the code is in ../orders-service"

## Answers
- "yes, it was reviewed"
- Approve each gate

## Expected
- `FEAT-order-notes` stays `InDev`; it is not set `Released`
- "Next" says `sdlc-edit-wiki` sets the Feature `Released` when it ships
- `validate` has no error; it warns `pending.feature-built`
