# Checkout — change log

Append-only history. Newest first.

## 2026-10-05

* **Stories**: Added the user stories [STORY-checkout-pay-and-confirm](STORY-checkout-pay-and-confirm.md) and [STORY-checkout-retry-safely](STORY-checkout-retry-safely.md), and linked them from [TASK-order-creation-endpoint](TASK-order-creation-endpoint.md).

## 2026-10-03

* **Merge recorded**: Added the merge commit and time to [TASK-order-creation-endpoint](TASK-order-creation-endpoint.md).

## 2026-10-01

* **Status correction**: Marked [TASK-order-creation-endpoint](TASK-order-creation-endpoint.md) Done and the Feature Released; the order service, endpoint, table, and channel it covers were already live and tested.

## 2026-07-14

* **Architecture decision**: Recorded the accepted checkout idempotency boundary in [ADR-idempotent-checkout](../../decisions/ADR-idempotent-checkout.md).
* **Target architecture**: Added high-level/runtime diagrams and requirement traceability.
* **Architecture enrichment**: Documented cart-to-payment-to-confirm flow, idempotency requirement, and full verification coverage.
* **Scope enrichment**: Recorded order service, endpoint, table, and channel as planned scope.

## 2026-06-01

* **Initialization**: Created Checkout requirements, initial architecture, and [TASK-order-creation-endpoint](TASK-order-creation-endpoint.md).
* **Creation**: Created Todo task for Checkout order creation.
