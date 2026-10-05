---
type: TestCase
title: SMS sent
description: Prove SMS honors customer opt-out.
risk: high
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# SMS sent

# Covers

* [Feature REQ-order-notifications-channel-opt-out](../../features/FEAT-order-notifications/overview.md#req-order-notifications-channel-opt-out)
* [CR REQ-order-notifications-channel-opt-out](../../change-requests/CR-sms-notifications/overview.md#req-order-notifications-channel-opt-out)
* [ADR-twilio-for-sms](../../decisions/ADR-twilio-for-sms.md)
* [SVC-notifications](../../services/SVC-notifications/overview.md)
* [SUB-order-created](../../services/SVC-notifications/SUB-order-created.md)
* [TBL-customers](../../datastores/DB-shop/TBL-customers.md)
* [TBL-notifications](../../datastores/DB-shop/TBL-notifications.md)
* [EXT-twilio](../../externals/EXT-twilio/overview.md)
* [OP-messages-create](../../externals/EXT-twilio/OP-messages-create.md)

# Purpose

Prove SMS honors customer opt-out.

# Preconditions

Twilio stub/table captures are empty; SMS path is enabled.

# Test data

Two customers with `sms_opt_out=false` and `sms_opt_out=true`.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Publish event for opted-in customer | One SMS is attempted | Twilio count is one and row channel=sms |
| 2 | Publish event for opted-out customer | No SMS is attempted | Twilio count remains one and no SMS row exists for second order |

# Postconditions and cleanup

Reset stub and delete fixtures. Current failure: SMS path is not implemented.
