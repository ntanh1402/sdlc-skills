---
type: TestCase
title: Double submit is one order
description: Prove checkout idempotency prevents duplicate order and charge.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Double submit is one order

# Covers

* [REQ-checkout-pay-before-confirm](../../features/FEAT-checkout/overview.md#req-checkout-pay-before-confirm)
* [ADR-idempotent-checkout](../../decisions/ADR-idempotent-checkout.md)

# Purpose

Prove checkout idempotency prevents duplicate order and charge.

# Preconditions

Valid cart exists; no order/payment uses the client token.

# Test data

One cart, `tok_visa`, and one fixed client idempotency token.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Submit checkout | Confirmed order is created | Capture returned order ID |
| 2 | Resubmit identical request/token | First result is returned | Order ID/body match first response |
| 3 | Count side effects | Only one order, payment, charge, and event exist | Database/provider/event counts each equal one |

# Postconditions and cleanup

Delete created fixtures.
