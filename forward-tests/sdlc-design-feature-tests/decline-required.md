# Decline required

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design.

## Request
"Design the end-to-end tests for gift cards, without error-handling cases"

## Answers
- Decline `error-handling`, accepting the risk

## Expected
- Says which evidence makes `error-handling` required (a new Endpoint), and goes on only after the explicit acceptance
- Records the accepted risk in `TS-gift-cards/GENERAL/log.md`
- No case has `testCategory: error-handling`
