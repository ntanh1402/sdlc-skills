---
type: TestCase
title: Happy path
description: Prove a shopper completes purchase and receives confirmation.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Happy path

# Covers

* [REQ-checkout-complete-purchase](../../features/FEAT-checkout/overview.md#req-checkout-complete-purchase)
* [SVC-orders](../../services/SVC-orders/overview.md)
* [SVC-cart](../../services/SVC-cart/overview.md)
* [TBL-orders](../../datastores/DB-shop/TBL-orders.md)
* [CHAN-order-created](../../channels/CHAN-order-created/overview.md)

# Purpose

Prove a shopper completes purchase and receives confirmation.

# Preconditions

Active shopper/product exist; cart is empty; Stripe test mode and notification consumer are healthy.

# Test data

One product, quantity one, and Stripe token `tok_visa`.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Log in and add product | Cart contains priced item | UI/API cart matches product, quantity, and snapshot price |
| 2 | Submit checkout | One confirmed order is returned | Response/order row show same ID and confirmed status |
| 3 | Observe downstream effects | One order event and email are produced | Event store/provider stub counts equal one |
| 4 | View confirmation page | Page shows created order | Displayed ID and total match persisted order |

# Postconditions and cleanup

Delete shopper/order/cart fixtures and drain messages.
