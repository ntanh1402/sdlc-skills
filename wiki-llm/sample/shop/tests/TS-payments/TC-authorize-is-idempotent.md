---
type: TestCase
title: Authorize is idempotent
description: Prove repeated authorization cannot double charge.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Authorize is idempotent

# Covers

* [REQ-payments-authorize-once](../../features/FEAT-payments/overview.md#req-payments-authorize-once)

# Purpose

Prove repeated authorization cannot double charge.

# Preconditions

No payment exists for order; Stripe mock authorizes.

# Test data

Two identical calls using one order ID.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call authorize | Payment is authorized | Capture response and persisted row |
| 2 | Repeat same call | First result is returned | Response equals first result |
| 3 | Count effects | Only one Stripe call, row, and event exist | Mock/repository/publisher counts each equal one |

# Postconditions and cleanup

Reset mocks and repository.
