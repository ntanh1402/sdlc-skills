# Fold a story that has test cases

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec --fixture gift-cards-stories --fixture gift-cards-tests`;
then in the wiki give `STORY-gift-cards-refused-card` a test group: create
`shop/tests/TS-gift-cards/STORY-gift-cards-refused-card/` with a copy of
`GENERAL/overview.md` and `GENERAL/log.md`, with the title and first heading
`Refused card` and `# Scope` and its text replaced by `# Story` linking the
story; move `GENERAL/TC-2-refused-card.md` into it and add
`* [STORY-gift-cards-refused-card](../../../features/FEAT-gift-cards/STORY-gift-cards-refused-card.md) — AC 1, 2`
as the first item of its `# Covers`. Run
`python3 .wiki-llm/tools/wiki_llm.py sync` and `validate` (no finding),
commit, push.

## Request
"Fold the refused gift card story into the pay with card story"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Deletes `STORY-gift-cards-refused-card.md`; `STORY-gift-cards-pay-with-card.md` now lists `REQ-gift-cards-reject-invalid` too
- Changes nothing under `shop/tests/`
- `validate` reports the stale group as warnings only (`tests.story-folder`, `links.unresolved` on the gone story); `draft finish` is `ok`
