# Upgrade a schema 1 wiki: test suites are removed

## Wiki
`forward-tests/seed.sh <dir>`; then in the wiki replace `wiki/shop/tests/`
with the schema 1 suites of commit `485aea0`
(`git -C <this clone> archive 485aea0 forward-tests/sample/shop/tests | tar -x --strip-components=3 -C wiki/shop`),
set `schema_version: "1"` in `wiki/index.md`, set `.wiki-llm/manifest.json`
`release_version` to `1.1.0` and `schema_version` to `"1"`, commit, push.

## Request
"upgrade the wiki"

## Answers
- Upgrade: approve
- Every other gate: approve

## Expected
- Before approval, says the Schema version changes from 1 to 2, that every TestSuite is removed, and that `sdlc-design-story-tests` and `sdlc-design-feature-tests` write them again
- `migrate` in the draft removes the six schema 1 suites under `wiki/shop/tests/` and sets `schema_version: "2"`
- `draft finish` is `ok`
- After the commit, says to run sdlc-design-story-tests and sdlc-design-feature-tests for each Feature or ChangeRequest the removed suites verified (`FEAT-accounts`, `FEAT-catalog`, `FEAT-checkout`, `FEAT-order-notifications`, `CR-sms-notifications`, `FEAT-payments`)
