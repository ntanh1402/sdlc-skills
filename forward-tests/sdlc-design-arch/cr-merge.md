# Cr merge

## Wiki
`forward-tests/seed.sh <dir> --fixture cart-clear-cr`.

## Request
"Design CR-cart-clear"

## Answers
- Approve

## Expected
- `# Delta` filled
- `CR-cart-clear` `Approved` (it was `ReqApproved`), with `designBasedOn` naming its version; the target Feature updated in the same draft
- `FEAT-cart`'s Requirements gain `REQ-cart-clear-all` and its Architecture shows the change
- `SVC-cart` (or its endpoint) `Modifying` with an entry for `CR-cart-clear`
- `validate` ok
