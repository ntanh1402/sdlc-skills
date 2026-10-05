---
type: Task
title: Implement order creation endpoint
description: Build POST /orders in the orders service.
resource: https://acme.atlassian.net/browse/SHOP-123
status: Done
trackerKey: SHOP-123
taskType: dev
mergedAt: 2026-06-20T14:05:00Z
mergeCommitSha: 7c2e41a
generated: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
---

# Implement order creation endpoint

Jira `SHOP-123`. Broken out of
[FEAT-checkout](overview.md).

# Acceptance

`POST /orders` persists an order and emits `order.created`. Satisfies
[REQ-checkout-complete-purchase](overview.md#req-checkout-complete-purchase).

# Stories

* [STORY-checkout-pay-and-confirm](STORY-checkout-pay-and-confirm.md)
* [STORY-checkout-retry-safely](STORY-checkout-retry-safely.md)

# Planned scope

* [SVC-orders](../../services/SVC-orders/overview.md) — new — the service itself.
* [EP-orders-create](../../services/SVC-orders/EP-orders-create.md) — new — the endpoint.
* [TBL-orders](../../datastores/DB-shop/TBL-orders.md) — new — the table it writes.
* [CHAN-order-created](../../channels/CHAN-order-created/overview.md) — new — the topic it publishes.

This is the **planned** scope. Actual scope is whatever the merged change-set
touched; the delta is drift.
