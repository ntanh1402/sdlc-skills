# Add an application to an older wiki

## Wiki
`forward-tests/seed.sh <dir>`; then in the wiki set `.wiki-llm/manifest.json`
`release_version` to `0.9.0`, commit, push.

## Request
"add a billing application"

## Answers
- Upgrade: approve
- Every other gate: approve

## Expected
- Says the wiki is older than the skills
- Offers the upgrade, in a draft `wiki/setup-2.1.<n>`
- Does not add the application in the same run
- Says to run the skill again once the upgrade's pull request is merged
