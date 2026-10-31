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

| No | Input | Value |
|---|---|---|
| 1 | product | one product, quantity 1 |
| 2 | payment token | `tok_visa` |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Log in and add product | Cart contains priced item | UI/API cart matches product, quantity, and snapshot price |
| 2 | Submit checkout with data 2. Request: see Step 2 | One confirmed order is returned | Response/order row show same ID and confirmed status |
| 3 | Observe downstream effects | One order event and email are produced | Event store/provider stub counts equal one |
| 4 | View confirmation page | Page shows created order | Displayed ID and total match persisted order |

### Step 2

Request:

```http
POST /orders
Authorization: Bearer <shopper session token>
Content-Type: application/json

{
  "cartId": "<the shopper's cart id>",
  "customerId": "<the shopper's id>",
  "paymentMethod": "tok_visa",
  "clientToken": "<a new client token>"
}
```

Expected response:

```http
201 Created

{
  "orderId": "<a uuid>",
  "status": "confirmed"
}
```

Other fields are ignored.

# Postconditions and cleanup

Delete shopper/order/cart fixtures and drain messages.
