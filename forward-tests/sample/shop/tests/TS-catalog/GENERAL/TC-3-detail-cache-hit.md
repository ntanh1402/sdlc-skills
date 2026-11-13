---
type: TestCase
title: Detail cache hit
description: Prove repeated detail reads use cache without changing response.
risk: med
testType: integration
testCategory: functional
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Detail cache hit

# Covers

* [EP-products-get](../../../services/SVC-catalog/EP-products-get.md)
* [CACHE-catalog](../../../datastores/CACHE-catalog/overview.md)

# Purpose

Prove repeated detail reads use cache without changing response.

# Preconditions

Product exists, cache is empty, and database query counter is enabled.

Data that must exist:

* product: one active product with image metadata

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `GET /products/{id}` with the product's id | Response GET /products/{id}:<br>- status: 200<br>Table products:<br>- Queries run: 1<br>Cache product:{product_id}:<br>- Entry found: yes | Read the query counter and look up the cache key; check **status**, **queries run** and **entry found** |
| 2 | Call API `GET /products/{id}` again with the same id | Response GET /products/{id}:<br>- body: equal to the first response<br>Table products:<br>- Queries run: still 1 | Compare the bodies and read the query counter; check **body** and **queries run** |

# Postconditions and cleanup

Delete product and cache key.
