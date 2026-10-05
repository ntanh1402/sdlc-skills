---
type: Table
title: notifications
description: One row per (order, channel) send attempt — the idempotency and audit record.
status: Modifying
tableName: notifications
pii: false
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# notifications

Table `notifications` in [DB-shop](overview.md).

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `notification_id` | uuid | yes | primary key |
| `order_id` | uuid | yes | → [orders](TBL-orders.md) |
| `channel` | text | yes | `email` \| `sms` \| `receipt` |
| `status` | text | yes | `pending` \| `sent` \| `failed` |
| `attempts` | int | yes | retry count |
| `last_error` | text | no | nullable — last provider error |
| `sent_at` | timestamptz | no | nullable until delivered |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_notifications_order_channel` | `(order_id, channel)` | yes |

The unique index is not an optimization — it is the **idempotency mechanism**. A
redelivered [CHAN-order-created](../../channels/CHAN-order-created/overview.md)
message makes the consumer insert before it sends, so the duplicate insert fails
instead of double-sending. Satisfies
[REQ-order-notifications-failure-never-blocks](../../features/FEAT-order-notifications/overview.md#req-order-notifications-failure-never-blocks). Drop this
index and the retry policy starts spamming customers.

# Used by

* [Notifications Service](../../services/SVC-notifications/overview.md) — write

# Pending changes

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — modified — `channel` does not hold `sms` in production yet.
