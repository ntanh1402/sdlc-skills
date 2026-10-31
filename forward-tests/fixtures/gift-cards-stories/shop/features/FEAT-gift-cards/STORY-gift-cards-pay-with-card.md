---
type: UserStory
title: Pay with a gift card
description: A customer pays part or all of an order with a gift card balance.
priority: P1
generated: { by: human:sample-author, at: 2026-10-02T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-02T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Pay with a gift card

As a **customer**, I want to pay with my gift card balance, so that I can use
the card I was given.

# Acceptance criteria

1. **Given** a card with a balance of 50.00, **when** the customer pays an
   order of 30.00 with it, **then** the order is paid and the card keeps 20.00.
   ([REQ-gift-cards-redeem-at-checkout](overview.md#req-gift-cards-redeem-at-checkout))
2. **Given** a card with a balance of 10.00, **when** the customer pays an
   order of 30.00, **then** the card pays 10.00, keeps 0.00, and the customer
   pays the other 20.00 by another method.
   ([REQ-gift-cards-redeem-at-checkout](overview.md#req-gift-cards-redeem-at-checkout))

# Requirements

* [REQ-gift-cards-redeem-at-checkout](overview.md#req-gift-cards-redeem-at-checkout)
