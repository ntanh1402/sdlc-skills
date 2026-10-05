---
type: TestCase
title: Archived returns 410
description: Prove archived products disappear from detail and search surfaces.
risk: med
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Archived returns 410

# Covers

* [REQ-catalog-product-detail](../../features/FEAT-catalog/overview.md#req-catalog-product-detail)

# Purpose

Prove archived products disappear from detail and search surfaces.

# Preconditions

Active product exists in database and search index.

# Test data

One product changed from active to archived.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Archive product | Source record becomes archived | Database status and update event match product ID |
| 2 | Request product detail | Gone response is returned | Status is 410 and no product body is exposed |
| 3 | Search after indexer drains | Product is absent | Search result contains zero matching IDs |

# Postconditions and cleanup

Delete product and search fixture.
