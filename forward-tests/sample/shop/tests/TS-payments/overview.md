---
type: TestSuite
title: Payments Suite
description: Integration tests for authorize/capture logic and idempotency.
resource: https://github.com/acme/payments-service/tree/main/src/test
framework: junit
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Payments Suite

Tests of the payments service with the Stripe client stubbed, focused on the state machine and the
idempotency key handling — the parts where a bug means a double charge.

# Verifies

* [FEAT-payments](../../features/FEAT-payments/overview.md) — authorize and capture.
