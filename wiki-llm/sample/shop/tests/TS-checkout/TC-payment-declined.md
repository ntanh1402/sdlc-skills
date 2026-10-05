---
type: TestCase
title: Payment declined
description: Prove a declined payment cannot confirm or announce an order.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Payment declined

# Covers

* [REQ-checkout-pay-before-confirm](../../features/FEAT-checkout/overview.md#req-checkout-pay-before-confirm)
* [SVC-payments](../../services/SVC-payments/overview.md)

# Purpose

Prove a declined payment cannot confirm or announce an order.

# Preconditions

Shopper has a valid nonempty cart; event/provider captures are empty.

# Test data

Stripe token `tok_chargeDeclined`.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Submit checkout | Payment failure is returned | HTTP status is 402 with stable decline body |
| 2 | Inspect order | Order remains pending_payment | Exactly one row exists with expected status |
| 3 | Inspect side effects | No confirmation event or charge exists | Event count and successful-charge count are zero |

# Postconditions and cleanup

Delete order/cart fixtures.
