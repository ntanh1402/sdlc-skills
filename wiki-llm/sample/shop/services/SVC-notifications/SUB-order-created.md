---
type: Subscription
title: On order created
description: Consumes order.created and sends the customer their confirmation.
status: Modifying
consumerGroup: notifications
maxAttempts: 5
concurrency: 8
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# On order created

Consumes [CHAN-order-created](../../channels/CHAN-order-created/overview.md) as
consumer group `notifications`, for
[SVC-notifications](overview.md).

Satisfies [REQ-order-notifications-confirmation-sent](../../features/FEAT-order-notifications/overview.md#req-order-notifications-confirmation-sent),
[REQ-order-notifications-failure-never-blocks](../../features/FEAT-order-notifications/overview.md#req-order-notifications-failure-never-blocks), and
[REQ-order-notifications-channel-opt-out](../../features/FEAT-order-notifications/overview.md#req-order-notifications-channel-opt-out).

# Consumes

* [order.created](../../channels/CHAN-order-created/overview.md)

# Validations

No validations.

# Handler

1. Read the customer from
   [customers](../../datastores/DB-shop/TBL-customers.md).
2. For each channel the customer has **not** opted out of (`email`, `sms`):
   1. Insert a `pending` row into
      [notifications](../../datastores/DB-shop/TBL-notifications.md) keyed
      by `(order_id, channel)`, or load the existing row. **Persist before
      send.**
   2. If the existing row is `sent`, this is a redelivery. Stop for this channel;
      do not send again. A `pending` or `failed` row remains retryable.
   3. Send via [OP-mail-send](../../externals/EXT-sendgrid/OP-mail-send.md)
      or
      [OP-messages-create](../../externals/EXT-twilio/OP-messages-create.md).
   4. On success mark `sent`; on failure mark `failed`, record `last_error`, and
      let the retry policy redeliver.

# Flowchart

```mermaid
flowchart TD
    A[Deliver order.created] --> B[Read customer preferences]
    B --> C[Next enabled channel: insert pending row or load by order_id and channel]
    C --> D{Row already sent?}
    D -- yes --> E[Skip this channel]
    D -- no --> F[Send via OP-mail-send or OP-messages-create]
    F --> G{Sent?}
    G -- yes --> H[Mark sent]
    G -- no --> I[Mark failed, record last_error]
    E --> J{More enabled channels?}
    H --> J
    I --> J
    J -- yes --> C
    J -- no --> K{Any channel failed?}
    K -- no --> ACK[ack]
    K -- yes --> L{Attempts left?}
    L -- yes --> RETRY[retry]
    L -- no --> DL[dead letter]
```

# Sequence diagram

```mermaid
sequenceDiagram
    participant Channel as CHAN-order-created
    participant Notifications as SVC-notifications
    participant Customers as TBL-customers
    participant Rows as TBL-notifications
    participant Email as OP-mail-send
    participant SMS as OP-messages-create
    participant DLQ as order.created.dlq

    Channel->>Notifications: Deliver order.created
    loop Each delivery attempt, maximum 5
        Notifications->>Customers: Read customer preferences
        Customers-->>Notifications: Email and SMS opt-outs
        loop Each enabled channel
            Notifications->>Rows: Insert pending or load by order_id + channel
            alt Existing status is sent
                Rows-->>Notifications: Already sent
                Notifications->>Notifications: Skip duplicate channel
            else New, pending, or failed notification
                Rows-->>Notifications: Retryable state row
                alt Email enabled
                    Notifications->>Email: Send order confirmation
                    Email-->>Notifications: Send result
                else SMS enabled
                    Notifications->>SMS: Send order confirmation
                    SMS-->>Notifications: Send result
                end
                alt Send succeeds
                    Notifications->>Rows: Mark sent
                else Send fails
                    Notifications->>Rows: Mark failed and record last_error
                end
            end
        end
        alt All enabled sends succeeded or were duplicates
            Notifications-->>Channel: Acknowledge delivery
        else Handler failed and attempts remain
            Notifications-->>Channel: Reject for exponential-backoff redelivery
        else Fifth attempt failed
            Notifications->>DLQ: Publish failed delivery
            Notifications-->>Channel: Acknowledge exhausted delivery
        end
    end
```

# Idempotency

| | |
|---|---|
| Key | `(order_id, channel)` |
| Enforced by | the unique index on [notifications](../../datastores/DB-shop/TBL-notifications.md) |

The broker guarantees **at-least-once**, so a redelivery is normal, not
exceptional. The unique index gives every `(order_id, channel)` one durable state
row. A `sent` row suppresses a duplicate send; a `pending` or `failed` row is
reused by a retry. The database state, not the broker or a dedupe cache, decides
whether work remains.

Ordering is not required: notifications for two different orders are independent,
which is why `concurrency: 8` is safe.

# Failure behavior

| | |
|---|---|
| Retry | exponential backoff, 1s base |
| Max attempts | 5 |
| Then | dead-letter, following the channel's [dead-letter policy](../../channels/CHAN-order-created/overview.md#dead-letter) |

A failure is **never** acked back to
[SVC-orders](../SVC-orders/overview.md) — the order stands regardless.
A customer who never gets an email still has an order.

# Pending changes

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — modified — the handler loop over channels is not live; production sends one email.
