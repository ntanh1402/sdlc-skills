---
type: Task
title: Remove the order lookup endpoint
description: Delete GET /orders/{id} from the orders service.
status: Todo
taskType: dev
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Remove the order lookup endpoint

# Acceptance

`GET /orders/{id}` returns 404 for every id, and its handler and its entry in
the OpenAPI file are gone.

Satisfies [REQ-checkout-no-direct-order-lookup](overview.md#req-checkout-no-direct-order-lookup).

# Planned scope

* [EP-orders-get](../../services/SVC-orders/EP-orders-get.md) — removed — the endpoint.
