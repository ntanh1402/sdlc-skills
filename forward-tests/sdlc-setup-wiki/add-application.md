# Add an application

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"add a billing application to the wiki, owned by finance"

## Answers
- Title: "Billing"
- Every gate: approve

## Expected
- Finds the wiki from the workspace note; does not ask for its path
- `copy check` reports `current`
- Shows `wiki/billing/overview.md` before writing it
- Branch `wiki/app-billing` is pushed to the remote
- `validate` is ok on that branch
- The workspace's `AGENTS.md` and `CLAUDE.md` are not rewritten
