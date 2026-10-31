# Blocked by another skill's change

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design.

## Request
"Design the tests for gift cards"

## Answers
- To the first round: "the redeem endpoint in the wiki is wrong: a gift card must also take a PIN. Test it with the PIN"

## Expected
- Designs no case for a field the contract does not have
- Stops before the Intent gate: the design of an `Approved` Feature changes through a ChangeRequest, with `sdlc-write-spec`
- No draft
