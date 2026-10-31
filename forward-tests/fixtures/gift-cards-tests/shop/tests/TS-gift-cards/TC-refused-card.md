---
type: TestCase
title: Refused gift card
description: Prove an invalid gift card is refused with a reason.
risk: high
generated: { by: human:sample-author, at: 2026-10-05T09:00:00Z }
---

# Refused gift card

# Covers

* [REQ-gift-cards-reject-invalid](../../features/FEAT-gift-cards/overview.md#req-gift-cards-reject-invalid)

# Purpose

Prove an invalid gift card is refused with a reason.

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
