---
type: MessageChannel
title: order.created
description: Emitted when an order is created.
status: Active
channelName: order.created
kind: kafka
channelType: topic
schemaFormat: json
schemaVersion: "1.1"
partitions: 6
retentionHours: 168
ordering: false
deliveryGuarantee: at-least-once
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Overview

Kafka topic carrying one event per confirmed order. Six partitions, seven days of
retention, **at-least-once** delivery — every consumer must tolerate redelivery.
Keyed by `orderId`, so all events for one order land on the same partition, but
global ordering across orders is not guaranteed and is not needed.

The event is a **thin notification**: it carries the shop's own ids and the total,
never contact details or line items. A consumer that needs the customer's email
looks it up.

## Dead letter

| | |
|---|---|
| DLQ channel | `order.created.dlq` (kafka topic, same partition count) |
| DLQ retention | 336h (14 days) |
| Alert | page `orders` on-call when DLQ depth > 0 |
| Drain | replay from DLQ back onto `order.created` after the fix; handlers are idempotent, so replay is safe |

A dead-lettered order event never rolls back the order. The order stands; only its
downstream effect (an email, a receipt) is delayed until the DLQ is drained.

# Payload

## Key

| | |
|---|---|
| Key | `orderId` |
| Type | string (uuid) |
| Serialization | UTF-8 string, not JSON |

Partitioning by `orderId` keeps a redelivered event on the same partition as the
original, so a single consumer instance sees both.

## Header

| Name | Required | Type | Description |
|---|---|---|---|
| `message-id` | yes | string (uuid) | Unique per produced message. Distinct from `orderId`: a replayed event reuses `orderId` but gets a new `message-id`. |
| `event-type` | yes | string | Always `order.created`. |
| `event-version` | yes | string | Schema version of the body, e.g. `1.1`. Consumers reject a major they do not know. |
| `occurred-at` | yes | string (ISO 8601) | When the order was confirmed, not when the message was produced. |
| `correlation-id` | yes | string (uuid) | Propagated from the inbound HTTP request, so a checkout can be traced end to end. |
| `producer` | yes | string | Service key that published, e.g. `SVC-orders`. |
| `retry-count` | no | integer | Set by the consumer's retry wrapper. Absent on first delivery. |

## Body

| Field | Required | Type | Description |
|---|---|---|---|
| `orderId` | yes | string (uuid) | The order's primary key in [orders](../../datastores/DB-shop/TBL-orders.md). |
| `customerId` | yes | string (uuid) | The buyer. Look up contact details from [customers](../../datastores/DB-shop/TBL-customers.md). |
| `totalUsd` | yes | number | Order total in USD, two decimal places. |
| `currency` | yes | string | ISO 4217 code. Always `USD` today; present so a second currency is not a breaking change. |
| `itemCount` | yes | integer | Number of line items. Lets a consumer render "3 items" without reading the order. |
| `placedAt` | yes | string (ISO 8601) | When the order was confirmed. |
| `paymentId` | no | string (uuid) | The authorizing payment, when one exists. Absent for zero-total orders. |

# Payload example

[payload.example.json](payload.example.json)

# Publishers

* [Orders Service](../../services/SVC-orders/overview.md)

# Subscribers

* [On order created](../../services/SVC-notifications/SUB-order-created.md)
