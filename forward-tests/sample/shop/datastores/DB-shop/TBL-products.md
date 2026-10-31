---
type: Table
title: products
description: One row per sellable product, the catalog's source of truth.
status: Active
tableName: products
pii: false
rowCountEstimate: 45000
retentionPolicy: never deleted; discontinued products set status=archived
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# products

Table `products` in [DB-shop](overview.md). The
**write-side source of truth** for the catalog. Reads are served from
[CACHE-catalog](../CACHE-catalog/overview.md) and searches from
[IDX-products](../IDX-products/overview.md); both are derived from
this table, never the other way round.

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `product_id` | uuid | yes | primary key |
| `sku` | text | yes | unique, human-facing stock code |
| `title` | text | yes | display name |
| `description` | text | yes | long description |
| `price_usd` | numeric | yes | current list price |
| `currency` | text | yes | ISO 4217; `USD` today, column exists for later markets |
| `category_id` | uuid | yes | → [categories](TBL-categories.md) |
| `status` | text | yes | `draft` \| `active` \| `archived` |
| `image_key` | text | no | object key in [BLOB-product-images](../BLOB-product-images/overview.md), nullable |
| `stock_qty` | int | yes | on-hand units |
| `updated_at` | timestamptz | yes | drives cache and index invalidation |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_products_sku` | `(sku)` | yes |
| `ix_products_category` | `(category_id, status)` | no |
| `ix_products_updated_at` | `(updated_at)` | no |

Every update bumps `updated_at`; the catalog service reads that column to decide
what to publish on
[CHAN-product-updated](../../channels/CHAN-product-updated/overview.md), which is
how [IDX-products](../IDX-products/overview.md) and
[CACHE-catalog](../CACHE-catalog/overview.md) stay fresh without a
nightly rebuild.

# Used by

* [Cart Service](../../services/SVC-cart/overview.md) — read
* [Catalog Service](../../services/SVC-catalog/overview.md) — rw
* [Search Indexer](../../services/SVC-search-indexer/overview.md) — read
