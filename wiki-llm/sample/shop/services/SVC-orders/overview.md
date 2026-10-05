---
type: Service
title: Orders Service
description: Owns the order lifecycle.
resource: https://github.com/acme/orders-service
status: Active
serviceType: api
ownerTeam: payments
language: java
framework: spring-boot
runtime: jdk21
deployTarget: k8s
slaTier: tier-0
version: "6.1.0"
port: 8080
healthcheckPath: /actuator/health
generated: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
---

# Orders Service

Owns the order lifecycle: build an order from the customer's cart, take payment,
persist it, announce it. It writes the order `pending_payment`, calls
[SVC-payments](../SVC-payments/overview.md) synchronously to
authorize, and only on success moves the order to `confirmed` and publishes
[CHAN-order-created](../../channels/CHAN-order-created/overview.md). Once the event
is out, this service's job is done — it does not know or care who consumes it.

The synchronous payment call is an in-app service-to-service dependency, so it is
recorded under `# Calls`, not as an external dependency. The async fan-out to
notifications, on the other hand, is the event boundary — that is what keeps a
notification outage from failing a purchase.

# Publishes

* [CHAN-order-created](../../channels/CHAN-order-created/overview.md) — emitted once an order is confirmed.

# Calls

* [EP-payments-authorize](../SVC-payments/EP-payments-authorize.md) — authorizes payment synchronously before the order is confirmed.

# Reads

* [TBL-carts](../../datastores/DB-shop/TBL-carts.md) — the cart an order is built from.
* [TBL-cart_items](../../datastores/DB-shop/TBL-cart-items.md) — the lines and their snapshotted prices.
* [TBL-customers](../../datastores/DB-shop/TBL-customers.md) — validates the ordering customer.

# Writes

* [TBL-orders](../../datastores/DB-shop/TBL-orders.md) — one row per order.

