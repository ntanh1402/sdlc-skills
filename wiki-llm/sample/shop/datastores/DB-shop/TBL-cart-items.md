---
type: Table
title: cart_items
description: One row per (cart, product) line — quantity and the price captured at add time.
status: Active
tableName: cart_items
pii: false
rowCountEstimate: 240000
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# cart_items

Table `cart_items` in [DB-shop](overview.md). The lines
of a [cart](TBL-carts.md).

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `cart_item_id` | uuid | yes | primary key |
| `cart_id` | uuid | yes | → [carts](TBL-carts.md) |
| `product_id` | uuid | yes | → [products](TBL-products.md) |
| `quantity` | int | yes | ≥ 1 |
| `unit_price_usd` | numeric | yes | **captured at add time**, not read live |
| `added_at` | timestamptz | yes | |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_cart_items_cart_product` | `(cart_id, product_id)` | yes |

`unit_price_usd` is snapshotted when the item is added: a price change between
adding to cart and checking out must **not** silently re-price the customer's
cart. The unique index means "add the same product twice" increments quantity
rather than creating a duplicate line.

# Used by

* [Cart Service](../../services/SVC-cart/overview.md) — write
* [Orders Service](../../services/SVC-orders/overview.md) — read
