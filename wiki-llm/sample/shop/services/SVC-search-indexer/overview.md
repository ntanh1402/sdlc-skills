---
type: Service
title: Search Indexer
description: Projects product changes into the search index.
resource: https://github.com/acme/search-indexer
status: Active
serviceType: consumer
ownerTeam: catalog
language: go
runtime: go1.22
deployTarget: k8s
slaTier: tier-2
version: "1.6.0"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Search Indexer

A worker with no endpoints. It consumes
[CHAN-product-updated](../../channels/CHAN-product-updated/overview.md), reads the
current product row, and upserts (or deletes, on archive) the corresponding
document in [IDX-products](../../datastores/IDX-products/overview.md).

Keeping this out of [SVC-catalog](../SVC-catalog/overview.md) is
deliberate: the write path stays fast and the index can be rebuilt — replay the
topic, or bulk-reindex from Postgres — without touching the catalog API. A slow
or failing search cluster never slows down a product edit.

# Reads

* [TBL-products](../../datastores/DB-shop/TBL-products.md) — reads the current row named by the event.

# Uses

* [IDX-products](../../datastores/IDX-products/overview.md) — write — the only writer of the index.
