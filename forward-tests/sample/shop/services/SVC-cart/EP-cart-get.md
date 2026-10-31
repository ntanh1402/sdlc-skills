---
type: Endpoint
title: Get cart
description: GET /cart — the current cart.
status: Active
method: GET
path: /cart
protocol: http
authType: jwt
idempotent: true
version: "2"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Get cart

`GET /cart`, exposed by [SVC-cart](overview.md). Returns
the caller's open cart with each line re-joined to the current product for title
and image, but priced at the snapshot in
[cart_items](../../datastores/DB-shop/TBL-cart-items.md). Satisfies
[REQ-cart-view-total](../../features/FEAT-cart/overview.md#req-cart-view-total).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Session token. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `cartId` | 200 | string (uuid) | yes | Cart identifier. |
| `items` | 200 | array of `{ productId, title, quantity, unitPriceUsd, lineTotalUsd }` | yes | Current lines; empty when no open cart exists. |
| `totalUsd` | 200 | number | yes | Sum of line totals; zero for an empty cart. |

Response `401` has no response body.

## Status codes

| Code | When |
|---|---|
| 200 | cart returned (possibly empty) |
| 401 | missing or expired session |

# Validations

| Rule | Fails with |
|---|---|
| `Authorization` carries a valid session | `401` |

# Behavior

Resolves the session via
[CACHE-session](../../datastores/CACHE-session/overview.md). If the customer has
no open cart, returns `200` with an empty cart rather than `404` — an empty cart
is a valid state, not a missing resource.

# Flowchart

```mermaid
flowchart TD
    A[GET /cart] --> B{Valid session?}
    B -- no --> X401[401]
    B -- yes --> C{Open cart exists?}
    C -- no --> X200a[200 empty cart]
    C -- yes --> X200b[200 cart with lines and total]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Cart as SVC-cart
    participant Sessions as CACHE-session
    participant Carts as TBL-carts
    participant Items as TBL-cart-items
    participant Products as TBL-products

    Caller->>Cart: GET /cart
    Cart->>Sessions: Resolve bearer token
    alt Session missing or expired
        Sessions-->>Cart: No active session
        Cart-->>Caller: 401 Unauthorized
    else Session active
        Sessions-->>Cart: customerId
        Cart->>Carts: Read customer's open cart
        alt No open cart
            Carts-->>Cart: Not found
            Cart-->>Caller: 200 empty items, zero total
        else Open cart exists
            Carts-->>Cart: cartId
            Cart->>Items: Read lines and snapshotted prices
            Cart->>Products: Join current titles and images
            Products-->>Cart: Product display data
            Cart-->>Caller: 200 cartId, items, totalUsd
        end
    end
```
