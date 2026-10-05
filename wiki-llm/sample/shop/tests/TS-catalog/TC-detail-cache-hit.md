---
type: TestCase
title: Detail cache hit
description: Prove repeated detail reads use cache without changing response.
risk: med
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Detail cache hit

# Covers

* [EP-products-get](../../services/SVC-catalog/EP-products-get.md)
* [CACHE-catalog](../../datastores/CACHE-catalog/overview.md)

# Purpose

Prove repeated detail reads use cache without changing response.

# Preconditions

Product exists, cache is empty, and database query counter is enabled.

# Test data

One active product with image metadata.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Request product detail | Product is returned and cached | One database query and cache key exists |
| 2 | Request same detail again | Identical response comes from cache | Body equality holds and query count remains one |

# Postconditions and cleanup

Delete product and cache key.
