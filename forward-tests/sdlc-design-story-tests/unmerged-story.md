# Unmerged story

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design; then in the wiki repository `python3 .wiki-llm/tools/wiki_llm.py draft start stories-FEAT-gift-cards`, copy `forward-tests/fixtures/gift-cards-stories/.` over the worktree's `wiki/`, commit and push that branch only (not merged).

## Request
"Design the tests for STORY-gift-cards-pay-with-card"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Finds the story in `wiki/stories-FEAT-gift-cards` and stops as `NOT_MERGED`, naming that draft
- Does not route to `sdlc-write-stories` as if the story did not exist
- Starts no draft
