# First feature

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`.

## Request
"Design the gift cards feature"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`
- The first round names `FEAT-gift-cards` and its state, and puts the design choices as numbered questions, each with a recommendation and wiki paths
- A round asks what else in the wiki must change, with its own answer
- One Intent gate, after the rounds
- Reuses `SVC-orders`, `SVC-payments` or `WEB-storefront` where they fit and says why
- The Design gate shows the packet with all eight parts, in full, and the Run plan
- At the Design gate, `<wiki>/.worktrees/arch-FEAT-gift-cards/plan.md` lists `features/FEAT-gift-cards/overview.md` first, then each concept file, decision and `log.md`; it does not hold the packet
- The Change-set gate says what the self review checked and fixed, as `## Self review` of the Run plan records it
- Branch `wiki/arch-FEAT-gift-cards` pushed; `plan.md` is not in it
- `FEAT-gift-cards` `Approved` (it was `ReqApproved`) with every `# Architecture` section and `designBasedOn: { version: 1, at: <its versionDate> }`
- Each new concept `Planned`, each changed one `Modifying`, each with a `# Pending changes` entry linking `FEAT-gift-cards`
- Any decision in `decisions/ADR-<name>.md` `Accepted`
- Every Requirement in `## Traceability`
- The last message is the summary, at most four lines; "Next" names `sdlc-plan-tasks` and `sdlc-design-tests`
- `validate` ok. **Keep this directory**: merge the branch into `main` and push
- Later scenarios copy it as "designed"
