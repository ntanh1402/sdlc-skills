# Open questions

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design.

## Request
"Design the tests for gift cards"

## Answers
- To a question about a Requirement or acceptance criterion: "I don't know yet, ask the product owner"
- Approve each gate

## Expected
- The unanswered question is written under `# Open questions` in `TS-gift-cards/GENERAL/overview.md` as a numbered item linking the Requirement or story it is about
- The group is written with `status: Draft`
- The summary lists the open question under "Not done"
- `validate` ok

A later run with the answer applies it to the cases, removes the question,
logs the answer in the group's `log.md`, and writes the group `Approved` when
no question is left.
