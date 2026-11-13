# Draft feature

A spec that is still a draft is designed like an agreed one, and stays a
draft.

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`; then set `status: Draft`, commit, push. Keep the directory: `sdlc-write-spec/revise-designed-draft.md` starts from it after the merge.

## Request
"Design the gift cards feature"

## Answers
- Confirm the recommendations
- Approve each gate

## Expected
- `READY`, not a refusal; the first round says the Requirements are still a draft, so the design may have to be redone when they change, and that the Feature becomes `Approved` only once they are agreed
- `FEAT-gift-cards/overview.md` keeps `status: Draft`, has `# Architecture` filled and `designBasedOn: { version: 1, at: <its versionDate> }`
- Each new Design file is `Planned` with a pending entry linking `FEAT-gift-cards`
- `validate` ok, with no `basis.*` finding
- "Next" names `sdlc-plan-tasks`, `sdlc-design-story-tests` and `sdlc-design-feature-tests` after the merge, and says the Tasks can be built and closed while the spec is a draft (the Design files' pending entries stay until the target is approved)
