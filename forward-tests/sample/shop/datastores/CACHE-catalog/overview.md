---
type: Cache
title: Catalog Cache
description: Redis read-through cache for product and category reads.
status: Active
engine: redis
version: "7"
keyPattern: product:{product_id} | category:tree
dataType: json
evictionPolicy: allkeys-lru
ttlSeconds: 3600
maxMemory: 8gb
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Catalog Cache

Redis read-through cache in front of
[products](../DB-shop/TBL-products.md) and
[categories](../DB-shop/TBL-categories.md). The catalog is read
thousands of times for every write, so a product read hits Redis first and falls
back to Postgres only on a miss.

Invalidation is **event-driven, not TTL-driven**: when a product changes,
[SVC-catalog](../../services/SVC-catalog/overview.md) deletes the key as it
publishes [CHAN-product-updated](../../channels/CHAN-product-updated/overview.md).
The one-hour TTL is only a backstop against a missed invalidation, never the
primary freshness mechanism.

# Value

| Key | Value shape |
|---|---|
| `product:{product_id}` | the full product JSON as returned by [EP-products-get](../../services/SVC-catalog/EP-products-get.md) |
| `category:tree` | the whole category tree, one JSON blob |

# Caches

* [TBL-products](../DB-shop/TBL-products.md) — a per-product entry, invalidated on change.
* [TBL-categories](../DB-shop/TBL-categories.md) — the whole tree under one key.
* [EP-products-get](../../services/SVC-catalog/EP-products-get.md) — the endpoint this cache serves.

# Used by

* [Catalog Service](../../services/SVC-catalog/overview.md) — rw
