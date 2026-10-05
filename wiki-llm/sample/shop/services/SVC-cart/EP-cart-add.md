---
type: Endpoint
title: Add cart item
description: POST /cart/items — add or increment a line.
status: Active
method: POST
path: /cart/items
protocol: http
authType: jwt
idempotent: false
version: "2"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Add cart item

`POST /cart/items`, exposed by
[SVC-cart](overview.md). Adds a product to the cart, or
increments the quantity if it is already there. Satisfies
[REQ-cart-edit-items](../../features/FEAT-cart/overview.md#req-cart-edit-items).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Session token. |
| `productId` | body | string (uuid) | yes | Product to add. |
| `quantity` | body | integer | no | Quantity to add; defaults to 1. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `cartId` | 201 | string (uuid) | yes | Open cart. |
| `item` | 201 | object | yes | Added or updated cart line. |

Responses `401`, `404`, `409`, and `422` have no response body.

## Status codes

| Code | When |
|---|---|
| 201 | line added or incremented |
| 401 | missing or expired session |
| 404 | no such product |
| 409 | insufficient stock |
| 422 | quantity out of range |

# Validations

| Field | Constraint |
|---|---|
| `productId` | must be an `active` product in [products](../../datastores/DB-shop/TBL-products.md) |
| `quantity` | 1–99 |
| stock | requested quantity ≤ `stock_qty`, else 409 |

# Behavior

Creates the open cart on first add (the partial unique index on
[carts](../../datastores/DB-shop/TBL-carts.md) makes the create race-safe), then
upserts the line, snapshotting `price_usd` into `unit_price_usd`. Adding the same
product twice increments quantity via the unique index on
[cart_items](../../datastores/DB-shop/TBL-cart-items.md) — it never creates a
duplicate line.

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Cart as SVC-cart
    participant Sessions as CACHE-session
    participant Products as TBL-products
    participant Carts as TBL-carts
    participant Items as TBL-cart-items

    Caller->>Cart: POST /cart/items
    Cart->>Sessions: Resolve bearer token
    alt Session missing or expired
        Sessions-->>Cart: No active session
        Cart-->>Caller: 401 Unauthorized
    else Session active
        Sessions-->>Cart: customerId
        Cart->>Cart: Validate quantity
        alt Quantity outside 1-99
            Cart-->>Caller: 422 Unprocessable Entity
        else Quantity valid
            Cart->>Products: Read active product and stock
            alt Product missing or inactive
                Products-->>Cart: Not found
                Cart-->>Caller: 404 Not Found
            else Insufficient stock
                Products-->>Cart: stock_qty below requested quantity
                Cart-->>Caller: 409 Conflict
            else Product available
                Cart->>Carts: Find or race-safely create open cart
                Carts-->>Cart: cartId
                Cart->>Items: Upsert line and snapshot price
                Items-->>Cart: Added or incremented item
                Cart-->>Caller: 201 cartId, item
            end
        end
    end
```
