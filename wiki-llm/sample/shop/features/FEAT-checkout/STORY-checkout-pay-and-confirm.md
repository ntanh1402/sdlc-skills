---
type: UserStory
title: Pay and get an order confirmation
description: A shopper turns a cart into one confirmed, paid order.
priority: P1
generated: { by: human:sample-author, at: 2026-10-05T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-05T09:00:00Z }
---

# Pay and get an order confirmation

As a **shopper**, I want to pay for my cart and get an order confirmation, so
that I know my order is placed.

# Acceptance criteria

1. **Given** a cart with two items totalling 40.00, **when** the shopper pays
   with a valid card, **then** they see a confirmation with an order number.
   ([REQ-checkout-complete-purchase](overview.md#req-checkout-complete-purchase))
2. **Given** a cart totalling 40.00, **when** the card is declined, **then**
   no order is confirmed and the cart is unchanged.
   ([REQ-checkout-pay-before-confirm](overview.md#req-checkout-pay-before-confirm))

# Requirements

* [REQ-checkout-complete-purchase](overview.md#req-checkout-complete-purchase)
* [REQ-checkout-pay-before-confirm](overview.md#req-checkout-pay-before-confirm)
