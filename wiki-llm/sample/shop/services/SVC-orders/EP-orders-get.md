---
type: Endpoint
title: Get Order
description: GET /orders/{id} — read one order.
status: Active
method: GET
path: /orders/{id}
protocol: http
authType: jwt
idempotent: true
version: "6"
resource: https://github.com/acme/orders-service/blob/main/src/main/java/com/acme/orders/OrderController.java
generated: { by: sdlc-import/1.0.0, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T15:00:00Z }
sources:
  - id: openapi
    resource: https://github.com/acme/orders-service/blob/main/openapi.yaml
    title: Orders service OpenAPI document
---

# Get Order

`GET /orders/{id}`, exposed by
[SVC-orders](overview.md). Returns one order and its
lines for the order-confirmation and order-history pages.

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Customer session token. |
| `id` | path | string (uuid) | yes | Order identifier. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `order` | 200 | object | yes | Owned order with lines and status. |

Responses `401` and `404` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | order returned |
| 401 | missing or expired session |
| 404 | no such order for this customer |

# Behavior

Reads [orders](../../datastores/DB-shop/TBL-orders.md). An order that belongs to a
different customer returns `404`, never another customer's order — ownership is
checked against the session, not just the id.

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Orders as SVC-orders
    participant Sessions as CACHE-session
    participant OrderRows as TBL-orders

    Caller->>Orders: GET /orders/{id}
    Orders->>Sessions: Resolve bearer token
    alt Session missing or expired
        Sessions-->>Orders: No active session
        Orders-->>Caller: 401 Unauthorized
    else Session active
        Sessions-->>Orders: customerId
        Orders->>OrderRows: Read order and lines by id and customerId
        alt Order missing or belongs to another customer
            OrderRows-->>Orders: Not found
            Orders-->>Caller: 404 Not Found
        else Owned order found
            OrderRows-->>Orders: Order, lines, status
            Orders-->>Caller: 200 order
        end
    end
```
