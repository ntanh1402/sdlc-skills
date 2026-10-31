# Material drift

## Wiki
`forward-tests/seed.sh <dir> --fixture cart-clear-cr`; then put `<dir>/workspace/cart-api/openapi.yaml` declaring no remove-item endpoint at all.

## Request
"Design CR-cart-clear; the cart service code is in cart-api"

## Answers
- None scripted; improvise the most plausible short reply

## Expected
- Reports material Drift with both paths
- Stops before the Intent gate and asks which is true
- Names the remedy for each answer: `sdlc-import` on the cart code when the wiki is wrong, a bugfix ChangeRequest when the code is wrong
- No draft
