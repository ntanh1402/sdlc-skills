# Story folded into another

## Wiki
`forward-tests/seed.sh <dir>` (the sample). Then fold `STORY-checkout-pay-and-confirm` away as `sdlc-write-stories` does: delete it, move its Requirements and criteria to a new story `STORY-checkout-place-order` in the same folder, fix the Task's `# Stories` link, and leave `wiki/shop/tests/` as it is. Sync, validate (the stale group gives warnings only), commit, push.

## Request
"Design the Feature-level tests for checkout again; the stories changed"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- Names the stale group `TS-checkout/STORY-checkout-pay-and-confirm/` and its warnings in the first round
- Moves its three cases into `TS-checkout/GENERAL/`, keeping each file name and id (`TC-1-happy-path`, `TC-2-payment-declined`, `TC-4-double-submit-is-one-order`), drops the link to the gone story from their `# Covers`, deletes the empty group folder, and logs the moves in `GENERAL/log.md`
- Or, when the person says the cases now prove `STORY-checkout-place-order`, names `sdlc-design-story-tests` for it instead of moving them
- The summary's "Next" names `sdlc-design-story-tests STORY-checkout-place-order`
- `validate` gives no warning about `TS-checkout`
