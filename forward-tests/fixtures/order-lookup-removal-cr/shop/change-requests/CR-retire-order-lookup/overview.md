---
type: ChangeRequest
title: Retire the order lookup endpoint
description: Remove GET /orders/{id}; nothing calls it any more.
status: Approved
changeType: refactor
riskLevel: low
priority: P3
requestedBy: checkout
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
designBasedOn: { version: 1, at: 2026-10-01 }
---

# Retire the order lookup endpoint

# Changes

* [FEAT-checkout](../../features/FEAT-checkout/overview.md)

# Reason

The storefront reads an order from the response of the order-creation request,
and no other caller is left. Rejected alternative: keeping the endpoint for
support; support reads orders in its own tool.

# Requirements

### REQ-checkout-no-direct-order-lookup

**Could** — The orders service no longer answers `GET /orders/{id}`.
Functional. Verified by inspection.

# Delta

## Target delta

* [EP-orders-get](../../services/SVC-orders/EP-orders-get.md) — removed — the lookup endpoint.

## Runtime sequences

```mermaid
sequenceDiagram
  participant Caller
  participant Orders as SVC-orders
  Caller->>Orders: GET /orders/{id}
  Orders-->>Caller: 404
```

## Decisions

None.

## Traceability

| Requirement | Target concepts |
|---|---|
| [REQ-checkout-no-direct-order-lookup](#req-checkout-no-direct-order-lookup) | [EP-orders-get](../../services/SVC-orders/EP-orders-get.md) |
