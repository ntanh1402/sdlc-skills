---
type: Endpoint
title: Refund Order
description: POST /orders/{id}/refund — refund a confirmed order in full.
status: Planned
method: POST
path: /orders/{id}/refund
protocol: http
authType: jwt
idempotent: true
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
---

# Refund Order

`POST /orders/{id}/refund`, exposed by [SVC-orders](overview.md). Called by the
support tool.

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Support session token. |
| `id` | path | string (uuid) | yes | Order identifier. |
| `reason` | body | string | yes | Why the order is refunded; 1 to 200 characters. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `orderId` | 200 | string (uuid) | yes | The refunded order. |
| `status` | 200 | string | yes | Always `refunded`. |

Responses `401`, `404`, `409` and `422` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | order refunded |
| 401 | missing or expired session |
| 404 | no such order |
| 409 | the order is not confirmed, or is already refunded |
| 422 | `reason` missing or longer than 200 characters |

# Validations

| Rule | Fails with |
|---|---|
| `Authorization` carries a valid session | `401` |
| `reason` is 1 to 200 characters | `422` |
| The order exists | `404` |
| The order status is `confirmed` | `409` |

# Behavior

1. Read the [order](../../datastores/DB-shop/TBL-orders.md).
2. Refuse with `409` unless its status is `confirmed`.
3. Mark the order `refunded`.

# Flowchart

```mermaid
flowchart TD
    A[POST /orders/id/refund] --> B{Valid session?}
    B -- no --> X401[401]
    B -- yes --> C{reason 1 to 200 characters?}
    C -- no --> X422[422]
    C -- yes --> D{Order exists?}
    D -- no --> X404[404]
    D -- yes --> E{Status is confirmed?}
    E -- no --> X409[409]
    E -- yes --> F[Mark order refunded]
    F --> X200[200 orderId and refunded]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Orders as SVC-orders
    participant OrderRows as TBL-orders
    Caller->>Orders: POST /orders/{id}/refund
    alt Session invalid
        Orders-->>Caller: 401
    else reason missing or over 200 characters
        Orders-->>Caller: 422
    else Continue
        Orders->>OrderRows: Read order by id
        alt Order missing
            OrderRows-->>Orders: Not found
            Orders-->>Caller: 404
        else Status is not confirmed
            OrderRows-->>Orders: Order
            Orders-->>Caller: 409
        else Status is confirmed
            Orders->>OrderRows: Mark refunded
            Orders-->>Caller: 200 orderId and status
        end
    end
```

# Pending changes

* [CR-order-refund](../../change-requests/CR-order-refund/overview.md) — new — the refund endpoint is not built yet.
