---
type: Endpoint
title: List products
description: GET /products — browse a category page.
status: Active
method: GET
path: /products
protocol: http
authType: none
rateLimit: 200/s
idempotent: true
version: "3"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# List products

`GET /products`, exposed by
[SVC-catalog](overview.md). Public — no auth; the
storefront calls it for every category page. Satisfies
[REQ-catalog-browse-by-category](../../features/FEAT-catalog/overview.md#req-catalog-browse-by-category).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `category` | query | string (slug) | no | Category filter. |
| `page` | query | integer | no | Page number; defaults to 1. |
| `pageSize` | query | integer | no | Items per page; defaults to 24 and is capped at 100. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `items` | 200 | array of product summaries | yes | Active products with signed card-image URLs. |
| `total` | 200 | integer | yes | Matching active-product count. |

Responses `404` and `429` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | page returned |
| 404 | unknown category slug |
| 429 | rate limit exceeded |

# Validations

| Rule | Fails with |
|---|---|
| Request is under the rate limit | `429` |
| `category`, when given, resolves to a category slug | `404` |

# Behavior

A `pageSize` over 100 is clamped to 100, not rejected. Served from [CACHE-catalog](../../datastores/CACHE-catalog/overview.md); only
`active` products appear. Each item carries a signed
[image](../../datastores/BLOB-product-images/overview.md) URL for the `card` size.

# Flowchart

```mermaid
flowchart TD
    A[GET /products] --> B{Under the rate limit?}
    B -- no --> X429[429]
    B -- yes --> C[Clamp pageSize to 100]
    C --> D{Category given and unknown?}
    D -- yes --> X404[404]
    D -- no --> E[Read active products from CACHE-catalog]
    E --> X200[200 page]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Catalog as SVC-catalog
    participant Cache as CACHE-catalog
    participant Images as BLOB-product-images

    Caller->>Catalog: GET /products with filters
    Catalog->>Catalog: Check 200/s rate limit
    alt Rate limit exceeded
        Catalog-->>Caller: 429 Too Many Requests
    else Request allowed
        Catalog->>Catalog: Clamp pageSize to 1-100 and resolve category
        alt Category slug is unknown
            Catalog-->>Caller: 404 Not Found
        else Category valid or omitted
            Catalog->>Cache: Read active product page
            Cache-->>Catalog: Product summaries and total
            loop Each product summary
                Catalog->>Images: Sign card-size image URL
                Images-->>Catalog: Signed URL
            end
            Catalog-->>Caller: 200 items, total
        end
    end
```
