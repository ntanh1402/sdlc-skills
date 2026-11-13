# A case moved to GENERAL

## Wiki
The directory left by `first-story-group.md`, after merging `wiki/tests-STORY-gift-cards-pay-with-card` into `main`, with no `GENERAL/` group in `TS-gift-cards`. Then remove `REQ-gift-cards-reject-invalid` from `STORY-gift-cards-pay-with-card.md` (from `# Requirements` and from the criterion that cites it, which is deleted and the rest renumbered), sync, commit, push. A case of the group that covered only that Requirement now gives `tests.story-covers` and `tests.story-ac` warnings.

## Request
"The pay with card story changed; update its tests"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Moves that case to `TS-gift-cards/GENERAL/`, keeping its file name and id, and drops the story link from its `# Covers`
- Creates `GENERAL/overview.md` with `status: Draft`, `basedOn` and a `# Scope`, and `GENERAL/log.md` with the move
- Corrects the AC numbers the other cases name after the renumbering
- The Run plan's `## Files` lists the moved case and the `GENERAL/` files
- `validate` ok, with no `tests.general-story` error and no warning about the story group
