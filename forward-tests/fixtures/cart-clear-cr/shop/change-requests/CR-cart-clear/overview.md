---
type: ChangeRequest
title: Clear the whole cart at once
description: Let a customer remove every item from the cart in one action.
status: ReqApproved
changeType: feature
riskLevel: low
priority: P3
requestedBy: support
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
---

# Clear the whole cart at once

# Changes

* [FEAT-cart](../../features/FEAT-cart/overview.md)

# Reason

Customers who change their mind remove items one by one; support hears about it
weekly. Rejected alternative: doing nothing, since carts expire anyway.

# Requirements

### REQ-cart-clear-all

**Should** — A customer can remove every item from their cart in one action, and
the cart total becomes zero. Functional. Verified by test.

# Delta

None — pending architecture

# References

* [REF-cart-clear-change-prd](../../references/REF-cart-clear-change-prd/overview.md) — the PRD this ChangeRequest was written from.
