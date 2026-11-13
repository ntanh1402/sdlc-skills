# Flow across stories

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design; then copy `forward-tests/fixtures/gift-cards-stories/.` over its `wiki/`, run `python3 .wiki-llm/tools/wiki_llm.py sync`, commit and push.

## Request
"Design an end-to-end test that pays with a card and then has a second card refused"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Says a flow across stories belongs in `GENERAL/` and routes to `sdlc-design-feature-tests`
- Writes no case for it
