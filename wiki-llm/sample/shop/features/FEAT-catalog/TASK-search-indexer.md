---
type: Task
title: Build the search indexer and search endpoint
description: Consume product.updated, index into OpenSearch, expose search.
resource: https://acme.atlassian.net/browse/SHOP-146
status: Done
trackerKey: SHOP-146
taskType: dev
prUrl: https://github.com/acme/search-indexer/pull/58
mergedAt: 2026-05-14T11:30:00Z
generated: { by: human:sample-author, at: 2026-05-14T11:30:00Z }
verified: { by: human:sample-author, at: 2026-05-14T11:30:00Z }
---

# Build the search indexer and search endpoint

Jira `SHOP-146`. Broken out of
[FEAT-catalog](overview.md).

# Acceptance

A `product.updated` event lands in the search index within a minute, and
`GET /products/search` returns faceted results. Satisfies
[REQ-catalog-keyword-search](overview.md#req-catalog-keyword-search).

# Planned scope

* [SVC-search-indexer](../../services/SVC-search-indexer/overview.md) — new — the consumer.
* [SUB-product-updated](../../services/SVC-search-indexer/SUB-product-updated.md) — new — the handler.
* [IDX-products](../../datastores/IDX-products/overview.md) — new — the search index.
* [EP-products-search](../../services/SVC-catalog/EP-products-search.md) — new — the search endpoint.

This is the **planned** scope. Actual scope is whatever PR #58 touched; the delta
is drift.
