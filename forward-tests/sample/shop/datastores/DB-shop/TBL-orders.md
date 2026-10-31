---
type: Table
title: orders
description: One row per customer order.
status: Active
tableName: orders
pii: false
rowCountEstimate: 1200000
partitionKey: created_at (monthly)
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# orders

Table `orders` in [DB-shop](overview.md).

The services that read and write it are listed under `# Used by`, which the tool
writes from each service's `# Reads` and `# Writes`.

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `order_id` | uuid | yes | primary key |
| `customer_id` | uuid | yes | → [customers](TBL-customers.md) |
| `cart_id` | uuid | yes | → [carts](TBL-carts.md); the cart this order was built from |
| `total_usd` | numeric | yes | order total, summed from the cart at checkout |
| `currency` | text | yes | ISO 4217; `USD` today |
| `status` | text | yes | `pending_payment` \| `confirmed` \| `cancelled` |
| `client_token` | text | yes | idempotency token from the client (see the endpoint) |
| `created_at` | timestamptz | yes | partition key (monthly) |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_orders_client_token` | `(customer_id, client_token)` | yes |
| `ix_orders_customer` | `(customer_id, created_at)` | no |

An order is written `pending_payment`, moves to `confirmed` once
[EP-payments-authorize](../../services/SVC-payments/EP-payments-authorize.md)
returns an authorization, and only then is
[CHAN-order-created](../../channels/CHAN-order-created/overview.md) published. The
unique index on `(customer_id, client_token)` is what makes
[EP-orders-create](../../services/SVC-orders/EP-orders-create.md) safe to retry —
a duplicate submit returns the existing order instead of creating a second one.

# Used by

* [Orders Service](../../services/SVC-orders/overview.md) — write
