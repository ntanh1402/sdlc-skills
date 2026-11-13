---
type: TestCase
title: Browse by category
description: Prove category browsing returns only active, paginated products.
risk: med
testType: integration
testCategory: functional
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Browse by category

# Covers

* [REQ-catalog-browse-by-category](../../../features/FEAT-catalog/overview.md#req-catalog-browse-by-category)

# Purpose

Prove category browsing returns only active, paginated products.

# Preconditions

Category contains active and archived products across two pages.

Data that must exist:

* page size: 2
* active products: 3 in the category
* archived product: 1 in the category

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `GET /products` with the category and page size 2 | Response GET /products:<br>- items: 2 active products of the category<br>- next cursor: present | Read the response; check the **ids** and **statuses** of the items and the **next cursor** |
| 2 | Call API `GET /products` with the category, page size 2 and the next cursor of the first page | Response GET /products:<br>- items: the third active product only<br>- archived product: absent | Read the response; check the **ids**: no duplicate and no **archived** product |
| 3 | Read the image URL of every item the two calls returned | Image URLs:<br>- bucket: acme-shop-product-images<br>- signature: valid<br>- expiry: in the future | Parse each URL; check **bucket**, **signature** and **expiry** |

# Postconditions and cleanup

Delete category fixtures.
