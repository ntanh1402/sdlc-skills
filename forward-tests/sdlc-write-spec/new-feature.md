# New feature

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Write the spec for gift cards: customers pay part or all of an order with a gift card balance"

## Answers
- Answer each round plausibly; confirm the recommendations
- Approve each gate
- "the requirements are agreed"

## Expected
- The first round asks to confirm `shop` and the mode new Feature, and cites the overlap with `FEAT-checkout` and `FEAT-payments` by path
- Questions come in numbered rounds, each question with a recommended answer; no question is asked alone in its own turn unless it is the only one open
- A round asks what else in the wiki must change, with its own answer
- One Intent gate, after the rounds; no approval is asked before the first round
- Design gate shows the full PRD, the mapping table and the Run plan, and asks the status question, recommending the draft and saying that either can be merged and designed
- At the Design gate, `<wiki>/.worktrees/spec-FEAT-gift-cards/` holds `plan.md` with `## Answers` and `## Files`, and the PRD in `wiki/shop/references/REF-gift-cards-prd/prd.md`; `plan.md` does not hold the PRD text
- Change-set gate shows the diff, the commit message and what the self review could not fix (or that nothing is left)
- Branch `wiki/spec-FEAT-gift-cards` pushed; `plan.md` is not in it
- `FEAT-gift-cards/overview.md` has `status: ReqApproved`, `version: 1`, `versionDate` today, no `designBasedOn`, `# Architecture` `None`, no `sources`, and `# References` linking `REF-gift-cards-prd`
- `FEAT-gift-cards/log.md` exists; `references/REF-gift-cards-prd/` holds `overview.md` (a summary with `# Contents` listing `prd.md`), `prd.md` (no frontmatter) and `log.md`, and `overview.md` has `verified.by` `human:tester`
- `generated.by` is `sdlc-write-spec/2.5.<n>` and `verified.by` `human:tester`
- `validate` ok
- The last message is the summary: "Done" and "Next" (`sdlc-design-arch` after the merge), at most four lines
