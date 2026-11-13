---
type: TestSuite
title: SMS Notifications Suite
description: Integration tests for the SMS notification channel.
resource: https://github.com/acme/notifications-service/tree/main/tests/integration
framework: pytest
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# SMS Notifications Suite

Integration tests: a real Kafka message in, provider calls stubbed, the
[notifications](../../datastores/DB-shop/TBL-notifications.md) table
asserted.

`TC-1-sms-sent` currently fails because
[TASK-sms-channel](../../change-requests/CR-sms-notifications/TASK-sms-channel.md) is still in progress.
That is the expected state of a suite written before the code.

# Verifies

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — the SMS channel it added.
