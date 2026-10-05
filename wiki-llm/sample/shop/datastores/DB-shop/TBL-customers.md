---
type: Table
title: customers
description: One row per customer, with contact details and per-channel opt-outs.
status: Modifying
tableName: customers
pii: true
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# customers

Table `customers` in [DB-shop](overview.md). Holds PII —
email and phone. Read-only to everything outside the customer domain.

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | uuid | yes | primary key |
| `email` | text | yes | **PII** |
| `phone` | text | no | **PII**, nullable — not every customer has one |
| `email_opt_out` | boolean | yes | true = do not email |
| `sms_opt_out` | boolean | yes | true = do not SMS |

A carrier-level STOP reply sets `sms_opt_out` — see
[OP-messages-create](../../externals/EXT-twilio/OP-messages-create.md).

# Used by

* [Accounts Service](../../services/SVC-accounts/overview.md) — rw
* [Notifications Service](../../services/SVC-notifications/overview.md) — read
* [Orders Service](../../services/SVC-orders/overview.md) — read

# Pending changes

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — modified — `phone` and `sms_opt_out` are not in production yet.
