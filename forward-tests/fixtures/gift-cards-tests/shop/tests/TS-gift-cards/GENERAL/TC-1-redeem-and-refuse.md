---
type: TestCase
title: Redeem and refuse in one order
description: Prove a valid card pays and an invalid one is refused.
risk: high
testType: e2e
testCategory: functional
generated: { by: human:sample-author, at: 2026-10-05T09:00:00Z }
---

# Redeem and refuse in one order

# Covers

* [REQ-gift-cards-redeem-at-checkout](../../../features/FEAT-gift-cards/overview.md#req-gift-cards-redeem-at-checkout)
* [REQ-gift-cards-reject-invalid](../../../features/FEAT-gift-cards/overview.md#req-gift-cards-reject-invalid)

# Purpose

Prove a valid card pays and an invalid one is refused.

# Preconditions

Shopper has a nonempty cart.

Data that must exist:

* valid card: `GC-VALID-10`, balance 10.00
* expired card: `GC-EXPIRED-01`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Open page Checkout and enter gift card code `GC-VALID-10` | Page Checkout:<br>- gift card applied: 10.00 | Read the page; check the **gift card applied** |
| 2 | Enter gift card code `GC-EXPIRED-01` on page Checkout | Page Checkout:<br>- message: the card is refused as expired | Read the page; check the **message** |

# Postconditions and cleanup

Delete the cart fixtures.
