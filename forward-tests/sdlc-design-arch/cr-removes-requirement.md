# CR removes a Requirement

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-plan-tasks/first-plan.md`, with `main` holding the merged design and Tasks. On `main`: copy `forward-tests/fixtures/gift-cards-stories/shop/features/FEAT-gift-cards/STORY-*.md` into `wiki/shop/features/FEAT-gift-cards/`; add `# Stories` with a link to `STORY-gift-cards-refused-card.md` to one Task of `FEAT-gift-cards`, and set that Task to `status: Done`; copy `forward-tests/fixtures/gift-cards-reject-removal-cr/shop/change-requests` into `wiki/shop/`; run `python3 .wiki-llm/tools/wiki_llm.py sync` and `validate`; commit and push.

## Request
"Design CR-gift-cards-provider-checks"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- In the same draft, `REQ-gift-cards-reject-invalid` is removed from `FEAT-gift-cards`'s Requirements and its Traceability
- The Run plan and the Design gate list the story fix: `STORY-gift-cards-refused-card` is deleted (it lists no other Functional Requirement); `STORY-gift-cards-pay-with-card` is unchanged
- The `Done` Task loses only its link to `STORY-gift-cards-refused-card`; nothing else in it changes
- `FEAT-gift-cards/log.md` records the deleted story and the dropped link
- `CR-gift-cards-provider-checks` `Approved`; `validate` ok on branch `wiki/arch-CR-gift-cards-provider-checks`
