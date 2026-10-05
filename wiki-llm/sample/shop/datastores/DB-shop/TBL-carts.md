---
type: Table
title: carts
description: One open cart per customer; the checkout reads it to build the order.
status: Active
tableName: carts
pii: false
rowCountEstimate: 90000
retentionPolicy: abandoned carts purged after 30 days by a nightly job
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# carts

Table `carts` in [DB-shop](overview.md). At most one
`open` cart per customer; checkout marks it `ordered` when the order is created.

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `cart_id` | uuid | yes | primary key |
| `customer_id` | uuid | yes | → [customers](TBL-customers.md) |
| `status` | text | yes | `open` \| `ordered` \| `abandoned` |
| `created_at` | timestamptz | yes | drives the 30-day abandonment purge |
| `updated_at` | timestamptz | yes | last item change |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_carts_customer_open` | `(customer_id) WHERE status='open'` | yes |

The partial unique index guarantees **one open cart per customer** at the
database level, so two concurrent "add to cart" requests cannot create two carts.
The line items live in
[cart_items](TBL-cart-items.md).

# Used by

* [Cart Service](../../services/SVC-cart/overview.md) — write
* [Orders Service](../../services/SVC-orders/overview.md) — read
