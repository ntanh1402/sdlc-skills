---
type: TestCase
title: Amount mismatch rejected
description: Prove caller cannot authorize an amount different from order total.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Amount mismatch rejected

# Covers

* [EP-payments-authorize](../../services/SVC-payments/EP-payments-authorize.md)

# Purpose

Prove caller cannot authorize an amount different from order total.

# Preconditions

Order total is known; Stripe mock and repository are empty.

# Test data

Order total 100.00 and requested amount 99.00.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Submit mismatched authorization | Validation failure is returned | Status is 422 and body identifies amount mismatch |
| 2 | Inspect effects | No provider call, payment row, or event exists | All mock/repository/publisher counts are zero |

# Postconditions and cleanup

Reset fixtures.
