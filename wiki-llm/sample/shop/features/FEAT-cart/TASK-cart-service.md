---
type: Task
title: Build the cart service
description: Add/remove/view cart with price snapshotting.
resource: https://acme.atlassian.net/browse/SHOP-160
status: Done
trackerKey: SHOP-160
taskType: dev
prUrl: https://github.com/acme/cart-service/pull/33
mergedAt: 2026-05-11T09:45:00Z
generated: { by: human:sample-author, at: 2026-05-11T09:45:00Z }
verified: { by: human:sample-author, at: 2026-05-11T09:45:00Z }
---

# Build the cart service

Jira `SHOP-160`. Broken out of
[FEAT-cart](overview.md).

# Acceptance

Add, change, remove, and view a cart; the line price is fixed at add time.
Satisfies [REQ-cart-view-total](overview.md#req-cart-view-total),
[REQ-cart-edit-items](overview.md#req-cart-edit-items), and
[REQ-cart-price-fixed-on-add](overview.md#req-cart-price-fixed-on-add).

# Planned scope

* [SVC-cart](../../services/SVC-cart/overview.md) — new — the service.
* [EP-cart-get](../../services/SVC-cart/EP-cart-get.md) — new — read cart.
* [EP-cart-add](../../services/SVC-cart/EP-cart-add.md) — new — add/increment.
* [EP-cart-remove](../../services/SVC-cart/EP-cart-remove.md) — new — remove line.
* [TBL-carts](../../datastores/DB-shop/TBL-carts.md) — new — the cart.
* [TBL-cart_items](../../datastores/DB-shop/TBL-cart-items.md) — new — the lines.

This is the **planned** scope. Actual scope is whatever PR #33 touched; the delta
is drift.
