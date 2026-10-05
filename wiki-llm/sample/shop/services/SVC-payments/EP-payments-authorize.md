---
type: Endpoint
title: Authorize payment
description: POST /payments/authorize — authorize a charge for an order.
status: Active
method: POST
path: /payments/authorize
protocol: http
authType: jwt
idempotent: true
version: "4"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Authorize payment

`POST /payments/authorize`, exposed by
[SVC-payments](overview.md). Called synchronously by
[SVC-orders](../SVC-orders/overview.md) during checkout, before the
order is confirmed. Satisfies
[REQ-payments-authorize-once](../../features/FEAT-payments/overview.md#req-payments-authorize-once).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Calling-service token. |
| `orderId` | body | string (uuid) | yes | Order and idempotency key. |
| `amountUsd` | body | number | yes | Amount that must match the server-side order total. |
| `paymentMethod` | body | string | yes | Stripe token from the browser. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `paymentId` | 200, 402 | string (uuid) | yes | Payment attempt. |
| `status` | 200, 402 | string (`authorized` \| `declined`) | yes | Authorization result. |
| `declineCode` | 402 | string | conditional | Required when `status` is `declined`. |

Responses `401`, `409`, `422`, and `502` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | authorized |
| 401 | missing or invalid calling-service token |
| 402 | card declined (terminal; body carries `declineCode`) |
| 409 | order not in `pending_payment` |
| 422 | amount does not match the order total |
| 502 | Stripe unavailable after retry |

# Validations

| Field | Constraint |
|---|---|
| `orderId` | must reference an order in `pending_payment` |
| `amountUsd` | must equal the order total server-side — never trust the client amount |

# Behavior

Idempotent on `orderId`: the row in
[payments](../../datastores/DB-shop/TBL-payments.md) is inserted with
`idempotency_key = orderId` before the Stripe call, and the same key is forwarded
to [OP-payment-intents-create](../../externals/EXT-stripe/OP-payment-intents-create.md),
so a retry never double-authorizes. On success, publishes
[CHAN-payment-authorized](../../channels/CHAN-payment-authorized/overview.md).

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller as SVC-orders
    participant Payments as SVC-payments
    participant Orders as TBL-orders
    participant PaymentRows as TBL-payments
    participant Stripe as OP-payment-intents-create
    participant Channel as CHAN-payment-authorized

    Caller->>Payments: POST /payments/authorize
    Payments->>Payments: Authenticate calling-service token
    alt Token missing or invalid
        Payments-->>Caller: 401 Unauthorized
    else Caller authenticated
        Payments->>Orders: Read order state and server-side total
        alt Order not pending_payment
            Orders-->>Payments: Invalid state
            Payments-->>Caller: 409 Conflict
        else Amount differs from order total
            Orders-->>Payments: Amount mismatch
            Payments-->>Caller: 422 Unprocessable Entity
        else Order and amount valid
            Payments->>PaymentRows: Insert by idempotency_key = orderId
            alt Existing payment attempt
                PaymentRows-->>Payments: Existing result
                Payments-->>Caller: Existing 200 or 402 result
            else New payment attempt
                PaymentRows-->>Payments: paymentId
                Payments->>Stripe: Create intent with orderId idempotency key
                alt Stripe unavailable after retry
                    Stripe-->>Payments: Unavailable
                    Payments-->>Caller: 502 Bad Gateway
                else Card declined
                    Stripe-->>Payments: Decline code
                    Payments->>PaymentRows: Mark declined
                    Payments-->>Caller: 402 paymentId, declined, declineCode
                else Authorized
                    Stripe-->>Payments: Authorized intent
                    Payments->>PaymentRows: Mark authorized
                    Payments->>Channel: Publish payment.authorized
                    Channel-->>Payments: Accepted
                    Payments-->>Caller: 200 paymentId, authorized
                end
            end
        end
    end
```
