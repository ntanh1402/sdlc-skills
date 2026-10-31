---
type: ChangeRequest
title: Refund a confirmed order
description: Let support refund a confirmed order in full, once.
status: Approved
changeType: feature
riskLevel: med
priority: P2
requestedBy: support
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
designBasedOn: { version: 1, at: 2026-10-01 }
---

# Refund a confirmed order

# Changes

* [FEAT-checkout](../../features/FEAT-checkout/overview.md)

# Reason

Support refunds orders by hand in the payment provider's dashboard, and the
shop never learns of it. Rejected alternative: a partial refund; nobody asked
for one.

# Requirements

### REQ-checkout-refund-order

**Should** — A confirmed order can be refunded in full, once, with a reason.
A second refund of the same order is refused. Functional. Verified by test.

# Delta

## Target delta

* [EP-orders-refund](../../services/SVC-orders/EP-orders-refund.md) — new — the refund endpoint.

## Runtime sequences

```mermaid
sequenceDiagram
  participant Support
  participant Orders as SVC-orders
  participant OrderRows as TBL-orders
  Support->>Orders: POST /orders/{id}/refund
  Orders->>OrderRows: read the order
  alt already refunded
    Orders-->>Support: 409
  else confirmed
    Orders->>OrderRows: mark refunded
    Orders-->>Support: 200
  end
```

## Decisions

None.

## Traceability

| Requirement | Target concepts |
|---|---|
| [REQ-checkout-refund-order](#req-checkout-refund-order) | [EP-orders-refund](../../services/SVC-orders/EP-orders-refund.md) |
