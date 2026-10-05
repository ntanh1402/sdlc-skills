---
type: TestCase
title: Payment latency budget
description: Prove synchronous payment leaves room inside checkout deadline.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Payment latency budget

# Covers

* [REQ-checkout-pay-before-confirm](../../features/FEAT-checkout/overview.md#req-checkout-pay-before-confirm)

# Purpose

Prove synchronous payment leaves room inside checkout deadline.

# Preconditions

Peak workload is active and payment latency spans are available.

# Test data

Successful Stripe test authorizations sampled throughout peak hold.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Measure authorize spans under peak | p95 stays below 500 ms | Trace query reports p95 at or below threshold |
| 2 | Measure full checkout | Request deadline is not exhausted | p99 checkout and timeout counts remain within suite limits |

# Postconditions and cleanup

Archive trace query and result; last authorize p95 was 410 ms.
