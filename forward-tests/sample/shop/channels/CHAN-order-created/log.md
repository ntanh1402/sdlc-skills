# order.created — change log

Append-only. Newest first. One entry per contract change: schema version, key,
headers, retention, partitions, or DLQ policy.

## 2026-07-14

* **Contract documentation**: No wire change. The key (`orderId`), the header set, and the dead-letter policy
were already in production but lived only in the producer's code; they are now
part of the contract. Retention restated in hours (168h) rather than milliseconds.

## 2026-06-02

* **Schema 1.1**: Added `currency`, `itemCount`, and `paymentId`. Additive,
backward compatible; consumers on 1.0 ignore the new fields.
`currency` was added so a second currency is not a breaking change later,
`itemCount` so the confirmation email can say "3 items" without reading the order,
and `paymentId` when [SVC-payments](../../services/SVC-payments/overview.md)
landed. Shipped by [TASK-payments-service](../../features/FEAT-payments/TASK-payments-service.md).

## 2026-05-18

* **Retention**: Raised 72h to 168h after a weekend outage in
[SVC-notifications](../../services/SVC-notifications/overview.md)
came within hours of losing events. Seven days gives a full working week to
recover a consumer before replay is impossible.

## 2026-04-30

* **Schema 1.0**: Created with six partitions, keyed by `orderId`,
at-least-once. Introduced by
[TASK-order-creation-endpoint](../../features/FEAT-checkout/TASK-order-creation-endpoint.md) to decouple the
confirmation email from the purchase: a notification failure must not fail a sale.
