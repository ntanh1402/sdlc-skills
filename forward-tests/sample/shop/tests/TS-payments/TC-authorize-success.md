---
type: TestCase
title: Authorize success
description: Prove successful authorization persists and emits once.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Authorize success

# Covers

* [REQ-payments-authorize-once](../../features/FEAT-payments/overview.md#req-payments-authorize-once)

# Purpose

Prove successful authorization persists and emits once.

# Preconditions

Order exists; payment repository/event publisher are isolated; Stripe mock authorizes.

# Test data

| No | Input | Value |
|---|---|---|
| 1 | order ID | a unique order ID |
| 2 | amount | the order's expected amount |
| 3 | payment token | a valid token |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Authorize order | Stripe is called with order idempotency key | Mock records one call with `Idempotency-Key = order_id` |
| 2 | Inspect payment state | Authorized row is persisted | Row order, amount, and status match request/result |
| 3 | Inspect events | One payment.authorized event is emitted | Publisher captures one event with payment/order IDs |

# Postconditions and cleanup

Reset mocks and repository.
