# First stories

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Break gift cards into user stories"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`
- The first round names `FEAT-gift-cards` (`ReqApproved`) and shows the inventory: `REQ-gift-cards-redeem-at-checkout` and `REQ-gift-cards-reject-invalid` need a story; `REQ-gift-cards-single-use-per-order` (Constraint) and `REQ-gift-cards-fast-balance` (Nonfunctional) are optional
- The first round proposes the stories (key, actor, goal, Requirements) as numbered questions, each with a recommendation; a round asks what else in the wiki must change
- One Intent gate, after the rounds
- The Design gate shows every story in full, the coverage matrix and the Run plan
- At the Design gate, `<wiki>/.worktrees/stories-FEAT-gift-cards/plan.md` lists one line per story file and the folder's `log.md`
- `STORY-gift-cards-*.md` files in `FEAT-gift-cards/`, no `status`, no `trackerKey`; each has the "As a …, I want …, so that …" sentence and numbered Given/When/Then criteria with real values, each citing a Requirement it lists
- No story lists only Nonfunctional Requirements or Constraints
- Each story has `basedOn: { version: 1, at: <FEAT-gift-cards versionDate> }`
- `FEAT-gift-cards/overview.md` and `REF-gift-cards-prd` are unchanged
- `coverage stories --feature FEAT-gift-cards` empty on the branch
- Branch `wiki/stories-FEAT-gift-cards` pushed; `plan.md` is not in it; `validate` ok
- Before the summary, each story is printed as `paste-format.md` shows: no frontmatter, no links, Requirement keys as plain text, the story's wiki path
- The last message is the summary, at most four lines; "Next" names `sdlc-plan-tasks` once the design is merged
