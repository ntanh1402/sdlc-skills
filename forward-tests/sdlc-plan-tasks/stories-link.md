# Stories link

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design; then copy `forward-tests/fixtures/gift-cards-stories/shop/features/FEAT-gift-cards/STORY-*.md` into `wiki/shop/features/FEAT-gift-cards/`, run `python3 .wiki-llm/tools/wiki_llm.py sync`, commit on `main` and push.

## Request
"Plan the tasks for gift cards"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`; the scope inventory lists the two stories beside the concepts
- The Design gate's task plan has a Stories column, and the coverage matrix maps each story to the Tasks that link it
- Each story is linked under `# Stories` by at least one Task; no Task links a story of another folder
- A Task that serves no story (a table, a migration) has no `# Stories`
- `coverage tasks --feature FEAT-gift-cards` empty on branch `wiki/tasks-FEAT-gift-cards`; `validate` ok
- The story files are unchanged
