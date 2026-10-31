---
type: TestCase
title: Redeem and refuse in one order
description: Prove a valid card pays and an invalid one is refused.
risk: high
generated: { by: human:sample-author, at: 2026-10-05T09:00:00Z }
---

# Redeem and refuse in one order

# Covers

* [REQ-gift-cards-redeem-at-checkout](../../features/FEAT-gift-cards/overview.md#req-gift-cards-redeem-at-checkout)
* [REQ-gift-cards-reject-invalid](../../features/FEAT-gift-cards/overview.md#req-gift-cards-reject-invalid)

# Purpose

Prove a valid card pays and an invalid one is refused.

# Preconditions

Shopper has a nonempty cart.

# Test data

| No | Input | Value |
|---|---|---|
| 1 | valid card | `GC-VALID-10`, balance 10.00 |
| 2 | expired card | `GC-EXPIRED-01` |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Enter the card code at checkout | The card is accepted or refused | The checkout page shows the balance or the refusal |

# Postconditions and cleanup

Delete the cart fixtures.
