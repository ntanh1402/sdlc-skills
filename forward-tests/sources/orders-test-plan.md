# Checkout: manual test plan

Kept by the QA team. Version of 2026-01-15. A tester runs these by hand in
the staging shop before each release.

| # | Case | Priority | Steps | Expected result |
|---|---|---|---|---|
| 1 | Checkout needs a login | High | 1. Log out. 2. Open `/checkout` | The login page opens, and after login the shopper is back on `/checkout` |
| 2 | Gift note reaches the packing slip | Medium | 1. Add a mug to the cart. 2. At checkout type the gift note "Happy birthday". 3. Pay with the test card 4242 4242 4242 4242. 4. Open the order in the warehouse tool | The packing slip shows "Happy birthday" |
| 3 | Declined card | High | 1. Add a mug to the cart. 2. Pay with the test card 4000 0000 0000 0002 | The page says the card was declined, the cart still holds the mug, and no order appears under "My orders" |
| 4 | Double click on Pay | Critical | 1. Add a mug to the cart. 2. Click "Pay" twice quickly | "My orders" shows one new order, and the Stripe dashboard shows one payment |
| 5 | Checkout on a phone | Low | 1. Open the checkout page on a phone | |
