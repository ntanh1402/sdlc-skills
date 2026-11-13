# First story group

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design; then copy `forward-tests/fixtures/gift-cards-stories/.` over its `wiki/`, run `python3 .wiki-llm/tools/wiki_llm.py sync`, commit and push.

## Request
"Design the tests for STORY-gift-cards-pay-with-card"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Finds the story's Feature `FEAT-gift-cards` and lists each acceptance criterion by number in the inventory
- Asks the categories in the first round, with a round asking what else in the wiki must change; one Intent gate after the rounds
- The Design gate shows a coverage matrix by criterion; every criterion has a case
- Creates the suite `TS-gift-cards` (`overview.md` with `# Verifies` only) and the group `STORY-gift-cards-pay-with-card/` with `status: Approved`, `basedOn`, `# Story` linking the story, and `log.md`
- Cases `TC-1-…`, `TC-2-…`, … each link the story first under `# Covers` with `— AC <n>`, then a Requirement the story lists; each has `testType`, `testCategory` and `risk`, `<name>:` checkpoint Expected results joined with `<br>`, and Validations with the checked fields in bold
- No `GENERAL/` group is written; the summary's "Next" names `sdlc-design-feature-tests`
- `checklist.csv` has `Group` `STORY-gift-cards-pay-with-card` and `Covers` `AC <n>` on each row
- Branch `wiki/tests-STORY-gift-cards-pay-with-card` pushed; `validate` ok with no warning about the group
