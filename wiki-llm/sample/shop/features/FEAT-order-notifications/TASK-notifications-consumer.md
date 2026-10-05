---
type: Task
title: Build the notifications consumer and email send
description: Consume order.created, look up the customer, send the confirmation email.
resource: https://acme.atlassian.net/browse/SHOP-201
status: Done
trackerKey: SHOP-201
taskType: dev
prUrl: https://github.com/acme/notifications-service/pull/88
mergedAt: 2026-07-08T16:20:00Z
generated: { by: human:sample-author, at: 2026-07-08T16:20:00Z }
verified: { by: human:sample-author, at: 2026-07-08T16:20:00Z }
---

# Build the notifications consumer and email send

Jira `SHOP-201`. Broken out of
[FEAT-order-notifications](overview.md).

# Acceptance

An `order.created` message results in exactly one confirmation email, and a
redelivered message sends nothing. Satisfies
[REQ-order-notifications-confirmation-sent](overview.md#req-order-notifications-confirmation-sent) and
[REQ-order-notifications-failure-never-blocks](overview.md#req-order-notifications-failure-never-blocks).

# Planned scope

* [SVC-notifications](../../services/SVC-notifications/overview.md) — new — the consumer itself.
* [SUB-order-created](../../services/SVC-notifications/SUB-order-created.md) — new — the handler.
* [TBL-notifications](../../datastores/DB-shop/TBL-notifications.md) — new — the idempotency record.
* [EXT-sendgrid](../../externals/EXT-sendgrid/overview.md) — new — the email provider.

This is the **planned** scope. Actual scope is whatever PR #88 touched; the delta
is drift.
