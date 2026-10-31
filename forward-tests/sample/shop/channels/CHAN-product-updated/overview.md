---
type: MessageChannel
title: product.updated
description: Emitted when a product's catalog data changes.
status: Active
channelName: product.updated
kind: kafka
channelType: topic
schemaFormat: json
schemaVersion: "1.0"
partitions: 3
retentionHours: 24
ordering: true
deliveryGuarantee: at-least-once
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Overview

Kafka topic carrying one event per product change — create, edit, archive. It is
the seam between the catalog's write side and its derived read models: the search
index is rebuilt from it and the cache is invalidated by it.

**Ordering matters here** and does not on the order and payment topics: two edits
to the same product must be applied in order, or the index ends up showing a stale
title. The topic is keyed by `productId`, so all events for one product land on the
same partition and are consumed in order. One day of retention — a consumer that
falls a day behind is re-bootstrapped from Postgres, not from the log.

The event is a **thin notification**, not the product itself: the consumer reads
the current row from [products](../../datastores/DB-shop/TBL-products.md) using
`productId`. That is what makes the failure story below cheap.

## Dead letter

| | |
|---|---|
| DLQ channel | `product.updated.dlq` (kafka topic, 3 partitions) |
| DLQ retention | 168h (7 days) |
| Alert | ticket `catalog` on DLQ depth > 0; no page — nothing is lost, only stale |
| Drain | usually **do not replay**. Inspect, fix, and let the nightly full reindex heal the row |

Dead-lettering an ordered topic breaks per-key order: the consumer moves past the
poisoned message and applies the *next* edit for that product. That is safe only
because the event is a thin notification — the consumer always reads the current
row, so applying event N+1 without N converges on the same state. The nightly full
reindex from [products](../../datastores/DB-shop/TBL-products.md) is the backstop:
worst case, a product is stale in
[IDX-products](../../datastores/IDX-products/overview.md) until the next run.
Replaying a stale event from the DLQ can only move the index *backwards*, which is
why the drain is "inspect, don't replay".

# Payload

## Key

| | |
|---|---|
| Key | `productId` |
| Type | string (uuid) |
| Serialization | UTF-8 string, not JSON |

The key is what makes ordering work: all events for one product go to one
partition, so one consumer applies them in sequence.

## Header

| Name | Required | Type | Description |
|---|---|---|---|
| `message-id` | yes | string (uuid) | Unique per produced message. |
| `event-type` | yes | string | Always `product.updated`, including for `created` and `archived` — `changeType` in the body carries the distinction. |
| `event-version` | yes | string | Schema version of the body, e.g. `1.0`. |
| `occurred-at` | yes | string (ISO 8601) | When the product row was committed. |
| `correlation-id` | yes | string (uuid) | Propagated from the admin request that made the edit. |
| `producer` | yes | string | Always `SVC-catalog`. |
| `retry-count` | no | integer | Set by the consumer's retry wrapper. Absent on first delivery. |

## Body

| Field | Required | Type | Description |
|---|---|---|---|
| `productId` | yes | string (uuid) | Primary key in [products](../../datastores/DB-shop/TBL-products.md). The consumer reads the current row with it. |
| `changeType` | yes | string | One of `created`, `updated`, `archived`. Drives whether the consumer upserts or deletes from the index. |
| `revision` | yes | integer | Monotonic per product, bumped on every write. A consumer that has already applied a higher revision drops the event — the guard against reordering after a DLQ skip. |
| `updatedAt` | yes | string (ISO 8601) | When the row was committed. |

# Payload example

[payload.example.json](payload.example.json)

# Publishers

* [Catalog Service](../../services/SVC-catalog/overview.md)

# Subscribers

* [On product updated](../../services/SVC-search-indexer/SUB-product-updated.md)
