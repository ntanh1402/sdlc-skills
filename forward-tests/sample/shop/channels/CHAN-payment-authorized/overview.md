---
type: MessageChannel
title: payment.authorized
description: Emitted when a payment is authorized for an order.
status: Active
channelName: payment.authorized
kind: kafka
channelType: topic
schemaFormat: json
schemaVersion: "1.0"
partitions: 3
retentionHours: 720
ordering: false
deliveryGuarantee: at-least-once
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Overview

Kafka topic carrying one event per authorized payment. Thirty days of retention —
long enough for finance to replay a full reconciliation month — with at-least-once
delivery, so every consumer must tolerate redelivery. Keyed by `orderId` so a
payment event lands on the same partition as its retries.

The body carries **no card data**: only the shop's own ids, the amount, and the
brand and last four digits that a receipt needs. The Stripe intent id stays in
[payments](../../datastores/DB-shop/TBL-payments.md).

## Dead letter

| | |
|---|---|
| DLQ channel | `payment.authorized.dlq` (kafka topic, 3 partitions) |
| DLQ retention | 720h (30 days) — matches the main topic, so a dead-lettered event survives as long as the event it failed on |
| Alert | page `payments` on-call immediately on DLQ depth > 0 |
| Drain | replay onto `payment.authorized` after the fix; consumers key on `paymentId`, so replay cannot double-charge or double-send |

A dead-lettered event means a receipt or a ledger row is missing — **never** that
the money moved differently. The authorization already succeeded at Stripe and is
recorded in [payments](../../datastores/DB-shop/TBL-payments.md); the DLQ only
holds up what reads from the event.

# Payload

## Key

| | |
|---|---|
| Key | `orderId` |
| Type | string (uuid) |
| Serialization | UTF-8 string, not JSON |

Keyed on `orderId` rather than `paymentId` so that an authorization and a later
retry for the same order stay co-partitioned and a consumer sees them in order.

## Header

| Name | Required | Type | Description |
|---|---|---|---|
| `message-id` | yes | string (uuid) | Unique per produced message. |
| `event-type` | yes | string | Always `payment.authorized`. |
| `event-version` | yes | string | Schema version of the body, e.g. `1.0`. |
| `occurred-at` | yes | string (ISO 8601) | When Stripe authorized, not when the message was produced. |
| `correlation-id` | yes | string (uuid) | Propagated from the checkout request that triggered the authorization. |
| `producer` | yes | string | Always `SVC-payments`. |
| `retry-count` | no | integer | Set by the consumer's retry wrapper. Absent on first delivery. |

## Body

| Field | Required | Type | Description |
|---|---|---|---|
| `paymentId` | yes | string (uuid) | Primary key in [payments](../../datastores/DB-shop/TBL-payments.md). The consumer's idempotency key. |
| `orderId` | yes | string (uuid) | The order this authorization is for. |
| `customerId` | yes | string (uuid) | The payer. |
| `amountUsd` | yes | number | Authorized amount in USD, two decimal places. |
| `currency` | yes | string | ISO 4217 code. Always `USD` today. |
| `cardBrand` | yes | string | `visa`, `mastercard`, `amex`, … From Stripe. Safe to log; a receipt shows it. |
| `cardLast4` | yes | string | Last four digits. The only card-derived data in the event, and it is not PAN. |
| `authorizedAt` | yes | string (ISO 8601) | When the authorization succeeded. |

# Payload example

[payload.example.json](payload.example.json)

# Publishers

* [Payments Service](../../services/SVC-payments/overview.md)

# Subscribers

* [On payment authorized](../../services/SVC-notifications/SUB-payment-authorized.md)
