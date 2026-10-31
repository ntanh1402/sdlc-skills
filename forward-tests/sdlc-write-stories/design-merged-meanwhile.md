# Design merged meanwhile

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Write the user stories for gift cards"

## Answers
- Confirm the recommendations of each round
- Intent gate: approve
- Before answering the Design gate, in the wiki repository on `main`: set `status: Approved` in `wiki/shop/features/FEAT-gift-cards/overview.md` and replace `None` under `# Architecture` with one line `Designed elsewhere.`, commit and push (a design that merged while the stories were written). Then approve the Design gate
- Change-set gate: approve

## Expected
- The input check finds `overview.md` changed, compares its `# Requirements`, says they are the same and goes on
- It does not go back to the Run plan or ask the Design gate again
- Branch `wiki/stories-FEAT-gift-cards` pushed; `validate` ok on it
