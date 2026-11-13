---
type: TestCase
title: Refused gift card
description: Prove an invalid gift card is refused with a reason.
risk: high
testType: e2e
testCategory: negative
generated: { by: human:sample-author, at: 2026-10-05T09:00:00Z }
---

# Refused gift card

# Covers

* [REQ-gift-cards-reject-invalid](../../../features/FEAT-gift-cards/overview.md#req-gift-cards-reject-invalid)

# Purpose

Prove an invalid gift card is refused with a reason.

# Preconditions

Shopper has a nonempty cart.

Data that must exist:

* valid card: `GC-VALID-10`, balance 10.00
* expired card: `GC-EXPIRED-01`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Open page Checkout and enter gift card code `GC-EXPIRED-01` | Page Checkout:<br>- message: the card is refused as expired<br>- total: unchanged | Read the page; check the **message** and the **total** |

# Postconditions and cleanup

Delete the cart fixtures.
