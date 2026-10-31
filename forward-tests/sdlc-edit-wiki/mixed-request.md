# A mixed request is split

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"In the order notifications feature, change 'is done' to 'does nothing more' in the sentence about checkout, and also add a requirement that SMS is sent within one minute"

## Answers
- Approve each gate

## Expected
- The stop shows the wording change, and says the requirement is not done here
- Makes the wording change only
- The summary has a "For other skills" line naming `sdlc-write-spec`
- `# Requirements` of the Feature is unchanged
