---
type: Task
title: Build the catalog API and cache
description: Product/category reads and writes, cached, with signed image URLs.
resource: https://acme.atlassian.net/browse/SHOP-140
status: Done
trackerKey: SHOP-140
taskType: dev
prUrl: https://github.com/acme/catalog-service/pull/51
mergedAt: 2026-05-02T14:10:00Z
generated: { by: human:sample-author, at: 2026-05-02T14:10:00Z }
verified: { by: human:sample-author, at: 2026-05-02T14:10:00Z }
---

# Build the catalog API and cache

Jira `SHOP-140`. Broken out of
[FEAT-catalog](overview.md).

# Acceptance

`GET /products`, `GET /products/{id}` serve from cache with a Postgres fallback;
writes publish `product.updated`. Satisfies
[REQ-catalog-browse-by-category](overview.md#req-catalog-browse-by-category) and
[REQ-catalog-product-detail](overview.md#req-catalog-product-detail).

# Planned scope

* [SVC-catalog](../../services/SVC-catalog/overview.md) — new — the service.
* [EP-products-list](../../services/SVC-catalog/EP-products-list.md) — new — browse.
* [EP-products-get](../../services/SVC-catalog/EP-products-get.md) — new — detail.
* [TBL-products](../../datastores/DB-shop/TBL-products.md) — new — the source of truth.
* [TBL-categories](../../datastores/DB-shop/TBL-categories.md) — new — the tree.
* [CACHE-catalog](../../datastores/CACHE-catalog/overview.md) — new — read-through cache.
* [BLOB-product-images](../../datastores/BLOB-product-images/overview.md) — new — image bucket.
* [CHAN-product-updated](../../channels/CHAN-product-updated/overview.md) — new — the change topic.

This is the **planned** scope. Actual scope is whatever PR #51 touched; the delta
is drift.
