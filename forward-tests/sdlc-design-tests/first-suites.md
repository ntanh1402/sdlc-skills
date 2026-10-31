# First suites

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design.

## Request
"Design the tests for gift cards"

## Answers
- Choose `integration` and `e2e`; decline `load`, accepting the gap
- Confirm the other recommendations
- Approve each gate

## Expected
- Recommends types with evidence, including `load` for `REQ-gift-cards-fast-balance`
- Asks to choose, in the first round, with the other numbered questions; a round asks what else in the wiki must change
- One Intent gate, after the rounds
- The Design gate shows each suite, each case, the coverage matrix, the totals and the Run plan
- At the Design gate, `<wiki>/.worktrees/tests-FEAT-gift-cards/plan.md` lists each suite's `overview.md`, one line per case file, and the logs
- The Change-set gate says what the self review checked and fixed, as `## Self review` of the Run plan records it
- `TS-gift-cards-integration` and `TS-gift-cards-e2e` with `status: Approved`
- One `TC-*.md` per case with `risk`, a `# Steps` table with validations
- `coverage tests --feature FEAT-gift-cards` reports only `REQ-gift-cards-fast-balance`, which the
  user accepts as an uncovered gap when declining `load`; the acceptance is recorded in the suite logs
- Branch `wiki/tests-FEAT-gift-cards` pushed; `plan.md` is not in it; `validate` ok
- The last message is the summary, at most four lines, with the accepted gap under "Not done"; no totals after the commit

The plan first expected `coverage tests` empty. Choosing only `integration`
and `e2e` leaves the load Requirement without a case, so the skill rightly
asks the user to accept that gap.
