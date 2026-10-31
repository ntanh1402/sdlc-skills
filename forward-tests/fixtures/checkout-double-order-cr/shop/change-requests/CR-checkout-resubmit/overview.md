---
type: ChangeRequest
title: Resubmitted checkout places a new order
description: Treat a repeated checkout submission as a new order.
status: ReqApproved
changeType: feature
riskLevel: high
priority: P2
requestedBy: sales
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
---

# Resubmitted checkout places a new order

# Changes

* [FEAT-checkout](../../features/FEAT-checkout/overview.md)

# Reason

Sales wants a customer who presses "Place order" twice to get two orders, for quick repeat purchases. Rejected alternative: a separate "buy again" button.

# Requirements

### REQ-checkout-resubmit-new-order

**Must** — A repeated checkout submission creates a second order. Functional. Verified by test.

# Delta

None — pending architecture

# References

* [REF-checkout-resubmit-change-prd](../../references/REF-checkout-resubmit-change-prd/overview.md) — the PRD this ChangeRequest was written from.
