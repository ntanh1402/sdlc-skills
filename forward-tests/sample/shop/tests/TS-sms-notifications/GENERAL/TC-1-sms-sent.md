---
type: TestCase
title: SMS sent
description: Prove SMS honors customer opt-out.
risk: high
testType: integration
testCategory: functional
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# SMS sent

# Covers

* [Feature REQ-order-notifications-channel-opt-out](../../../features/FEAT-order-notifications/overview.md#req-order-notifications-channel-opt-out)
* [CR REQ-order-notifications-channel-opt-out](../../../change-requests/CR-sms-notifications/overview.md#req-order-notifications-channel-opt-out)
* [ADR-twilio-for-sms](../../../decisions/ADR-twilio-for-sms.md)
* [SVC-notifications](../../../services/SVC-notifications/overview.md)
* [SUB-order-created](../../../services/SVC-notifications/SUB-order-created.md)
* [TBL-customers](../../../datastores/DB-shop/TBL-customers.md)
* [TBL-notifications](../../../datastores/DB-shop/TBL-notifications.md)
* [EXT-twilio](../../../externals/EXT-twilio/overview.md)
* [OP-messages-create](../../../externals/EXT-twilio/OP-messages-create.md)

# Purpose

Prove SMS honors customer opt-out.

# Preconditions

Twilio stub/table captures are empty; SMS path is enabled.

Data that must exist:

* customer A: `sms_opt_out=false`
* customer B: `sms_opt_out=true`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Publish message to topic `order.created` for an order of customer A (`sms_opt_out=false`) | Operation POST /2010-04-01/Accounts/{AccountSid}/Messages.json:<br>- Calls received: 1<br>Table notifications:<br>- channel: sms | Read the Twilio stub's calls and the rows; check **calls received** and **channel** |
| 2 | Publish message to topic `order.created` for an order of customer B (`sms_opt_out=true`) | Operation POST /2010-04-01/Accounts/{AccountSid}/Messages.json:<br>- Calls received: still 1<br>Table notifications:<br>- SMS rows for customer B's order: 0 | Read the Twilio stub's calls and the rows; check **calls received** and **SMS rows** |

# Postconditions and cleanup

Reset stub and delete fixtures. Current failure: SMS path is not implemented.
