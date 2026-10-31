---
type: ChangeRequest
title: Validate the delivery address at checkout
description: Refuse an order whose delivery address cannot be delivered to.
status: ReqApproved
changeType: feature
riskLevel: med
priority: P2
requestedBy: operations
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
---

# Validate the delivery address at checkout

# Changes

* [FEAT-checkout](../../features/FEAT-checkout/overview.md)

# Reason

Undeliverable addresses cause returned parcels; operations wants them caught when the order is created. Rejected alternative: checking after the order.

# Requirements

### REQ-checkout-deliverable-address

**Must** — Creating an order with a delivery address that cannot be delivered to is refused with a reason, and no order or payment is created. Functional. Verified by test.

# Delta

None — pending architecture

# References

* [REF-checkout-address-validation-change-prd](../../references/REF-checkout-address-validation-change-prd/overview.md) — the PRD this ChangeRequest was written from.
