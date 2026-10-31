---
type: Table
title: payments
description: One row per payment attempt against an order — the Stripe authorization record.
status: Active
tableName: payments
pii: false
rowCountEstimate: 1200000
partitionKey: created_at (monthly)
retentionPolicy: retained 7 years for finance; no PANs stored
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# payments

Table `payments` in [DB-shop](overview.md). One row per
authorization attempt. **No card data is stored** — only the Stripe
`payment_intent` id; the card never touches this system (see
[EXT-stripe](../../externals/EXT-stripe/overview.md)), which is what keeps the
shop out of PCI-DSS scope for cardholder data.

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `payment_id` | uuid | yes | primary key |
| `order_id` | uuid | yes | → [orders](TBL-orders.md) |
| `stripe_intent_id` | text | yes | Stripe `PaymentIntent` id — the only card handle we keep |
| `amount_usd` | numeric | yes | authorized amount |
| `status` | text | yes | `requires_action` \| `authorized` \| `captured` \| `declined` \| `failed` |
| `decline_code` | text | no | nullable — Stripe decline reason |
| `idempotency_key` | text | yes | our key sent to Stripe, `= order_id` |
| `created_at` | timestamptz | yes | partition key (monthly) |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_payments_idempotency` | `(idempotency_key)` | yes |
| `ix_payments_order` | `(order_id)` | no |

`idempotency_key = order_id`: a retried authorize call for the same order reuses
the same key, so [EXT-stripe](../../externals/EXT-stripe/overview.md) returns the
original PaymentIntent instead of charging twice. That is the same insert-first
idempotency shape as
[notifications](TBL-notifications.md), enforced here by
`uq_payments_idempotency`.

# Used by

* [Payments Service](../../services/SVC-payments/overview.md) — write
