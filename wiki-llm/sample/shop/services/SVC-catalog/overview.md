---
type: Service
title: Catalog Service
description: Serves product and category reads, and owns product writes.
resource: https://github.com/acme/catalog-service
status: Active
serviceType: api
ownerTeam: catalog
language: go
framework: chi
runtime: go1.22
deployTarget: k8s
slaTier: tier-1
version: "3.4.0"
port: 8080
healthcheckPath: /healthz
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Catalog Service

The read path for the storefront and the write path for merchandisers. Reads are
served from [CACHE-catalog](../../datastores/CACHE-catalog/overview.md) with
Postgres as the fallback; searches go to
[IDX-products](../../datastores/IDX-products/overview.md); image URLs are signed
against [BLOB-product-images](../../datastores/BLOB-product-images/overview.md).

Writes go to Postgres and then publish
[CHAN-product-updated](../../channels/CHAN-product-updated/overview.md) — the
service never writes the search index directly. That is
[SVC-search-indexer](../SVC-search-indexer/overview.md)'s job, so the
read model can be rebuilt independently of the write path.

# Publishes

* [CHAN-product-updated](../../channels/CHAN-product-updated/overview.md) — emitted after a product row is committed.

# Reads

* [TBL-products](../../datastores/DB-shop/TBL-products.md) — the product source of truth.
* [TBL-categories](../../datastores/DB-shop/TBL-categories.md) — the category tree.

# Writes

* [TBL-products](../../datastores/DB-shop/TBL-products.md) — merchandiser create/edit/archive.
* [TBL-categories](../../datastores/DB-shop/TBL-categories.md) — category tree edits.

# Uses

* [CACHE-catalog](../../datastores/CACHE-catalog/overview.md) — rw — read-through on reads, key-delete on writes.
* [IDX-products](../../datastores/IDX-products/overview.md) — read — search queries only; writes go through the indexer.
* [BLOB-product-images](../../datastores/BLOB-product-images/overview.md) — read — signs short-lived image URLs.
