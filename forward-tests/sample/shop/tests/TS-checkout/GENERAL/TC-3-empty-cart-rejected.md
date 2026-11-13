---
type: TestCase
title: Empty cart rejected
description: Prove invalid empty checkout has no side effects.
risk: high
testType: e2e
testCategory: field-validation
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Empty cart rejected

# Covers

* [REQ-checkout-complete-purchase](../../../features/FEAT-checkout/overview.md#req-checkout-complete-purchase)

# Purpose

Prove invalid empty checkout has no side effects.

# Preconditions

Authenticated shopper has an empty cart.

Data that must exist:

* cart: an empty cart
* payment token: `tok_visa`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /orders` with the shopper's empty cart and payment method `tok_visa` | Response POST /orders:<br>- status: 422<br>- body: none | Read the response; check **status** and that there is no **body** |
| 2 | Query tables `orders` and `payments`, consume topic `order.created` and read the Stripe test-mode charges | Table orders:<br>- Rows found for the cart: 0<br>Table payments:<br>- Rows found: 0<br>Topic order.created:<br>- Messages found: 0<br>Stripe charges:<br>- Charges found: 0 | Count each; check every **rows found**, **messages found** and **charges found** |

# Postconditions and cleanup

Delete shopper/cart fixtures.
