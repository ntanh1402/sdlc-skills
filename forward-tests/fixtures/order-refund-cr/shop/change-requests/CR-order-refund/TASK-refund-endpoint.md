---
type: Task
title: Build the refund endpoint
description: Add POST /orders/{id}/refund to the orders service.
status: Todo
taskType: dev
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Build the refund endpoint

# Acceptance

- `POST /orders/{id}/refund` with a `reason` refunds a confirmed order and
  returns 200 with status `refunded`.
- A request without `reason` returns 422.
- A second refund of the same order returns 409 and changes nothing.

Satisfies [REQ-checkout-refund-order](overview.md#req-checkout-refund-order).

# Planned scope

* [EP-orders-refund](../../services/SVC-orders/EP-orders-refund.md) — new — the endpoint.
