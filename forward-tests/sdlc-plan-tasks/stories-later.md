# Stories later

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-plan-tasks/first-plan.md`, with `main` holding the merged Tasks. On `main`: set one Task of `FEAT-gift-cards` to `status: Done`; copy `forward-tests/fixtures/gift-cards-stories/shop/features/FEAT-gift-cards/STORY-*.md` into `wiki/shop/features/FEAT-gift-cards/`; run `python3 .wiki-llm/tools/wiki_llm.py sync`; commit and push.

## Request
"Link the gift card stories to the tasks"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`: `coverage tasks` reports the two stories
- Plans no new Task; the change set adds `# Stories` to Tasks and an entry to the folder's `log.md`, nothing else
- The `Done` Task gets a `# Stories` link if it serves a story; nothing else in it changes
- `coverage tasks --feature FEAT-gift-cards` empty; `validate` ok
