---
type: TestCase
title: Edit propagates to search
description: Prove catalog edits reach search within the consistency SLA.
risk: high
testType: integration
testCategory: data-validation
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Edit propagates to search

# Covers

* [REQ-catalog-keyword-search](../../../features/FEAT-catalog/overview.md#req-catalog-keyword-search)

# Purpose

Prove catalog edits reach search within the consistency SLA.

# Preconditions

Indexed product exists and event-lag timer is enabled.

Data that must exist:

* old title: a unique product title
* new title: a second unique title

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Change the product's title from the old title to the new title through the catalog service | Table products:<br>- title: the new title<br>Topic product.updated:<br>- Messages found: 1<br>- title: the new title | Query the row and read the captured message; check **title** and **messages found** |
| 2 | Wait until the search indexer acknowledges the message on topic `product.updated` | Index products-v3:<br>- title of the product: the new title<br>- Time to update: under 5 seconds | Read the indexed document and the lag timer; check **title** and **time to update** |
| 3 | Call API `GET /products/search` with the new title, then with the old title | Response GET /products/search:<br>- new title: returns the product<br>- old title: returns no result | Read both results; check the **ids** and **titles** returned |

# Postconditions and cleanup

Delete source and search fixtures.
