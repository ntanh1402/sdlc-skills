# Blocked by another skill's change

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Add gift wrapping to the returns feature"

## Answers
- "Returns is live in production; it was just never written into the wiki"

## Expected
- Finds no Feature for returns and asks
- Stops before the Intent gate: the built returns capability is recorded first, with `sdlc-import`
- No draft
