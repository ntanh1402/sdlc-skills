---
type: ChangeRequest
title: Push notifications for orders
description: Send order confirmations as mobile push notifications too.
status: ReqApproved
changeType: feature
riskLevel: med
priority: P2
requestedBy: growth
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
---

# Push notifications for orders

# Changes

* [FEAT-order-notifications](../../features/FEAT-order-notifications/overview.md)

# Reason

Mobile customers miss emails; push reaches them in the app. Rejected alternative: SMS only.

# Requirements

### REQ-order-notifications-push-sent

**Should** — A customer with the mobile app installed receives an order confirmation as a push notification within 60 seconds of the order being created, unless they opted out of push. Functional. Verified by test.

# Delta

None — pending architecture

# References

* [REF-push-notifications-change-prd](../../references/REF-push-notifications-change-prd/overview.md) — the PRD this ChangeRequest was written from.
