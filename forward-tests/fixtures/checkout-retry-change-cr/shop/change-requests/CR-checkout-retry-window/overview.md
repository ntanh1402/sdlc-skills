---
type: ChangeRequest
title: Retry window for checkout
description: Keep a retried checkout safe for 24 hours and tell the shopper while it is in progress.
status: ReqApproved
changeType: feature
riskLevel: med
priority: P2
requestedBy: support
generated: { by: human:sample-author, at: 2026-10-02T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-02T09:00:00Z }
version: 1
versionDate: 2026-10-02
---

# Retry window for checkout

# Changes

* [FEAT-checkout](../../features/FEAT-checkout/overview.md)

# Reason

Support sees shoppers retry a checkout the next morning and get a second
charge, because the retry protection lasts only the browser session. Shoppers
also retry because nothing tells them a slow payment is still in progress.

# Requirements

### REQ-checkout-pay-before-confirm

**Must** — Payment is taken before the order is confirmed, and a checkout
retried with the same client token within 24 hours never creates a second
order or a second charge. Functional. Verified by test.

### REQ-checkout-retry-status

**Should** — A shopper who submits a checkout whose payment is still in
progress sees that it is in progress, not an error. Functional. Verified by
test.

# Delta

None — pending architecture

# References

* [REF-checkout-retry-window-change-prd](../../references/REF-checkout-retry-window-change-prd/overview.md) — the PRD this ChangeRequest was written from.
