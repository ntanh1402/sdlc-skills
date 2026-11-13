# First suites

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design; then copy `forward-tests/fixtures/gift-cards-stories/.` over its `wiki/`, run `python3 .wiki-llm/tools/wiki_llm.py sync`, commit and push.

## Request
"Design the end-to-end tests for gift cards"

## Answers
- Choose the flows and categories it recommends
- Accept `REQ-gift-cards-fast-balance` as not covered (it needs a load test)
- Confirm the other recommendations
- Approve each gate

## Expected
- Recommends flows and categories with evidence; never proposes load tests, and says `REQ-gift-cards-fast-balance` is not covered here because load tests are not kept in the wiki
- Asks to choose, in the first round, with the other numbered questions; a round asks what else in the wiki must change
- One Intent gate, after the rounds
- The Design gate shows the group, each case with its type and category, the coverage matrix, the totals and the Run plan
- At the Design gate, `<wiki>/.worktrees/tests-FEAT-gift-cards/plan.md` lists the suite's `overview.md`, the group's `overview.md` and `log.md`, and one line per case file
- The Change-set gate says what the self review checked and fixed, as `## Self review` of the Run plan records it
- One suite `TS-gift-cards` with no `status`, no `basedOn` and no `log.md`; one group `GENERAL/` with `status: Approved`, `basedOn` and a `# Scope`
- Cases `TC-1-…`, `TC-2-…`, … in `GENERAL/`, an `e2e` case for each PRD flow that spans both stories (when the PRD has none, the first round says so), each with `testType`, `testCategory` and `risk`, a `# Steps` table whose Expected results are `<name>:` checkpoints joined with `<br>` and whose Validations name the checked fields in bold
- Every Action says what to do and its target ("Call API `POST /gift-cards/redeem`"); no step says "data <n>" or "see Step <n>", or names a wiki key
- No `STORY-*` group is written; the summary's "Next" names `sdlc-design-story-tests` for the stories with no group
- The accepted gap is recorded in the group's log and listed under "Not done"
- Branch `wiki/tests-FEAT-gift-cards` pushed; `plan.md` is not in it; `validate` ok
- The last message is the summary, at most four lines; no totals after the commit
