---
type: TestCase
title: Archived returns 410
description: Prove archived products disappear from detail and search surfaces.
risk: med
testType: integration
testCategory: negative
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Archived returns 410

# Covers

* [REQ-catalog-product-detail](../../../features/FEAT-catalog/overview.md#req-catalog-product-detail)

# Purpose

Prove archived products disappear from detail and search surfaces.

# Preconditions

Active product exists in database and search index.

Data that must exist:

* product: one product changed from active to archived

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Archive the product: set its status to `archived` through the catalog service | Table products:<br>- status: archived<br>Topic product.updated:<br>- Messages found for the product: 1 | Query the row and read the captured messages; check **status** and **messages found** |
| 2 | Call API `GET /products/{id}` with the product's id | Response GET /products/{id}:<br>- status: 410<br>- product fields: absent | Read the response; check **status** and that no **product field** is returned |
| 3 | Wait until the search indexer has consumed topic `product.updated`, then call API `GET /products/search` with the product's title | Response GET /products/search:<br>- Results with the product's id: 0 | Read the results; check **results with the product's id** |

# Postconditions and cleanup

Delete product and search fixture.
