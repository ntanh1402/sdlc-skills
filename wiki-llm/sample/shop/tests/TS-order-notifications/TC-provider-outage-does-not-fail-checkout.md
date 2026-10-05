---
type: TestCase
title: Provider outage does not fail checkout
description: Prove notification outage is isolated from checkout and retried.
risk: critical
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Provider outage does not fail checkout

# Covers

* [REQ-order-notifications-failure-never-blocks](../../features/FEAT-order-notifications/overview.md#req-order-notifications-failure-never-blocks)
* [EP-orders-create](../../services/SVC-orders/EP-orders-create.md)

# Purpose

Prove notification outage is isolated from checkout and retried.

# Preconditions

SendGrid stub returns 503; notification retry scheduler is active.

# Test data

One valid checkout and its resulting order event.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Complete checkout | Order creation succeeds | Endpoint returns 201 and order is confirmed |
| 2 | Consume event with provider outage | Notification remains pending and retries | Row status=pending and attempts increase per policy |
| 3 | Inspect checkout after retries | Purchase remains successful | Order status unchanged and no checkout error is emitted |

# Postconditions and cleanup

Restore provider stub and delete fixtures.
