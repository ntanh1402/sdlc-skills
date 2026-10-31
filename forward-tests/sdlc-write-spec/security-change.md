# Security change

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Lock an account for 15 minutes after 5 failed logins"

## Answers
- Approve

## Expected
- ChangeRequest on `FEAT-accounts`, `changeType: security`, `riskLevel` `med` or `high` with a reason
