---
type: Endpoint
title: Put Order Note
description: PUT /orders/{id}/note — attach or replace the note of an order.
status: Planned
method: PUT
path: /orders/{id}/note
protocol: http
authType: jwt
idempotent: true
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
---

# Put Order Note

`PUT /orders/{id}/note`, exposed by [SVC-orders](overview.md). Called by the
support tool.

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Support session token. |
| `id` | path | string (uuid) | yes | Order identifier. |
| `text` | body | string | yes | The note; 1 to 500 characters. |

# Response

The response has no body.


## Status codes

| Code | When |
|---|---|
| 204 | note stored |
| 401 | missing or expired session |
| 404 | no such order |
| 422 | `text` empty or longer than 500 characters |

# Validations

| Rule | Fails with |
|---|---|
| `Authorization` carries a valid session | `401` |
| `text` is 1 to 500 characters | `422` |
| The order exists | `404` |

# Behavior

1. Read the [order](../../datastores/DB-shop/TBL-orders.md).
2. Store the note in `support_note`, replacing an earlier one.

# Flowchart

```mermaid
flowchart TD
    A[PUT /orders/id/note] --> B{Valid session?}
    B -- no --> X401[401]
    B -- yes --> C{text 1 to 500 characters?}
    C -- no --> X422[422]
    C -- yes --> D{Order exists?}
    D -- no --> X404[404]
    D -- yes --> E[Store support_note, replacing any earlier one]
    E --> X204[204]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Orders as SVC-orders
    participant OrderRows as TBL-orders
    Caller->>Orders: PUT /orders/{id}/note
    alt Session invalid
        Orders-->>Caller: 401
    else text empty or over 500 characters
        Orders-->>Caller: 422
    else Continue
        Orders->>OrderRows: Read order by id
        alt Order missing
            OrderRows-->>Orders: Not found
            Orders-->>Caller: 404
        else Order found
            Orders->>OrderRows: Store support_note
            Orders-->>Caller: 204
        end
    end
```

# Pending changes

* [FEAT-order-notes](../../features/FEAT-order-notes/overview.md) — new — the endpoint is not built yet.
