---
type: Endpoint
title: Remove cart item
description: DELETE /cart/items/{id} — remove a line.
status: Active
method: DELETE
path: /cart/items/{id}
protocol: http
authType: jwt
idempotent: true
version: "2"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Remove cart item

`DELETE /cart/items/{id}`, exposed by
[SVC-cart](overview.md). Removes one line from the
caller's cart. Idempotent: deleting a line that is already gone returns `204`, not
`404`, so a double-tap on "remove" is harmless.

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Session token. |
| `id` | path | string (uuid) | yes | `cart_item_id` to remove. |

# Response

Responses `204`, `401`, and `404` have no response body.

## Status codes

| Code | When |
|---|---|
| 204 | removed, or already absent |
| 401 | missing or expired session |
| 404 | line id not in the caller's cart |

# Behavior

Deletes the row from [cart_items](../../datastores/DB-shop/TBL-cart-items.md) only
if it belongs to the caller's cart — a line id from someone else's cart returns
`404`, never a cross-customer delete.

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Cart as SVC-cart
    participant Sessions as CACHE-session
    participant Items as TBL-cart-items

    Caller->>Cart: DELETE /cart/items/{id}
    Cart->>Sessions: Resolve bearer token
    alt Session missing or expired
        Sessions-->>Cart: No active session
        Cart-->>Caller: 401 Unauthorized
    else Session active
        Sessions-->>Cart: customerId
        Cart->>Items: Find line and verify cart ownership
        alt Line belongs to another customer
            Items-->>Cart: Ownership mismatch
            Cart-->>Caller: 404 Not Found
        else Line belongs to caller
            Cart->>Items: Delete line
            Items-->>Cart: Deleted
            Cart-->>Caller: 204 No Content
        else Line already absent
            Items-->>Cart: Not found
            Cart-->>Caller: 204 No Content
        end
    end
```
