---
type: ArchitectureDecision
title: Make checkout creation idempotent
description: Use a client idempotency token to return one order and charge for repeated checkout submissions.
status: Accepted
ownerTeam: payments
decisionDate: 2026-06-01
generated: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
---

# Make checkout creation idempotent

# Context

Clients and gateways retry requests after timeouts. Checkout spans order state,
payment authorization, persistence, and event publication, so an uncoordinated
retry can create duplicate orders, charges, or notifications.

# Decision

Require a stable client idempotency token on order creation. SVC-orders owns the
token-to-order result and returns the first completed result for identical
retries. A conflicting payload with the same token is rejected. Downstream
payment and event effects reuse the same identity.

# Alternatives

* Relying on client-side button disabling was rejected because it does not cover
  network, gateway, or SDK retries.
* Deduplicating only at the payment provider was rejected because duplicate
  orders and events could still be created.
* At-most-once transport was rejected because request loss is worse than a safe
  retry and cannot be guaranteed across every hop.

# Consequences

The API contract must define token scope, retention, conflict behavior, and
replay response. Order persistence needs a uniqueness constraint. Tests and
telemetry must distinguish legitimate replays from token conflicts.

# Affected concepts

* [SVC-orders](../services/SVC-orders/overview.md)
* [EP-orders-create](../services/SVC-orders/EP-orders-create.md)
* [TBL-orders](../datastores/DB-shop/TBL-orders.md)
* [SVC-payments](../services/SVC-payments/overview.md)
* [CHAN-order-created](../channels/CHAN-order-created/overview.md)
