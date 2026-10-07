---
type: Endpoint
title: Search products
description: GET /products/search — full-text search and facets.
status: Active
method: GET
path: /products/search
protocol: http
authType: none
rateLimit: 100/s
idempotent: true
version: "3"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Search products

`GET /products/search`, exposed by
[SVC-catalog](overview.md). Full-text search with
category and price facets, served by
[IDX-products](../../datastores/IDX-products/overview.md). Satisfies
[REQ-catalog-keyword-search](../../features/FEAT-catalog/overview.md#req-catalog-keyword-search).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `q` | query | string | no | Search terms; empty falls back to category browsing. |
| `category` | query | string | no | Category facet filter. |
| `minPrice` / `maxPrice` | query | number | no | Inclusive non-negative price range. |
| `page` / `pageSize` | query | integer | no | Result pagination. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `items` | 200 | array of product summaries | yes | Matching active products. |
| `facets` | 200 | object | yes | Category and price-bucket counts. |
| `total` | 200 | integer | yes | Matching document count. |

Responses `400` and `429` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | results (possibly empty) |
| 400 | `minPrice` > `maxPrice` |
| 429 | rate limit exceeded |

# Validations

| Rule | Fails with |
|---|---|
| Request is under the rate limit | `429` |
| `minPrice` is at most `maxPrice` | `400` |

# Behavior

Only `status=active` documents are searchable — the index filters archived
products out, so search can never surface something the detail page would 410.
The search index is eventually consistent with Postgres (see
[SVC-search-indexer](../SVC-search-indexer/overview.md)); a product
edited a second ago may take a moment to re-rank.

# Flowchart

```mermaid
flowchart TD
    A[GET /products/search] --> B{Under the rate limit?}
    B -- no --> X429[429]
    B -- yes --> C{minPrice greater than maxPrice?}
    C -- yes --> X400[400]
    C -- no --> D{q empty?}
    D -- yes --> E[Browse by category]
    D -- no --> F[Query the search index, active only]
    E --> X200[200 results and facets]
    F --> X200
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Catalog as SVC-catalog
    participant Search as IDX-products

    Caller->>Catalog: GET /products/search with filters
    Catalog->>Catalog: Check 100/s rate limit
    alt Rate limit exceeded
        Catalog-->>Caller: 429 Too Many Requests
    else Request allowed
        Catalog->>Catalog: Validate query and non-negative price range
        alt minPrice is greater than maxPrice
            Catalog-->>Caller: 400 Bad Request
        else Filters valid
            opt q is empty
                Catalog->>Catalog: Use category-browse query
            end
            Catalog->>Search: Search status=active documents with facets
            Search-->>Catalog: Items, facets, total
            Catalog-->>Caller: 200 results, possibly empty
        end
    end
```
