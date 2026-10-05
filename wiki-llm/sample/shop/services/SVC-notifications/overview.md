---
type: Service
title: Notifications Service
description: Consumes order events and notifies the customer by email and SMS.
resource: https://github.com/acme/notifications-service
status: Modifying
serviceType: consumer
ownerTeam: growth
language: python
deployTarget: k8s
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Notifications Service

A worker, not an API — it exposes no endpoints. It subscribes to order events,
resolves the customer's contact details and opt-outs, and sends on every channel
the customer still accepts.

Failures retry with backoff and never propagate back to
[SVC-orders](../SVC-orders/overview.md) — the event is the boundary,
and that is what keeps a notification outage from becoming a checkout outage.

# Calls

* [OP-mail-send](../../externals/EXT-sendgrid/OP-mail-send.md) — sends the confirmation email. A SendGrid outage stops email; sends queue and retry.
* [OP-messages-create](../../externals/EXT-twilio/OP-messages-create.md) — sends the confirmation SMS. An outage degrades SMS only; email still goes out.

# Reads

* [TBL-customers](../../datastores/DB-shop/TBL-customers.md) — email, phone, and per-channel opt-outs.

# Writes

* [TBL-notifications](../../datastores/DB-shop/TBL-notifications.md) — one row per (order, channel) send attempt.

# Pending changes

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — modified — the SMS send path and the call to Twilio are not live yet.
