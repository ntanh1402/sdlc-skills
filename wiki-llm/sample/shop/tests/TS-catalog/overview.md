---
type: TestSuite
title: Catalog Suite
description: Integration tests for browse, detail, search, and indexing.
resource: https://github.com/acme/catalog-service/tree/main/tests/integration
status: Implemented
suiteType: integration
framework: gotest
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Catalog Suite

Integration tests against real Postgres, Redis, and OpenSearch containers: exercise
the read cache, the archived-product cases, and the write-to-search propagation
via a real `product.updated` message.

# Verifies

* [FEAT-catalog](../../features/FEAT-catalog/overview.md) — browse, detail, and search.
