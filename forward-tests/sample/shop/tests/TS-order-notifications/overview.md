---
type: TestSuite
title: Order Notifications Suite
description: Integration tests for the order notification flow.
resource: https://github.com/acme/notifications-service/tree/main/tests/integration
framework: pytest
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Order Notifications Suite

Integration tests: a real Kafka message in, provider calls stubbed, the
[notifications](../../datastores/DB-shop/TBL-notifications.md) table
asserted.

# Verifies

* [FEAT-order-notifications](../../features/FEAT-order-notifications/overview.md) — the whole notification flow.
