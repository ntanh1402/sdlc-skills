# Change to feature

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Customers should be able to empty their whole cart in one go"

## Answers
- Approve
- "the requirements are agreed"

## Expected
- Mode ChangeRequest on `FEAT-cart` (Released)
- `CR-<name>` with `status: ReqApproved`, `version: 1`, `changeType: feature`, `# Delta` `None — pending architecture`, `# References` linking `REF-<name>-change-prd`, whose folder holds `change-prd.md`
- In the diff, `FEAT-cart/overview.md` changes only in `# Change history`, which the tool writes
