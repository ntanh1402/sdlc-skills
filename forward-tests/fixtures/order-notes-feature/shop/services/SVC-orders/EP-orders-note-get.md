---
type: Endpoint
title: Get Order Note
description: GET /orders/{id}/note — read the note of an order.
status: Planned
method: GET
path: /orders/{id}/note
protocol: http
authType: jwt
idempotent: true
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
---

# Get Order Note

`GET /orders/{id}/note`, exposed by [SVC-orders](overview.md). Called by the
support tool.

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Support session token. |
| `id` | path | string (uuid) | yes | Order identifier. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `text` | 200 | string | yes | The note. |

Responses `401` and `404` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | the note |
| 401 | missing or expired session |
| 404 | no such order, or the order has no note |

# Validations

| Rule | Fails with |
|---|---|
| `Authorization` carries a valid session | `401` |
| The order exists and has a note | `404` |

# Behavior

1. Read `support_note` of the [order](../../datastores/DB-shop/TBL-orders.md).
2. Answer `404` when there is none.

# Flowchart

```mermaid
flowchart TD
    A[GET /orders/id/note] --> B{Valid session?}
    B -- no --> X401[401]
    B -- yes --> C[Read support_note of the order]
    C --> D{Order exists and has a note?}
    D -- no --> X404[404]
    D -- yes --> X200[200 text]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Orders as SVC-orders
    participant OrderRows as TBL-orders
    Caller->>Orders: GET /orders/{id}/note
    alt Session invalid
        Orders-->>Caller: 401
    else Session valid
        Orders->>OrderRows: Read support_note by id
        alt Order missing or no note
            OrderRows-->>Orders: Not found or empty
            Orders-->>Caller: 404
        else Note found
            OrderRows-->>Orders: support_note
            Orders-->>Caller: 200 text
        end
    end
```

# Pending changes

* [FEAT-order-notes](../../features/FEAT-order-notes/overview.md) — new — the endpoint is not built yet.
