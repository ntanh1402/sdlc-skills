---
type: Task
title: Build the payments service
description: Authorize and capture via Stripe, idempotent on order.
resource: https://acme.atlassian.net/browse/SHOP-120
status: Done
trackerKey: SHOP-120
taskType: dev
prUrl: https://github.com/acme/payments-service/pull/27
mergedAt: 2026-04-03T15:00:00Z
generated: { by: human:sample-author, at: 2026-04-03T15:00:00Z }
verified: { by: human:sample-author, at: 2026-04-03T15:00:00Z }
---

# Build the payments service

Jira `SHOP-120`. Broken out of
[FEAT-payments](overview.md).

# Acceptance

Authorize a charge with `order_id` as the idempotency key so a retry never
double-charges; capture at fulfilment. Satisfies
[REQ-payments-authorize-once](overview.md#req-payments-authorize-once) and
[REQ-payments-capture-at-fulfilment](overview.md#req-payments-capture-at-fulfilment).

# Planned scope

* [SVC-payments](../../services/SVC-payments/overview.md) — new — the service.
* [EP-payments-authorize](../../services/SVC-payments/EP-payments-authorize.md) — new — authorize.
* [EP-payments-capture](../../services/SVC-payments/EP-payments-capture.md) — new — capture.
* [TBL-payments](../../datastores/DB-shop/TBL-payments.md) — new — the attempt record.
* [EXT-stripe](../../externals/EXT-stripe/overview.md) — new — the payment rail.
* [OP-payment-intents-create](../../externals/EXT-stripe/OP-payment-intents-create.md) — new — authorize call.
* [OP-payment-intents-capture](../../externals/EXT-stripe/OP-payment-intents-capture.md) — new — capture call.
* [CHAN-payment-authorized](../../channels/CHAN-payment-authorized/overview.md) — new — the authorized event.

This is the **planned** scope. Actual scope is whatever PR #27 touched; the delta
is drift.
