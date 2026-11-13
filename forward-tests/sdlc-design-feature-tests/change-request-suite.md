# ChangeRequest gets its own suite

## Wiki
The directory left by `sdlc-design-arch/downstream-stale.md`, after merging `wiki/arch-CR-checkout-address-validation` into `main` (an `Approved` ChangeRequest on `FEAT-checkout` with a designed Delta).

## Request
"Design the e2e tests for it"

## Answers
- Approve

## Expected
- Writes a new suite `TS-checkout-address-validation` whose `# Verifies` links only `CR-checkout-address-validation`, and its `GENERAL/` group with `basedOn` of the CR's version
- Its cases are numbered from `TC-1-…`, all in `GENERAL/`; a case that proves only one story's criteria is named for `sdlc-design-story-tests`, not written
- Does not change `TS-checkout` or any of its cases
