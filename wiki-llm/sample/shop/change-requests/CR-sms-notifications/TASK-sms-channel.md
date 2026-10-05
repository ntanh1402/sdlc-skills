---
type: Task
title: Add the SMS notification channel
description: Send an SMS via Twilio alongside the confirmation email.
resource: https://acme.atlassian.net/browse/SHOP-211
status: Todo
trackerKey: SHOP-211
taskType: dev
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Add the SMS notification channel

Jira `SHOP-211`. Broken out of
[CR-sms-notifications](overview.md).

# Acceptance

An `order.created` message sends both an email and an SMS, unless the customer has
opted out of that channel. Satisfies
[REQ-order-notifications-channel-opt-out](../../features/FEAT-order-notifications/overview.md#req-order-notifications-channel-opt-out).

# Planned scope

* [EXT-twilio](../../externals/EXT-twilio/overview.md) — new — the SMS provider.
* [OP-messages-create](../../externals/EXT-twilio/OP-messages-create.md) — new — the call we make on it.
* [SVC-notifications](../../services/SVC-notifications/overview.md) — modified — the second send path.
* [SUB-order-created](../../services/SVC-notifications/SUB-order-created.md) — modified — the handler loops over channels.
* [TBL-customers](../../datastores/DB-shop/TBL-customers.md) — modified — `phone`, `sms_opt_out`.

This is the **planned** scope. Actual scope is whatever the merged change-set
touched; the delta is drift.
