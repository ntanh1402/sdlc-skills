---
type: Subscription
title: On payment authorized
description: Consumes payment.authorized and emails the customer a receipt.
status: Active
consumerGroup: notifications-receipts
maxAttempts: 5
concurrency: 4
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# On payment authorized

Consumes [CHAN-payment-authorized](../../channels/CHAN-payment-authorized/overview.md)
as consumer group `notifications-receipts`, for
[SVC-notifications](overview.md). Sends the
payment receipt — distinct from the order-placed confirmation that
[SUB-order-created](SUB-order-created.md) sends.

# Consumes

* [payment.authorized](../../channels/CHAN-payment-authorized/overview.md)

# Handler

1. Read the customer from
   [customers](../../datastores/DB-shop/TBL-customers.md).
2. Insert a `pending` row into
   [notifications](../../datastores/DB-shop/TBL-notifications.md) keyed by
   `(order_id, channel)` with `channel = receipt`, or load the existing row.
   **Persist before send.**
3. If the existing row is `sent`, this is a redelivery — stop. A `pending` or
   `failed` row remains retryable.
4. Send the receipt email via
   [OP-mail-send](../../externals/EXT-sendgrid/OP-mail-send.md); mark `sent` or
   `failed`.

# Idempotency

| | |
|---|---|
| Key | `(order_id, 'receipt')` |
| Enforced by | the unique index on [notifications](../../datastores/DB-shop/TBL-notifications.md) |

Same durable-state idempotency as the order-created handler: the `receipt`
channel value keeps a receipt from colliding with the order confirmation for the
same order. A `sent` row deduplicates a redelivery; `pending` and `failed` rows
allow the configured retries to continue.

# Failure behavior

| | |
|---|---|
| Retry | exponential backoff, 1s base |
| Max attempts | 5 |
| Then | dead-letter, following the channel's [dead-letter policy](../../channels/CHAN-payment-authorized/overview.md#dead-letter) |

A failed receipt never affects the payment or the order — it is a downstream
courtesy, decoupled by the event just like the order confirmation.

# Sequence diagram

```mermaid
sequenceDiagram
    participant Channel as CHAN-payment-authorized
    participant Notifications as SVC-notifications
    participant Customers as TBL-customers
    participant Rows as TBL-notifications
    participant Email as OP-mail-send
    participant DLQ as payment.authorized.dlq

    Channel->>Notifications: Deliver payment.authorized
    loop Each delivery attempt, maximum 5
        Notifications->>Customers: Read customer
        Customers-->>Notifications: Customer email
        Notifications->>Rows: Insert pending or load by order_id + receipt
        alt Existing status is sent
            Rows-->>Notifications: Already sent
            Notifications-->>Channel: Acknowledge duplicate
        else New, pending, or failed receipt
            Rows-->>Notifications: Retryable state row
            Notifications->>Email: Send receipt
            alt Send succeeds
                Email-->>Notifications: Sent
                Notifications->>Rows: Mark sent
                Notifications-->>Channel: Acknowledge delivery
            else Send fails and attempts remain
                Email-->>Notifications: Failure
                Notifications->>Rows: Mark failed
                Notifications-->>Channel: Reject for exponential-backoff redelivery
            else Fifth send fails
                Email-->>Notifications: Failure
                Notifications->>Rows: Mark failed
                Notifications->>DLQ: Publish failed delivery
                Notifications-->>Channel: Acknowledge exhausted delivery
            end
        end
    end
```
