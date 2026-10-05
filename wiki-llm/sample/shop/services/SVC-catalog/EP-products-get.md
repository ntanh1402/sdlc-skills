---
type: Endpoint
title: Get product
description: GET /products/{id} — one product's detail.
status: Active
method: GET
path: /products/{id}
protocol: http
authType: none
rateLimit: 300/s
idempotent: true
version: "3"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Get product

`GET /products/{id}`, exposed by
[SVC-catalog](overview.md). The product detail page.
Read-through cached, so it is the endpoint
[CACHE-catalog](../../datastores/CACHE-catalog/overview.md) exists to serve.
Satisfies [REQ-catalog-product-detail](../../features/FEAT-catalog/overview.md#req-catalog-product-detail).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `id` | path | string (uuid) | yes | Product identifier. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `product` | 200 | object | yes | Product detail with all image sizes. |

Responses `404`, `410`, and `429` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | product returned |
| 404 | no such product id |
| 410 | product archived |
| 429 | rate limit exceeded |

# Behavior

On a cache miss, reads [products](../../datastores/DB-shop/TBL-products.md), fills
the cache, and returns. An `archived` product returns 410 rather than 404 — the
URL was once valid, which matters for SEO and for old links.

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Catalog as SVC-catalog
    participant Cache as CACHE-catalog
    participant Products as TBL-products

    Caller->>Catalog: GET /products/{id}
    Catalog->>Catalog: Check 300/s rate limit
    alt Rate limit exceeded
        Catalog-->>Caller: 429 Too Many Requests
    else Request allowed
        Catalog->>Cache: Read product detail
        alt Cache hit
            Cache-->>Catalog: Active product
            Catalog-->>Caller: 200 product
        else Cache miss
            Cache-->>Catalog: Miss
            Catalog->>Products: Read product by id
            alt Product does not exist
                Products-->>Catalog: Not found
                Catalog-->>Caller: 404 Not Found
            else Product archived
                Products-->>Catalog: Archived product
                Catalog-->>Caller: 410 Gone
            else Product active
                Products-->>Catalog: Product detail
                Catalog->>Cache: Store product detail
                Cache-->>Catalog: Stored
                Catalog-->>Caller: 200 product
            end
        end
    end
```
