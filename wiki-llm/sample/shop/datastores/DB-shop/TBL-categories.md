---
type: Table
title: categories
description: The product category tree — one row per category, self-referencing.
status: Active
tableName: categories
pii: false
rowCountEstimate: 320
resource: https://github.com/acme/catalog-service/blob/main/migrations/0002_categories.sql
generated: { by: sdlc-import/1.0.0, at: 2026-10-01T09:00:00Z }
sources:
  - id: code
    resource: https://github.com/acme/catalog-service
    title: migrations/0002_categories.sql at 9b1d4e7
---

# categories

Table `categories` in [DB-shop](overview.md). A small,
slow-changing tree; every [product](TBL-products.md)
points at exactly one leaf.

# Schema

| Column | Type | Required | Notes |
|---|---|---|---|
| `category_id` | uuid | yes | primary key |
| `parent_id` | uuid | no | → this table, nullable at the root |
| `name` | text | yes | display name |
| `slug` | text | yes | URL segment, unique among siblings |
| `sort_order` | int | yes | position among siblings |

# Indexes

| Index | Columns | Unique |
|---|---|---|
| `uq_categories_parent_slug` | `(parent_id, slug)` | yes |

The tree is shallow (three levels in practice) and read almost every request, so
the catalog service holds it in
[CACHE-catalog](../CACHE-catalog/overview.md) and refreshes on
change rather than joining it on every product read.

# Used by

* [Catalog Service](../../services/SVC-catalog/overview.md) — rw
