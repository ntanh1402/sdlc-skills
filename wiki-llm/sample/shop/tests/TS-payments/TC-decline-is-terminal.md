---
type: TestCase
title: Decline is terminal
description: Prove card decline is stable, visible, and not retried.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Decline is terminal

# Covers

* [REQ-payments-authorize-once](../../features/FEAT-payments/overview.md#req-payments-authorize-once)

# Purpose

Prove card decline is stable, visible, and not retried.

# Preconditions

Stripe mock returns `card_declined`; no payment row exists.

# Test data

Unique order ID and decline code `insufficient_funds`.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Authorize order | Decline maps to HTTP 402 | Response contains stable decline code |
| 2 | Inspect payment state | Declined row is persisted | Status and decline_code match mock result |
| 3 | Advance retry scheduler | No retry occurs | Stripe call count remains one and no event exists |

# Postconditions and cleanup

Reset mock/repository/scheduler.
