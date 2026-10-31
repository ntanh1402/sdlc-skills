# product.updated — change log

Append-only. Newest first. One entry per contract change: schema version, key,
headers, retention, partitions, or DLQ policy.

## 2026-07-14

* **Contract documentation**: No wire change. Retention restated in hours (24h). The dead-letter policy is now
part of the contract, including the reason the drain is "inspect, don't replay":
on an ordered topic, replaying a stale event can move the index backwards.

## 2026-07-01

* **Schema 1.0**: Added `revision`, the field that made a DLQ safe on an ordered topic. Skipping a poisoned message
breaks per-key order, so the indexer needs a way to drop an event it has already
overtaken; `revision` is monotonic per product and the indexer discards anything at
or below what it last applied. Additive, but every consumer had to adopt it before
`dlqMaxAttempts` could be lowered from ∞ to 3.

## 2026-05-09

* **Schema 0.9**: Created with three partitions, keyed by `productId`,
**ordered**, one-day retention. Introduced
by [TASK-catalog-api-and-cache](../../features/FEAT-catalog/TASK-catalog-api-and-cache.md) as the seam between
the catalog's write side and its derived read models. Ordering was required from day
one: two edits to one product applied out of order leave a stale title in
[IDX-products](../../datastores/IDX-products/overview.md).
