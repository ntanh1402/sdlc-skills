---
type: Endpoint
title: Capture payment
description: POST /payments/{id}/capture — capture an authorized charge at fulfilment.
status: Active
method: POST
path: /payments/{id}/capture
protocol: http
authType: jwt
idempotent: true
version: "4"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Capture payment

`POST /payments/{id}/capture`, exposed by
[SVC-payments](overview.md). Captures a payment that
was authorized at checkout, called by the fulfilment flow when an order ships.
Separating capture from authorize means the customer is only charged for goods
that actually go out. Satisfies
[REQ-payments-capture-at-fulfilment](../../features/FEAT-payments/overview.md#req-payments-capture-at-fulfilment).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Calling-service token. |
| `id` | path | string (uuid) | yes | Payment to capture. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `status` | 200 | string (`captured`) | yes | Final payment status. |

Responses `401`, `404`, `409`, and `502` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | captured (or already captured) |
| 401 | missing or invalid calling-service token |
| 404 | no such payment |
| 409 | payment not in `authorized` state |
| 502 | Stripe unavailable after retry |

# Validations

| Rule | Fails with |
|---|---|
| `Authorization` carries a valid calling-service token | `401` |
| The payment exists | `404` |
| The payment is `authorized`, or already `captured` | `409` |

# Behavior

Reads the [payments](../../datastores/DB-shop/TBL-payments.md) row, calls
[OP-payment-intents-capture](../../externals/EXT-stripe/OP-payment-intents-capture.md),
and moves the row to `captured`. Capturing an already-captured payment returns
`200` unchanged — capture is idempotent per Stripe intent.

# Flowchart

```mermaid
flowchart TD
    A[POST /payments/id/capture] --> B{Valid calling-service token?}
    B -- no --> X401[401]
    B -- yes --> C{Payment exists?}
    C -- no --> X404[404]
    C -- yes --> D{Status?}
    D -- captured --> X200a[200 unchanged]
    D -- other than authorized --> X409[409]
    D -- authorized --> E[Call OP-payment-intents-capture]
    E --> F{Stripe answers?}
    F -- unavailable after retry --> X502[502]
    F -- captured --> G[Move row to captured]
    G --> X200b[200 captured]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller as Fulfilment flow
    participant Payments as SVC-payments
    participant PaymentRows as TBL-payments
    participant Stripe as OP-payment-intents-capture

    Caller->>Payments: POST /payments/{id}/capture
    Payments->>Payments: Authenticate calling-service token
    alt Token missing or invalid
        Payments-->>Caller: 401 Unauthorized
    else Caller authenticated
        Payments->>PaymentRows: Read payment by id
        alt Payment missing
            PaymentRows-->>Payments: Not found
            Payments-->>Caller: 404 Not Found
        else Already captured
            PaymentRows-->>Payments: captured
            Payments-->>Caller: 200 captured
        else Payment not authorized
            PaymentRows-->>Payments: Invalid state
            Payments-->>Caller: 409 Conflict
        else Payment authorized
            Payments->>Stripe: Capture payment intent
            alt Stripe unavailable after retry
                Stripe-->>Payments: Unavailable
                Payments-->>Caller: 502 Bad Gateway
            else Capture succeeds
                Stripe-->>Payments: Captured
                Payments->>PaymentRows: Mark captured
                Payments-->>Caller: 200 captured
            end
        end
    end
```
