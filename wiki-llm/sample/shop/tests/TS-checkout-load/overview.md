---
type: TestSuite
title: Checkout Load Suite
description: Load test for the checkout path under peak traffic.
resource: https://github.com/acme/load-tests/tree/main/checkout
status: Implemented
suiteType: load
framework: k6
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Checkout Load Suite

A weekly k6 run against staging that ramps to the modelled Black-Friday peak
(3,000 checkouts/min) with Stripe in test mode. It guards the latency and
error-rate budgets for the money path, not correctness — correctness is
[TS-checkout](../TS-checkout/overview.md)'s job.

# Verifies

* [FEAT-checkout](../../features/FEAT-checkout/overview.md) — the checkout path under load.
