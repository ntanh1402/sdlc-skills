---
type: TestCase
title: Double submit is one order
description: Prove checkout idempotency prevents duplicate order and charge.
risk: critical
testType: e2e
testCategory: error-handling
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Double submit is one order

# Covers

* [STORY-checkout-pay-and-confirm](../../../features/FEAT-checkout/STORY-checkout-pay-and-confirm.md) — AC 3
* [REQ-checkout-pay-before-confirm](../../../features/FEAT-checkout/overview.md#req-checkout-pay-before-confirm)
* [ADR-idempotent-checkout](../../../decisions/ADR-idempotent-checkout.md)

# Purpose

Prove checkout idempotency prevents duplicate order and charge.

# Preconditions

Valid cart exists; no order/payment uses the client token.

Data that must exist:

* cart: one cart
* payment token: `tok_visa`
* idempotency token: one fixed client token

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /orders` with the cart, payment method `tok_visa` and the fixed client token | Response POST /orders:<br>- status: 201<br>- order status: confirmed | Read the response; check **status** and keep the **orderId** |
| 2 | Call API `POST /orders` again with the same cart, payment method `tok_visa` and the same client token | Response POST /orders:<br>- status: 201<br>- orderId: the orderId of the first call | Read the response; check **status** and **orderId** |
| 3 | Query tables `orders` and `payments`, consume topic `order.created` and read the Stripe test-mode charges | Table orders:<br>- Rows found for the client token: 1<br>Table payments:<br>- Rows found: 1<br>Topic order.created:<br>- Messages found: 1<br>Stripe charges:<br>- Charges found: 1 | Count each; check every **rows found**, **messages found** and **charges found** |

# Postconditions and cleanup

Delete created fixtures.
