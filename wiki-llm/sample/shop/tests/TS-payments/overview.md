---
type: TestSuite
title: Payments Unit Suite
description: Unit tests for authorize/capture logic and idempotency.
resource: https://github.com/acme/payments-service/tree/main/src/test
status: Implemented
suiteType: unit
framework: junit
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Payments Unit Suite

Unit tests with the Stripe client mocked, focused on the state machine and the
idempotency key handling — the parts where a bug means a double charge.

# Verifies

* [FEAT-payments](../../features/FEAT-payments/overview.md) — authorize and capture.
