---
type: TestCase
title: Payment declined
description: Prove a declined payment cannot confirm or announce an order.
risk: critical
testType: e2e
testCategory: negative
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Payment declined

# Covers

* [STORY-checkout-pay-and-confirm](../../../features/FEAT-checkout/STORY-checkout-pay-and-confirm.md) — AC 2
* [REQ-checkout-pay-before-confirm](../../../features/FEAT-checkout/overview.md#req-checkout-pay-before-confirm)
* [SVC-payments](../../../services/SVC-payments/overview.md)

# Purpose

Prove a declined payment cannot confirm or announce an order.

# Preconditions

Shopper has a valid nonempty cart; event/provider captures are empty.

Data that must exist:

* payment token: `tok_chargeDeclined`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /orders` with the shopper's cart and payment method `tok_chargeDeclined` | Response POST /orders:<br>- status: 402<br>- body: none | Read the response; check **status** and that there is no **body** |
| 2 | Query table `orders` for the shopper's cart | Table orders:<br>- Rows found: 1<br>- status: pending_payment | Read the rows; check **rows found** and **status** |
| 3 | Consume topic `order.created` and read the Stripe test-mode charges of the order | Topic order.created:<br>- Messages found for the order: 0<br>Stripe charges:<br>- Successful charges: 0 | Count the messages and the charges; check **messages found** and **successful charges** |

# Postconditions and cleanup

Delete order/cart fixtures.
