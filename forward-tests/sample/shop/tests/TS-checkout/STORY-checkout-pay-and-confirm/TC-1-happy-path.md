---
type: TestCase
title: Happy path
description: Prove a shopper completes purchase and receives confirmation.
risk: critical
testType: e2e
testCategory: functional
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Happy path

# Covers

* [STORY-checkout-pay-and-confirm](../../../features/FEAT-checkout/STORY-checkout-pay-and-confirm.md) — AC 1
* [REQ-checkout-complete-purchase](../../../features/FEAT-checkout/overview.md#req-checkout-complete-purchase)
* [SVC-orders](../../../services/SVC-orders/overview.md)
* [SVC-cart](../../../services/SVC-cart/overview.md)
* [TBL-orders](../../../datastores/DB-shop/TBL-orders.md)
* [CHAN-order-created](../../../channels/CHAN-order-created/overview.md)

# Purpose

Prove a shopper completes purchase and receives confirmation.

# Preconditions

Active shopper/product exist; cart is empty; Stripe test mode and notification consumer are healthy.

Data that must exist:

* product: one product, quantity 1
* payment token: `tok_visa`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Log in as the shopper, then call API `POST /cart/items` with the product and quantity 1 | Response POST /cart/items:<br>- product: the product<br>- quantity: 1<br>- price: the product's current price | Read the response; check **product**, **quantity** and **price** |
| 2 | Call API `POST /orders` with the shopper's cart and payment method `tok_visa` | Response POST /orders:<br>- status: 201<br>- order status: confirmed<br>Table orders:<br>- Rows found for the order id: 1<br>- status: confirmed | Read the response and query table `orders` by the returned order id; check **status**, **order status** and **rows found** |
| 3 | Consume topic `order.created` and read the email provider stub | Topic order.created:<br>- Messages found for the order: 1<br>Email provider stub:<br>- Calls received: 1 | Count the messages and the stub calls; check **messages found** and **calls received** |
| 4 | Open the order confirmation page | Page Order confirmation:<br>- order id: the returned order id<br>- total: the order's `total_usd` | Compare the page with the `orders` row; check **order id** and **total** |

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
