---
type: TestCase
title: Redelivery is idempotent
description: Prove broker redelivery cannot duplicate customer contact.
risk: critical
testType: integration
testCategory: error-handling
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Redelivery is idempotent

# Covers

* [REQ-order-notifications-failure-never-blocks](../../../features/FEAT-order-notifications/overview.md#req-order-notifications-failure-never-blocks)

# Purpose

Prove broker redelivery cannot duplicate customer contact.

# Preconditions

Customer allows email; provider/table captures are empty.

Data that must exist:

* delivery 1: a message with event id `evt-1` and message id `msg-1`
* delivery 2: the same message, event id `evt-1` and message id `msg-1`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Publish message to topic `order.created` with event id `evt-1` and message id `msg-1` | Operation POST /v3/mail/send:<br>- Calls received: 1<br>Table notifications:<br>- Rows found: 1 | Read the stub's calls and the rows; check **calls received** and **rows found** |
| 2 | Publish message to topic `order.created` again with event id `evt-1` and message id `msg-1` | Operation POST /v3/mail/send:<br>- Calls received: still 1<br>Table notifications:<br>- Rows found: still 1<br>Topic order.created:<br>- Consumer errors: 0 | Read the stub's calls, the rows and the consumer log; check **calls received**, **rows found** and **consumer errors** |

# Postconditions and cleanup

Delete row and reset broker/provider fixtures.
