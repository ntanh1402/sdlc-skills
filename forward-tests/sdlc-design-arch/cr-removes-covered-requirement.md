# CR removes a Requirement that TestCases cover

## Wiki
The wiki of `cr-removes-requirement`, built the same way. Also copy `forward-tests/fixtures/gift-cards-tests/shop/tests` into `wiki/shop/`, run `python3 .wiki-llm/tools/wiki_llm.py sync` and `validate`, commit and push to `main`.

## Request
"Design CR-gift-cards-provider-checks"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- In the same draft, `REQ-gift-cards-reject-invalid` is removed from `FEAT-gift-cards`'s Requirements and its Traceability
- The Run plan and the Design gate list the TestCase fix beside the story fix: `GENERAL/TC-2-refused-card` is deleted (it covered only that Requirement); `GENERAL/TC-1-redeem-and-refuse` loses only its `# Covers` link to the Requirement and keeps the link to `REQ-gift-cards-redeem-at-checkout`
- `TS-gift-cards/GENERAL/log.md` records the deleted case and the dropped link; no other TestCase text changes
- No Task, TestSuite or TestGroup `overview.md` is edited
- `CR-gift-cards-provider-checks` `Approved`; `validate` ok on branch `wiki/arch-CR-gift-cards-provider-checks`
