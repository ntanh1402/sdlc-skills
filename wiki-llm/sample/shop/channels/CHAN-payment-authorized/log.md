# payment.authorized — change log

Append-only. Newest first. One entry per contract change: schema version, key,
headers, retention, partitions, or DLQ policy.

## 2026-07-14

* **Contract documentation**: No wire change. Retention restated in hours (720h). The dead-letter policy is now
part of the contract, including the rule that a dead letter never implies the money
moved — the authorization is already committed in
[payments](../../datastores/DB-shop/TBL-payments.md).

## 2026-06-21

* **DLQ retention**: Raised 168h to 720h. A dead-lettered payment event outliving the topic it failed on is the whole point;
14 days was shorter than the reconciliation window, so a finance replay could find
the DLQ already empty. Now matches the main topic at 30 days.

## 2026-06-01

* **Schema 1.0**: Created with three partitions, keyed by `orderId`,
at-least-once, 30-day retention for finance
replay. Introduced by [TASK-payments-service](../../features/FEAT-payments/TASK-payments-service.md) so a
receipt email and a ledger row could react to an authorization without coupling to
checkout. `cardBrand` and `cardLast4` were the only card-derived fields allowed
past PCI review; no PAN, no token, no intent id.
