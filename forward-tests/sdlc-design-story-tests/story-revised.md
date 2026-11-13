# Story revised after its tests

## Wiki
The directory left by `first-story-group.md`, after merging `wiki/tests-STORY-gift-cards-pay-with-card` into `main`. Then add a criterion 3 to `STORY-gift-cards-pay-with-card.md` (a card used twice in one order is refused, citing `REQ-gift-cards-single-use-per-order`, which the story then lists), sync, commit, push. `validate` warns that AC 3 is covered by no case.

## Request
"The pay with card story changed; update its tests"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Names the `tests.story-ac` warning in the first round
- Adds a case for AC 3 with the next id in the suite; changes no other case except one whose named criteria no longer say what it proves
- Logs the change in the group's `log.md`
- `validate` gives no warning about the group
