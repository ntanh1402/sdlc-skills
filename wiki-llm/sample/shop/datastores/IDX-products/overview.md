---
type: SearchIndex
title: Product Search Index
description: OpenSearch index backing product search and faceting.
status: Active
engine: opensearch
indexName: products-v3
shards: 3
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Product Search Index

OpenSearch index that powers full-text product search and category/price facets
for [EP-products-search](../../services/SVC-catalog/EP-products-search.md). It is
a **derived read model**, never a source of truth: every document is projected
from [products](../DB-shop/TBL-products.md) by
[SVC-search-indexer](../../services/SVC-search-indexer/overview.md), which
consumes [CHAN-product-updated](../../channels/CHAN-product-updated/overview.md).

Because it is derived, it can be rebuilt from Postgres at any time — a corrupt or
lost index is an operational annoyance, not data loss. The `-v3` suffix is the
alias-and-reindex pattern: a rebuild populates `products-v4` and flips the alias,
so search never serves a half-built index.

# Indexed fields

`title` and `description` (analyzed, full-text), `sku`
(keyword), `category_id` and `price_usd` (facets), `status` (filter — only
`active` products are searchable).

# Used by

* [Catalog Service](../../services/SVC-catalog/overview.md) — read
* [Search Indexer](../../services/SVC-search-indexer/overview.md) — write
