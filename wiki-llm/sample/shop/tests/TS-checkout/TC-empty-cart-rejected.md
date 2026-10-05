---
type: TestCase
title: Empty cart rejected
description: Prove invalid empty checkout has no side effects.
risk: high
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Empty cart rejected

# Covers

* [REQ-checkout-complete-purchase](../../features/FEAT-checkout/overview.md#req-checkout-complete-purchase)

# Purpose

Prove invalid empty checkout has no side effects.

# Preconditions

Authenticated shopper has an empty cart.

# Test data

Empty cart and valid payment token.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Submit checkout | Validation failure is returned | Status is 422 and body names empty cart |
| 2 | Inspect downstream systems | No order, payment, charge, or event exists | All relevant counts remain zero |

# Postconditions and cleanup

Delete shopper/cart fixtures.
