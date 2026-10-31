# Draft spec

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`; then on `main` set `status: Draft` in `wiki/shop/features/FEAT-gift-cards/overview.md`, commit and push.

## Request
"Write the user stories for gift cards"

## Answers
- Confirm the recommendations
- Approve each gate

## Expected
- `READY`, not a refusal; the first round says the Requirements are still a draft, so the stories may change with the spec
- Each `STORY-gift-cards-*.md` has `basedOn: { version: 1, at: <the Feature's versionDate> }`
- `validate` ok
