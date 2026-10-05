---
type: TestCase
title: Browse by category
description: Prove category browsing returns only active, paginated products.
risk: med
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Browse by category

# Covers

* [REQ-catalog-browse-by-category](../../features/FEAT-catalog/overview.md#req-catalog-browse-by-category)

# Purpose

Prove category browsing returns only active, paginated products.

# Preconditions

Category contains active and archived products across two pages.

# Test data

Page size two; three active products and one archived product.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Request first category page | Two active products and continuation data | IDs/statuses and pagination fields match fixture |
| 2 | Request next page | Remaining active product only | No duplicate or archived ID appears |
| 3 | Inspect returned images | Every item has signed image URL | URL signature and expiry fields are valid |

# Postconditions and cleanup

Delete category fixtures.
